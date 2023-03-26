import threading
import socket
import sys
import select
import os

class CustomHTTPServer:

    def __init__(self):
        self.threads = []

    def start_server(self, serv_addr):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sck:
            serv_sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serv_sck.bind(serv_addr)
            serv_sck.listen(3)

            sys.stdout.write('Server berhasil berjalan di 127.0.0.1:5000!\n')

            inp_sckt = [serv_sck]

            try:
                while True:
                    read_ready, _, _ = select.select(inp_sckt, [], [])

                    for sck in read_ready:
                        if sck == serv_sck:
                            clt_sck, _ = serv_sck.accept()
                            # inp_sckt.append(clt_sck)
                            clt = threading.Thread(target=self.server_response, args=(clt_sck,))
                            clt.start()
                            self.threads.append(clt)
                        
                        else:
                            pass
                            
            except KeyboardInterrupt:
                serv_sck.close()

                for clt in self.threads:
                    clt.join()

                sys.exit(0)
    
    def server_response(self, sck):
        data = sck.recv(4096)
        data = data.decode('utf-8')
        
        if not data:
            sck.close()
            return

        request_header = data.split('\r\n')

        request_file = request_header[0].split()[1]

        response_header = b''
        response_data = b''

        DATASET_DIR = os.path.abspath("./dataset/")
        
        if request_file == 'index.html' or request_file == '/' or request_file == '/index.html':
            f = open(os.path.abspath('./index.html'), 'r')
            response_data = f.read()
            f.close()
            
            content_length = len(response_data)
            content_length = str(content_length)

            response_header = f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'

            sck.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

        elif request_file == '/dataset':
            response_data = """
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <title>Document</title>
                            </head>
                            <body>
                                <h2>dataset/</h2>
                                <ul>
                            """

            for file in os.listdir(DATASET_DIR):
                path = 'dataset/' + file
                response_data += f'\t<li><a href="{path}" download="{file}">{file}</a></li>\n'
            
            response_data += "\t</ul>\n</body>\n</html>"

            content_length = len(response_data)
            content_length = str(content_length)
            response_header = f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n'
            
            sck.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

        else:
            file = request_file.split('/')[-1]

            if file not in os.listdir(DATASET_DIR):
                f = open('404.html', 'r')
                response_data = f.read()
                f.close()
                
                response_header = 'HTTP/1.1 404 Not found\r\n\r\n'
                sck.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

                return

            f = open('dataset/' + file, 'rb')
            response_data = f.read()
            f.close()

            content_length = len(response_data)
            content_length = str(content_length)

            response_header = f'HTTP/1.1 200 OK\r\nContent-Type: multipart/form-data; charset=UTF-8\r\nContent-Length: {content_length}\r\nContent-Disposition: attachment; filename={file};\r\n\r\n'
            
            sck.sendall(response_header.encode('utf-8') + response_data)

        sck.close()
            
if __name__ == "__main__":
    srv = CustomHTTPServer()

    # Membuka file config
    f = open(os.path.abspath('./httpserver.conf'), 'r')
    config_data = f.read()
    f.close()

    # Memuat data config
    config = {}
    for cfg in config_data.split('\n'):
        config[cfg.split('=')[0]] = cfg.split('=')[1]

    config['PORT'] = int(config['PORT'])
    
    srv.start_server((config['HOST'], config['PORT']))