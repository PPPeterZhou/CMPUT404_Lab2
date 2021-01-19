import socket, sys

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

def main():
    host = "localhost"
    port = 8001
    buffer_size = 4096

    # make the sokect, get the ip, and connect
    s = create_tcp_socket()
    remote_ip = get_remote_ip(host)
    s.connect((remote_ip, port))
    print(f"Socket Connected to {host} on ip {remote_ip}")
    
    payload = f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'
        
    #send the data and shutdown
    send_data(s, payload)
    s.shutdown(socket.SHUT_WR)

    #continue accepting data until no more left
    full_data = b""
    while True:
        data = s.recv(buffer_size)
        if not data:
            break
        full_data += data
    print(full_data)
    s.close()
    print("\nRequest has finished!")

if __name__ == "__main__":
    main()
