from socket import *

def create_server_socket(port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    print(f"Ready to serve on port {port}")
    return server_socket

def handle_client_connection(client_socket, initial_location=None):
    if initial_location is None:
        # Esta es la llamada inicial, necesitas analizar la solicitud para obtener la ubicación inicial.
        request = client_socket.recv(1024).decode('utf-8')
        request_lines = request.split('\r\n')
        if len(request_lines) < 1:
            print("Invalid request format")
            return

        request_words = request_lines[0].split()
        if len(request_words) < 2:
            print("Invalid request format")
            return

        initial_location = request_words[1].lstrip('/').replace("www.", "", 1)

    filename = initial_location
    file_path = "./" + filename

    try:
        with open(file_path, "rb") as file:
            content = file.read()
            client_socket.send("HTTP/1.0 200 OK\r\n".encode('utf-8'))
            client_socket.send("Content-Type: text/html\r\n".encode('utf-8'))
            client_socket.send("\r\n".encode('utf-8'))
            client_socket.sendall(content)
            print('Read from cache')

    except FileNotFoundError:
        try:
            remote_socket = socket(AF_INET, SOCK_STREAM)
            host = filename.replace("www.", "", 1)
            remote_socket.connect((host, 80))
            remote_socket.sendall(request.encode('utf-8'))
            
            response = b""
            while True:
                data = remote_socket.recv(4096)
                if not data:
                    break
                response += data
                client_socket.sendall(data)

            # Parse the response to check for redirection
            response_lines = response.decode('utf-8').split('\r\n')
            if response_lines[0].startswith('HTTP/1.0 3') or response_lines[0].startswith('HTTP/1.1 3'):
                for line in response_lines:
                    if line.startswith('Location:'):
                        new_location = line.split(' ')[1]
                        print(f"Redirecting to: {new_location}")
                        # Recur with the new location
                        handle_client_connection(client_socket, new_location)
                        return

            with open(file_path, "wb") as file:
                file.write(response)

            print('Received response from web server')

        except Exception as e:
            print(f"Error: {e}")
            client_socket.send("HTTP/1.0 404 Not Found\r\n".encode('utf-8'))
            client_socket.send("Content-Type: text/html\r\n".encode('utf-8'))
            client_socket.send("\r\n".encode('utf-8'))
            client_socket.send("<html><body><h1>404 Not Found</h1></body></html>".encode('utf-8'))

    finally:
        client_socket.close()




def start_proxy_server(port):
    server_socket = create_server_socket(port)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Received a connection from: {addr}")
        handle_client_connection(client_socket)

    server_socket.close()

if __name__ == "__main__":
    start_proxy_server(8886)
