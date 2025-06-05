CREATE OR REPLACE FUNCTION print_available_seats_by_bus(p_license_plate VARCHAR)
RETURNS VOID AS $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN
        SELECT s.seatNumber, s.tripID
        FROM Seat s
        JOIN Trip t ON s.tripID = t.trip_id
        WHERE t.license_plate = p_license_plate
          AND s.isAvailable = TRUE
    LOOP
        RAISE NOTICE 'Trip %: number of avelible seats - %', rec.tripID, rec.seatNumber;
    END LOOP;
END;
$$ LANGUAGE plpgsql;