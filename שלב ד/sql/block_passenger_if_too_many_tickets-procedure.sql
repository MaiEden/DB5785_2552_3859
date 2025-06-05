CREATE OR REPLACE PROCEDURE block_passenger_if_too_many_tickets(p_passenger_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    ticket_count INT;
    passenger_name VARCHAR(255);
BEGIN
    SELECT COUNT(*) INTO ticket_count
    FROM Ticket
    WHERE passengerID = p_passenger_id;

    IF ticket_count > 10 THEN
        SELECT fullName INTO passenger_name
        FROM Passenger
        WHERE passengerID = p_passenger_id;

        INSERT INTO BlockedPassenger (passengerID, reason, blockedDate)
        VALUES (p_passenger_id, 'Exceeded ticket limit', CURRENT_DATE)
        ON CONFLICT (passengerID) DO NOTHING;

        RAISE NOTICE 'Passenger % has been blocked due to too many tickets (% tickets).', passenger_name, ticket_count;
    END IF;
END;
$$;
