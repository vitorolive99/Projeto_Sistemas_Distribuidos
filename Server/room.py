import threading
import numpy as np
from domino import Domino 

class Room:
    def __init__(self, room_id, max_players):
        self.room_id = room_id
        self.max_players = max_players
        self.fist_game = True
        self.players = []
        self.lock = threading.Lock()
        self.game_started = False
        self.current_player = None  # Jogador atual
        self.dominoes = np.array([])  # Dominós na mesa
        self.last_winner = None
        
        self.In_Game = False

        self.possibility_of_lock_the_game = False
        self.locked = False
        self.winner = None

    def add_player(self, player):
        with self.lock:
            if not self.is_full():
                self.players.append(player)
            else:
                print(f"Sala {self.room_id} está cheia!")

    def is_full(self):
        return len(self.players) >= self.max_players

    def start_game(self):
        if not self.is_full():
            return
        with self.lock:
            if not self.game_started:
                # Definir jogador inicial (por exemplo, o com o maior domino)
                self.current_player = self.get_starting_player()
                self.game_started = True
                game_thread = threading.Thread(target=self.play_game)
                game_thread.start()

    def play_game(self):
        print(f"Partida iniciada na sala {self.room_id}")
        for player in self.players:
            player.send_message("Partida iniciada!\n")
            
        # Loop principal do jogo
        
        self.dominoes_distribution()
        
        for player in self.players:
            player.send_message("Sua mão: ")
            for domino in player.mao:
                player.send_message(str(domino.values))
        
        while True:
            # Verificar se a partida terminou
            if self.check_game_over(last_turn):
                break

            # Jogada do jogador atual
            self.current_player.send_message("Sua vez!\n")
            
            jogada = self.current_player.receive_message()
            
            self.add_jogada(jogada)
                
            last_turn = self.current_player
            # Trocar para o próximo jogador (implementar lógica circular)
            self.current_player = self.get_next_player()

    def get_starting_player(self):
        if self.fist_game:
            for player in self.players:
                for domino in player.mao:
                    if domino.values[0] == 6 and domino.values[1] == 6:
                        return player
                    
            self.fist_game = False
            
        else:
            return self.last_winner
        

    def get_next_player(self):
        next_index = (self.players.index(self.current_player) + 1) % len(self.players)
        next_player = self.players[next_index]
        return next_player
        

    def check_game_over(self):
        players_without_dominos = 0

        for player in self.players:
            winner = self.check_for_winner(player)

            if winner:
                self.win(player)
                return True
                
            if self.possibility_of_lock_the_game:
                can_play = self.check_player_dominoes(player)
                if can_play:
                    continue
                else:
                    players_without_dominos += 1

            if players_without_dominos >= self.max_players and self.check_table_dominoes():
                self.game_locked()
                return True
            
        return False

    def dominoes_distribution(self):
        for i in range(7):
            for j in range(i, 7):
                self.dominoes = np.append(self.dominoes, Domino((i, j)))

        for player in self.players:
            for _ in range(7):
                player.add_domino(self.draw_random())
                
    def draw_random(self):
        domino = np.random.choice(self.dominoes)
        self.dominoes = np.delete(self.dominoes, np.where(self.dominoes == domino))
        return domino
    
    def check_for_winner(self, player):
        if len(player.mao) == 0:
            return True
        
    def check_player_dominoes(self, player):
        if len(self.dominoes) == 0:
            return True

        left = self.dominoes[0].values[0]
        right = self.dominoes[-1].values[-1]
        for domino in player.dominoes:
            if left in domino.values:
                return True
            if right in domino.values:
                return True

        return False
    
    def check_table_dominoes(self):
        left = self.dominoes[0].values[0]
        right = self.dominoes[-1].values[-1]
        for domino in self.dominoes:
            if left in domino.values:
                return False
            if right in domino.values:
                return False
        
        return True
    
    def game_locked(self):
        self.locked = True
        winner = 1000
        for player in self.players:
            count = player.count_tiles()
            if count < winner:
                winner = count
                self.winner = player
                
        self.win(self.winner)
    
    def win(self, player):
        for player in self.players:
            if self.locked:
                player.send_message("Jogo fechado!\n")
            else:
                player.send_message("Fim de jogo!\n")
            player.send_message(f"O vencedor foi: {player.addr}\n")
            
    def add_jogada(self, domino):
        
        if len(self.dominoes) == 0:
            self.dominoes = np.insert(self.dominoes, 0, domino)

        if domino.values[1] == self.dominoes[0].values[0] or domino.values[0] == self.dominoes[0].values[0]:
            if domino.values[0] == self.dominoes[0].values[0]:
                domino.values = domino.values[::-1] # Inverte os valores do domino
                
            self.dominoes = np.insert(self.dominoes, 0, domino)
            
        elif domino.values[0] == self.dominoes[-1].values[-1] or domino.values[1] == self.dominoes[-1].values[-1]:
            if domino.values[1] == self.dominoes[-1].values[-1]:
                domino.values = domino.values[::-1] # Inverte os valores do domino
            
            self.dominoes = np.append(self.dominoes, domino)
            
        