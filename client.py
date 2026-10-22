import socket
import threading
import sys

# Configuration
HOST = '127.0.0.1'
PORT = 65432

alias = input("Choose your chat alias: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except ConnectionRefusedError:
    print("Could not connect to the server. Is server.py running?")
    sys.exit()

def receive_messages():
    """Continuously listens for messages from the server."""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'ALIAS_REQUEST':
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred! Disconnected from server.")
            client.close()
            break

def send_messages():
    """Continuously captures user input and sends it to the server."""
    while True:
        try:
            user_input = input("")
            if user_input.lower() == 'exit':
                client.close()
                break
            message = f"{alias}: {user_input}"
            client.send(message.encode('utf-8'))
        except:
            break

# Start threads for simultaneous receiving and sending
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=send_messages)
write_thread.start()
