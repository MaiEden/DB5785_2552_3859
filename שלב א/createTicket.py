import csv
import random

# קריאת מזהי נוסעים מקובץ
passenger_ids = []
with open("passenger_ids.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # דילוג על הכותרת אם יש
    passenger_ids = [int(row[0]) for row in reader]

# הגדרות נתונים
ticket_prices = [5.5, 8.5, 20, 50, 80, 120]
seat_ids = list(range(1, 401))  # רשימה של כל ה-seatID מ-1 עד 400

# יצירת נתוני הכרטיסים
tickets = []
for ticket_id in range(1, 401):
    purchase_date = f"2024-0{random.randint(1, 9)}-{random.randint(1, 28)}"  # תאריכים רנדומליים עד ספטמבר
    price = random.choice(ticket_prices)
    passenger_id = random.choice(passenger_ids)
    seat_id = seat_ids[ticket_id - 1]  # כל seatID מופיע פעם אחת בלבד

    tickets.append([ticket_id, purchase_date, price, passenger_id, seat_id])

# כתיבה לקובץ CSV
with open("tickets.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["ticketID", "purchaseDate", "price", "passengerID", "seatID"])
    writer.writerows(tickets)

print("קובץ tickets.csv נוצר בהצלחה!")