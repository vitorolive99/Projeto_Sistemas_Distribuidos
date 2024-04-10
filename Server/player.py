import json
from domino import Domino

class Player:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.mao: list[Domino] = []  # Lista de dominós do jogador

    def send_message(self, message):
        """Envia uma mensagem para o cliente."""
        try:
            json_data = json.dumps(message)
            encoded_data = json_data.encode()
            self.conn.sendall(encoded_data)
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

    def receive_message(self):
        """Recebe uma mensagem do cliente."""
        try:
            encoded_data = self.conn.recv(4096)
            json_data = encoded_data.decode()
            return json.loads(json_data)
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            return None

      
    def add_domino(self, domino):
        self.mao.append(domino)
        
    def count_tiles(self):
        sum_of_dominoes = 0

        for domino in self.mao:
            sum_of_dominoes += domino.sum_vals()

        return sum_of_dominoes

