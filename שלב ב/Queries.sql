--1
-- Find tickets that received the highest number of discounts,
-- including the number of discounts and the passenger ID who purchased the ticket
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
    	) AS counts);

--2
-- Identify blocked passengers who bought tickets during their block period
-- Returns passenger ID, full name, and number of tickets purchased
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


--3
--בדיקת טיולים עם נוסעים בעלי צרכים מיוחדים בתקופה לחוצה
SELECT s.tripID, COUNT(*) AS special_needs_count
FROM Seat s
JOIN Ticket t ON s.seatID = t.seatID
WHERE 
  t.passengerID IN (SELECT passengerID FROM SpecialNeedPassenger)
  AND t.purchaseDate BETWEEN DATE '2024-07-01' AND DATE '2024-09-01'
GROUP BY s.tripID;

--4
--מציאת לקוחות פרימיום
SELECT 
  p.fullName,
  p.email,
  ROUND(AVG(t.price), 2) AS avg_price_per_passenger,
  (SELECT ROUND(AVG(price), 2) FROM Ticket) AS overall_avg_price
FROM Ticket t
JOIN Passenger p ON t.passengerID = p.passengerID
GROUP BY p.passengerID, p.fullName, p.email
HAVING AVG(t.price) >= (
  SELECT AVG(price)
  FROM Ticket
) * 1.7
ORDER BY avg_price_per_passenger DESC;

--5
-- תפוסת מושבים לכל נסיעה (Occupancy Rate per Trip)

SELECT tripID, ROUND(100.0 * COUNT(seatID) / 50, 2) AS precent , COUNT(seatID) as occupied_seats
FROM Seat
WHERE isAvailable = FALSE
GROUP BY tripID

--6
--מציאת מחבל בנסיעה מספר 16
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
  tr.tripID =16
ORDER BY t.purchaseDate;

--7
--חמשת הכיסאות הכי פופולריים
SELECT s.seatNumber, COUNT(t.ticketID) AS ticketCount
FROM Ticket t
JOIN Seat s ON t.seatID = s.seatID
WHERE s.isAvailable = FALSE
GROUP BY s.seatNumber
ORDER BY ticketCount DESC
LIMIT 5;

--8
--Show available seats for a specific trip
SELECT s.seatNumber
FROM Seat s
WHERE s.isAvailable = TRUE AND s.tripID = 12
ORDER BY s.seatNumber;




---------delete-----------
DELETE FROM Passenger
WHERE passengerID=422491937	

--1
--Clean up inactive passengers who have not purchased any tickets since before
--the year 2020 or never made a purchase at all.
DELETE FROM Passenger
WHERE passengerID IN (
  SELECT p.passengerID
  FROM Passenger p
  LEFT JOIN Ticket t ON p.passengerID = t.passengerID
  GROUP BY p.passengerID
  HAVING MAX(EXTRACT(YEAR FROM t.purchaseDate)) IS NULL 
     OR MAX(EXTRACT(YEAR FROM t.purchaseDate)) < 2020
);

