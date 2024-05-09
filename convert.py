import csv
import datetime
from pathlib import Path

reader = csv.DictReader(open(f"data/gelbe_karten_stuttgart.csv"))
day = None
data = []
for row in reader:
    if not day:
        day = row["first_seen_date"]
    if day != row["first_seen_date"]:
        dt = datetime.date(*[int(i) for i in day.split("-")])
        Path(f"data/{dt.year}").mkdir(exist_ok=True)
        with open(f"data/{dt.year}/{day}.csv", "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=row.keys())
            for incident in data:
                writer.writerow(incident)
        day = row["first_seen_date"]
        data = [row]
    else:
        data.append(row)
