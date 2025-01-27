package project;

public class Emp_Flight_Menu {
    public static void main(String[] args) {
        Menu m = new Menu(3);
        m.add("Search Flight");
        m.add("Display Flight Board");
        m.add("Quit");
        int choice;
        Flights f = new Flights();
        do{
            System.out.println("\n FLIGHT MANAGER");
            choice = m.getChoice();
            switch(choice){
                case 1: //f.Search_Flight(); break;
                case 2: //f.Display_Flight(); break;
                case 3: System.exit(0);
            }
        }while(choice >=1 && choice<3);
    }
}
