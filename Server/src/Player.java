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

    public void sendPedrasMao() {
        try {
            for (Pedra pedra : mao) {
                outputStream.writeObject(pedra);
            }
            outputStream.flush();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Recebe a pedra jogada pelo jogador
    public Pedra receivePedra() {
        Pedra pedra = null;
        try {
            Object receivedObject = inputStream.readObject();

            if (receivedObject instanceof Pedra) {
                pedra = (Pedra) receivedObject;
            } else {
                System.err.println("Objeto recebido não é uma instância de Pedra.");
            }
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
        return pedra;
    }

    public boolean temSena() {
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
        boolean pingo = false;
        try {
            pingo = inputStream.readBoolean();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return pingo;
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

    public void sendPedrasMesa(ArrayList<Pedra> pedras) {
        try {
            for (Pedra pedra : pedras) {
                outputStream.writeObject(pedra);
            }
            outputStream.flush();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void removePedra(Pedra pedra) {
        mao.remove(pedra);
    }

    // Outros métodos relevantes para a lógica do jogo podem ser adicionados aqui
}

