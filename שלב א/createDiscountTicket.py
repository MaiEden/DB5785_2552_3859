import csv
import random
from datetime import datetime, timedelta

# פונקציה ליצירת תאריך רנדומלי
def generate_random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# יצירת נתוני הזוגות discountID ו-ticketID
discount_ids = list(range(1, 401))  # מספרים מ-1 עד 400
ticket_ids = list(range(1, 41))  # מספרים מ-1 עד 40

# הכנת קובץ CSV
filename = "discount_ticket_data.csv"

# יצירת תאריך התחלה ותאריך סיום
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 1, 1)

# רשימה לשמירת נתונים
data = []

# יצירת 400 שורות עם מידע
for _ in range(400):
    # בחר discountID ו-ticketID רנדומליים כך שאין חזרתיות
    discount_id = random.choice(discount_ids)
    ticket_id = random.choice(ticket_ids)

    # ודא שזוג discountID ו-ticketID לא יחזור על עצמו
    while (discount_id, ticket_id) in data:
        discount_id = random.choice(discount_ids)
        ticket_id = random.choice(ticket_ids)

    # תאריך התחלה
    start = generate_random_date(start_date, end_date)

    # תאריך סיום - חייב להיות אחרי תאריך ההתחלה
    expiration = generate_random_date(start, end_date)

    # הוסף את המידע לשורה, הפורמט יהיה YYYY-MM-DD
    data.append((expiration.strftime("%Y-%m-%d"), start.strftime("%Y-%m-%d"), discount_id, ticket_id))

# כתיבה לקובץ CSV
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["expirationDate", "startDate", "discountID", "ticketID"])  # כותרות
    writer.writerows(data)

print(f"יצרתי את קובץ ה-CSV בשם {filename} עם 400 שורות של מידע.")
