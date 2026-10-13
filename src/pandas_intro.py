import pandas as pd

df = pd.read_csv("students.csv")
#print(df)
#print(df["name"])             # one column, like row["name"]
#print(df[df["city"] == "Pune"])   # only Pune students, like your if
#print(df["score"].mean())     # average score, skipping NaN automatically
#top = df[df["score"] > 80]
#print(top)
#pune = df[(df["city"] == "Pune") & (df["score"] > 60)][["name", "city", "score"]]
#print(pune)
#top.to_csv("top_students_pandas.csv", index=False)
#pune.to_csv("top_students_Pune_pandas.csv", index=False)
print(df.groupby("city")["score"].mean())
print(df.groupby("city")["score"].count())