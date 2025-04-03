--Show all rows in blockedpassenger
SELECT * FROM public.blockedpassenger
ORDER BY passengerid ASC

--Show all rows in disability
SELECT * FROM public.disability
ORDER BY disabilitytype ASC 

--Show all rows in discount 
SELECT * FROM public.discount
ORDER BY discountid ASC 

--Show all rows in discountticket
SELECT * FROM public.discountticket
ORDER BY discountid ASC, ticketid ASC 

--Show all rows in passenger
SELECT * FROM public.passenger
ORDER BY passengerid ASC 

--Show all rows in seat
SELECT * FROM public.seat
ORDER BY seatid ASC 

--Show all rows in specialneedpassenger
SELECT * FROM public.specialneedpassenger
ORDER BY passengerid ASC 

--Show all rows in ticket
SELECT * FROM public.ticket
ORDER BY ticketid ASC 

--Show all rows in trip
SELECT * FROM public.trip
ORDER BY tripid ASC 