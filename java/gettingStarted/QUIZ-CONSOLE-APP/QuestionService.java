import java.util.Scanner;

public class QuestionService {

    Question[] questions = new Question[5];
    String selection[] = new String[5];
    
    public QuestionService() {
        questions[0] = new Question(1,"What is the capital of France?", "Paris", "London", "Berlin", "Madrid", "Paris");
        questions[1] = new Question(2, "What is 2 + 2?", "4", "3", "5", "6", "4");
        questions[2] = new Question(3, "What is the largest planet in our solar system?", "Jupiter", "Earth", "Mars", "Saturn", "Jupiter");
        questions[3] = new Question(4, "What is the boiling point of water?", "100 degrees Celsius", "90 degrees Celsius", "80 degrees Celsius", "110 degrees Celsius", "100 degrees Celsius");
        questions[4] = new Question(5, "Who wrote 'To Kill a Mockingbird'?", "Harper Lee", "Mark Twain", "Ernest Hemingway", "F. Scott Fitzgerald", "Harper Lee");
    }

    public void playQuiz() {
        int i = 0;
       for(Question q: questions){
        System.out.println("Question no." + q.getId());
        System.out.println(q.getQuestion());
        System.out.println("1. " + q.getOpt1());
        System.out.println("2. " + q.getOpt2());
        System.out.println("3. " + q.getOpt3());
        System.out.println("4. " + q.getOpt4());

        Scanner sc = new Scanner(System.in);
        selection[i] = sc.nextLine();
        i++;

       }

       for (String s : selection) {
           System.out.println("You selected: " + s);
       }    
    }

    public void printScore() {
        int score = 0;
        for (int i = 0; i < questions.length; i++) {
            if (selection[i].equalsIgnoreCase(questions[i].getAnswer())) {
                score++;
            }
        }
        System.out.println("Your score is: " + score + "/" + questions.length);
    }
    
}
