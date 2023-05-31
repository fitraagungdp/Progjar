import smtplib
import re

email = 'XXXXXX'
password = 'XXXXXXX'

server = smtplib.SMTP('smtp.office365.com', 587)
server.set_debuglevel(1)
debug1 = server.starttls()
server.login(email, password)

receiver = ['XXXXXXXXX']

body = "Hai, apa kabar?"

msg = f"From: {email}\r\nTo: {', '.join(receiver)}\r\n\r\n" + body

response = server.sendmail(email, receiver, msg)

server.quit()