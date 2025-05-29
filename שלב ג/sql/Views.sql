--מבט 1: מנקודת המבט של אגף "Ticketing & Booking" – עם שילוב נתוני נסיעות
CREATE VIEW TicketedTripDetails AS
SELECT
    p.fullName AS PassengerName,
    t.ticketID,
    s.seatNumber,
    ROUND((t.price * (1 - COALESCE(d.percentage, 0) / 100.0)),2)  AS FinalPrice,
    tr.trip_id AS tripId,
    tr.departure_time AS TripDepartureTime
FROM
    Passenger AS p
JOIN
    Ticket AS t ON p.passengerID = t.passengerID
JOIN
    Seat AS s ON t.seatID = s.seatID
JOIN
    Trip AS tr ON s.tripID = tr.trip_id -- שילוב טבלת Trip
LEFT JOIN
    discountTicket AS dt ON t.ticketID = dt.ticketID
LEFT JOIN
    Discount AS d ON dt.discountID = d.discountID;

--שאילתה 1: הצגת כל הכרטיסים שנמכרו לטיול מסוים, כולל פרטי הנוסעים והמחיר הסופי
SELECT
    TripID,
    TripDepartureTime,
    PassengerName,
    ticketID,
    seatNumber,
    FinalPrice
FROM
    TicketedTripDetails
WHERE
    TripID = 20; -- החלף ב-ID של טיול ספציפי

--Xשאילתה 2: מציאת נוסעים שרכשו כרטיסים לטיולים היוצאים בתאריך מסוים, וששילמו מחיר סופי הגבוה מ.
SELECT
    PassengerName,
    TripID,
    TripDepartureTime,
    ticketID,
    FinalPrice
FROM
    TicketedTripDetails
WHERE
    TripDepartureTime > '2025-05-20' AND TripDepartureTime  < '2025-05-24' AND FinalPrice > 30.00; -- החלף בתאריך ובמחיר


--מבט 2: מנקודת המבט של אגף "Route & Scheduling" / "Fleet Management" – עם שילוב נתוני הזמנות
CREATE VIEW TripOccupancySummary AS
SELECT
    t.trip_id,
    t.departure_time,
    t.license_plate AS BusLicensePlate,
    b.capacity AS BusTotalCapacity,
    r.route_number,
    r.start_location,
    r.end_location,
    COUNT(tk.ticketID) AS OccupiedSeats,
    (b.capacity - COUNT(tk.ticketID)) AS AvailableSeats,
    ROUND((CAST(COUNT(tk.ticketID) AS DECIMAL) / b.capacity) * 100,2) AS OccupancyPercentage
FROM
    Trip AS t
JOIN
    Bus AS b ON t.license_plate = b.license_plate
JOIN
    Route AS r ON b.route_number = r.route_number
LEFT JOIN
    Seat AS s ON t.trip_id = s.tripID -- שילוב טבלת Seat
LEFT JOIN
    Ticket AS tk ON s.seatID = tk.seatID -- שילוב טבלת Ticket לחישוב תפוסה
GROUP BY
    t.trip_id, t.departure_time, t.arrival_time, t.license_plate, b.line_num, b.capacity, r.route_number, r.start_location, r.end_location;

--שאילתה 1: מציאת טיולים עם אחוז תפוסה גבוה מ-80% לתאריך ספציפי (לצורך זיהוי קווים עמוסים).
SELECT
    trip_id,
    departure_time,
    BusLicensePlate,
    route_number,
    OccupiedSeats,
    BusTotalCapacity,
    OccupancyPercentage
FROM
    TripOccupancySummary
WHERE
    CAST (departure_time AS DATE) > '2025-05-20' AND departure_time  < '2025-05-24' AND OccupancyPercentage > 60; -- החלף בתאריך

--שאילתה 2: הצגת טיולים עם פחות מ-10 מקומות זמינים, יחד עם פרטי הקו והאוטובוס.	
SELECT
    trip_id,
    departure_time,
    BusLicensePlate,
    BusTotalCapacity,
    AvailableSeats,
    route_number,
    start_location,
    end_location
FROM
    TripOccupancySummary
WHERE
    AvailableSeats < 10;
