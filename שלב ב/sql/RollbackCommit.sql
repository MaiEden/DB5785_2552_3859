--delete--
--1. Cleaning Up Inactive Passengers
--commit & delete
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

--2. Cleaning Up Expired and Unused Discounts  
DELETE FROM Discount
WHERE discountID IN (
    SELECT DISTINCT discountID
    FROM discountTicket
    WHERE expirationDate <= CURRENT_DATE - INTERVAL '5 year');

--3. Removing High Discounts from Popular Tickets 
--rollback & delete
START TRANSACTION;

DELETE FROM discountTicket
WHERE ticketID = 47
  AND discountID IN (
    SELECT discountID
    FROM Discount
    WHERE percentage > 40
);

rollback;

--updates--
--1. Extending Expiration for Least-Used Expired Discounts
UPDATE discountTicket
SET expirationDate = CURRENT_DATE + INTERVAL '14 days'
WHERE discountID IN (
    SELECT discountID
    FROM discountTicket
    WHERE expirationDate BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
    GROUP BY discountID
    ORDER BY COUNT(ticketID) ASC
    LIMIT 5
);

--2. Mark Seats as Unavailable for Past Trips  
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

--3. Automatically Unblock Long-Blocked Passengers Due to Payment Issues
UPDATE BlockedPassenger
SET unblockDate = CURRENT_DATE + INTERVAL '1 month'
WHERE reason = 'Payment issues'
  AND unblockDate IS NULL
  AND blockedDate <= CURRENT_DATE - INTERVAL '6 months';