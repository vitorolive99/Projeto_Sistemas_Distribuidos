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