import os, socketserver

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.processrequest(self.data.decode('utf-8').split(' '), self.request)
    
    def processrequest(self, request, sock):
        if request[0] == 'download':
            # Mencari file
            file_path = ""
            for path, curr_dir, files in os.walk('server'):
                if request[1] in files:
                    file_path = os.path.join(path, request[1])

            if not file_path:
                sock.sendall(b"404 Not Found")
                return

            # Mendapatkan data file
            file_name = request[1]
            file_size = os.stat(file_path).st_size
            header = "file-name: {},\nfile-size: {},\n\n\n".format(file_name, file_size)

            sock.sendall(bytes(header, 'utf-8'))

            with open(file_path, 'rb') as file:
                while True:
                    request = file.read(1024)

                    if not request:
                        break

                    sock.sendall(request)

        else:
            sock.sendall(b"400 Bad Request")

if __name__ == "__main__":
    serv_addr = ('127.0.0.1', 5000)

    with socketserver.TCPServer(serv_addr, Handler) as serv_sck:
        print('Server berhasil berjalan di 127.0.0.1:5000!')
        serv_sck.serve_forever()