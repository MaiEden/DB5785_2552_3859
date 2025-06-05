CREATE OR REPLACE FUNCTION trg_prevent_ticket_for_blocked()
RETURNS TRIGGER AS $$
DECLARE
    is_blocked BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM BlockedPassenger WHERE passengerID = NEW.passengerID
    ) INTO is_blocked;

    IF is_blocked THEN
        RAISE EXCEPTION 'Passenger % is blocked and cannot buy tickets', NEW.passengerID;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_ticket_insert
BEFORE INSERT ON Ticket
FOR EACH ROW
EXECUTE FUNCTION trg_prevent_ticket_for_blocked();
