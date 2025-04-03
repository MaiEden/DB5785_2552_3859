import pandas as pd
import random

# קריאה לקובץ המקורי
df = pd.read_csv('spacialNeedPassenger.csv')

# קריאה לקובץ שמכיל את העמודה disabilityType
disability_df = pd.read_csv('disabilities.csv')

# הגרלת ערכים מהעמודה disabilityType
disability_types = disability_df['disabilityType'].tolist()
df['disabiltyType'] = [random.choice(disability_types) for _ in range(len(df))]

# שמירה לקובץ החדש
df.to_csv('spacialNeedPassenger.csv', index=False)
