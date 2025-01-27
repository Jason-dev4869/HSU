package project;

public class Login_Test {
    public static void main(String[] args) {
        Menu m = new Menu(3);
        System.out.println("What account you're ?");
        m.add("Admin");
        m.add("User");
        m.add("Quit");
        int choice;
        do{
            System.out.println("\n FLIGHT MANAGER");
            choice = m.getChoice();
            switch(choice){
                case 1: Flight_Management.main(args); break;
                case 2: Emp_Flight_Menu.main(args); break;
            }
        }while(choice >=1 && choice<3);
    }
}
