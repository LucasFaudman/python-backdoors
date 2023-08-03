# python-backdoors
Python backdoors written by me for SANS courses and CTFs:
* [socket-backdoor.py](socket-backdoor.py) - A simple socket backdoor that can upload, download, and execute files.

* [pyterperter-ba.py](pyterpreter.py) - A backdoor allows the user to execute Python commands on the target machine throught the Python interpreter via `code.interact()` by redirecting stdin, stdout, and stderr to a socketIO instance which has the file object methods needed to read and write from the underlying socket.

* [os-dup2-backdoor.py](os-dup2-backdoor.py) - A backdoor that uses `os.dup2` to redirect stdin, stdout, and stderr directly to a socket's file descriptor. This allows the backdoor to be used with any program that uses stdin, stdout, and stderr.


## [socket-backdoor.py](socket-backdoor.py)  
```
usage: socket-backdoor.py [-h] [-l HOST] [-p PORTS] [-f FAMILY] [-t TYPE]
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
  -w WAIT, --wait WAIT  The number of seconds to wait between connection attempts
  ```


## [pyterperter-backdoor.py](pyterpreter.py)
```
usage: pyterpreter-backdoor.py [-h] [-l HOST] [-p PORT] [-f FAMILY] [-t TYPE]
                               [--protocol PROTOCOL] [--fileno FILENO]

options:
  -h, --help            show this help message and exit
  -l HOST, --host HOST  The IP address to connect to
  -p PORT, --port PORT  A comma separated list of ports to try to connect to
  -f FAMILY, --family FAMILY
                        The socket family to use
  -t TYPE, --type TYPE  The socket type to use
  --protocol PROTOCOL   The socket protocol to use
  --fileno FILENO       The file descriptor to use
```

### [os-dup2-backdoor.py](os-dup2-backdoor.py)
```
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
```