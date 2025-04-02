import random
import csv
from datetime import datetime, timedelta

# אפשרויות לסיבת חסימה
REASONS = [
    "Fraudulent activity",
    "Multiple no-shows",
    "Payment issues",
    "Violation of terms",
    "Aggressive behavior",
    "Suspicious booking patterns",
    "Fake ID used"
]


def generate_random_date(start_date, end_date):
    """צור תאריך אקראי בין start_date ל-end_date."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def load_passenger_ids_from_csv(file_path):
    """טען מזהי נוסעים ייחודיים מקובץ CSV."""
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader if row]


def generate_csv(output_file, csv_file):
    """צור קובץ CSV עם נתוני חסימת נוסעים."""
    passenger_ids = load_passenger_ids_from_csv(csv_file)
    random.shuffle(passenger_ids)  # ערבב כדי להבטיח אקראיות

    data = []
    for i in range(min(50, len(passenger_ids))):
        reason = random.choice(REASONS)
        blocked_date = generate_random_date(datetime(2020, 1, 1), datetime(2025, 1, 1))
        unblock_date = blocked_date + timedelta(days=random.randint(30, 420))  # 1 עד 14 חודשים (בערך)
        passenger_id = passenger_ids[i]  # שמירת ייחודיות

        data.append([reason, blocked_date.strftime('%Y-%m-%d'), unblock_date.strftime('%Y-%m-%d'), passenger_id])

    # כתיבה לקובץ CSV
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Reason", "BlockedDate", "UnblockDate", "PassengerID"])  # כותרות עמודות
        writer.writerows(data)

    print(f"{len(data)} שורות נכתבו בהצלחה לקובץ {output_file}!")


if __name__ == "__main__":
    generate_csv("blocked_passengers.csv", "passenger_ids.csv")
