--set constraint on percentage 
ALTER TABLE Discount
ADD CONSTRAINT chk_percentage_range CHECK (percentage >= 0 AND percentage <= 100);

--set price of Ticket to NOT NULL
ALTER TABLE Ticket
ALTER COLUMN price SET NOT NULL;

ALTER TABLE Seat
ADD CONSTRAINT unique_seat_per_trip
UNIQUE (tripID, seatNumber);

--check that all emails are valid
ALTER TABLE Passenger
ADD CONSTRAINT chk_valid_email
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');


--add delete on casecade
ALTER TABLE BlockedPassenger
DROP CONSTRAINT blocked_passenger_passengerid_fkey;


ALTER TABLE BlockedPassenger
ADD CONSTRAINT fk_blocked_passenger
FOREIGN KEY (passengerID)
REFERENCES Passenger(passengerID)
ON DELETE CASCADE;


ALTER TABLE Seat
ADD CONSTRAINT fk_seat_trip
FOREIGN KEY (tripID)
REFERENCES Trip(tripID)
ON DELETE CASCADE;

ALTER TABLE SpecialNeedPassenger
ADD CONSTRAINT fk_snp_passenger
FOREIGN KEY (passengerID)
REFERENCES Passenger(passengerID)
ON DELETE CASCADE;

ALTER TABLE SpecialNeedPassenger
ADD CONSTRAINT fk_snp_disability
FOREIGN KEY (disabilityType)
REFERENCES Disability(disabilityType)
ON DELETE CASCADE;


ALTER TABLE Ticket
ADD CONSTRAINT fk_ticket_passenger
FOREIGN KEY (passengerID)
REFERENCES Passenger(passengerID)
ON DELETE CASCADE;

ALTER TABLE Ticket
ADD CONSTRAINT fk_ticket_seat
FOREIGN KEY (seatID)
REFERENCES Seat(seatID)
ON DELETE CASCADE;


ALTER TABLE discountTicket
DROP CONSTRAINT discountticket_discountid_fkey;

ALTER TABLE discountTicket
ADD CONSTRAINT fk_discount_ticket
FOREIGN KEY (discountID)
REFERENCES Discount(discountID)
ON DELETE CASCADE;

ALTER TABLE discountTicket
ADD CONSTRAINT fk_ticket_discount
FOREIGN KEY (ticketID)
REFERENCES Ticket(ticketID)
ON DELETE CASCADE;
