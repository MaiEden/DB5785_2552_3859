CREATE OR REPLACE PROCEDURE apply_discount_to_passenger_tickets(
    p_passenger_id INT,
    p_discount_id INT,
    p_start_date DATE,
    p_end_date DATE
)
LANGUAGE plpgsql
AS $$
DECLARE
    ticket_rec RECORD;
    cur CURSOR FOR
        SELECT t.ticketID
        FROM Ticket t
        LEFT JOIN discountTicket dt ON t.ticketID = dt.ticketID
        WHERE t.passengerID = p_passenger_id
          AND t.purchaseDate BETWEEN p_start_date AND p_end_date
          AND dt.ticketID IS NULL;
BEGIN
    OPEN cur;
    LOOP
        FETCH cur INTO ticket_rec;
        EXIT WHEN NOT FOUND;

        BEGIN
            INSERT INTO discountTicket (discountID, ticketID, startDate, expirationDate)
            VALUES (p_discount_id, ticket_rec.ticketID, p_start_date, p_end_date);
            
            --הדפסת הצלחה
            RAISE NOTICE 'Discount % applied to ticket % successfully.', p_discount_id, ticket_rec.ticketID;

        EXCEPTION
            WHEN OTHERS THEN
                --הדפסת כישלון
                RAISE NOTICE 'Could not apply discount % to ticket %.', p_discount_id, ticket_rec.ticketID;
        END;

    END LOOP;
    CLOSE cur;
END;
$$;
