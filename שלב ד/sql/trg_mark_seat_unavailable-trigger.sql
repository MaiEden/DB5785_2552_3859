CREATE OR REPLACE FUNCTION trg_mark_seat_unavailable()
RETURNS TRIGGER AS $$
DECLARE
    seat_num INT;
BEGIN
    -- עדכון המושב
    UPDATE Seat
    SET isAvailable = FALSE
    WHERE seatID = NEW.seatID;

    -- קבלת מספר המושב להדפסה
    SELECT seatNumber INTO seat_num
    FROM Seat
    WHERE seatID = NEW.seatID;

    -- הדפסת הודעה
    RAISE NOTICE 'Seat number % (seatID: %) marked as unavailable due to ticket purchase by passengerID %.',
        seat_num, NEW.seatID, NEW.passengerID;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
