from flask import Flask, render_template, request, redirect, url_for
from db import get_db_connection
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/passengers')
def passengers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Passenger ORDER BY passengerID')
    passengers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('passengers.html', passengers=passengers)

@app.route('/add_passenger', methods=['POST'])
def add_passenger():
    passengerID = request.form['passengerID']
    fullName = request.form['fullName']
    email = request.form['email']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO Passenger (passengerID, fullName, email) VALUES (%s, %s, %s)',
                (passengerID, fullName, email))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('passengers'))


@app.route('/edit_passenger/<int:passenger_id>')
def edit_passenger(passenger_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Passenger WHERE passengerID = %s', (passenger_id,))
    passenger = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('edit_passenger.html', passenger=passenger)

@app.route('/update_passenger/<int:passenger_id>', methods=['POST'])
def update_passenger(passenger_id):
    fullName = request.form['fullName']
    email = request.form['email']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Passenger SET fullName = %s, email = %s WHERE passengerID = %s',
                (fullName, email, passenger_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('passengers'))

@app.route('/delete_passenger/<int:passenger_id>')
def delete_passenger(passenger_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Passenger WHERE passengerID = %s', (passenger_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('passengers'))

@app.route('/tickets')
def tickets():
    conn = get_db_connection()
    cur = conn.cursor()

    # שליפת נוסעים (ID + Name)
    cur.execute('SELECT passengerID, fullName FROM Passenger ORDER BY fullName')
    passengers = cur.fetchall()

    # שליפת מושבים זמינים בלבד
    cur.execute('SELECT seatID, seatNumber, tripID FROM Seat WHERE isAvailable = TRUE ORDER BY tripID, seatNumber')
    seats = cur.fetchall()

    # שליפת כל הכרטיסים עם מידע על הנוסע והמושב
    cur.execute('''
        SELECT 
            t.ticketID, p.passengerID, p.fullName,
            t.price, s.seatNumber, s.tripID, t.purchaseDate
        FROM Ticket t
        JOIN Passenger p ON t.passengerID = p.passengerID
        JOIN Seat s ON t.seatID = s.seatID
        ORDER BY t.ticketID
    ''')
    tickets = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('tickets.html', passengers=passengers, seats=seats, tickets=tickets)

@app.route('/add_ticket', methods=['POST'])
def add_ticket():
    passengerID = request.form['passengerID']
    seatID = request.form['seatID']
    price = request.form['price']
    purchaseDate = request.form['purchaseDate']

    conn = get_db_connection()
    cur = conn.cursor()

    # יצירת כרטיס חדש
    cur.execute('''
        INSERT INTO Ticket (purchaseDate, price, passengerID, seatID)
        VALUES (%s, %s, %s, %s)
    ''', (purchaseDate, price, passengerID, seatID))

    # עדכון זמינות המושב
    cur.execute('UPDATE Seat SET isAvailable = FALSE WHERE seatID = %s', (seatID,))

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('tickets'))

@app.route('/delete_ticket/<int:ticket_id>')
def delete_ticket(ticket_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # שליפת מושב כדי לפנות אותו
    cur.execute('SELECT seatID FROM Ticket WHERE ticketID = %s', (ticket_id,))
    seat_row = cur.fetchone()
    if seat_row:
        seatID = seat_row[0]
        cur.execute('UPDATE Seat SET isAvailable = TRUE WHERE seatID = %s', (seatID,))

    # מחיקת הכרטיס
    cur.execute('DELETE FROM Ticket WHERE ticketID = %s', (ticket_id,))

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('tickets'))

@app.route('/edit_ticket/<int:ticket_id>')
def edit_ticket(ticket_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # נתונים לכרטיס הספציפי
    cur.execute('''
        SELECT ticketID, purchaseDate, price, passengerID, seatID
        FROM Ticket WHERE ticketID = %s
    ''', (ticket_id,))
    ticket = cur.fetchone()

    # כל הנוסעים להצגה בתפריט
    cur.execute('SELECT passengerID, fullName FROM Passenger ORDER BY fullName')
    passengers = cur.fetchall()

    # כל המושבים (כולל תפוסים, כדי לשמור רצף)
    cur.execute('SELECT seatID, seatNumber, tripID FROM Seat ORDER BY tripID, seatNumber')
    seats = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('edit_ticket.html', ticket=ticket, passengers=passengers, seats=seats)

@app.route('/update_ticket/<int:ticket_id>', methods=['POST'])
def update_ticket(ticket_id):
    purchaseDate = request.form['purchaseDate']
    price = request.form['price']
    passengerID = request.form['passengerID']
    seatID = request.form['seatID']

    conn = get_db_connection()
    cur = conn.cursor()

    # נעדכן את הכרטיס
    cur.execute('''
        UPDATE Ticket
        SET purchaseDate = %s, price = %s, passengerID = %s, seatID = %s
        WHERE ticketID = %s
    ''', (purchaseDate, price, passengerID, seatID, ticket_id))

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('tickets'))

@app.route('/discounts')
def discounts():
    conn = get_db_connection()
    cur = conn.cursor()

    # כרטיסים: ticketID + passengerName
    cur.execute('''
        SELECT t.ticketID, p.fullName
        FROM Ticket t
        JOIN Passenger p ON t.passengerID = p.passengerID
    ''')
    tickets = cur.fetchall()

    # הנחות: discountID + אחוז
    cur.execute('SELECT discountID, percentage FROM Discount')
    discounts = cur.fetchall()

    # כל הקשרים
    cur.execute('''
        SELECT dt.ticketID, p.fullName, d.percentage,
               dt.startDate, dt.expirationDate, dt.discountID
        FROM discountTicket dt
        JOIN Ticket t ON dt.ticketID = t.ticketID
        JOIN Passenger p ON t.passengerID = p.passengerID
        JOIN Discount d ON dt.discountID = d.discountID
    ''')
    discount_rows = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('discounts.html', tickets=tickets, discounts=discounts, discount_rows=discount_rows)


@app.route('/add_discount', methods=['POST'])
def add_discount():
    ticketID = request.form['ticketID']
    discountID = request.form['discountID']
    startDate = request.form['startDate']
    expirationDate = request.form['expirationDate']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO discountTicket (ticketID, discountID, startDate, expirationDate)
        VALUES (%s, %s, %s, %s)
    ''', (ticketID, discountID, startDate, expirationDate))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('discounts'))


@app.route('/delete_discount/<int:ticket_id>/<int:discount_id>')
def delete_discount(ticket_id, discount_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM discountTicket
        WHERE ticketID = %s AND discountID = %s
    ''', (ticket_id, discount_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('discounts'))


@app.route('/edit_discount/<int:ticket_id>/<int:discount_id>')
def edit_discount(ticket_id, discount_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # שליפת ההנחה הספציפית
    cur.execute('''
        SELECT startDate, expirationDate
        FROM discountTicket
        WHERE ticketID = %s AND discountID = %s
    ''', (ticket_id, discount_id))
    row = cur.fetchone()

    # כל ההנחות להצגה בתפריט
    cur.execute('SELECT discountID, percentage FROM Discount')
    discounts = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('edit_discount.html',
                           ticket_id=ticket_id,
                           discount_id=discount_id,
                           current_discount_id=discount_id,
                           startDate=row[0],
                           expirationDate=row[1],
                           discounts=discounts)


@app.route('/update_discount/<int:ticket_id>/<int:discount_id>', methods=['POST'])
def update_discount(ticket_id, discount_id):
    new_discount_id = request.form['discountID']
    startDate = request.form['startDate']
    expirationDate = request.form['expirationDate']

    conn = get_db_connection()
    cur = conn.cursor()

    # אם discountID שונה – צריך למחוק ולהכניס רשומה חדשה (כי זה PK)
    if int(new_discount_id) != discount_id:
        cur.execute('''
            DELETE FROM discountTicket
            WHERE ticketID = %s AND discountID = %s
        ''', (ticket_id, discount_id))

        cur.execute('''
            INSERT INTO discountTicket (ticketID, discountID, startDate, expirationDate)
            VALUES (%s, %s, %s, %s)
        ''', (ticket_id, new_discount_id, startDate, expirationDate))
    else:
        cur.execute('''
            UPDATE discountTicket
            SET startDate = %s, expirationDate = %s
            WHERE ticketID = %s AND discountID = %s
        ''', (startDate, expirationDate, ticket_id, discount_id))

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('discounts'))


#################מהיום

@app.route('/reports')
def reports_home():
    return render_template('reports.html')

@app.route('/reports/occupancy')
def report_occupancy():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT tripID, ROUND(100.0 * COUNT(seatID) / 50, 2) AS percent, COUNT(seatID) AS occupied_seats
        FROM Seat
        WHERE isAvailable = FALSE
        GROUP BY tripID
        ORDER BY tripID
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('reports.html', section='occupancy', data=results)

@app.route('/reports/top_discounts')
def report_top_discounts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT dt.ticketID, t.passengerID, COUNT(*) AS discount_count
        FROM discountTicket dt
        NATURAL JOIN Ticket t
        GROUP BY dt.ticketID, t.passengerID
        HAVING COUNT(*) = (
            SELECT MAX(discount_count)
            FROM (
                SELECT COUNT(*) AS discount_count
                FROM discountTicket
                GROUP BY ticketID
            ) AS counts
        )
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('reports.html', section='top_discounts', data=results)

@app.route('/reports/delayed_trips')
def report_delayed_trips():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.trip_id, t.departure_time, t.arrival_time,
               r.duration_minutes, r.route_number,
               ROUND(EXTRACT(EPOCH FROM (t.arrival_time - t.departure_time))/60.0, 2) AS actual_duration
        FROM Trip t
        JOIN Bus b ON t.license_plate = b.license_plate
        JOIN Route r ON b.route_number = r.route_number
        WHERE EXTRACT(EPOCH FROM (t.arrival_time - t.departure_time))/60.0 > r.duration_minutes
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('reports.html', section='delayed_trips', data=results)

@app.route('/reports/available_seats', methods=['GET', 'POST'])
def report_available_seats():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT license_plate FROM Bus ORDER BY license_plate')
    license_plates = [row[0] for row in cur.fetchall()]
    results = []
    selected_plate = None

    if request.method == 'POST':
        selected_plate = request.form['license_plate']
        cur.execute("""
            SELECT s.tripID, s.seatNumber
            FROM Seat s
            JOIN Trip t ON s.tripID = t.trip_id
            WHERE t.license_plate = %s AND s.isAvailable = TRUE
            ORDER BY s.tripID, s.seatNumber
        """, (selected_plate,))
        results = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('reports.html', section='available_seats', data=results,
                           license_plates=license_plates, selected_plate=selected_plate)

if __name__ == '__main__':
    app.run(debug=True)