import socket, sys, time

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
    print("Payload sent successfully")

def get_remote_ip(host):
    print(f"Getting IP for {host}")
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print("Hostname could not be resolved. Exiting")
        sys.exit()
    
    print(f"IP address of {host} is {remote_ip}")
    return remote_ip

def create_tcp_socket():
    print("Creating socket")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f"Failed to create socket. Error code: {str(msg[0])}, Error message: {msg[1]}")
        sys.exit()
    print("scoket created successfully")
    return s

def connect(host, port):
    s = create_tcp_socket()
    remote_ip = get_remote_ip(host)
    s.connect((remote_ip, port))
    print(f"Socket Connected to {host} on ip {remote_ip}")
    return s

def main():
    host = "www.google.com"
    port = 80
    buffer_size = 4096

    # set up server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:

        s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s1.bind((HOST, PORT))
        s1.listen(2)

        #continously listen for connections
        while True:
            s = connect(host, port)

            print("Wating...")
            conn, addr = s1.accept()
            print("Connected by", addr)

            #receive data, wait a bit
            full_data = conn.recv(BUFFER_SIZE)
            full_data = str(full_data.decode('utf-8'))
            payload = full_data
            print("Payload:", payload)

            # send it to google
            send_data(s, payload)
            s.shutdown(socket.SHUT_WR)

            #continue accepting data until no more left
            full_data = b""
            while True:
                data = s.recv(buffer_size)
                if not data:
                    break
                full_data += data

            # send back
            conn.sendall(full_data)
            conn.close()
            print("Finished\n")
           

if __name__ == "__main__":
    main()