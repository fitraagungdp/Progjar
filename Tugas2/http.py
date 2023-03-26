
# # import requests module
# import requests

# # Making a get request
# response = requests.get('https://www.its.ac.id/')
# version = requests.get("https://www.its.ac.id/", timeout=60, verify=False)
  
# if response.status_code == 200:
#     print('Success!')
# elif response.status_code == 404:
#     print('Not Found.')
    
# if version.raw.version == 10:
#     print('HTTP/1.0')
# elif version.raw.version == 11:
#     print('HTTP/1.1')
    
# print(response.encoding)

# print(response.json())
    
# # print response
# # print(response)
# # print(version.raw.version)
  
# # # print headers of response
# # print(response.headers)


import socket
from bs4 import BeautifulSoup

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = input("Web Adress to check: ")
s.connect((url, 80))


request = b"GET / HTTP/1.0\r\nHost:{url}\r\n\r\n"
s.send(request)

response = ''
while True:
    received = s.recv(1024)
    if not received:
        break
    response += received.decode('utf-8')
    
pisahkan = response.split()


print("Versi HTTP : " + pisahkan[0])
print("Content-Encoding : ")
for line in pisahkan:
    if 'Content-Encoding' in line:
        print(line)
        
print("Status Code : " + pisahkan[1] + " " + pisahkan[2])
print("Charset: ")
for line in pisahkan:
    if 'charset' in line:
        print(line)
s.close()
