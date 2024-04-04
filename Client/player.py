class Player:
  def __init__(self, conn, addr):
    self.conn = conn
    self.addr = addr
    self.dominoes = []  # Lista de dominós do jogador

  def send_message(self, message):
    self.conn.sendall(message.encode())

  def receive_message(self):
    return self.conn.recv(1024).decode()

  def take_turn(self, room):
    # Exibir opções para o jogador (ex: dominos na mão, mesa)
    self.send_message("Sua vez! Escolha uma ação:\n")
    self.send_message("1. Listar dominos\n")
    self.send_message("2. Jogar um domino\n")
    # ... (outras ações possíveis)

    choice = self.receive_message()
    if choice == "1":
      # Exibir lista de dominos do jogador
      self.send_message("Seus dominos:\n")
      # ... (implementar lógica para mostrar dominos)
    elif choice == "2":
      # Jogar um domino
      domino_choice = self.receive_message()
      # ... (implementar lógica para validar e jogar domino na mesa)
      room.play_domino(self, domino_choice)  # Envia jogada para a sala
    else:
      self.send_message("Opção inválida. Tente novamente.\n")

