import socket, sys, os

serv_addr = ('127.0.0.1', 5000)

try:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clt_sck:
            clt_sck.connect(serv_addr)
            
            request = input("Input: ")
            clt_sck.sendall(bytes(request, 'utf-8'))

            response = clt_sck.recv(1024).decode('utf-8')

            if response == "400 Bad Request":
                sys.stdout.write("Perintah tidak ditemukan.\n\n")
            elif response == "404 Not Found":
                sys.stdout.write("File tidak ditemukan.\n\n")
            else:
                file_name = response.split('file-name: ')[1].split(',')[0]
                file_size = response.split('file-size: ')[1].split(',')[0]
                
                with open(os.path.join(os.path.abspath('client'), file_name), 'wb') as file:
                    while True:
                        response = clt_sck.recv(1024)

                        if not response:
                            break

                        file.write(response)
                
                sys.stdout.write('File berhasil diunduh!\n\n')

except KeyboardInterrupt:
    sys.exit(0)

    