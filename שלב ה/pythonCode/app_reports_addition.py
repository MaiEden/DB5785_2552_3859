
from flask import render_template, request
from db import get_db_connection
#
# @app.route('/reports')
# def reports_home():
#     return render_template('reports.html')
#
# @app.route('/reports/occupancy')
# def report_occupancy():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT tripID, ROUND(100.0 * COUNT(seatID) / 50, 2) AS percent, COUNT(seatID) AS occupied_seats
#         FROM Seat
#         WHERE isAvailable = FALSE
#         GROUP BY tripID
#         ORDER BY tripID
#     """)
#     results = cur.fetchall()
#     cur.close()
#     conn.close()
#     return render_template('reports.html', section='occupancy', data=results)
#
# @app.route('/reports/top_discounts')
# def report_top_discounts():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT dt.ticketID, t.passengerID, COUNT(*) AS discount_count
#         FROM discountTicket dt
#         NATURAL JOIN Ticket t
#         GROUP BY dt.ticketID, t.passengerID
#         HAVING COUNT(*) = (
#             SELECT MAX(discount_count)
#             FROM (
#                 SELECT COUNT(*) AS discount_count
#                 FROM discountTicket
#                 GROUP BY ticketID
#             ) AS counts
#         )
#     """)
#     results = cur.fetchall()
#     cur.close()
#     conn.close()
#     return render_template('reports.html', section='top_discounts', data=results)
#
# @app.route('/reports/delayed_trips')
# def report_delayed_trips():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT t.trip_id, t.departure_time, t.arrival_time,
#                r.duration_minutes, r.route_number,
#                ROUND(EXTRACT(EPOCH FROM (t.arrival_time - t.departure_time))/60.0, 2) AS actual_duration
#         FROM Trip t
#         JOIN Bus b ON t.license_plate = b.license_plate
#         JOIN Route r ON b.route_number = r.route_number
#         WHERE EXTRACT(EPOCH FROM (t.arrival_time - t.departure_time))/60.0 > r.duration_minutes
#     """)
#     results = cur.fetchall()
#     cur.close()
#     conn.close()
#     return render_template('reports.html', section='delayed_trips', data=results)
#
# @app.route('/reports/available_seats', methods=['GET', 'POST'])
# def report_available_seats():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute('SELECT DISTINCT license_plate FROM Bus ORDER BY license_plate')
#     license_plates = [row[0] for row in cur.fetchall()]
#     results = []
#     selected_plate = None
#
#     if request.method == 'POST':
#         selected_plate = request.form['license_plate']
#         cur.execute("""
#             SELECT s.tripID, s.seatNumber
#             FROM Seat s
#             JOIN Trip t ON s.tripID = t.trip_id
#             WHERE t.license_plate = %s AND s.isAvailable = TRUE
#             ORDER BY s.tripID, s.seatNumber
#         """, (selected_plate,))
#         results = cur.fetchall()
#
#     cur.close()
#     conn.close()
#     return render_template('reports.html', section='available_seats', data=results,
#                            license_plates=license_plates, selected_plate=selected_plate)
