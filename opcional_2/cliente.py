import sys
from socket import *

def http_client(server_host, server_port, filename):
    # Crear un socket TCP
    client_socket = socket(AF_INET, SOCK_STREAM)

    # Conectar al servidor
    client_socket.connect((server_host, server_port))

    # Construir la solicitud HTTP
    request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"

    # Enviar la solicitud al servidor
    client_socket.sendall(request.encode())

    # Recibir y mostrar la respuesta del servidor
    response = client_socket.recv(4096).decode()
    print(response)

    # Cerrar el socket del cliente
    client_socket.close()

if __name__ == "__main__":
    # Verificar que se proporcionen los argumentos necesarios
    if len(sys.argv) != 4:
        print("Uso: python client.py server_host server_port filename")
        sys.exit(1)

    # Obtener los argumentos de la línea de comandos
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    # Llamar a la función del cliente
    http_client(server_host, server_port, filename)
