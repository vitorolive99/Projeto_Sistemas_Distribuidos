
import java.util.ArrayList;
import java.util.List;

public class Room extends Thread{
    private List<Player> players;
    private boolean gameStarted;
    private ArrayList<Pedra> pedras;
    private boolean primeiraPartida = true;
    private int jogadorVez;
    private int ultimoGanhador;
    private boolean fechou = false;
    private boolean pingou = false;
    private int pingo = 0;

    public Room() {
        players = new ArrayList<>();
        gameStarted = false;
    }

    public synchronized void addPlayer(Player player) {
        players.add(player);
        System.out.println("Player added to room. Total players: " + players.size());
    }

    public synchronized boolean isFull() {
        return players.size() == 4;
    }

    public synchronized void startGame() {
        gameStarted = true;
        System.out.println("Game started in room. Total players: " + players.size());

        distribuicaoPedras();

        if (primeiraPartida = true) {
            for (Player player : players) {
                if (player.isSena()) {
                    jogadorVez = players.indexOf(player);
                }
            }
            primeiraPartida = false;            
        }

        //enviando as pecas para os jogadores no cliente
        for (Player player : players) {
            player.sendPedras();
        }

        Pedra jogada;
        //codigo 10 para o jogador da vez
        players.get(jogadorVez).sendMessage(10);

        //recebendo a jogada do jogador
        jogada = players.get(jogadorVez).receivePedra();

        pedras.add(jogada);

        
        while(!fechou || !players.get(jogadorVez).acabouMao()){
            jogadorVez++;
            if (jogadorVez == 4) {
                jogadorVez = 0;
            }   
            
            players.get(jogadorVez).sendMessage(10);

            pingou=players.get(jogadorVez).receivePingo();

            if(!pingou){

                pingo = 0;
                //recebendo a jogada do jogador
                jogada = players.get(jogadorVez).receivePedra();

                if (jogada.getLado2() == pedras.get(0).getLado1() || jogada.getLado1() == pedras.get(0).getLado1() ) {
                    if (jogada.getLado1() == pedras.get(0).getLado1()) {
                        jogada.inverte();
                    }
                    pedras.add(0, jogada);                
                }
                if (jogada.getLado2() == pedras.get(pedras.size()-1).getLado2() || jogada.getLado1() == pedras.get(pedras.size()-1).getLado2()){
                    if (jogada.getLado2() == pedras.get(0).getLado2()) {
                        jogada.inverte();
                    }
                    pedras.add(jogada);    
                }
            }else{
                pingo++;
            }
            if (pingo ==4) {
                fechou = true;
            }
        }

        

        // Implemente a lógica para distribuir peças, etc.
        // Você pode chamar um método para iniciar o jogo com a lista de jogadores aqui.
    }

    @Override
    public void run() {
        startGame();
    }

    private void distribuicaoPedras() {
        for (int i = 0; i < 7; i++) {
            for (int j = i; j < 7; j++) {
                pedras.add(new Pedra(i, j));
            }
        }

        for (Player player : players) {
            for (int k = 0; k < 7; k++) {
                player.addPedra(pedraAleatoria());
            }
        }
    }
    
    private Pedra pedraAleatoria() {
        Pedra pedra = pedras.get((int) (Math.random() * pedras.size()));
        pedras.remove(pedra);
        return pedra;
    }

    // Outros métodos relevantes para a lógica do jogo podem ser adicionados aqui
}

class Pedra {
    private int lado1;
    private int lado2;

    public Pedra(int lado1, int lado2) {
        this.lado1 = lado1;
        this.lado2 = lado2;
    }

    public int getLado1() {
        return lado1;
    }

    public int getLado2() {
        return lado2;
    }

    public void inverte() {
        int aux;
        aux = lado1;
        lado1 = lado2;
        lado2 = aux;
    }
}

