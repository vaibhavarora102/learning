class Calc
{
    public int add(int a, int b) {
        return a + b;
    }
    public int subtract(int a, int b) {
        return a - b;
    }
}



public class Inheritence {
    public static void main(String[] args) {
        VeryAdvCalc c = new VeryAdvCalc();
        int r1 = c.add(10, 12);
        int r2 = c.subtract(10, 12);
        int r3 = c.multiply(10, 12);
        double r4 = c.power(10, 2);
        double r5 = c.divide(10, 2);
        System.out.println(r1 + " " + r2 + " " + r3 + " " + r4 + " " + r5 );
        System.out.println("Hello, Inheritance!");
    }
}