# Database Project - Phase A

## Table of Contents
1. Introduction
2. Database Design
   - ERD Diagram
   - DSD Schema
   - Normalization
3. Database Implementation
   - Creating Tables
   - Data Insertion Methods
   - Querying Data
4. Backup and Restoration
5. Conclusion

---

## 1. Introduction
This project involves designing and implementing a database for a transportation system, handling passengers, trips, seating, tickets, and discounts. The database is structured to ensure data integrity, efficient querying, and compliance with normalization standards.

The key functionalities of the system include:
- Managing passenger information
- Handling trip and seat assignments
- Processing ticket purchases and discounts
- Managing accessibility requirements

---

## 2. Database Design

### **ERD Diagram**
The Entity-Relationship Diagram (ERD) was designed using ERDPlus and represents the relationships between the six main entities: `Passenger`, `Trip`, `Seat`, `Ticket`, `Discount`, and `Disability`.

👉 **[ERD Diagram](./ERD_Diagram.png)**

### **DSD Schema**
After validating the ERD, we generated the Data Structure Diagram (DSD) to confirm that relationships and constraints were correctly defined.

👉 **[DSD Schema](./DSD_Schema.png)**

### **Normalization**
The schema adheres to **Third Normal Form (3NF)** by ensuring:
- Elimination of redundant data
- Every non-key attribute is functionally dependent on the primary key
- No transitive dependencies exist

---

## 3. Database Implementation

### **Creating Tables**
Tables were created using SQL scripts, ensuring proper data types and relationships. Below is a simplified version of the schema:

```sql
CREATE TABLE Passenger (
    passengerID INT PRIMARY KEY,
    fullName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE Ticket (
    ticketID INT PRIMARY KEY,
    purchaseDate DATE NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    passengerID INT NOT NULL,
    FOREIGN KEY (passengerID) REFERENCES Passenger(passengerID)
);
```
👉 **[Full Schema Script](./createTables.sql)**

### **Data Insertion Methods**
Data was inserted using three different methods:
1. **Manual SQL Inserts** - Directly adding data via SQL scripts.
   - 👉 **[Insert Script](./insertTables.sql)**
2. **Data Import from CSV** - Using external files for batch inserts.
   - 👉 **[Data Import Files](./DataImportFiles/)**
3. **Automated Script (Python)** - Generating inserts dynamically.
   - 👉 **[Python Script](./Programming/data_generator.py)**

Each table contains at least **400 records** to ensure a realistic dataset.

### **Querying Data**
A script was created to retrieve all data from the tables:
- 👉 **[Select Queries](./selectAll.sql)**

Example query:
```sql
SELECT * FROM Passenger;
```

---

## 4. Backup and Restoration
To ensure data integrity, a full backup of the database was created and tested for restoration.
- **Backup File:** 👉 **[Database Backup](./backup_YYYYMMDD.sql)**
- **Restoration Process:** Successfully tested on a different system to verify correctness.

---

## 5. Conclusion
This phase covered the full database design and implementation, ensuring:
- A normalized database structure
- Efficient data handling
- Secure backup and recovery procedures

Future steps include optimizing queries, adding advanced indexing, and integrating stored procedures.

---

## Submission
All required files are included in the **DBProject** repository under the "Phase A" folder.
