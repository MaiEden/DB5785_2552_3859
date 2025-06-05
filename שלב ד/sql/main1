DO $$
DECLARE
    v_passenger_id INT := 216967489;
    v_discount_id INT := 3;
    v_start_date DATE := CURRENT_DATE - INTERVAL '2 year';
    v_end_date DATE := CURRENT_DATE;
BEGIN
    -- קודם נבדוק אילו נסיעות התעכבו
    PERFORM find_delayed_trips();

    -- מתן הנחה על כרטיסים לנוסע בטווח תאריכים
    CALL apply_discount_to_passenger_tickets(v_passenger_id, v_discount_id, v_start_date, v_end_date);
END;
$$;
