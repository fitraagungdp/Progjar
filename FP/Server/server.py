import threading
import socket
import sys
import select
import os
import json

PAGE_DIR = os.path.abspath("./pages/")

class CustomHTTPServer:

    def __init__(self):
        self.threads = []

    def start_server(self, serv_addr):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sck:
            serv_sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serv_sck.bind(serv_addr)
            serv_sck.listen(3)

            sys.stdout.write(f'Server berhasil berjalan di {serv_addr[0]}:{serv_addr[1]}!\n')

            inp_sckt = [serv_sck]

            while True:
                try:
                    read_ready, _, _ = select.select(inp_sckt, [], [])

                    for sck in read_ready:
                        if sck == serv_sck:
                            clt_sck, _ = serv_sck.accept()

                            clt = threading.Thread(target=self.server_response, args=(clt_sck,))
                            clt.start()
                            self.threads.append(clt)
                                
                except KeyboardInterrupt:
                    serv_sck.close()

                    for clt in self.threads:
                        clt.join()

                    sys.exit(0)
    
    def get(self, request_line):
        
        response_header = ''
        response_body = ''

        # 200 OK
        if request_line[1] == '/' or request_line[1] == 'index.html' or request_line[1] == '/index.html':
            with open(os.path.join(PAGE_DIR, 'index.html'), 'r') as file:
                response_body = file.read()
            
            content_length = len(response_body)
            content_length = str(content_length)

            response_header = f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'

        # 301 Moved Permanently
        elif request_line[1] == '/redirect1.html':
            
            content_length = len(response_body)
            content_length = str(content_length)

            redirect_to = 'redirect2.html'
            response_header = f'HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\nLocation: {redirect_to}\r\n\r\n'

        # 403 Forbidden
        elif request_line[1] == '/password_rahasia.html':
            with open('./403.html', 'r') as file:
                response_body = file.read()
            
            content_length = len(response_body)
            content_length = str(content_length)

            response_header = f'HTTP/1.1 403 Forbidden\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'

        # 500 Internal Server Error
        elif 'bagi' in request_line[1]:
            operand1 = float(request_line[1].split('bagi')[0][1:])
            operand2 = float(request_line[1].split('bagi')[1])

            try:
                result = operand1 / operand2
                response_body = str(result)

                content_length = len(response_body)
                content_length = str(content_length)

                response_header = f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'

            except Exception:
                with open('./500.html', 'r') as file:
                    response_body = file.read()

                content_length = len(response_body)
                content_length = str(content_length)
                
                response_header = f'HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'

        # 200 OK
        elif request_line[1][1:] in os.listdir(PAGE_DIR):
            with open(os.path.join(PAGE_DIR, request_line[1][1:]), 'r') as file:
                response_body = file.read()
            
            content_length = len(response_body)
            content_length = str(content_length)

            response_header = f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'        

        # 404 Not Found
        else:
            with open('./404.html', 'r') as file:
                response_body = file.read()
            
            content_length = len(response_body)
            content_length = str(content_length)

            response_header = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'


        return response_header + response_body
        
    def head(self, request_line):
        response_header = ''
        response_body = ''

        # 200 OK
        if request_line[1] == '/' or request_line[1] == 'index.html' or request_line[1] == '/index.html':
            with open(os.path.join(PAGE_DIR, 'index.html'), 'r') as file:
                response_body = file.read()
            
            content_length = len(response_body)
            content_length = str(content_length)

            response_header = f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'

        # 301 Moved Permanently
        elif request_line[1] == '/redirect1.html':
            
            content_length = len(response_body)
            content_length = str(content_length)

            redirect_to = 'redirect2.html'
            response_header = f'HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\nLocation: {redirect_to}\r\n\r\n'

        # 403 Forbidden
        elif request_line[1] == '/password_rahasia.html':
            with open('./403.html', 'r') as file:
                response_body = file.read()
            
            content_length = len(response_body)
            content_length = str(content_length)

            response_header = f'HTTP/1.1 403 Forbidden\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'

        # 500 Internal Server Error
        elif 'bagi' in request_line[1]:
            operand1 = float(request_line[1].split('bagi')[0][1:])
            operand2 = float(request_line[1].split('bagi')[1])

            try:
                result = operand1 / operand2
                response_body = str(result)

                content_length = len(response_body)
                content_length = str(content_length)

                response_header = f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'

            except Exception:
                with open('./500.html', 'r') as file:
                    response_body = file.read()

                content_length = len(response_body)
                content_length = str(content_length)
                
                response_header = f'HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'

        # 200 OK
        elif request_line[1][1:] in os.listdir(PAGE_DIR):
            with open(os.path.join(PAGE_DIR, request_line[1][1:]), 'r') as file:
                response_body = file.read()
            
            content_length = len(response_body)
            content_length = str(content_length)

            response_header = f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'        

        # 404 Not Found
        else:
            with open('./404.html', 'r') as file:
                response_body = file.read()
            
            content_length = len(response_body)
            content_length = str(content_length)

            response_header = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'


        return response_header

    def post(self, request_line, request_body):        
        if request_line[1] == '/salam.html':
            data = json.loads(request_body)
            
            with open(os.path.join(PAGE_DIR, request_line[1][1:]), 'r') as file:
                content = file.read()
            
                content = content.split("</ul>")[0]
                content += f"\t<li><a href=\"{data['wiki']}\">{data['salam']}</a></li>\n"
                content += " </ul></body></html>"

            with open(os.path.join(PAGE_DIR, request_line[1][1:]), 'w') as file:
                file.write(content)

            with open(os.path.join(PAGE_DIR, request_line[1][1:]), 'r') as file:
                response_body = file.read()                

                content_length = len(response_body)
                content_length = str(content_length)
                response_header = f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'

        return response_header + response_body

    def server_response(self, sck):
        data = sck.recv(4096)
        data = data.decode('utf-8')
        
        if not data:
            sck.close()
            return

        request_line = data.split('\r\n')[0]
        request_line = request_line.split()
        # request_header = data.split('\r\n')[1:]

        if "GET" == request_line[0]:
            response = self.get(request_line)
        elif "HEAD" == request_line[0]:
            response = self.head(request_line)
        elif "POST" == request_line[0]:
            request_body = data.split('\r\n\r\n')[1]
            response = self.post(request_line, request_body)

        sck.sendall(response.encode('utf-8'))

        sck.close()
            
if __name__ == "__main__":
    srv = CustomHTTPServer()

    f = open(os.path.abspath('./httpserver.conf'), 'r')
    config_data = f.read()
    f.close()

    config = {}
    for cfg in config_data.split('\n'):
        config[cfg.split('=')[0]] = cfg.split('=')[1]

    config['PORT'] = int(config['PORT'])
    
    srv.start_server((config['HOST'], config['PORT']))