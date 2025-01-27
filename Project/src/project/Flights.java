package project;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.Scanner;

public class Flights {
    private ArrayList<Flight> FL = new ArrayList<>();
    protected static final String FILE_PATH = "Flight.csv";

    private ArrayList<Flight> readFromFile() {
        ArrayList<Flight> fs = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(FILE_PATH))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] fields = line.split(",");
                if (fields.length < 8) continue;
                try {
                    Flight f = new Flight(
                        fields[0],
                        fields[1],
                        fields[2],
                        fields[3],
                        fields[4],
                        Integer.parseInt(fields[5]),
                        LocalDateTime.parse(fields[6], Flight.dt_format),
                        LocalDateTime.parse(fields[7], Flight.dt_format)
                    );
                    fs.add(f);
                } catch (NumberFormatException | DateTimeParseException e) {
                    System.out.println("Error parsing flight data: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            System.out.println("Error reading the file: " + e.getMessage());
        }
        return fs;
    }
    
    private boolean isDuplicateID(String id) {
        ArrayList<Flight> fs = readFromFile();
        for (Flight f : fs) {
            if (f.getID().equalsIgnoreCase(id)) {
                return true;
            }
        }
        return false;
    }
    
    private void writeToFile(ArrayList<Flight> fs, boolean append) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_PATH, append))) {
            for (Flight f : fs) {
                String line = String.format(
                    "%s,%s,%s,%s,%s,%d,%s,%s%n",
                    f.getID(),
                    f.getAirline_Name(),
                    f.getLocateStart(),
                    f.getLocateEnd(),
                    f.getStatus(),
                    f.getChairs(),
                    f.getDatetimeStart().format(f.dt_format),
                    f.getDatetimeEnd().format(f.dt_format)
                );
                writer.write(line);
            }
        } catch (IOException e) {
            System.out.println("Error writing to file: " + e.getMessage());
        }
    }
    
    public void Add_Flight() {
        Scanner sc = new Scanner(System.in);
        boolean addMore;

        do {
            String id, airlineName, locateStart, locateEnd, status;
            int chairs;
            LocalDateTime datetimeStart, datetimeEnd;

           do {
                System.out.println("Enter Flight ID:");
                id = sc.nextLine().trim();
                if (id.isEmpty()) {
                    System.out.println("Flight ID cannot be empty.");
                } else if (isDuplicateID(id)) {
                    System.out.println("Flight ID already exists. Please enter a different ID.");
                    id = "";
                }
            } while (id.isEmpty());

            do {
                System.out.println("Enter Airline Name:");
                airlineName = sc.nextLine().trim();
                if (airlineName.isEmpty()) {
                    System.out.println("Airline Name cannot be empty.");
                }
            } while (airlineName.isEmpty());

            do {
                System.out.println("Enter Start Location:");
                locateStart = sc.nextLine().trim();
                if (locateStart.isEmpty()) {
                    System.out.println("Start Location cannot be empty.");
                }
            } while (locateStart.isEmpty());

            do {
                System.out.println("Enter End Location:");
                locateEnd = sc.nextLine().trim();
                if (locateEnd.isEmpty()) {
                    System.out.println("End Location cannot be empty.");
                }
            } while (locateEnd.isEmpty());

            while (true) {
                System.out.println("Enter number of chairs:");
                try {
                    chairs = Integer.parseInt(sc.nextLine().trim());
                    if (chairs <= 0) {
                        System.out.println("Chairs must be greater than 0.");
                    } else {
                        break;
                    }
                } catch (NumberFormatException e) {
                    System.out.println("Invalid number format. Please enter a valid integer.");
                }
            }

            while (true) {
                System.out.println("Enter Start Date & Time (HH:mm dd/MM/yyyy):");
                try {
                    datetimeStart = LocalDateTime.parse(sc.nextLine().trim(), Flight.dt_format);
                    break;
                } catch (DateTimeParseException e) {
                    System.out.println("Invalid format. Please use HH:mm dd/MM/yyyy.");
                }
            }

            while (true) {
                System.out.println("Enter End Date & Time (HH:mm dd/MM/yyyy):");
                try {
                    datetimeEnd = LocalDateTime.parse(sc.nextLine().trim(), Flight.dt_format);
                    if (datetimeEnd.isBefore(datetimeStart)) {
                        System.out.println("End Date & Time must be after Start Date & Time.");
                    } else {
                        break;
                    }
                } catch (DateTimeParseException e) {
                    System.out.println("Invalid format. Please use HH:mm dd/MM/yyyy.");
                }
            }

            do {
                System.out.println("Enter Flight Status:");
                status = sc.nextLine().trim();
                if (status.isEmpty()) {
                    System.out.println("Flight Status cannot be empty.");
                }
            } while (status.isEmpty());

            Flight newFlight = new Flight(id, locateStart, locateEnd, status, airlineName, chairs, datetimeStart, datetimeEnd);
            newFlight.setChairs(chairs);
            newFlight.setDatetimeStart(datetimeStart);
            newFlight.setDatetimeEnd(datetimeEnd);

            FL.add(newFlight);

            ArrayList<Flight> temp = new ArrayList<>();
            temp.add(newFlight);
            writeToFile(temp, true);

            System.out.println("Flight added successfully!");

            System.out.println("Do you want to add another flight? (Y/N): ");
            addMore = sc.nextLine().trim().equalsIgnoreCase("Y");

        } while (addMore);
    }
    
    public void Display_Flight() {
        System.out.println("Loading data from file...");
        FL = readFromFile();

        if (FL.isEmpty()) {
            System.out.println("No flights available to display.");
            return;
        }

        System.out.printf("%-10s %-20s %-20s %-20s %-10s %-10s %-20s %-20s%n",
            "ID", "Airline", "Start Location", "End Location", "Status", "Chairs", "Start Time", "End Time");
        System.out.println("-----------------------------------------------------------------------------------------------------------------------------");

        for (Flight FD : FL) {
            System.out.printf("%-10s %-20s %-20s %-20s %-10s %-10d %-20s %-20s%n",
                FD.getID(),
                FD.getAirline_Name(),
                FD.getLocateStart(),
                FD.getLocateEnd(),
                FD.getStatus(),
                FD.getChairs(),
                FD.getDatetimeStart().format(FD.dt_format),
                FD.getDatetimeEnd().format(FD.dt_format));
        }
    }
    
    public void Remove_Flight() {
    Display_Flight();

    Scanner sc = new Scanner(System.in);
    boolean rm_more;

    do {
        System.out.println("Enter the Flight ID to remove:");
        String idToRemove = sc.nextLine().trim();

        boolean found = false;
        for (int i = 0; i < FL.size(); i++) {
            if (FL.get(i).getID().equalsIgnoreCase(idToRemove)) {
                Flight FR = FL.get(i);
                System.out.println("Flight found:");
                System.out.printf(
                    "%-10s %-20s %-20s %-20s %-10s %-10d %-20s %-20s%n",
                    FR.getID(),
                    FR.getAirline_Name(),
                    FR.getLocateStart(),
                    FR.getLocateEnd(),
                    FR.getStatus(),
                    FR.getChairs(),
                    FR.getDatetimeStart().format(FR.dt_format),
                    FR.getDatetimeEnd().format(FR.dt_format)
                );

                System.out.println("Are you sure you want to remove this flight? (Y/N): ");
                String confirmation = sc.nextLine().trim().toUpperCase();
                if (confirmation.equals("Y")) {
                    FL.remove(i);
                    System.out.println("Flight with ID: " + idToRemove + " has been removed.");
                    writeToFile(FL, false);
                } else {
                    System.out.println("Flight removal canceled.");
                }
                found = true;
                break;
            }
        }
        if (!found) {
            System.out.println("Flight ID: " + idToRemove + " not found in the list.");
        }

        System.out.println("Do you want to remove another flight? (Y/N): ");
        String choice = sc.nextLine().trim().toUpperCase();
        rm_more = choice.equals("Y");
        } while (rm_more);
    }
    
    public void Update_Flight() {
    Display_Flight();

    Menu m = new Menu(8);
    Scanner sc = new Scanner(System.in);
    boolean up_more;

    do {
        System.out.println("Enter the Flight ID to Update:");
        String idToUpdate = sc.nextLine().trim();
        boolean found = false;

        for (int i = 0; i < FL.size(); i++) {
            if (FL.get(i).getID().equalsIgnoreCase(idToUpdate)) {
                Flight FU = FL.get(i);
                found = true;

                System.out.println("Flight Found:");
                System.out.printf(
                    "%-10s %-20s %-20s %-20s %-10s %-10d %-20s %-20s%n",
                    FU.getID(),
                    FU.getAirline_Name(),
                    FU.getLocateStart(),
                    FU.getLocateEnd(),
                    FU.getStatus(),
                    FU.getChairs(),
                    FU.getDatetimeStart().format(FU.dt_format),
                    FU.getDatetimeEnd().format(FU.dt_format)
                );

                m.add("Airline Name");
                m.add("Start Location");
                m.add("End Location");
                m.add("Number of Chairs");
                m.add("Start DateTime");
                m.add("End DateTime");
                m.add("Flight Status");
                m.add("Back to Main Menu");

                int slt;
                do {
                    System.out.println("\nUpdate Menu:");
                    slt = m.getChoice();
                    switch (slt) {
                        case 1:
                            System.out.println("Enter new Airline Name:");
                            FU.setAirline_Name(sc.nextLine().trim());
                            confirmAndWriteToFile(FU, FL);
                            break;

                        case 2:
                            System.out.println("Enter new Start Location:");
                            FU.setLocateStart(sc.nextLine().trim());
                            confirmAndWriteToFile(FU, FL);
                            break;

                        case 3:
                            System.out.println("Enter new End Location:");
                            FU.setLocateEnd(sc.nextLine().trim());
                            confirmAndWriteToFile(FU, FL);
                            break;

                        case 4:
                            boolean validChairs = false;
                            do {
                                System.out.println("Enter new number of chairs:");
                                try {
                                    FU.setChairs(Integer.parseInt(sc.nextLine().trim()));
                                    validChairs = true;
                                } catch (NumberFormatException e) {
                                    System.out.println("Invalid number format. Please enter a valid integer.");
                                }
                            } while (!validChairs);
                            confirmAndWriteToFile(FU, FL);
                            break;

                        case 5:
                            LocalDateTime newStartTime = null;
                            do {
                                System.out.println("Enter new Start DateTime (HH:mm dd/MM/yyyy):");
                                try {
                                    newStartTime = LocalDateTime.parse(sc.nextLine().trim(), FU.dt_format);
                                    FU.setDatetimeStart(newStartTime);
                                } catch (DateTimeParseException e) {
                                    System.out.println("Invalid format. Please use HH:mm dd/MM/yyyy.");
                                }
                            } while (newStartTime == null);
                            confirmAndWriteToFile(FU, FL);
                            break;

                        case 6:
                            LocalDateTime newEndTime = null;
                            do {
                                System.out.println("Enter new End DateTime (HH:mm dd/MM/yyyy):");
                                try {
                                    newEndTime = LocalDateTime.parse(sc.nextLine().trim(), FU.dt_format);
                                    FU.setDatetimeEnd(newEndTime);
                                } catch (DateTimeParseException e) {
                                    System.out.println("Invalid format. Please use HH:mm dd/MM/yyyy.");
                                }
                            } while (newEndTime == null);
                            confirmAndWriteToFile(FU, FL);
                            break;

                        case 7:
                            System.out.println("Enter new Flight Status:");
                            FU.setStatus(sc.nextLine().trim());
                            confirmAndWriteToFile(FU, FL);
                            break;

                        case 8:
                            System.out.println("Returning to Main Menu...");
                            return; // Quay về menu chính
                            
                            default:
                                System.out.println("Invalid choice. Please select a valid option.");
                        }
                    } while (slt >= 1 && slt <= 8);
                }
            }

            if (!found) {
                System.out.println("Flight getID(): " + idToUpdate + " not found in the list.");
            }

            System.out.println("Do you want to update another flight? (Y/N): ");
            String choice = sc.nextLine().trim().toUpperCase();
            up_more = choice.equals("Y");

        } while (up_more);
    }

    
    private void confirmAndWriteToFile(Flight updatedFlight, ArrayList<Flight> fs) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Do you want to save this change to the file? (Y/N): ");
        String choice = sc.nextLine().trim().toUpperCase();

        if (choice.equals("Y")) {
            writeToFile(fs, false); // Ghi toàn bộ danh sách
            System.out.println("Changes for flight ID " + updatedFlight + " have been saved.");
        } else {
            System.out.println("Changes were not saved.");
    }
}
    
    public void Search_Flight() {
        Scanner sc = new Scanner(System.in);
        boolean searchAgain;

        do {
            System.out.println("Enter a keyword to search for flights:");
            String keyword = sc.nextLine().trim().toLowerCase();

            ArrayList<Flight> fileFlights = readFromFile();
            boolean found = false;

            System.out.printf(
                "%-10s %-20s %-20s %-20s %-10s %-10s %-20s %-20s%n",
                "ID", "Airline Name", "Start Location", "End Location",
                "Status", "Chairs", "Start DateTime", "End DateTime"
            );
            System.out.println("-------------------------------------------------------------------------------------------");

            for (Flight f : fileFlights) {
                if (f.getID().toLowerCase().contains(keyword) ||
                    f.getAirline_Name().toLowerCase().contains(keyword) ||
                    f.getLocateStart().toLowerCase().contains(keyword) ||
                    f.getLocateEnd().toLowerCase().contains(keyword) ||
                    f.getStatus().toLowerCase().contains(keyword) ||
                    String.valueOf(f.getChairs()).contains(keyword) || 
                    f.getDatetimeStart().format(f.dt_format).toLowerCase().contains(keyword) ||
                    f.getDatetimeEnd().format(f.dt_format).toLowerCase().contains(keyword)) {

                    System.out.printf(
                        "%-10s %-20s %-20s %-20s %-10s %-10d %-20s %-20s%n",
                        f.getID(),
                        f.getAirline_Name(),
                        f.getLocateStart(),
                        f.getLocateEnd(),
                        f.getStatus(),
                        f.getChairs(),
                        f.getDatetimeStart().format(f.dt_format),
                        f.getDatetimeEnd().format(f.dt_format)
                    );
                    found = true;
                }
            }

            if (!found) {
                System.out.println("No flights matched the keyword: " + keyword);
            }

            System.out.println("Do you want to search for another flight? (Y/N): ");
            String choice = sc.nextLine().trim().toUpperCase();
            searchAgain = choice.equals("Y");
        } while (searchAgain);

        System.out.println("Exiting search. Thank you!");
    }
    
}
