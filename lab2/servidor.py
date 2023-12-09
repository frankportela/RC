# UDPPingerServer.py
# Necesitaremos el siguiente módulo para generar paquetes perdidos aleatorios
import random
from socket import *

# Crear un socket UDP
# Observa el uso de SOCK_DGRAM para paquetes UDP
socket_servidor = socket(AF_INET, SOCK_DGRAM)

# Asignar la dirección IP y el número de puerto al socket
socket_servidor.bind(('', 12000))

while True:
    # Generar un número aleatorio en el rango de 0 a 10
    rand = random.randint(0, 10)
    
    # Recibir el paquete del cliente junto con la dirección de origen
    mensaje, direccion_cliente = socket_servidor.recvfrom(1024)
    
    # Capitalizar el mensaje del cliente
    mensaje = mensaje.upper()
    
    # Si rand es menor que 4, consideramos que el paquete se perdió y no respondemos
    if rand < 4:
        continue
    
    # De lo contrario, el servidor responde
    socket_servidor.sendto(mensaje, direccion_cliente)

