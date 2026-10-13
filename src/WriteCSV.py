import csv

with open("students.csv", encoding="utf-8-sig") as infile, \
     open("top_students.csv", "w", newline="") as top_file, \
     open("top_students_Pune.csv", "w", newline="") as pune_file:

    reader = csv.DictReader(infile)
    fields = ["name", "age", "city", "score"]
    fields_p = ["name", "city", "score"]


    top_writer = csv.DictWriter(top_file, fieldnames=fields)
    pune_writer = csv.DictWriter(pune_file, fieldnames=fields_p, extrasaction="ignore") # extrasaction ignores unused fields
    top_writer.writeheader()
    pune_writer.writeheader()

    for row in reader:
        if row["score"] == "":
            continue
        score = int(row["score"])
        if score > 80:
            top_writer.writerow(row)
        if score > 60 and row["city"] == "Pune":
            pune_writer.writerow(row)