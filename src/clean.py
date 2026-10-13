import pandas as pd

df = pd.read_csv("messy.csv")
print(df)

df["city"] = df["city"].str.strip().str.title()   # fix spaces and capitalization
print(df)
df = df.drop_duplicates()                          # remove repeated rows
print(df)
#df["score"] = df["score"].fillna(0)                # fill missing scores
#print(df)
df["score_missing"] = df["score"].isna()
df["age_missing"] = df["age"].isna()
print(df)
print(df["score"].mean())              # with NaN left as is
print(df["score"].fillna(0).mean()) # with 0 filled in
print(df["age"].mean())   # with NaN left as is
print(df["age"].fillna(0).mean()) # with 0 filled in
print(df["score"].count())             # non-missing only
print(len(df))                         # all rows
print(df[~df["score_missing"]]["score"].mean()) # average score, real scores only
df.to_csv("clean_students.csv", index=False)