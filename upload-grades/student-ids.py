import csv, json

with open("students.json") as f:
    data = json.load(f)
ids = [(record["short_name"], record["id"])
       for record in data if record["short_name"] != "Test Student"]
with open("students.csv", "w") as f:
    writer = csv.writer(f)
    for record in sorted(ids):
        writer.writerow(record)
