import json
import csv

def export_json(session):
    with open("session.json", "w") as f:
        json.dump(session.__dict__, f, indent=2)

def export_csv(session):
    with open("events.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["event"])
        for e in session.events:
            writer.writerow([e])
