import connexion

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from medicine import Medicine
from functions import calculate_remaining
import create_db
from os.path import exists
import datetime

import yaml

import logging
import logging.config

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
        end_date, remaining_days = calculate_remaining(quantity, modifier)

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

def modify_medication(body):
    session = DB_SESSION()

    "Extract information from body"
    id, name, quantity, modifier = body["id"], body["name"], body["quantity"], body["modifier"]

    logger.info(f"Beginning query for ID: {id}")

    if session.query(Medicine).count() < 1:
        "Check if anything exists in DB"
        logger.info(f"Empty db. Nothing returned")
        return "No values in DB. Please populate", 404

    elif not bool(session.query(Medicine).filter_by(id=id).first()):
        "Check if medication exists in DB. If not, return error."
        logger.info(f"Medication does not exist in DB")
        return "Medication not found", 404

    else:
        "Calculate remaining_days and end_date"
        end_date, remaining_days = calculate_remaining(quantity, modifier)

        medication = session.query(Medicine).filter_by(id=id).first()
        logger.info(f"Found medication with ID: {id}")
        
        medication.name = name
        medication.quantity = quantity
        medication.remaining_days = remaining_days
        medication.modifier = modifier
        medication.end_date = end_date
        
        session.commit()
        logger.info(f"Updated medication with id: {id}")
        return "Updated medication", 200

def remove_medication(body):
    session = DB_SESSION()

    "Get ID from body"
    id = body["id"]
    logger.info(f"Beginning query for ID: {id}")

    if session.query(Medicine).count() < 1:
        "Check if anything exists in DB"
        logger.info(f"Empty db. Nothing returned")
        return "No values in DB. Please populate", 404

    elif not bool(session.query(Medicine).filter_by(id=id).first()):
        "Check if medication exists in DB. If not, return error."
        logger.info(f"Medication does not exist in DB")
        return "Medication not found", 404

    else:
        session.query(Medicine).filter_by(id=id).delete()
        logger.info(f"Found medication with ID: {id}")
        session.commit()
        logger.info(f"Succesfully removed medication with ID: {id}")
        return "Removed medication", 200

def daily_update(body):
    session = DB_SESSION()

    if session.query(Medicine).count() < 1:
        "Check if anything exists in DB"
        logger.info(f"Empty db. Nothing returned")
        return "No values in DB. Please populate", 404
    else:
        "Get todays date"
        today = datetime.datetime.now().date()
        input_date = datetime.datetime.strptime(body["date"], "%Y-%m-%d").date()

        "Return 202 if there is nothing to update"
        if input_date >= today:
            return "No updates needed", 202
        else:
            "Get all medications"
            medications = session.query(Medicine).all()

            "for each medication"
            for medicine in medications:
                logger.info(f"Begin updating {medicine.name}")
                "Calculate quantity change"
                days_since = today - input_date
                used_amount = int(days_since.days * medicine.modifier)
                quantity = medicine.quantity - used_amount

                "Calculate remaining days and end date"
                end_date, remaining_days = calculate_remaining(medicine.quantity, medicine.modifier)

                "Update the medication"
                medicine.quantity = quantity
                medicine.remaining_days = remaining_days
                medicine.end_date = end_date
                
                logger.info(f"Updated {medicine.name}")
                session.commit()

            logger.info("Updated all medications")
            return "Updated all medications", 200


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8900)