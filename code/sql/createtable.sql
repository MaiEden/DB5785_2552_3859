CREATE TABLE Passenger (
  passengerID INT NOT NULL,
  fullName VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  PRIMARY KEY (passengerID)
);

CREATE TABLE Discount (
  discountID INT NOT NULL,
  discountCode VARCHAR(50) NOT NULL,
  percentage INT NOT NULL,
  PRIMARY KEY (discountID)
);

CREATE TABLE blocked_passenger (
  reason VARCHAR(255) NOT NULL,
  blockedDate DATE NOT NULL,
  unblockDate DATE NOT NULL,
  passengerID INT NOT NULL,
  PRIMARY KEY (passengerID),
  FOREIGN KEY (passengerID) REFERENCES Passenger(passengerID)
);

CREATE TABLE Trip (
  tripID INT NOT NULL,
  PRIMARY KEY (tripID)
);

CREATE TABLE Disability (
  disabilityType VARCHAR(100) NOT NULL,
  PRIMARY KEY (disabilityType)
);

CREATE TABLE Seat (
  seatID INT NOT NULL,
  seatNumber INT NOT NULL,
  isAvailable BOOLEAN NOT NULL,
  tripID INT NOT NULL,
  PRIMARY KEY (seatID),
  FOREIGN KEY (tripID) REFERENCES Trip(tripID)
);

CREATE TABLE SpecialNeed_passenger (
  hasAssistAnimal BOOLEAN NOT NULL,
  ContactPhone VARCHAR(11) NOT NULL,
  passengerID INT NOT NULL,
  disabilityType VARCHAR(100) NOT NULL,
  PRIMARY KEY (passengerID),
  FOREIGN KEY (passengerID) REFERENCES Passenger(passengerID),
  FOREIGN KEY (disabilityType) REFERENCES Disability(disabilityType)
);

CREATE TABLE Ticket (
  ticketID INT NOT NULL,
  purchaseDate DATE NOT NULL,
  price NUMERIC(10,2) NOT NULL,
  passengerID INT NOT NULL,
  seatID INT NOT NULL,
  PRIMARY KEY (ticketID),
  FOREIGN KEY (passengerID) REFERENCES Passenger(passengerID),
  FOREIGN KEY (seatID) REFERENCES Seat(seatID)
);

CREATE TABLE discountTicket (
  expirationDate DATE NOT NULL,
  startDate DATE NOT NULL,
  discountID INT NOT NULL,
  ticketID INT NOT NULL,
  PRIMARY KEY (discountID, ticketID),
  FOREIGN KEY (discountID) REFERENCES Discount(discountID),
  FOREIGN KEY (ticketID) REFERENCES Ticket(ticketID)
);