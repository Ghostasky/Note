import argparse
import socket

MAX_BYTES = 65535
parse = argparse.ArgumentParser()
parse.add_argument("-c", "--client", help="clint",  action="store_true")
parse.add_argument("-s", "--server", help="server", action="store_true")
# parse.add_argument("-p", "--port", type=int)
parse.add_argument("-m", "--message", help="client message")

args = parse.parse_args()

if args.server:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind(("localhost", 1234))
    print("listening at {}".format(server_sock.getsockname()))
    while True:
        data, address = server_sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print("OG ip&port {},message is : {}".format(address, text))
        text = "server recved!"
        server_sock.sendto(text.encode('ascii'), address)

if args.client:
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.connect(("192.168.0.5", 1234))  # server ip & port
    print("client : " + str(client_sock.getsockname()))
    data = args.message.encode('ascii')
    client_sock.send(data)
    data = client_sock.recv(MAX_BYTES)
    text = data.decode('ascii')
    print(text)
