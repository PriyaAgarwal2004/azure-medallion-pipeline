import requests
import pandas as pd
import sqlite3
import logging

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
) 

def extract(url):
    """Download user data from the API and return it as a list of dictionaries."""
    try:
        response = requests.get(url, timeout=10)  # give up after 10 seconds
        response.raise_for_status()               # raise an error if status is not 200
    except requests.exceptions.RequestException as e:
        print("Extract failed:", e) 
        logging.error("Extract failed: %s", e)              # one clear line instead of a long traceback
        raise SystemExit(1)                       # stop here so later steps don't run
    return response.json()                        # hand the data back to the caller


def transform(data):
    """Flatten the nested JSON into a clean table (DataFrame)."""
    rows = []
    for user in data:
        rows.append({
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "city": user["address"]["city"],      # nested: address -> city
            "company": user["company"]["name"],   # nested: company -> name
        })

    df = pd.DataFrame(rows)

    df["city"] = df["city"].str.strip()  # remove extra spaces, keep original capitalization

    # Speak up only when something is wrong
    if df.isna().sum().sum() > 0:
        print("Warning: missing values found")
    if df.duplicated().sum() > 0:
        print("Warning: duplicate rows found")

    return df


def load(df, db_name):
    """Write the DataFrame into a SQLite table called 'users'."""
    conn = sqlite3.connect(db_name)                             # open (or create) the database file
    df.to_sql("users", conn, if_exists="replace", index=False)  # rebuild the table on each run
    conn.close()


def run_query(db_name, query):
    """Run a SQL query and return the result as a DataFrame."""
    conn = sqlite3.connect(db_name)
    result = pd.read_sql(query, conn)
    conn.close()
    return result


# SQL queries
query_company_counts = """
SELECT company, COUNT(*) AS users
FROM users
GROUP BY company
ORDER BY users DESC
"""

query_names_with_c = """
SELECT name, city FROM users WHERE name LIKE 'C%'
"""


# Run the pipeline
if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/users"

    logging.info("Pipeline started")
    data = extract(url)               # 1. Extract
    df = transform(data)              # 2. Transform
    print(df.shape)                   # should print (10, 5)
    load(df, "users.db")              # 3. Load
    logging.info("Pipeline finished: %s rows loaded", len(df))
    print(run_query("users.db", query_company_counts))  # 4. Query