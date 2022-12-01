import json
import datetime

class Medicine():
    def __init__(self):
        self.medicines = {}
        self.read_JSON()

    def read_JSON(self):
        with open ("medicine.json", "r") as f:
            self.medicines = json.load(f)

    def write_JSON(self):
        with open ("medicine.json", "w") as f:
            json.dump(self.medicines, f)

    def add_medicine(self, name:str, quantity:int):
        self.medicines["medicines"][name]["quantity"] += quantity
        self.get_dates()
        self.write_JSON()

    def __str__(self)->str:
        string = ""
        for medicine in self.medicines["medicines"]:
            medication = self.medicines["medicines"][medicine]
            string += f"{medicine} has {medication['quantity']} and {medication['remaining_days']} and will run out on {medication['end_date']} \n"
        return(string)

    def get_dates(self):
        last_check = datetime.datetime.strptime(self.medicines["last_check"][0:10], "%Y-%m-%d")
        today = datetime.datetime.today().strptime(datetime.datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")

        if str(last_check) != str(today):
            for medicine in self.medicines["medicines"]:
                if medicine == "phen":
                    modifier = 5
                else:
                    modifier = 6

                self.medicines["medicines"][medicine]["quantity"] -= int(str(today - last_check).removesuffix(f" days, 0:00:00"))

                remaining_days = int(self.medicines["medicines"][medicine]["quantity"])//modifier
                end_date = today + datetime.timedelta(days=remaining_days)

                self.medicines["last_check"] = str(today)
                self.medicines["medicines"][medicine]["remaining_days"] = remaining_days
                self.medicines["medicines"][medicine]["end_date"] = str(end_date)
            self.write_JSON()

a = Medicine()