import socket
import os
import sys
from html.parser import HTMLParser
from urllib.request import urlopen


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


# parser = MyHTMLParser()
# response = urlopen('http://www.python.org').read()
# parser.feed(response.decode('utf-8'))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (sys.argv[1], int(sys.argv[2]))
print(server_address)
client_socket.connect(server_address)

request_header = bytes('GET {} HTTP/1.0\r\nHost: \r\n\r\n'.format(sys.argv[3]), 'utf-8')
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    response += received.decode('utf-8')
    if len(received) < 1024:
        break

print(response)
client_socket.close()