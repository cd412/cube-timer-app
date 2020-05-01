import pandas as pd
import sqlite3

con = sqlite3.connect("data.db")
df = pd.read_sql_query("SELECT * from user", con)
print(df.head(100))

df = pd.read_sql_query("SELECT * from time", con)
print(df.head(100))

con.close()