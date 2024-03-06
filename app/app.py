import connexion

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from medicine import Medicine

import yaml
import datetime

import logging
import logging.config

"""Initial setup of application"""

"App config"
with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

"App logging"
with open("log_conf.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

"SQLite DB Connection"
DB_ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def get_medicine(medicine_id:int) -> dict:
    """Get data for medicine"""
    logger.info(f"Request started for {medicine_id}")

    session = DB_SESSION()

    if session.query(Medicine).count() < 1:
        "Check if anything exists in DB"
        return "No values in DB. Please populate", 404
    elif bool(session.query(Medicine).filter_by(id=medicine_id).first()):
        return "Medication does not exist yet", 404
    else:
        data = session.query(Medicine).filter_by(id=medicine_id)
    return



def populate_medicine(data:dict):
    """Post new data into db"""
    print("here")
    return

app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yml")

if __name__ == "__main__":
    app.run(port=2000)