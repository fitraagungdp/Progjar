import re

file = open('Tugas4/response.txt', 'r')
response = file.read()
file.close()

# Soal 1
print(re.findall(r'\'ehlo.*', response)[0])

# Soal 2
print(re.findall(r'\'250-START.*', response)[0])

# Soal 3
print(re.findall(r'retcode.*server ready.*', response)[0])

# Soal 4
print(re.search(r'send.*(\'AUTH LOGIN.*)', response).group(1))

# Soal 5
print(re.findall(r'\'250.*Hello.*', response)[0])

# Soal 6
print(re.findall(r'\'221.*', response)[0])