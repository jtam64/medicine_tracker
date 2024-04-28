import logging
import logging.config
import sched, time
import datetime
import requests
from base import Base
import create_db
from os.path import exists
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from last_update import LastUpdate
import yaml

with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

with open("log_conf.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.info("Begin logging")

# create db if it doesnt exist
if not exists(app_config["datastore"]["filename"]):
    logger.info("Creating DB")
    create_db.main()

DB_ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

s = sched.scheduler(time.time, time.sleep)

session = DB_SESSION()

def update_date():
    logger.info("Checking last update")
    try:
        logger.info("Last update entry found")
        db_query = session.query(LastUpdate).first()
        last_update = db_query.last_update
    except:
        "Empty DB. Add first entry"
        logger.info("No last update entry found. Adding first entry")
        last_update = datetime.datetime.now().date()

        data = LastUpdate(last_update)
        session.add(data)
        session.commit()

    today = datetime.datetime.now().date()

    if last_update < today:
        logger.info(f"Updating date {last_update} to {today}")
        requests.post(f"http://{app_config['update']['url']}:{app_config['update']['port']}/daily_update", json = {"date": str(last_update)})

        db_query.last_update = today

        session.commit()

        logger.info("Date updated")
    else:
        logger.info("Date already updated")

def run_daily_update():
    s.enter(app_config["update"]["frequency"], 1, update_date, ())
    s.enter(app_config["update"]["frequency"], 1, run_daily_update, ())

if __name__ == "__main__":
    run_daily_update()
    s.run()