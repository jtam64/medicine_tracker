import json
import datetime

'''A simple medication tracker using python
'''


class Medicine():
    def __init__(self):
        self.medicines = {}
        self.read_JSON()
        self.get_dates()

    def read_JSON(self):
        '''Read the json file
        '''
        with open("resources/medicine.json", "r") as f:
            self.medicines = json.load(f)

    def write_JSON(self):
        '''Write to the json file
        '''
        with open("resources/medicine.json", "w") as f:
            json.dump(self.medicines, f)

    def add_medicine(self, name: str, quantity: int)->str:
        '''Increase quantity for the specified medication

        Args:
            name (str): Name of the medication
            quantity (int): Number to increase by

        Returns:
            (str): A string for confirmation
        '''
        self.medicines["medicines"][name]["quantity"] += quantity
        self.get_dates()
        return f"\nAdded {quantity} to {name}\n"

    def __str__(self) -> str:
        '''Dunder method to print all the medicines and their total number remaining, days remaining, and end date

        Returns:
            str: A string of all the medicines
        '''
        string = ""
        for medicine in self.medicines["medicines"]:
            medication = self.medicines["medicines"][medicine]
            string += f"There is {medication['quantity']} pills of {medicine}. You will run out after {medication['remaining_days']} days which is {medication['end_date']} \n"
        return (string)

    def get_dates(self):
        '''Checks if todays date is the same as the last check. If it is, go through the medicaiton and change the remaining quantity, remaining days, days till depleted and updates the last check to todays date
        '''
        last_check = datetime.datetime.strptime(
            self.medicines["last_check"][0:10], "%Y-%m-%d")
        today = datetime.datetime.today().strptime(
            datetime.datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")

        if str(last_check) != str(today):
            for medicine in self.medicines["medicines"]:

                modifier = self.medicines["medicines"][medicine]["modifier"]
                try:
                    self.medicines["medicines"][medicine]["quantity"] -= int(
                        str(today - last_check).removesuffix(f" days, 0:00:00")) * modifier
                except:
                    self.medicines["medicines"][medicine]["quantity"] -= int(
                        str(today - last_check).removesuffix(f" day, 0:00:00")) * modifier

                remaining_days = int(
                    self.medicines["medicines"][medicine]["quantity"]) // modifier
                end_date = today + datetime.timedelta(days=remaining_days)

                self.medicines["last_check"] = str(today)
                self.medicines["medicines"][medicine]["remaining_days"] = remaining_days
                self.medicines["medicines"][medicine]["end_date"] = str(
                    end_date)
            self.write_JSON()

    def change_modifier(self, name: str, amount: int)->str:
        '''Change the modifier value

        Args:
            name (str): Name of medicine
            amount (int): New modifier amount
        
        Returns:
            (str): A string to confirm
        '''
        old = self.medicines["medicines"][name]["modifier"]
        self.medicines["medicines"][name]["modifier"] = amount
        self.write_JSON()
        return f"\n{name} modifier {old} changed to {amount}\n"

    def add_new(self, name:str, quantity:int)->str:
        self.medicines["medicines"][name] = {
            "quantity": quantity,
            "end_date": "",
            "remaining_days": 0,
            "modifier": 0
        }
        self.write_JSON()
        self.get_dates()
        return f"\nadded medication {name} with quantity {quantity}\n"
