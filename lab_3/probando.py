import ssl
import base64
from socket import *

msg = "\r\n¡Me encantan las redes de computadoras!"
endmsg = "\r\n.\r\n"

# Elija un servidor de correo (servidor SMTP de Gmail) y establezca el puerto
mailserver = "smtp.gmail.com"
port = 587

# Cree un socket llamado clientSocket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Establecer conexión con el servidor de correo
clientSocket.connect((mailserver, port))
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('No se recibió la respuesta 220 del servidor.')

# Envíe el comando EHLO y muestre la respuesta del servidor.
ehloCommand = 'EHLO Alice\r\n'
clientSocket.send(ehloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('No se recibió la respuesta 250 del servidor.')

# Solicitar inicio de la capa de transporte seguro (STARTTLS)
starttlsCommand = 'STARTTLS\r\n'
clientSocket.send(starttlsCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '220':
    print('No se recibió la respuesta 220 del servidor para STARTTLS.')

# Establecer una conexión segura utilizando SSL/TLS
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

# Autenticación con tu cuenta de Gmail
user = "frankalejoo99@gmail.com"
password = "ltyn wpgj cxjo cdwt"

# Iniciar sesión con tu cuenta de Gmail
authCommand = f'AUTH LOGIN\r\n'
clientSocket.send(authCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)

# Envía el nombre de usuario codificado en base64
clientSocket.send(base64.b64encode(user.encode()) + b'\r\n')
recv3 = clientSocket.recv(1024).decode()
print(recv3)

# Envía la contraseña codificada en base64
clientSocket.send(base64.b64encode(password.encode()) + b'\r\n')
recv4 = clientSocket.recv(1024).decode()
print(recv4)

# Resto del código

# Envíe el comando MAIL FROM y muestre la respuesta del servidor.
mailFromCommand = f'MAIL FROM: <{user}>\r\n'
clientSocket.send(mailFromCommand.encode())
recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '250':
    print('No se recibió la respuesta 250 del servidor.')

# Envíe el comando RCPT TO y muestre la respuesta del servidor.
rcptToCommand = 'RCPT TO: <lauraglza63@gmail.com>\r\n'
clientSocket.send(rcptToCommand.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '250':
    print('No se recibió la respuesta 250 del servidor.')

# Envíe el comando DATA y muestre la respuesta del servidor.
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv7 = clientSocket.recv(1024).decode()
print(recv7)
if recv7[:3] != '354':
    print('No se recibió la respuesta 354 del servidor.')

# Envíe los datos del mensaje.
clientSocket.send(msg.encode())

# El mensaje termina con un solo período.
clientSocket.send(endmsg.encode())
recv8 = clientSocket.recv(1024).decode()
print(recv8)
if recv8[:3] != '250':
    print('No se recibió la respuesta 250 del servidor.')

# Envíe el comando QUIT y obtenga la respuesta del servidor.
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)
if recv9[:3] != '221':
    print('No se recibió la respuesta 221 del servidor.')

# Cierre de la conexión
clientSocket.close()
