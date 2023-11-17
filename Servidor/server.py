# Importa el módulo de socket
from socket import *
import sys  # Para terminar el programa

# Crea un socket de servidor
serverSocket = socket(AF_INET, SOCK_STREAM)

# Configura el número de puerto en el que el servidor escuchará
serverPort = 6789

# Asocia el socket con la dirección y el puerto del servidor
serverSocket.bind(('', serverPort))

# Empieza a escuchar conexiones entrantes
serverSocket.listen(1)

print('El servidor está listo para recibir...')

while True:
    # Establece la conexión
    connectionSocket, addr = serverSocket.accept()

    try:
        # Recibe la solicitud HTTP del cliente
        message = connectionSocket.recv(1024).decode()

        # Obtiene el nombre del archivo solicitado desde la solicitud
        filename = message.split()[1][1:]  # Ignora el primer carácter ("/")

        # Abre el archivo solicitado
        with open(filename, "rb") as f:
            outputdata = f.read()

        # Envía una línea de encabezado HTTP al cliente
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # Envía el contenido del archivo solicitado al cliente
        connectionSocket.sendall(outputdata)

        # Cierra la conexión con el cliente
        connectionSocket.close()

    except IOError:
        # En caso de que el archivo no se encuentre, envía un mensaje "404 Not Found"
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send(b"<html><body><h1>404 Not Found</h1></body></html>")
        connectionSocket.close()

# Cierra el socket del servidor
serverSocket.close()
sys.exit()  # Termina el programa después de enviar los datos correspondientes
