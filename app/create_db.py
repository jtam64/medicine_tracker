import sqlite3
import yaml

with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

con = sqlite3.connect(app_config["datastore"]["filename"])

cur = con.cursor()

cur.execute("""CREATE TABLE medicine(
            id INTEGER PRIMARY KEY ASC,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            remaining_days INTEGER NOT NULL,
            modifier REAL NOT NULL,
            end_date TEXT NOT NULL
        )""")

con.commit()
con.close()