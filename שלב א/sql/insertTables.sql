-- insert into blockedPassenger
INSERT INTO blockedPassenger (reason, blockedDate, unblockDate, passengerID) VALUES
('Payment issues', '2020-10-01', '2021-07-20', 241228265),
('Multiple no-shows', '2022-06-19', '2023-07-27', 449210707),
('Multiple no-shows', '2024-06-03', NULL, 225375571);

-- insert into disability
INSERT INTO Disability (disabilityType) VALUES
('Chronic Illness'),
('Neurological Disorder'),
('Wheelchair User');

-- insert into discountTicket
INSERT INTO discountTicket (expirationDate, startDate, discountID, ticketID) VALUES
('2024-04-26', '2024-06-19', 3, 357),
('2024-05-20', '2024-01-08', 88, 97),
('2024-06-10', '2024-08-21', 64, 244);


-- insert into passenger
INSERT INTO Passenger (passengerID, fullName, email) VALUES
(302976554, 'Neill Renshell', 'nrenshellgl@mashable.com'),
(308422989, 'Georas Howson', 'ghowsongm@shop-pro.jp'),
(457178188, 'Meryl Ashford', 'mashfordgn@canalblog.com');

-- insert into seat
INSERT INTO Seat (seatID, seatNumber, isAvailable, tripID) VALUES
(398, 40, FALSE, 14),
(399, 27, TRUE, 17),
(400, 25, FALSE, 1);

-- insert into specialNeedPassenger
INSERT INTO SpecialNeedPassenger (hasAssistAnimal, ContactPhone, passengerID, disabilityType) VALUES
(FALSE, '052-8091002', 411191916, 'Intellectual Disability'),
(TRUE, '050-1524647', 432055871, 'Intellectual Disability'),
(FALSE, '054-3840999', 359879878, 'Neurological Disorder');

-- insert into ticket
INSERT INTO Ticket (ticketID, purchaseDate, price, passengerID, seatID) VALUES
(398, '2024-09-09', 120, 318468213, 398),
(399, '2024-09-07', 8.5, 220374128, 399),
(400, '2024-02-27', 5.5, 398298090, 400);

-- insert into trip
INSERT INTO Trip (tripID) VALUES
(21),
(22),
(23);

-- insert into dicount
insert into Discount (discountID, discountCode, percentage) values (398, 'mY0tW', 10);
insert into Discount (discountID, discountCode, percentage) values (399, 'm#YkL', 55);
insert into Discount (discountID, discountCode, percentage) values (400, 'T7rK8', 40);