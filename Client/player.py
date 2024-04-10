import json

class Player:
  def __init__(self, conn, addr):
    self.conn = conn
    self.addr = addr
    self.dominoes = []  # Lista de dominós do jogador

  def send_message(self, message):
    json_data = json.dumps(message)
    self.conn.sendall(json_data.encode())

  def receive_message(self):
    json_data = self.conn.recv(1024).decode()
    return json.loads(json_data)    

