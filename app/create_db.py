import sqlite3
import yaml

with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

con = sqlite3.connect(app_config["datastore"]["filename"])

cur = con.cursor()

cur.execute("""CREATE TABLE medicine(
            name TEXT,
            quantity INTEGER,
            remaining_days INTEGER,
            modifier REAL,
            end_date TEXT
)""")

con.commit()
