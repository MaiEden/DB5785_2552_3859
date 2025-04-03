import csv
import random

# הגדרת טווחי הנתונים
num_tickets = 400  # 400 כרטיסים
num_discounts = 100  # לדוגמה, 100 מזהי הנחות

discount_ids = list(range(1, num_discounts + 1))  # מזהי הנחות מ-1 עד 100
ticket_ids = list(range(1, num_tickets + 1))  # מזהי כרטיסים מ-1 עד 400

# יצירת צירופי discountID ו-ticketID ייחודיים
used_pairs = set()
discount_tickets = []

for _ in range(400):  # יצירת 400 שורות
    while True:
        discount_id = random.choice(discount_ids)
        ticket_id = random.choice(ticket_ids)

        if (discount_id, ticket_id) not in used_pairs:
            used_pairs.add((discount_id, ticket_id))
            break

    start_date = f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    expiration_date = f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

    discount_tickets.append([expiration_date, start_date, discount_id, ticket_id])

# כתיבת הנתונים לקובץ CSV
with open('discount_tickets.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["expirationDate", "startDate", "discountID", "ticketID"])  # כותרות
    writer.writerows(discount_tickets)

print("קובץ discount_tickets.csv נוצר בהצלחה!")