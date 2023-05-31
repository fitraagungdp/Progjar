from ftplib import FTP
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class FtpClient:
    def __init__(self, host, user, password, port):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.ftp = FTP()

    def connect(self):
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.user, self.password)

    def disconnect(self):
        self.ftp.quit()

    def getNameAndVersion(self):
        message = self.ftp.getwelcome()
        return message.split('\n')[0].split('-')[1]

    def getWelcomeMessage(self):
        message = self.ftp.getwelcome()
        return message
    
    def getListOfFiles(self):
        return self.ftp.nlst()
    
    def uploadFile(self, filename):
        response = ''
        with open(os.path.join(BASE_DIR, filename), 'rb') as file:
            response = self.ftp.storbinary(f"STOR {filename}", fp=file)
            
        return response

    def createDirectory(self, dirname):
        response = self.ftp.mkd(dirname)
        return response

    def getCurrentDirectory(self):
        response = self.ftp.pwd()
        return response
    
    def renameDirectory(self, oldname, newname):
        response = self.ftp.rename(oldname, newname)
        return response

    def removeDirectory(self, dirname):
        response = self.ftp.rmd(dirname)
        return response
        
if __name__ == '__main__':
    HOST = 'localhost'
    USER = 'progjar'
    PASS = 'Progjar123'
    PORT = 21

    ftp = FtpClient(HOST, USER, PASS, PORT)
    ftp.connect()

    # Soal 1
    # print(ftp.getNameAndVersion())
    
    # Soal 2
    # print(ftp.getWelcomeMessage())
    
    # Soal 3
    # print(ftp.getListOfFiles())
    
    # Soal 4
    # print(ftp.uploadFile('response_smtp.txt'))
    
    # Soal 5
    # print(ftp.createDirectory('data'))
    
    # Soal 6
    # print(ftp.getCurrentDirectory())
    
    # Soal 7
    # print(ftp.renameDirectory('data', 'new_data'))
    
    # Soal 8
    print(ftp.removeDirectory('new_data'))