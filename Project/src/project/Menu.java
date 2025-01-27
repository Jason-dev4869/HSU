package project;

import java.util.Scanner;

public class Menu {
    String[] hints;
    int n = 0;

    public Menu(int size) {
        if (size < 1) size = 10;
        hints = new String[size];
    }

    public void add(String aHint) {
        if (n < hints.length) {
            hints[n++] = aHint;
        }
    }

    public int getChoice() {
        int result = 0;
        if (n > 0) {
            Scanner sc = new Scanner(System.in);
            while (true) {
                try {
                    for (int i = 0; i < n; i++) {
                        System.out.println((i + 1) + "-" + hints[i]);
                    }
                    System.out.print("Please select an operation: ");
                    result = Integer.parseInt(sc.nextLine().trim());

                    if (result >= 1 && result <= n) {
                        break;
                    } else {
                        System.out.println("Invalid choice. Please select a number between 1 and " + n + ".\n");
                    }
                } catch (NumberFormatException e) {
                    System.out.println("Invalid input. Please enter a valid number.\n");
                }
            }
        }
        return result;
    }
}