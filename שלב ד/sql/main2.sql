DO $$
DECLARE
    v_license_plate VARCHAR := '180-57-515';
    v_passenger_id INT := 228524376;
BEGIN
    -- הדפסת מושבים פנויים באוטובוס מסוים
    PERFORM print_available_seats_by_bus(v_license_plate);

    -- לאחר מכן נבדוק אם צריך לחסום נוסע עם יותר מדי כרטיסים
    CALL block_passenger_if_too_many_tickets(v_passenger_id);
END;
$$;
