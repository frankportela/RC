# Importar el módulo de socket
from socket import *
import sys
import threading  # Importar el módulo de threading para multihilo

serverSocket = socket(AF_INET, SOCK_STREAM)

# Preparar un socket de servidor
# Completar inicio
serverPort = 8765
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
# Completar fin

def manejar_cliente(connectionSocket):
    try:
        mensaje = connectionSocket.recv(1024).decode()
        nombre_archivo = mensaje.split()[1]
        archivo = open(nombre_archivo[1:])
        datos_salida = archivo.read()

        # Enviar una línea de encabezado HTTP al socket
        # Completar inicio
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        # Completar fin

        # Enviar el contenido del archivo solicitado al cliente
        for i in range(0, len(datos_salida)):
            connectionSocket.send(datos_salida[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError:
        # Enviar mensaje de respuesta para archivo no encontrado
        # Completar inicio
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        # Completar fin

        # Cerrar el socket del cliente
        # Completar inicio
        connectionSocket.close()
        # Completar fin

while True:
    # Establecer la conexión
    print('Listo para servir...')
    connectionSocket, addr = serverSocket.accept()

    # Crear un nuevo hilo para cada conexión entrante
    hilo_cliente = threading.Thread(target=manejar_cliente, args=(connectionSocket,))
    hilo_cliente.start()
