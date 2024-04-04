import pygame
import socket
import threading
from player import Player

# Constantes
HOST = "127.0.0.1"
PORT = 5555
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class DominoClient:
  def __init__(self):
    # Conexão com o servidor
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.conn.connect((HOST, PORT))

    # Inicialização do PyGame
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.clock = pygame.time.Clock()

    # Estado do jogo
    self.room = None
    self.players = []
    self.dominoes = []

    # Inicialização do jogador
    self.player = Player(self.conn, self.receive_message)

    # Thread para receber mensagens do servidor
    self.receive_thread = threading.Thread(target=self.receive_messages)
    self.receive_thread.start()

  def run(self):
    # Loop principal do cliente
    while True:
      # Processar eventos
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.close()
          return

        # Atualizar estado do jogo
        self.update()

        # Desenhar tela
        self.draw()

        # Limitar taxa de atualização
        self.clock.tick(60)

  def receive_messages(self):
    while True:
      try:
        message = self.conn.recv(1024).decode()
        # ... (implementar lógica para processar mensagens do servidor)
      except Exception as e:
        print(f"Erro ao receber mensagem: {e}")
        self.close()
        return

  def update(self):
    # ... (implementar lógica para atualizar o estado do jogo com base nas mensagens recebidas)
    pass

  def draw(self):
    # Desenhar o fundo da tela
    self.screen.fill((255, 255, 255))

    # Desenhar elementos do jogo (mesa, dominós, jogadores)
    # ... (implementar lógica para desenhar os elementos específicos do jogo)

    # Atualizar a tela
    pygame.display.update()

  def close(self):
    self.conn.close()
    pygame.quit()

if __name__ == "__main__":
  client = DominoClient()
  client.run()
