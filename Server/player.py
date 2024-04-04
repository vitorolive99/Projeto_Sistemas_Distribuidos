
class Player:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.mao = []  # Lista de dominós do jogador

    def send_message(self, message):
        self.conn.sendall(message.encode())

    def receive_message(self):
        return self.conn.recv(1024).decode()
      
    def add_domino(self, domino):
        self.mao.append(domino)
        
    def count_tiles(self):
        sum_of_dominoes = 0

        for domino in self.dominoes:
            sum_of_dominoes += domino.sum_vals()

        return sum_of_dominoes

