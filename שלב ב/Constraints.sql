--set constraint on percentage 
ALTER TABLE Discount
ADD CONSTRAINT chk_percentage_range CHECK (percentage >= 0 AND percentage <= 100);

--set price of Ticket to NOT NULL
ALTER TABLE Ticket
ALTER COLUMN price SET NOT NULL;

--add delete on casecade
-- BlockedPassenger תלויה ב-Passenger
ALTER TABLE BlockedPassenger
ADD CONSTRAINT fk_blocked_passenger
FOREIGN KEY (passengerID)
REFERENCES Passenger(passengerID)
ON DELETE CASCADE;

-- Seat תלויה ב-Trip
ALTER TABLE Seat
ADD CONSTRAINT fk_seat_trip
FOREIGN KEY (tripID)
REFERENCES Trip(tripID)
ON DELETE CASCADE;

-- SpecialNeedPassenger תלויה ב-Passenger וב-Disability
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

-- Ticket תלויה ב-Passenger וב-Seat
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

-- discountTicket תלויה ב-Discount וב-Ticket
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
