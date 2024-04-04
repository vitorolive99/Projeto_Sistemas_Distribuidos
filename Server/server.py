import socket
import threading
from player import Player
from room import Room

# Função para lidar com cada cliente
def handle_client(conn, addr, rooms):
    try:
        # Criar um novo jogador
        player_obj = Player(conn, addr)
        
        # Informar o jogador sobre a conexão
        print(f"Novo jogador conectado: {addr}")

        # Enviar lista de salas disponíveis para o jogador
        conn.sendall(str(len(rooms)).encode())
        for room_obj in rooms:
            room_info = f"Sala {room_obj.room_id}: {len(room_obj.players)}/{room_obj.max_players} jogadores\n"
            conn.sendall(room_info.encode())

        # Solicitar ao jogador que escolha uma sala
        conn.sendall("Escolha uma sala pelo número: ".encode())
        room_choice = int(conn.recv(1024).decode())

        # Adicionar o jogador à sala escolhida
        rooms[room_choice].add_player(player_obj)
        print(f"Jogador {addr} adicionado à sala {room_choice}")

        # Verificar se a sala está cheia para iniciar a partida
        rooms[room_choice].start_game()

    except Exception as e:
        print(f"Erro ao lidar com o cliente {addr}: {e}")
        conn.close()

# Função principal do servidor
def main():
    # Configurações do servidor
    host = "127.0.0.1"
    port = 5555
    max_players_per_room = 4
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
