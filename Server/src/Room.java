
import java.util.ArrayList;
import java.util.List;

public class Room extends Thread{
    private List<Player> players;
    private boolean ganhou;
    private ArrayList<Pedra> mesa;
    private boolean primeiraPartida;
    private int jogadorVez;
    private int ultimoGanhador;
    private boolean fechou = false;
    private boolean pingou = false;
    private int pingo = 0;

    public Room() {
        players = new ArrayList<>();
        ganhou = false;
        primeiraPartida = true;
    }

    public synchronized void addPlayer(Player player) {
        players.add(player);
        System.out.println("Player added to room. Total players: " + players.size());
    }

    public synchronized boolean isFull() {
        return players.size() == 4;
    }

    public synchronized void startGame() {
        Pedra jogada;
        System.out.println("Game started in room. Total players: " + players.size());

        distribuicaoPedras();

        //enviando as pecas para os jogadores no cliente
        for (Player player : players) {
            player.sendPedrasMao();
        }

        //verificando qual o primeiro a jogar se for a primeira partida
        if (primeiraPartida == true) {
            for (Player player : players) {
                if (player.temSena()) {
                    jogadorVez = players.indexOf(player);
                }
            }
            primeiraPartida = false;
        }else{
            jogadorVez = ultimoGanhador;
        }
        
        while(!fechou || !ganhou){
            if (jogadorVez == 4) {
                jogadorVez = 0;
            }

            //codigo 1 para o jogador da vez
            players.get(jogadorVez).sendMessage(1);

            //recebendo se o jogador pingou
            pingou=players.get(jogadorVez).receivePingo();

            if(!pingou){
                pingo = 0;
                
                //recebendo a jogada do jogador
                jogada = players.get(jogadorVez).receivePedra();

                if (mesa.size() != 0) {
                    if (jogada.getLado2() == mesa.get(0).getLado1() || jogada.getLado1() == mesa.get(0).getLado1() ) {
                        if (jogada.getLado1() == mesa.get(0).getLado1()) {
                            jogada.inverte();
                        }
                        mesa.add(0, jogada);                
                    }else if (jogada.getLado2() == mesa.get(mesa.size()-1).getLado2() || jogada.getLado1() == mesa.get(mesa.size()-1).getLado2()){
                        if (jogada.getLado2() == mesa.get(0).getLado2()) {
                            jogada.inverte();
                        }
                        mesa.add(jogada);
                    }
                }else {
                    mesa.add(jogada);     
                }
                //removendo a pedra jogada da mao do jogador
                players.get(jogadorVez).removePedra(jogada);

                //enviando aos jogadores as pedras da mesa
                for (Player player : players) {
                    player.sendPedrasMesa(mesa);
                }

            }else{
                pingo++;
                for (Player player : players) {
                    //codigo 2 para informar q o jogador pingou
                    player.sendMessage(2);
                }
            }
            //Se pingo for 4, o jogo fechou
            if (pingo == 4) {
                fechou = true;
            }
            //verificando se o jogador ganhou
            ganhou = players.get(jogadorVez).acabouMao();

            if (ganhou) {
                ultimoGanhador = jogadorVez;
                for (Player player : players) {
                    //codigo 3 para informar q o jogO acabou
                    player.sendMessage(3);
                }
            }
            //passando a vez para o proximo jogador
            jogadorVez++;
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
                mesa.add(new Pedra(i, j));
            }
        }

        for (Player player : players) {
            for (int k = 0; k < 7; k++) {
                player.addPedra(pedraAleatoria());
            }
        }
    }
    
    private Pedra pedraAleatoria() {
        Pedra pedra = mesa.get((int) (Math.random() * mesa.size()));
        mesa.remove(pedra);
        return pedra;
    }

}