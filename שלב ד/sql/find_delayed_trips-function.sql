CREATE OR REPLACE FUNCTION find_delayed_trips()
RETURNS VOID AS $$
DECLARE
    rec RECORD;
    actual_duration_minutes INT;
BEGIN
    FOR rec IN
        SELECT t.trip_id, t.departure_time, t.arrival_time,
               r.duration_minutes, r.route_number
        FROM Trip t
        JOIN Bus b ON t.license_plate = b.license_plate
        JOIN Route r ON b.route_number = r.route_number
    LOOP
        -- חשב משך נסיעה בפועל בדקות
        actual_duration_minutes := EXTRACT(EPOCH FROM (rec.arrival_time - rec.departure_time)) / 60;

        IF actual_duration_minutes > rec.duration_minutes THEN
            RAISE NOTICE 'Trip % in route % delayed: expacted time % min, actuall time % min',
                         rec.trip_id, rec.route_number, actual_duration_minutes, rec.duration_minutes;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;