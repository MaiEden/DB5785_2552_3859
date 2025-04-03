import pandas as pd
import random

def assign_trip_ids(seat_file, trip_file, output_file):
    # קריאת הקבצים
    seat_df = pd.read_csv(seat_file)
    trip_df = pd.read_csv(trip_file)
    
    # הפיכת tripID לרשימה
    trip_ids = trip_df['tripID'].tolist()
    random.shuffle(trip_ids)  # ערבוב רשימת ה-tripID כדי ליצור שונות
    
    # שמירת היסטוריה של seat_number כדי למנוע כפילויות
    seat_history = {}
    num_trips = len(trip_ids)
    
    # יצירת עמודת tripID בטבלת המושבים
    assigned_trips = []
    for seat in seat_df['seatNumber']:
        if seat not in seat_history:
            seat_history[seat] = set()
        
        available_trips = [tid for tid in trip_ids if tid not in seat_history[seat]]
        
        # אם אין tripID פנוי, נבחר None
        selected_trip = random.choice(available_trips) if available_trips else None
        assigned_trips.append(selected_trip)
        
        # שמירת השימוש ב-tripID עבור seat_number אם נמצא ערך תקף
        if selected_trip is not None:
            seat_history[seat].add(selected_trip)

    seat_df['tripID'] = pd.Series(assigned_trips, dtype='Int64')
    # הוספת עמודת tripID לקובץ seat
    #seat_df['tripID'] = assigned_trips
    
    # שמירת הקובץ החדש
    seat_df.to_csv(output_file, index=False)
    print(f"File saved as {output_file}")

# קריאה לפונקציה לדוגמא
assign_trip_ids('../DB5785_2552_3859/code/python/שלב א/Seat_no_tripID.csv', 'Trip.csv', 'Seat.csv')
