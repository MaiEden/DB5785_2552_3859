# Database Project - Stage A
## Table of Contents

- [Introduction](#introduction)
- [Database Design](#database-design)
  - [ERD Diagram](#erd-diagram)
  - [DSD Schema](#dsd-schema)
  - [Normalization](#normalization)
- [Database Implementation](#database-implementation)
  - [Creating Tables](#creating-tables)
  - [Data Insertion Methods](#data-insertion-methods)
  - [Querying Data](#querying-data)
- [Backup and Restoration](#backup-and-restoration)
- [Conclusion](#conclusion)
---

## 1. Introduction
This project involves designing and implementing a database for a transportation system, handling passengers, trips, seating, tickets, and discounts. The database is structured to ensure data integrity, efficient querying, and compliance with normalization standards.

The key functionalities of the system include:
- Managing passenger information
- Handling trip and seat assignments
- Processing ticket purchases and discounts
- Managing accessibility requirements

## Entities  

### 1. Passenger  
Stores information about passengers using the bus services.  
**Attributes:**  
- `passengerID (PK)` – Unique identifier for the passenger.  
- `fullName` – The full name of the passenger.  
- `email` – The passenger’s email address.  

### 2. Discount  
Stores discount codes that can be applied to ticket purchases.  
**Attributes:**  
- `discountID (PK)` – Unique identifier for the discount.  
- `discountCode` – The code used for the discount.  
- `percentage` – The percentage of discount applied.  

### 3. BlockedPassenger  
Tracks passengers who have been blocked from using the service.  
**Attributes:**  
- `passengerID (PK, FK)` – The blocked passenger ID (reference to Passenger).  
- `reason` – The reason for the block.  
- `blockedDate` – The date when the passenger was blocked.  
- `unblockDate` – The date when the block was removed (if it was).  

### 4. Trip  
Stores information about bus trips.  
**Attributes:**  
- `tripID (PK)` – Unique identifier for the trip. 
 
This table is from other database. (for the integration that will be later)

### 5. Disability  
Stores types of disabilities for passengers with special needs. (used as an enum)
**Attributes:**  
- `disabilityType (PK)` – The type of disability.  

### 6. Seat  
Stores information about seats available on trips.  
**Attributes:**  
- `seatID (PK)` – Unique identifier for the seat.  
- `seatNumber` – The number assigned to the seat on the bus.  
- `isAvailable` – Indicates if the seat is available (`true/false`).  
- `tripID (FK)` – The trip to which the seat belongs. (contains the bus number)

### 7. SpecialNeedPassenger  
Tracks passengers with special needs.  
**Attributes:**  
- `passengerID (PK, FK)` – The passenger ID (reference to Passenger).  
- `disabilityType (FK)` – The type of disability (reference to Disability).  
- `hasAssistAnimal` – Indicates if the passenger has an assistance animal (`true/false`).  
- `ContactPhone` – The emergancy contact phone number of the passenger.  

### 8. Ticket  
Stores information about purchased tickets.  
**Attributes:**  
- `ticketID (PK)` – Unique identifier for the ticket.  
- `purchaseDate` – The date the ticket was purchased.  
- `price` – The price of the ticket.  
- `passengerID (FK)` – The passenger who bought the ticket.  
- `seatID (FK)` – The seat assigned to this ticket.  

### 9. discountTicket  
Manages the discounts applied to tickets.  
**Attributes:**  
- `discountID (PK, FK)` – The discount applied (reference to Discount).  
- `ticketID (PK, FK)` – The ticket receiving the discount (reference to Ticket).  
- `startDate` – The date when the discount starts.  
- `expirationDate` – The date when the discount expires.  

## Entity Relationships  

- **Passenger - Ticket** `(1:M)` → A passenger can purchase multiple tickets, but each ticket belongs to one passenger.  
- **Passenger - BlockedPassenger** `(1:1)` → A passenger can be blocked, and each blocked record belongs to one passenger.  
- **Passenger - SpecialNeedPassenger** `(1:1)` → A passenger can have special needs, and each record belongs to one passenger.  
- **Trip - Seat** `(1:M)` → A trip has multiple seats, but each seat belongs to one trip.  
- **Seat - Ticket** `(1:1)` → A ticket is assigned to one seat, and each seat can have only one ticket at a time.  
- **Disability - SpecialNeedPassenger** `(1:M)` → A type of disability can be shared by multiple passengers with special needs.  
- **Discount - discountTicket** `(M:M)` → A discount can apply to multiple tickets, and each ticket can receive multiple discount.  


---

## 2. Database Design

### **ERD Diagram**
The Entity-Relationship Diagram (ERD) was designed using ERDPlus and represents the relationships between the entities. 

![ERD Diagram](./שלב%20א/images/erd/erd.png)

### **DSD Schema**
After validating the ERD, we generated the Data Structure Diagram (DSD) to confirm that relationships and constraints were correctly defined.

![DSD Schema](./שלב%20א/images/erd/DSD.png)

### **Normalization**
The schema stick with the **Third Normal Form (3NF)** by ensuring:
- Elimination of redundant data
- Every non-key attribute is functionally dependent on the primary key
- No transitive dependencies exist

---

## 3. Database Implementation

### **Creating Tables**
Tables were created using SQL scripts, ensuring proper data types and relationships. Below is the begining of the `createtable.sql`:

```sql
CREATE TABLE Passenger (
  passengerID INT NOT NULL,
  fullName VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  PRIMARY KEY (passengerID)
);

CREATE TABLE Discount (
  discountID INT NOT NULL,
  discountCode VARCHAR(50) NOT NULL,
  percentage INT NOT NULL,
  PRIMARY KEY (discountID)
);
```

👉 **[full script here](./שלב%20א/sql/createtable.sql)**

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