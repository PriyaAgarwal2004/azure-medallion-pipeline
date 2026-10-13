import sqlite3
import pandas as pd

df = pd.read_csv("clean_students.csv")

conn = sqlite3.connect("students.db")
df.to_sql("students", conn, if_exists="replace", index=False)

#result = pd.read_sql("SELECT * FROM students", conn)
#print(result)

#result = pd.read_sql("SELECT city, AVG(score) FROM students GROUP BY city", conn)
#print(result)

#result = pd.read_sql("SELECT * FROM students WHERE age_missing = True", conn)
#print(result)

#result = pd.read_sql("SELECT * FROM students WHERE age IS NULL", conn)
#print(result)

#result = pd.read_sql("SELECT * FROM students WHERE score IS NOT NULL", conn)
#print(result)

#result = pd.read_sql("SELECT COUNT(*) FROM students", conn)
#print(result)

#result = pd.read_sql("SELECT COUNT(score) FROM students", conn)
#print(result)

#result = pd.read_sql("SELECT city, COUNT(*), AVG(score) FROM students GROUP BY city", conn)
#print(result)

#query = """
#SELECT city,
    #   COUNT(*) AS students,
     #  COUNT(score) AS scores_available,
     #  AVG(score) AS avg_score
#FROM students
#GROUP BY city
#"""

query_sorted = """SELECT * FROM students ORDER BY score"""

query_pune = """SELECT name, score FROM students WHERE score IS NOT NULL AND city = 'Pune'"""
result = pd.read_sql(query_sorted, conn)
print(result)

conn.close()