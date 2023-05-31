import socket, sys, os

serv_addr = ("127.0.0.1", 5000)   

try:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clt_sck:
            clt_sck.connect(serv_addr)

            request = input("Input: ")
            clt_sck.send(bytes(request, 'utf-8'))

            response = clt_sck.recv(1024).decode('utf-8')

            sys.stdout.write(">> ")
            if response == "400 Bad Request":
                sys.stdout.write("Perintah tidak ditemukan.\n\n")
            elif response == "404 Not Found":
                sys.stdout.write("File tidak ditemukan.\n\n")
            else:
                file_name = response.split('file-name: ')[1].split(',')[0]
                file_size = int(response.split('file-size: ')[1].split(',')[0])
                chunks_count = (file_size // 1024) if not (file_size % 1024) else (file_size // 1024) + 1

                file = open(os.path.join(os.path.abspath('client'), file_name), 'wb')
                
                i = 0
                while True:

                    if i == chunks_count:
                        file.close()
                        break
                    
                    response = clt_sck.recv(1024)
                    file.write(response)
                    i += 1

                print('File berhasil diunduh!\n')

except KeyboardInterrupt:
    sys.exit(0)