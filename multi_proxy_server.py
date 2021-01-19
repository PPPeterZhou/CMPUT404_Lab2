import socket, sys, time
from multiprocessing import Process

HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 4096

def send_data(serversocket, payload):
    print("Sending payload")
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print("Send failed")
        sys.exit()
    print("Payload sent successfully\n")

def get_remote_ip(host):
    print(f"Getting IP for {host}")
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print("Hostname could not be resolved. Exiting")
        sys.exit()
    
    print(f"IP address of {host} is {remote_ip}")
    return remote_ip

def handle_proxy(addr, conn):
    print("Connected by", addr)
    return 

def handle_request(conn, addr, proxy_end):
    #receive data, wait a bit
    full_data = conn.recv(BUFFER_SIZE)
    full_data = str(full_data.decode('utf-8'))
    payload = full_data

    # send it to google
    send_data(proxy_end, payload)
    proxy_end.shutdown(socket.SHUT_WR)

    #continue accepting data until no more left
    full_data = b""
    while True:
        data = proxy_end.recv(BUFFER_SIZE)
        if not data:
            break
        full_data += data
    # send back
    conn.sendall(full_data)
    conn.close()
    print("Finished\n")
           

def main():
    host = "www.google.com"
    port = 80

    # set up server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:

        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(10)
        print("Wating...\n")
        #continously listen for connections

        while True:
            conn, addr = proxy_start.accept()
            p = Process(target=handle_proxy, args=(addr, conn))
            p.daemon = True
            p.start()
            print("Started process...")


            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google...")
                remote_ip = get_remote_ip(host)

                proxy_end.connect((remote_ip, port))
                p = Process(target=handle_request, args=(conn, addr, proxy_end))
                p.daemon = True
                p.start()
                print("Started Process", p)

            conn.close()
           

if __name__ == "__main__":
    main()