import os, sys, socket, select

def processrequest(request):

    if request[0] == 'download':

        # Mencari file
        file_path = ""
        for path, curr_dir, files in os.walk('server'):
            if request[1] in files:
                file_path = os.path.join(path, request[1])

        if not file_path:
            return {
                'header': b"404 Not Found",
                'body': None
            }

        # Mendapatkan data file
        file_name = request[1]
        file_size = os.stat(file_path).st_size
        header = "file-name: {},\nfile-size: {},\n\n\n".format(file_name, file_size)

        body = []

        with open(file_path, 'rb') as file:
            while True:
                request = file.read(1024)

                if not request:
                    break

                body.append(request)

        return {
            'header': bytes(header, 'utf-8'),
            'body': body
        }

    else:
        return {
            'header': b"400 Bad Request",
            'body': None
        }

if __name__ == "__main__":
    serv_addr = ('127.0.0.1', 5000)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sck:
                
            serv_sck.bind(serv_addr)
            serv_sck.listen(3)

            sys.stdout.write('Server berhasil berjalan di 127.0.0.1:5000!')

            inp_sckt = [serv_sck]

            while True:
                read_ready, write_ready, exception = select.select(inp_sckt, [], [])

                for sck in read_ready:
                    if sck == serv_sck:
                        clt_sck, clt_addr = serv_sck.accept()
                        inp_sckt.append(clt_sck)
                    
                    else:
                        request = sck.recv(1024).strip()
                        
                        if request:
                            response = processrequest(request.decode('utf-8').split(' '))
                            sck.send(response['header'])

                            if response['body']:
                                for chunk in response['body']:
                                    sck.send(chunk)

                        else:
                            sck.close()
                            inp_sckt.remove(sck)

    except KeyboardInterrupt:
        sys.exit(0)