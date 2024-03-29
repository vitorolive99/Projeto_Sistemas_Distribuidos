import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;
import java.util.ArrayList;

public class Player {
    private Socket socket;
    private ObjectInputStream inputStream;
    private ObjectOutputStream outputStream;
    private ArrayList<Pedra> mao;

    public Player(Socket socket) {
        this.socket = socket;
        try {
            outputStream = new ObjectOutputStream(this.socket.getOutputStream());
            inputStream = new ObjectInputStream(this.socket.getInputStream());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    void addPedra(Pedra pedra) {
        mao.add(pedra);
    }

    // Métodos para enviar e receber mensagens entre o servidor e o cliente
    // incluir métodos para enviar peças, informações de jogo, etc.

    // Exemplo de método para enviar uma mensagem para o cliente
    public void sendMessage(int message) {
        try {
            outputStream.writeInt(message);
            outputStream.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void sendPedras() {
        try {
            for (Pedra pedra : mao) {
                outputStream.writeObject(pedra);
            }
            outputStream.flush();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Exemplo de método para receber uma mensagem do cliente
    public Pedra receivePedra() {
        Pedra pedra = null;
        try {
            // Recebe o objeto do inputStream
            Object receivedObject = inputStream.readObject();

            // Verifica se o objeto recebido é uma instância de Pedra
            if (receivedObject instanceof Pedra) {
                // Converte o objeto para uma instância de Pedra
                pedra = (Pedra) receivedObject;
            } else {
                // Caso o objeto não seja uma instância de Pedra, imprime uma mensagem de erro
                System.err.println("Objeto recebido não é uma instância de Pedra.");
            }
        } catch (IOException | ClassNotFoundException e) {
            // Trata possíveis exceções de IO ou ClassNotFoundException
            e.printStackTrace();
        }
        return pedra;
    }

    public boolean isSena() {
        for (Pedra pedra : mao) {
            if (pedra.getLado1() == 6 && pedra.getLado2() == 6) {
                return true;
            }
        }
        return false;
    }

    public Object getMao() {
        return mao;
    }

    public boolean acabouMao() {
        if (mao.size() == 0) {
            return true;
        }
        return false;
    }

    public boolean receivePingo() {
        try {
            return inputStream.readBoolean();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }

    public Object receiveMessage() {
        Object message = null;
        try {
            message = inputStream.readObject();
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
        return message;
    }

    // Outros métodos relevantes para a lógica do jogo podem ser adicionados aqui
}

