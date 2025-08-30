public class AdvancedCalculator extends Calc{
    public int multiply(int a, int b) {
        return a * b;
    }

    public int divide(int a, int b) {
        if (b == 0) {
            return 0;
            // throw new ArithmeticException("Division by zero is not allowed.");
        }
        return a / b;
    }
}
