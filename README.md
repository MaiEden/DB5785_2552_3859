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

- [Queries](#queries)
- [Delete queries](#delete-queries)
- [Update queries](#update-queries)
- [Constraints](#constraints)

## Queries
All the queries below are in the file **[Queries.sql](./שלב%20ב/sql/Queries.sql)**
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

### 2. Blocked Passengers Who Purchased Tickets During Their Block Period
#### Motivation:
The legal department received reports of blocked passengers being charged or able to buy tickets despite restrictions. This raised concerns about enforcement failures or system flaws in the blocking mechanism. The query helps identify passengers who managed to purchase tickets during their block period—potentially revealing authorization issues or legal risks.

#### What the Query Does:
Finds passengers who were blocked and still purchased at least one ticket during their block period. Returns the passenger ID, full name, and the number of tickets purchased while blocked.

```sql
SELECT sub.passengerid, sub.fullname, sub.number_of_ticket_purchased
FROM (
    SELECT p.passengerid, p.fullname,
        COUNT(*) AS number_of_ticket_purchased
    FROM passenger p
    NATURAL JOIN blockedpassenger b
    NATURAL JOIN ticket t
    WHERE 
        t.purchasedate >= b.blockeddate 
        AND (b.unblockdate IS NULL OR t.purchasedate <= b.unblockdate)
    GROUP BY p.passengerid, p.fullname
) AS sub
WHERE sub.number_of_ticket_purchased >= 1;
```

#### Query output:
![hgv](./שלב%20ב/images/Table2Sreenshot.png)

### 3. Identifying Trips with Special Needs Passengers During High-Demand Period
#### Motivation:
During the period from July to September, there is an increase in public transportation demand, especially due to summer vacation. To ensure a safe and accessible travel experience for passengers with special needs, the operations team needs to assess how many such passengers have booked tickets during this time period. The goal is to verify that adequate accessibility equipment (such as lifts and dedicated seating) is available, prepare additional staff at relevant stations, and monitor the allocation of accessible resources.

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

#### Query output:
![hgv](./שלב%20ב/images/Table3Sreenshot.png)

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

#### Query output:
![hgv](./שלב%20ב/images/Table4Sreenshot.png)

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

#### Query output:
![hgv](./שלב%20ב/images/Table5Sreenshot.png)


### 6. Identifying Passengers on a Specific Trip After a Security Incident
#### Motivation:  
A bombing incident occurred on trip number 16. A terrorist left an explosive device on the bus, and it detonated. The police are now conducting an investigation and have formally requested the list of all passengers who were on that trip. This query helps retrieve those passengers to support the ongoing investigation.
#### What the Query Does:  
Finds all passengers who were on trip 16, including their names, emails, and seat numbers.

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
  tr.tripID = 16;
```

#### Query output:
![hgv](./שלב%20ב/images/Table6Sreenshot.png)


### 7. Top 5 Most Popular Seats  
#### Motivation:  
Understanding which seats are booked most often can reveal passenger preferences and guide decisions on layout optimization or special seat promotions.

#### What the Query Does:  
Finds the five seats with the highest number of ticket bookings.

```sql
SELECT s.seatNumber, COUNT(t.ticketID) AS ticketCount
FROM Ticket t
JOIN Seat s ON t.seatID = s.seatID
WHERE s.isAvailable = FALSE
GROUP BY s.seatNumber
ORDER BY ticketCount DESC
LIMIT 5;
```

#### Query output:
![hgv](./שלב%20ב/images/Table7Sreenshot.png)


### 8. Displaying Available Seats for a Specific Trip  
#### Motivation:  
As part of a booking system, the platform needs to quickly fetch which seats are still available for a given trip. This query helps preventing double-booking and ensures passengers only see free seats when selecting theirs.

#### What the Query Does:  
Shows all available seats for trip ID 12.

```sql
SELECT s.seatNumber
FROM Seat s
WHERE s.isAvailable = TRUE AND s.tripID = 12
ORDER BY s.seatNumber;
```

#### Query output:
![hgv](./שלב%20ב/images/Table8Sreenshot.png)

## Delete queries
All the delete queries below are in the file **[RollbackCommit.sql](./שלב%20ב/sql/RollbackCommit.sql)**

### 1. Cleaning Up Inactive Passengers  
#### Motivation:  
The system retains data on passengers who haven't purchased tickets since before 2020. To reduce database clutter and improve performance, we need to remove these inactive users.

#### What the Query Does:  
Deletes passengers whose last ticket purchase was before 2020.

```sql
START TRANSACTION;

DELETE FROM Passenger
WHERE passengerID IN (
  SELECT p.passengerID
  FROM Passenger p
  LEFT JOIN Ticket t ON p.passengerID = t.passengerID
  GROUP BY p.passengerID
  HAVING MAX(EXTRACT(YEAR FROM t.purchaseDate)) < 2020
);

commit;
```

The table before delete query (with START TRANSACTION):

![BeforeDeleteSreenshot1](./שלב%20ב/images/BeforeDeleteSreenshot1.png)

In order to view all rows that need to be deleted, we replaced `DELETE` with `SELECT *` to 
the data before deletion:

![ViewRowsToDeleteSreenshot1](./שלב%20ב/images/ViewRowsToDeleteSreenshot1.png)

The table after delete query and commit:

![AfterDeleteSreenshot1](./שלב%20ב/images/AfterDeleteSreenshot1.png)

As we can see there are five less lines and John Cohen was deleted.

### 2. Cleaning Up Expired and Unused Discounts  
#### Motivation:  
Many discounts in the system haven’t been used in over five years. To focus on active and relevant deals, unused and expired discounts are removed.

#### What the Query Does:  
Deletes discounts not used in the past five years by checking their records in `discountTicket` table.

```sql
DELETE FROM Discount
WHERE discountID IN (
    SELECT DISTINCT discountID
    FROM discountTicket
    WHERE expirationDate <= CURRENT_DATE - INTERVAL '5 year');
```

The table before delete query:

![BeforeDeleteSreenshot2](./שלב%20ב/images/BeforeDeleteSreenshot2.png)

The table after delete query:

![AfterDeleteSreenshot2](./שלב%20ב/images/AfterDeleteSreenshot2.png)

### 3. Removing High Discounts from Popular Tickets  
#### Motivation:  
Some tickets are popular and no longer require significant discounts to sell. Since these tickets used to need promotions but now sell well on their own, unnecessary discounts are removed to protect revenue.
#### What the Query Does:  
Deletes discount entries over 40% for a specific popular ticket.

```sql
START TRANSACTION;

DELETE FROM discountTicket
WHERE ticketID = 47
  AND discountID IN (
    SELECT discountID
    FROM Discount
    WHERE percentage > 40
);

rollback;
```

The table before delete query (with START TRANSACTION):

![BeforeDeleteSreenshot3](./שלב%20ב/images/BeforeDeleteSreenshot3.png)

In order to view all rows that need to be deleted, we replaced `DELETE` with `SELECT *` to preview the data before deletion:

![ViewRowsToDeleteSreenshot3](./שלב%20ב/images/ViewRowsToDeleteSreenshot3.png)

The table after delete query before rollback:

![AfterDeleteSreenshot3](./שלב%20ב/images/AfterDeleteSreenshot3.png)

The table after delete query after rollback:

![afterRollback](./שלב%20ב/images/BeforeDeleteSreenshot3.png)


## Update queries
All the update queries below are in the file **[RollbackCommit.sql](./שלב%20ב/sql/RollbackCommit.sql)**
### 1. Extending Expiration for Least-Used Expired Discounts  
#### Motivation:  
Marketing aims to re-engage passengers by extending the expiration of the five least-used discounts that recently expired. This gives these underutilized discounts a second chance, potentially increasing ticket sales by offering them again to passengers who may have missed them or abandoned their bookings previously. The idea is to evaluate if extending their availability encourages more ticket purchases.
#### What the Query Does:  
Updates expiration dates for the 5 least-used discounts that expired in the past 7 days.

```sql
UPDATE discountTicket dt
JOIN (
    SELECT dt.discountID
    FROM discountTicket dt
    WHERE 
        dt.expirationDate BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
    GROUP BY dt.discountID
    ORDER BY COUNT(dt.ticketID) ASC
    LIMIT 5
) AS leastUsed ON dt.discountID = leastUsed.discountID
SET dt.expirationDate = DATE_ADD(CURDATE(), INTERVAL 60 DAY);
```

The table before update query (In order to view all rows that will be updte, we replaced `UPDATE` with `SELECT * FROM` to preview the data before updating):

![BeforeUpdating1](./שלב%20ב/images/BeforeUpdating1.png)

The table after update query:

![AfterUpdating1](./שלב%20ב/images/AfterUpdating1.png)


### 2. Mark Seats as Unavailable for Past Trips  
#### Motivation:  
In the bus booking system, we need to ensure that seats from past trips don’t appear as available for booking. This query helps maintain accurate seat availability by automatically marking seats as unavailable if the associated ticket purchase date is from a past month or year. This prevents users from mistakenly seeing expired trip seats as available.

#### What the Query Does:  
This query updates the `Seat` table by setting `isAvailable` to `FALSE` for seats associated with tickets purchased in a past month or year.

```sql
UPDATE Seat
SET "isavailable" = FALSE
WHERE seatID IN (
    SELECT s.seatID
    FROM Seat s
    JOIN Ticket t ON t.seatID = s.seatID
    WHERE 
        (EXTRACT(YEAR FROM t.purchaseDate) < EXTRACT(YEAR FROM CURRENT_DATE)
        OR (
            EXTRACT(YEAR FROM t.purchaseDate) = EXTRACT(YEAR FROM CURRENT_DATE)
            AND EXTRACT(MONTH FROM t.purchaseDate) < EXTRACT(MONTH FROM CURRENT_DATE)
        ))   AND S.isAvailable = True
);
```

The table before update query (In order to view all rows that will be updte, we replaced `UPDATE` with `SELECT * FROM` to preview the data before updating):

![BeforeUpdating2](./שלב%20ב/images/BeforeUpdating2.png)

The table after update query:

![AfterUpdating2](./שלב%20ב/images/AfterUpdating2.png)

### 3. Automatically Unblock Long-Blocked Passengers Due to Payment Issues  
#### Motivation:  
To prevent indefinite blocking of users due to unresolved payment issues, the system should reassess cases that have been inactive for over 6 months. This query helps initiate reactivation by scheduling an unblock date one month from today, aiding customer support in resolving long-term blocks.

#### What the Query Does:  
It updates the `unblockDate` to one month from today for passengers blocked over 6 months ago due to payment issues and who have not yet been assigned an unblock date.

```sql
UPDATE BlockedPassenger
SET unblockDate = CURRENT_DATE + INTERVAL '1 month'
WHERE reason = 'Payment issues'
  AND unblockDate IS NULL
  AND blockedDate <= CURRENT_DATE - INTERVAL '6 months';
```

The table before update query (In order to view all rows that will be updte, we replaced `UPDATE` with `SELECT * FROM` to preview the data before updating):

![BeforeUpdating3](./שלב%20ב/images/BeforeUpdating3.png)

The table after update query:

![AfterUpdating3](./שלב%20ב/images/AfterUpdating3.png)

## Constraints
All the constraints below are in the file **[Constraints.sql](./שלב%20ב/sql/Constraints.sql)**
### 1. Enforcing Logical Range for Discount Percentages  
#### Motivation:  
The system allows discounts on ticket prices, but without constraints, there's a risk of unrealistic discount values—like negative percentages or values over 100%. Such cases could lead to negative prices or price increases instead of reductions. This constraint ensures all discounts remain within logical business limits, protecting pricing integrity and invoice accuracy.

#### What the Query Does:  
It adds a check constraint to the `Discount` table to ensure the discount percentage is between 0 and 100, inclusive.

```sql
ALTER TABLE Discount
ADD CONSTRAINT chk_percentage_range CHECK (percentage >= 0 AND percentage <= 100);
```

Try to insert wrong valus:

![wrongInsert1](./שלב%20ב/images/wrongInsert1.png)

### 2. Validating Email Format for Passengers  
#### Motivation:  
To ensure reliable communication and reduce errors, email addresses stored in the system must follow a valid structure. This helps prevent issues with notification delivery and account verification.

#### What the Query Does:  
Adds a constraint to the `Passenger` table that enforces a proper email format using a regular expression.

```sql
ALTER TABLE Passenger
ADD CONSTRAINT chk_valid_email
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');
```

Try to insert wrong valus:

![wrongInsert4](./שלב%20ב/images/wrongInsert4.png)

### 3. Enforcing Unique Seat Numbers Per Trip  
#### Motivation:  
To ensure data consistency and avoid confusion during seat selection, each seat number must be unique within a single trip. This prevents situations where two passengers could be assigned the same seat number on the same trip.

#### What the Query Does:  
Adds a unique constraint to guarantee that the combination of `tripID` and `seatNumber` is unique across the `Seat` table.

```sql
ALTER TABLE Seat
ADD CONSTRAINT unique_seat_per_trip
UNIQUE (tripID, seatNumber);
```

Try to insert wrong valus:

![wrongInsert3](./שלב%20ב/images/wrongInsert3.png)

### 4. Enforcing Mandatory Ticket Price  
#### Motivation:  
To maintain pricing integrity and prevent incomplete records, every ticket must have a price. Allowing `NULL` prices could result in billing issues or inconsistencies in financial reports.

#### What the Query Does:  
Modifies the `Ticket` table to ensure that every entry has a non-null value for the `price` field.

```sql
ALTER TABLE Ticket
ALTER COLUMN price SET NOT NULL;
```

Try to insert wrong valus:

![wrongInsert2](./שלב%20ב/images/wrongInsert2.png)


# Stage C – Core Integration: Route, Bus, Trip
In this section, we integrate with the `Bus`, `Trip`, `Route` tables. These entities belong to the **Fleet Management** and **Route & Scheduling** modules of the system.

### **ERD Diagram**
After reviewing the backup we got, we performed reverse engineering and got this ERD schema:


![IntegrationERD](./שלב%20ג/images/IntegrationERD.png)
### **DSD Schema**
So we convert to the next DSD schema:


![IntegrationERD](./שלב%20ג/images/IntegrationDSD.png)

## Relation description
We wrote a description of the integrated system's entities and their relationships.

## Entities

### 1. Route  
Defines bus travel paths with start and end locations and total duration.  

**Attributes:**  
- `route_number (PK)` – Unique identifier for the route.  
- `length_km` – The total distance of the route in kilometers.  
- `duration_minutes` – Estimated time in minutes to complete the route.  
- `start_location` – The name of the starting point.  
- `end_location` – The name of the destination.  
- `active` – Indicates whether the route is currently in use (`true/false`).  

---

### 2. Bus  
Stores details about individual buses in the fleet.  

**Attributes:**  
- `license_plate (PK)` – Unique identifier for the bus (plate number).  
- `route_number (FK)` – The current route assigned to the bus (reference to `Route`).  
- `line_num` – The line number the bus is operating on.  
- `capacity` – The total number of passenger seats (must be greater than 0).   

---

### 3. Trip  
Stores records of individual bus trips made along a route.  

**Attributes:**  
- `tripID (PK)` – Unique identifier for the trip (auto-incremented).   
- `license_plate (FK)` – The bus performing the trip (reference to `Bus`).  
- `departure_time` – The scheduled departure time.  
- `arrival_time` – The scheduled arrival time.  

---

## Entity Relationships
- A **Bus** is linked to one **Route** at a time, and can appear in multiple **Trips**.
- Each **Trip** must be assigned to a **Bus**.

### **Full ERD Diagram**
Now, we drow the integraed system ERD:

![allSystemERD](./שלב%20ג/images/allSystemERD.png)


# Integration

We did integration between two PostgreSQL databases (`mydatabase` and `integrationDatabase`) using the `postgres_fdw` extension.

### 1. Enable Extension
```sql
CREATE EXTENSION IF NOT EXISTS postgres_fdw;
```

### 2. Create Foreign Server
```sql
CREATE SERVER integration_server
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'localhost', dbname 'integrationDatabase', port '5432');
```

### 3. Create User Mapping
```sql
CREATE USER MAPPING FOR current_user
SERVER integration_server
OPTIONS (user 'noder', password 'docker');
```

### 4. Define Foreign Tables
```sql
CREATE FOREIGN TABLE route_remote (
    route_number INT,
    length_km DECIMAL(5,2),
    duration_minutes INT,
    start_location VARCHAR(100),
    end_location VARCHAR(100),
    active BOOLEAN
) SERVER integration_server
OPTIONS (schema_name 'public', table_name 'route');

CREATE FOREIGN TABLE bus_remote (
    license_plate VARCHAR(30),
    route_number INT,
    line_num INT,
    capacity INT
) SERVER integration_server
OPTIONS (schema_name 'public', table_name 'bus');

CREATE FOREIGN TABLE trip_remote (
    trip_id INT,
    license_plate VARCHAR(30),
    departure_time TIMESTAMP,
    arrival_time TIMESTAMP
) SERVER integration_server
OPTIONS (schema_name 'public', table_name 'trip');
```

### 5. Create Local Tables
```sql
CREATE TABLE route (
    route_number INT PRIMARY KEY,
    length_km DECIMAL(5,2),
    duration_minutes INT,
    start_location VARCHAR(100),
    end_location VARCHAR(100),
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE bus (
    license_plate VARCHAR(30) PRIMARY KEY,
    route_number INT,
    line_num INT,
    capacity INT CHECK (capacity > 0),
    FOREIGN KEY (route_number) REFERENCES route(route_number)
);
```

### 6. Import Data from Remote Tables
```sql
INSERT INTO route
SELECT * FROM route_remote
ON CONFLICT (route_number) DO NOTHING;

INSERT INTO bus
SELECT * FROM bus_remote
ON CONFLICT (license_plate) DO NOTHING;
```

### 7. Update Existing `trip` Table
```sql
ALTER TABLE trip
ADD COLUMN license_plate VARCHAR(30),
ADD COLUMN departure_time TIMESTAMP,
ADD COLUMN arrival_time TIMESTAMP;

INSERT INTO trip (tripID, license_plate, departure_time, arrival_time)
SELECT trip_id, license_plate, departure_time, arrival_time
FROM trip_remote
ON CONFLICT (tripID) DO UPDATE
SET
    license_plate = EXCLUDED.license_plate,
    departure_time = EXCLUDED.departure_time,
    arrival_time = EXCLUDED.arrival_time;
```

## Notes

- Conflicts are handled safely using `ON CONFLICT DO NOTHING` or `DO UPDATE`.
- Existing structure of `trip` table was preserved by extending it without deletion.

# Views
## 1. Viewing Ticketed Trip Details
#### Motivation:  
The goal is to provide a comprehensive overview of ticket purchases, enriched with passenger, seat, discount, and trip details. This view aids operational staff in understanding the full context of each ticket — who bought it, when, where they’re headed, and what discount (if any) was applied. This is essential for handling changes, cancellations, and support inquiries more effectively.

#### What the Query Does:  
Displays detailed information about each ticket, including passenger name and contact, seat assignment, discount used, ticket pricing (base and final), and trip schedule details.

###  Query 1: Displaying All Tickets Sold for a Specific Trip
#### Motivation:  
This query enables the ticketing and operations teams to immediately view the list of passengers for a specific trip, along with their ticket details. It’s useful for occupancy management, validation checks, updates, or logistical coordination related to a particular trip.

#### What the Query Does:  
Returns all ticket records for Trip ID 20, including passenger name, seat number, ticket ID, and the final price paid (after discounts).

### Query 2: Finding Passengers Who Paid More Than X for Trips Departing on Specific Dates
#### Motivation:  
This query supports revenue analysis by identifying which passengers paid higher final prices for trips departing within a given date range. It can help financial analysts and marketing teams understand passenger spending patterns and pricing effectiveness.

#### What the Query Does: 
Returns a list of passengers whose trips depart between May 21 and May 23, 2025 (exclusive), and who paid more than 30.00 in final price. You can change the date range and price threshold as needed.

## 2. Trip Occupancy Summary for Route & Scheduling / Operations Planning
#### Motivation: 
This view is essential for efficient operations planning and route management. It not only displays detailed information about each trip, the route, and the assigned bus, but also calculates how many seats are occupied, how many are still available, and the overall occupancy rate. This data is critical for making decisions such as increasing service frequency, adjusting schedules, or allocating buses of different sizes based on demand.

#### What the Query Does: 
Creates a summary view called TripOccupancySummary that includes trip details, route information, bus capacity, and current occupancy statistics based on sold tickets.

### Query 1: Identifying Overcrowded Trips for a Specific Date Range
#### Motivation: 
Route planners and operations managers need to identify trips that are nearing or exceeding full capacity. Detecting trips with high occupancy helps in decision-making regarding adding more buses, increasing trip frequency, or reallocating fleet resources efficiently. 
  
#### What the Query Does: 
Shows trips departing between May 21 and May 23, 2025, with an occupancy rate higher than 60%.

### Query 2: Displaying Trips with Less Than 10 Available Seats
#### Motivation: 
Operations and ticketing teams need to quickly identify trips that are nearly full. This information helps in providing accurate recommendations to customers, managing last-minute ticket sales, and planning backup buses in case of issues.
  
#### What the Query Does: 
Shows trips where fewer than 10 seats are available, along with route and bus details.