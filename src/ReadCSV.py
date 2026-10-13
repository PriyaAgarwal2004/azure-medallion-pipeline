import csv

scores = []

with open("students.csv", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    #for row in reader:
        #print(row)
        #print(row["name"], row["city"])

    #for row in reader:
        #if row["city"] == "Pune":
            #print(row["name"])

    for row in reader:
        if row["score"] != "":
            scores.append(int(row["score"]))

print(scores)
print(sum(scores))
print(len(scores))
average = sum(scores) / len(scores)
print("Average score:", average)