from socket import *
import time

# Dirección y puerto del servidor
direccion_servidor = ('localhost', 12000)

# Crear un socket UDP
socket_cliente = socket(AF_INET, SOCK_DGRAM)

# Establecer el valor de tiempo de espera para el socket
socket_cliente.settimeout(1.0)  # Tiempo de espera de 1 segundo

# Número de pings a enviar
num_pings = 10

for i in range(1, num_pings + 1):
    # Preparar el mensaje en el formato requerido
    mensaje = f'Ping {i} {time.time()}'

    try:
        # Enviar el mensaje de ping al servidor
        socket_cliente.sendto(mensaje.encode(), direccion_servidor)

        # Registrar el tiempo cuando se envía el mensaje
        tiempo_inicio = time.time()

        # Recibir la respuesta del servidor
        respuesta, direccion_servidor = socket_cliente.recvfrom(1024)

        # Calcular el tiempo de ida y vuelta (RTT)
        rtt = time.time() - tiempo_inicio

        # Imprimir la respuesta y el RTT
        print(f'Respuesta desde {direccion_servidor}: {respuesta.decode()} | RTT: {rtt:.6f} segundos')

    except timeout:
        # Manejar el tiempo de espera (pérdida de paquetes)
        print(f'Tiempo de espera agotado para Ping {i}')

# Cerrar el socket
socket_cliente.close()
