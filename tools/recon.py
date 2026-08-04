import socket
import threading

## Needed Variables
ip = input("What IP do u want to scan?")
open_ports = []
lock = threading.Lock()

## Defining the main scanning function
def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
        
    if result == 0:
        with lock:
            open_ports.append(port)

    sock.close()


## Adding the Threading function
def scan(ip):
    threads = []

    for port in range(1, 1025): 
        thread = threading.Thread(
        target=scan_port,
        args=(ip,port)
    )

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

## Calling the scanning + thread function         
scan(ip)

## Final Output 
print("\nOpen ports found:")
print(sorted(open_ports))
