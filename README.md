# Database Project - Stage A
## Table of Contents

- [Introduction](#1-introduction)
- [Database Design](#2-database-design)
  - [ERD Diagram](#erd-diagram)
  - [DSD Schema](#dsd-schema)
  - [Normalization](#normalization)
- [Database Implementation](#3-database-implementation)
  - [Creating Tables](#creating-tables)
  - [Data Insertion Methods](#data-insertion-methods)
  - [Querying Data](#querying-data)
- [Backup and Restoration](#4-backup-and-restoration)
- [Conclusion](#5-conclusion)
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

> **Note:** We initially planned to use the combination of `seatNumber` and `tripId` as the primary key for the **Seat** schema. However, for the sake of efficiency and simplicity, we decided to create a separate `seatId` as the primary key.  Still, we ensure that the combination of `seatNumber` and `tripId` remains unique.


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
1. **Manual SQL Inserts** - We added the data to Discount using sql code. Here is the begining of insertDiscount.sql:

```sql
insert into Discount (discountID, discountCode, percentage) values (1, 'J@4Hq', 5);
insert into Discount (discountID, discountCode, percentage) values (2, 'qZt#D', 90);
insert into Discount (discountID, discountCode, percentage) values (3, 'pT2qZ', 90);
insert into Discount (discountID, discountCode, percentage) values (4, '3BzK1', 40);
```

- 👉 **[InsertDiscount here](./שלב%20א/sql/insertDiscount.sql)**
2. **Data Import from CSV** - We upload data generated by Mockaroo. We modified these files with python code when needed.
     # Passenger Table

The following table contains sample passenger data.

| passengerID  | Full Name              | Email                         |
|-------------|------------------------|-------------------------------|
| 359879878   | Georgeanne Briiginshaw | gbriiginshaw0@yale.edu       |
| 373832007   | Rochell Renzo          | rrenzo1@yellowbook.com       |
| 341538997   | Dalia Mulleary         | dmulleary2@cbsnews.com       |
| 232726970   | Barnabas Walework      | bwalework3@jigsy.com         |
| 293856512   | Prissie Haquin         | phaquin4@sun.com             |
| **...**     | **...**                 | **...**                      |

   - 👉 **[csv file of passenger here](./שלב%20א/csv/Passenger.csv)**
3. **Automated Script (Python)** - We generated and insert data using python script.
     
     One code file for creating the data using python:

```python
...
   data = []
    for i in range(min(50, len(passenger_ids))):
        reason = random.choice(REASONS)
....
        passenger_id = passenger_ids[i]  # שמירת ייחודיות
        data.append([reason, blocked_date.strftime('%Y-%m-%d'), unblock_date.strftime('%Y-%m-%d'), passenger_id])
    # כתיבה לקובץ CS
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Reason", "BlockedDate", "UnblockDate", "PassengerID"])  # כותרות עמודות
        writer.writerows(data)
...
```

And one code file for uploading the data using python:

```python
....
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
   ....
                cur.execute(
                    """
                    INSERT INTO blocked_passenger (reason, blockeddate, unblockdate, passengerid)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (reason, blocked_date, unblock_date, int(passenger_id))
                )
....
```

- 👉 **[creating here](./שלב%20א/python/creatBlockedPass.py)**
- 👉 **[uploding here](./שלב%20א/python/uploadBlockedPass.py)**
  
Each table contains at least **400 records**, except for `blockPassenger`, `disabilities`, and `SpecialNeedPassenger`, which have fewer due to their nature.

### **Querying Data**
A script was created to retrieve all data from the tables. Here is the begining of selectAll.sql:

```sql
--Show all rows in blockedpassenger
SELECT * FROM public.blockedpassenger
ORDER BY passengerid ASC
.....
```

- 👉 **[SelectAll here](./שלב%20א/sql/selectAll.sql)**

### **Drop tables**
We wrote a sql script that drop all tables from the database. begining of it:

```sql
DROP TABLE IF EXISTS discountTicket;
DROP TABLE IF EXISTS Ticket;
DROP TABLE IF EXISTS SpecialNeedPassenger;
.....
```

- 👉 **[DropTables here](./שלב%20א/sql/DropTables.sql)**

### **insert records using sql**
We inserted three records for each table using sql. begining of it:

```sql
-- insert into blockedPassenger
INSERT INTO blockedPassenger (reason, blockedDate, unblockDate, passengerID) VALUES
('Payment issues', '2020-10-01', '2021-07-20', 241228265),
('Multiple no-shows', '2022-06-19', '2023-07-27', 449210707),
('Multiple no-shows', '2024-06-03', NULL, 225375571);
.....
```

- 👉 **[insertTables here](./שלב%20א/sql/insertTables.sql)**

## 4. Backup and Restoration
To ensure data integrity, a full backup of the database was created and tested for restoration. Here how the  **[Database Backup](./שלב%20א/Tickets&bookingBackup03-04-2025)** was created:

**![backup](./שלב%20א/images/erd/creatingBackupScreenshot.png)**


- **Restoration Process:** We created an empty database and then we restored the backup that was created.We did that way:


**![restoration](./שלב%20א/images/erd/restoringDataScreenshot.png)**

We checked and all the data was restored successfully.

---

## 5. Conclusion
This phase covered the full database design and implementation, ensuring:
- A normalized database structure
- Efficient data handling
- Secure backup and recovery procedures

(All files relevent for this stage are in `שלב א`)

# Stage B
## Table of Contents

- [Introduction](#1-introduction)
- [Database Design](#2-database-design)
  - [ERD Diagram](#erd-diagram)
  - [DSD Schema](#dsd-schema)
  - [Normalization](#normalization)
- [Database Implementation](#3-database-implementation)
  - [Creating Tables](#creating-tables)
  - [Data Insertion Methods](#data-insertion-methods)
  - [Querying Data](#querying-data)
- [Backup and Restoration](#4-backup-and-restoration)
- [Conclusion](#5-conclusion)

## Queries
### 1. Detecting Tickets with the Highest Number of Discounts
#### Motivation:
The marketing team requested an analysis to identify tickets that received an unusually high number of discounts. This insight is critical for detecting potential misuse of discount codes, system glitches in coupon assignment, or overly permissive discount stacking rules. The goal is to evaluate whether stricter policies should be implemented to prevent abuse and ensure fair usage.

#### What the Query Does:
This query finds the tickets that received the most discounts. For each such ticket, it shows how many discounts were applied and the ID of the passenger who bought it.

```sql
SELECT dt.ticketID, t.passengerID,
  COUNT(*) AS discount_count
FROM discountTicket dt NATURAL JOIN Ticket t
GROUP BY 
  dt.ticketID, t.passengerID
HAVING COUNT(*) = (
    SELECT MAX(discount_count)
    FROM (
        SELECT COUNT(*) AS discount_count
        FROM discountTicket
        GROUP BY ticketID
    ) AS counts
```

#### Query output:
![hgv](./שלב%20ב/images/Table1Sreenshot.png)

#### Query output:
![hgv](./שלב%20ב/images/Table5Sreenshot.png)

#### Query output:
![hgv](./שלב%20ב/images/Table3Sreenshot.png)

#### Query output:
![hgv](./שלב%20ב/images/Table4Sreenshot.png)

#### Query output:
![hgv](./שלב%20ב/images/Table6Sreenshot.png)

#### Query output:
![hgv](./שלב%20ב/images/Table7Sreenshot.png)

#### Query output:
![hgv](./שלב%20ב/images/Table8Sreenshot.png)

### 3. Identifying Trips with Special Needs Passengers During High-Demand Period
#### Motivation:
During the period from July 1 to September 1, 2024, there is an increase in public transportation demand, especially due to summer vacation. To ensure a safe and accessible travel experience for passengers with special needs, the operations team needs to assess how many such passengers have booked tickets during this time period. The goal is to verify that adequate accessibility equipment (such as lifts and dedicated seating) is available, prepare additional staff at relevant stations, and monitor the allocation of accessible resources. This query supports the transport operations team’s preparation for the high-demand season by identifying trips with special needs passengers and the number of such passengers on each trip.

#### What the Query Does:
This SQL query identifies all trips that include passengers with special needs who purchased tickets between July 1 and September 1, 2024. It returns the trip ID and the count of special needs passengers per trip.

```sql
SELECT s.tripID, COUNT(*) AS special_needs_count
FROM Seat s
JOIN Ticket t ON s.seatID = t.seatID
WHERE 
  t.passengerID IN (SELECT passengerID FROM SpecialNeedPassenger)
  AND t.purchaseDate BETWEEN DATE '2024-07-01' AND DATE '2024-09-01'
GROUP BY s.tripID;
```

### 4. Identifying Premium Passengers Based on Average Spending

#### Motivation:
The sales and customer success teams aim to identify high-value (premium) passengers who consistently spend more than the average. By isolating these customers, the company can design targeted loyalty programs, premium service tiers, or exclusive promotions that enhance customer retention and satisfaction.

#### What the Query Does:
Finds passengers whose average ticket price is above the overall average, sorted by highest spenders first.

```sql
SELECT 
  p.fullName,
  p.email,
  ROUND(AVG(t.price), 2) AS avg_price_per_passenger,
  (SELECT ROUND(AVG(price), 2) FROM Ticket) AS overall_avg_price
FROM Ticket t
JOIN Passenger p ON t.passengerID = p.passengerID
GROUP BY p.passengerID, p.fullName, p.email
HAVING AVG(t.price) > (
  SELECT AVG(price)
  FROM Ticket
)
ORDER BY avg_price_per_passenger DESC;
```

### 5. Seat Occupancy Rate per Trip
#### Motivation:
To improve operational efficiency, the transport team needs visibility into seat usage across trips. This helps identify under- or over-utilized routes, guiding decisions on whether to add or reduce service. The query provides occupancy data to support resource optimization.
#### What the Query Does:
Calculates the seat occupancy rate per trip by checking how many seats are marked as unavailable. Assumes each trip has 50 seats.

```sql
SELECT tripID, ROUND(100.0 * COUNT(seatID) / 50, 2) AS precent, COUNT(seatID) AS occupied_seats
FROM Seat
WHERE isAvailable = FALSE
GROUP BY tripID;
```

### 6. Identifying Passengers on a Specific Trip  
#### Motivation:  
Security or operational staff may need to quickly identify all passengers on a specific trip, such as Trip 16, for auditing, investigation, or safety purposes.

#### What the Query Does:  
Lists the full name, email, trip ID, and seat number of all passengers on Trip 16, ordered by ticket purchase date.

```sql
SELECT 
  p.fullName, 
  p.email, 
  s.tripID, 
  s.seatNumber
FROM Passenger p
JOIN Ticket t ON p.passengerID = t.passengerID
JOIN Seat s ON t.seatID = s.seatID
JOIN Trip tr ON s.tripID = tr.tripID
WHERE 
  tr.tripID = 16
ORDER BY t.purchaseDate;
```