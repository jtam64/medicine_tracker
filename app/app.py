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

def get_medicine(medication_id:int):
    """Get data for medicine"""
    logger.info(f"Request started for medication with id: {medication_id}")

    session = DB_SESSION()

    if session.query(Medicine).count() < 1:
        "Check if anything exists in DB"
        logger.info(f"Empty db. Nothing returned")
        return "No values in DB. Please populate", 404

    elif not bool(session.query(Medicine).filter_by(id=medication_id).first()):
        "Check if medication exists in DB"
        logger.info(f"Invalid medication ID. Nothing returned")
        return "Medication does not exist yet", 404

    else:
        "Return medication data"
        medication = session.query(Medicine).get(medication_id)
        logger.info(f"Found medication with id {medication_id}.")
        
        data = {
            "id": medication.id,
            "name": medication.name,
            "quantity": medication.quantity,
            "remaining_days": medication.remaining_days,
            "modifier": medication.modifier,
            "end_date": medication.end_date,
        }
        return data, 200


def populate_medicine(body):
    """Post new data into db"""
    logger.info(f"Request started for adding {body} to db")

    session = DB_SESSION()

    if bool(session.query(Medicine).filter_by(name=body["name"]).first()):
        "Check if medication already exists in DB"
        logger.info(f"Medication found in DB. Don't overwrite information.")
        return "Medication already exists", 409

    else:
        "Extract information from body"
        name, quantity, modifier = body["name"], body["quantity"], body["modifier"]

        "Calculate remaining_days and end_date"
        today = datetime.date.today()
        end_date = today + datetime.timedelta(modifier)
        remaining_days = int(quantity / modifier)

        "Add new medication to DB"
        data = Medicine(
            name,
            quantity,
            remaining_days,
            modifier,
            end_date
        )

        session.add(data)
        logger.info("Adding data to DB")
        session.commit()
        logger.info(f"Medication {name} added to db. Information:\nname: {name}, quantity: {quantity}, remaining_days: {remaining_days}, modifier: {modifier}, end_date: {end_date}")

        "Get ID of new medication to be returned"
        written_data = session.query(Medicine).filter_by(name=body["name"]).first()
        return written_data.id, 201



app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    app.run(port=2000)