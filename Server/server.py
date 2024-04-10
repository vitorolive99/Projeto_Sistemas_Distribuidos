import socket
import threading
from player import Player
from room import Room
import json


# Função para lidar com cada cliente
def handle_client(conn, addr, rooms: list[Room]):
    try:
        # Criar um novo jogador
        player_obj = Player(conn, addr)

        # Informar o jogador sobre a conexão
        print(f"Novo jogador conectado: {addr}")

        # Enviar lista de salas disponíveis para o jogador
        # Código 1000 - Enviar lista de salas e suas informações
        room_data = []
        for room_obj in rooms:
            room_info = {
            "code": "1000",
            "room_id": room_obj.room_id,
            "players": f"{len(room_obj.players)}/{room_obj.max_players}"
            }
            room_data.append(room_info)
        
        json_data = json.dumps(room_data)
        conn.sendall(json_data.encode())

        # Esperar que o jogador escolha uma sala    
        json_data = conn.recv(1024).decode()
        room_choice = int(json.loads(json_data)["chose"])

        # Adicionar o jogador à sala escolhida
        rooms[room_choice].add_player(player_obj)
        print(f"Jogador {addr} adicionado à sala {room_choice}")

        # Verificar se a sala está cheia para iniciar a partida
        rooms[room_choice].start_game()

    except Exception as e:
        print(f"Jogador desconectado. {addr}: {e}")
        conn.close()


# Função principal do servidor
def main():
    # Configurações do servidor
    host = "127.0.0.1"
    port = 5555
    max_players_per_room = 1
    max_rooms = 3

    # Lista de salas
    rooms = [Room(room_id, max_players_per_room) for room_id in range(max_rooms)]

    # Inicializa o socket do servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Servidor de dominó iniciado em {host}:{port}")

    try:
        while True:
            # Aceitar novas conexões
            conn, addr = server.accept()
            
            # Criar uma thread para cada cliente
            thread = threading.Thread(target=handle_client, args=(conn, addr, rooms))
            thread.start()

    except Exception as e:
        print(f"Erro no servidor: {e}")
        server.close()

    finally:
        server.close()


if __name__ == "__main__":
    main()
