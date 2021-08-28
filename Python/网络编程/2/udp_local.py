import argparse
import socket

MAX_BYTES = 65535
parse = argparse.ArgumentParser()
parse.add_argument("-c", "--client", help="clint",  action="store_true")
parse.add_argument("-s", "--server", help="server", action="store_true")
parse.add_argument("-p", "--port", type=int)
parse.add_argument("-m", "--message", help="client message")

args = parse.parse_args()

if args.server:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind(('127.0.0.1', args.port))
    print("listening at {}".format(server_sock.getsockname()))
    while True:
        data, address = server_sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print("OG ip&port {},message is : {}".format(address, text))
        text = "server recved!"
        server_sock.sendto(text.encode('ascii'), address)

if args.client:
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = args.message.encode('ascii')
    client_sock.sendto(data, ('127.0.0.1', args.port))
    data, address = client_sock.recvfrom(MAX_BYTES)
    text = data.decode('ascii')
    print(address, text)
