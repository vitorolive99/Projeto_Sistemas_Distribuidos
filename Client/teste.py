import socket
import json
import numpy as np


def main():
    host = "127.0.0.1"  # Endereço IP do servidor
    port = 5555  # Porta do servidor

    # Conectar ao servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))

    try:

        # Simular escolha de sala
        chosen_room = {"chose": "1"}  # Escolha uma sala (exemplo)
        
        salas = receive_message(server_socket)
        len_message = len(salas)
            
        if salas[0]["code"] == "1000":
            for i in range(len_message):
                print(f"Sala {salas[i]['room_id']}\n Jogadores: {salas[i]['players']}")

            # Enviar escolha de sala
            send_message(server_socket, chosen_room)

        i = 1
        # Receber mensagens da sala
        while True:
            message = receive_message(server_socket)
                        
            if message["code"] == "1001":
                print("partida iniciada")
                send_message(server_socket, "ok")
            elif message["code"] == "1002":
                print(message["message"])
                send_message(server_socket, "ok")
                player_mao = receive_message(server_socket)
                print(player_mao)
                send_message(server_socket, "ok")
            elif message["code"] == "1003":
                
                jogada = np.array([i, 4])
                jogada = jogada.tolist()
                print(message["message"])
                send_message(server_socket, jogada)
                i = 4
            elif message["code"] == "1004":
                print("recebendo mesa")
                send_message(server_socket, "ok")
                mesa = receive_message(server_socket)
                send_message(server_socket, "ok")
                print(mesa)
            elif message["code"] == "1005":
                print("Mensagem da sala:", message)
                send_message(server_socket, "ok")

    except Exception as e:
        print("Erro:", e)


def send_message(socket, message):
    """Envia uma mensagem para o servidor."""
    try:
        json_data = json.dumps(message)
        encoded_data = json_data.encode()
        socket.sendall(encoded_data)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def receive_message(socket):
    """Recebe uma mensagem do servidor."""
    try:
        encoded_data = socket.recv(4096)
        json_data = encoded_data.decode()
        return json.loads(json_data)
    except Exception as e:
        print(f"Erro ao receber mensagem: {e}")
        return None



if __name__ == "__main__":
    main()
