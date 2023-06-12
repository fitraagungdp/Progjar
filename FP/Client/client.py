import socket

from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Tag Awal :", tag)
        for attr in attrs:
            print("     attr:", attr)

    def handle_endtag(self, tag):
        print("Tag Akhir:", tag)

    def handle_data(self, data):    
        print("Data     :", data)


parser = MyHTMLParser()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 5000)
client_socket.connect(server_address)

# request_header = bytes('POST /salam.html HTTP/1.1\r\nContent-Type: application/json\r\nContent-Length: 100\r\n\r\n' + '{' + '\"wiki\":\"link-menuju-wikipedia\", \"salam\":\"salamat\"' + '}', 'utf-8')
request_header = input().encode('utf-8')
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    response += received.decode('utf-8')
    if len(received) < 1024:
        break

print('\n\nHasil Parse Response')

response_body = response.split('\r\n\r\n')[1]
parser.feed(response_body)
# print(response)
client_socket.close()