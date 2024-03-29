import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;

public class DominoServer {
    private static final int PORT = 8888;

    private List<Room> rooms;

    public DominoServer() {
        rooms = new ArrayList<>();
    }

    public void start() {
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Servidor iniciado na porta " + PORT);
            while (true) {
                Socket socket = serverSocket.accept();
                System.out.println("New connection: " + socket);
                handleConnection(socket);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void handleConnection(Socket socket) {
        Room room = null;
        for (Room r : rooms) {
            if (!r.isFull()) {
                room = r;
                break;
            }
        }

        if (room == null) {
            room = new Room();
            rooms.add(room);
        }

        room.addPlayer(new Player(socket));

        if (room.isFull()) {
            Room thread = new Room();
            thread.start();
        }
    }

    public static void main(String[] args) {
        DominoServer server = new DominoServer();
        server.start();
    }
}

