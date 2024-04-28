import sqlite3
import yaml

with open("/app_configs/app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

def main():
    con = sqlite3.connect(app_config["datastore"]["filename"])

    cur = con.cursor()

    cur.execute("""CREATE TABLE medicine(
                id INTEGER PRIMARY KEY ASC,
                name VARCHAR(100) NOT NULL,
                quantity INTEGER NOT NULL,
                remaining_days INTEGER NOT NULL,
                modifier REAL NOT NULL,
                end_date VARCHAR(100) NOT NULL
            )""")

    con.commit()
    con.close()

if __name__ == "__main__":
    main()
