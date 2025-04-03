import pandas as pd
import random

def assign_trip_ids(seat_file, trip_file, output_file):
    # קריאת הקבצים
    seat_df = pd.read_csv(seat_file)
    trip_df = pd.read_csv(trip_file)
    
    # הפיכת tripID לרשימה והכנה לשימוש
    trip_ids = trip_df['tripID'].tolist()
    random.shuffle(trip_ids)  # ערבוב לשמירה על שונות
    
    # שמירת היסטוריית שימוש במושבים
    seat_history = {}
    assigned_trips = []
    
    for seat in seat_df['seatNumber']:
        if seat not in seat_history:
            seat_history[seat] = set()
        
        # חיפוש tripID שעדיין לא הוקצה לאותו seatNumber
        available_trips = [tid for tid in trip_ids if tid not in seat_history[seat]]
        
        if available_trips:
            selected_trip = random.choice(available_trips)
        else:
            # אם אין tripID זמין, נשתמש ב-tripID ממושב אחר
            all_used_trips = set(assigned_trips)
            unused_trips = [tid for tid in trip_ids if tid not in all_used_trips]
            selected_trip = random.choice(unused_trips) if unused_trips else random.choice(trip_ids)
        
        assigned_trips.append(selected_trip)
        seat_history[seat].add(selected_trip)

    # הוספת tripID לעמודה
    seat_df['tripID'] = pd.Series(assigned_trips, dtype='Int64')

    # שמירת הקובץ החדש
    seat_df.to_csv(output_file, index=False)
    print(f"✅ קובץ נשמר בהצלחה בשם {output_file}!")

# קריאה לפונקציה לדוגמא
assign_trip_ids('Seat_no_tripID.csv', 'Trip.csv', 'Seat.csv')
