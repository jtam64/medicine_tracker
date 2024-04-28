import sqlite3
import yaml

with open("/app_configs/app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

def main():
    con = sqlite3.connect(app_config["datastore"]["filename"])

    cur = con.cursor()

    cur.execute("""CREATE TABLE last_update(
                id INTEGER PRIMARY KEY ASC,
                last_update VARCHAR(100) NOT NULL
            )""")

    con.commit()
    con.close()

if __name__ == "__main__":
    main()
