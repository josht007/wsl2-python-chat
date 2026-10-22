import socket
import threading

HOST = '127.0.0.1'  
PORT = 65432        

clients = []
aliases = []

def broadcast(message, sender_client):
    """sends a message to all connected clients except the sender."""
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except:
                # Remove broken connections
                index = clients.index(client)
                clients.remove(client)
                client.close()
                alias = aliases[index]
                aliases.remove(alias)

def handle_client(client):
    """handles communication with an individual client."""
    while True:
        try:
            message = client.recv(1024)
            if not message:
                raise Exception("Disconnected")
            broadcast(message, client)
        except:
            # Handle client disconnecting gracefully
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                alias = aliases[index]
                print(f"[-] {alias} left the chat.")
                broadcast(f"\n📢 {alias} left the chat room!\n".encode('utf-8'), client)
                aliases.remove(alias)
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Server is listening on {HOST}:{PORT}...")

    while True:
        client, address = server.accept()
        print(f"[+] Connected with {str(address)}")

        # Request and store client alias
        client.send("ALIAS_REQUEST".encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)

        print(f"[*] Alias of client is {alias}")
        broadcast(f" {alias} joined the chat room!\n".encode('utf-8'), client)
        client.send("Connected to the server successfully!\n".encode('utf-8'))

        # Start a dedicated handling thread for the client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    start_server()
