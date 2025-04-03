import psycopg2
import csv

# פרטי חיבור למסד הנתונים
DB_NAME = "mydatabase"
DB_USER = "noder"
DB_PASSWORD = "docker"
DB_HOST = "localhost"
DB_PORT = "5432"

CSV_FILE = "blocked_passengers.csv"


def insert_data_from_csv(csv_file):
    """מכניס נתונים מקובץ CSV לטבלה blocked_passenger"""
    try:
        # יצירת חיבור למסד הנתונים
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        with open(csv_file, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # דילוג על שורת הכותרות

            for row in reader:
                reason, blocked_date, unblock_date, passenger_id = row

                # המרת ערכים ריקים ל-NULL
                unblock_date = unblock_date.strip() or None

                cur.execute(
                    """
                    INSERT INTO blocked_passenger (reason, blockeddate, unblockdate, passengerid)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (reason, blocked_date, unblock_date, int(passenger_id))
                )

        conn.commit()
        print("✅ הנתונים הוזנו בהצלחה למסד הנתונים!")

    except Exception as e:
        print(f"❌ שגיאה: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    insert_data_from_csv(CSV_FILE)
