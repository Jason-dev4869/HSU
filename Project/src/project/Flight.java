package project;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Flight {
    private String ID, LocateStart, LocateEnd, Status, Airline_Name;
    private LocalDateTime datetimeStart = null, datetimeEnd = null;
    private int Chairs = 0;

    public static final DateTimeFormatter dt_format = DateTimeFormatter.ofPattern("HH:mm dd/MM/yyyy");

    public Flight(String ID, String LocateStart, String LocateEnd, String Status, 
                  String Airline_Name, int Chairs, LocalDateTime datetimeStart, 
                  LocalDateTime datetimeEnd) {
        this.ID = ID;
        this.LocateStart = LocateStart;
        this.LocateEnd = LocateEnd;
        this.Status = Status;
        this.Airline_Name = Airline_Name;
        this.Chairs = Chairs;
        this.datetimeStart = datetimeStart;
        this.datetimeEnd = datetimeEnd;
    }

    public String getID() {
        return ID;
    }

    public void setID(String ID) {
        this.ID = ID;
    }

    public String getLocateStart() {
        return LocateStart;
    }

    public void setLocateStart(String LocateStart) {
        this.LocateStart = LocateStart;
    }

    public String getLocateEnd() {
        return LocateEnd;
    }

    public void setLocateEnd(String LocateEnd) {
        this.LocateEnd = LocateEnd;
    }

    public String getStatus() {
        return Status;
    }

    public void setStatus(String Status) {
        this.Status = Status;
    }

    public String getAirline_Name() {
        return Airline_Name;
    }

    public void setAirline_Name(String Airline_Name) {
        this.Airline_Name = Airline_Name;
    }

    public LocalDateTime getDatetimeStart() {
        return datetimeStart;
    }

    public void setDatetimeStart(LocalDateTime datetimeStart) {
        this.datetimeStart = datetimeStart;
    }

    public LocalDateTime getDatetimeEnd() {
        return datetimeEnd;
    }

    public void setDatetimeEnd(LocalDateTime datetimeEnd) {
        this.datetimeEnd = datetimeEnd;
    }

    public int getChairs() {
        return Chairs;
    }

    public void setChairs(int Chairs) {
        this.Chairs = Chairs;
    }

    @Override
    public String toString() {
        return "Flight{" + "ID=" + ID + ", LocateStart=" + LocateStart + 
                ", LocateEnd=" + LocateEnd + ", Status=" + Status + 
                ", Airline_Name=" + Airline_Name + ", datetimeStart=" + datetimeStart + 
                ", datetimeEnd=" + datetimeEnd + ", Chairs=" + Chairs + '}';
    }
}
