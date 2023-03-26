import json
import datetime

'''A simple medication tracker using python
'''


class Medicine():
    def __init__(self):
        self.medicines = {}
        self.read_JSON()
        self.update_quantity()


    def pre_check(self, name):
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")


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


    def add_medicine(self, name: str, quantity: int) -> str:
        '''Increase quantity for the specified medication

        Args:
            name (str): Name of the medication
            quantity (int): Number to increase by

        Returns:
            (str): A string for confirmation
        '''
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        if quantity < 0:
            return False

        self.medicines["medicines"][name]["quantity"] += quantity
        self.write_JSON()
        self.update_quantity()
        return f"\nAdded {quantity} to {name}\n"


    def remove_medicine(self, name: str, quantity: int) -> str:
        '''Decrease quantity for the specified medication

        Args:
            name (str): Name of the medication
            quantity (int): Number to decrease by

        Returns:
            (str): A string for confirmation
        '''
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        if quantity < 0:
            return False

        self.medicines["medicines"][name]["quantity"] -= quantity
        self.write_JSON()
        self.update_quantity()
        return f"\nRemoved {quantity} from {name}\n"


    def check_quantity(self, name: str) -> int:
        '''Check the quantity for the specified medication

        Args:
            name (str): Name of the medication

        Returns:
            (str): A string for confirmation
        '''
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        return int(self.medicines['medicines'][name]['quantity'])


    def medicine_quantity(self, name: str, quantity: int) -> bool:
        '''Update the quantity for the specified medication

        Args:
            name (str): Name of the medication
            quantity (int): Number to update to

        Returns:
            (str): A string for confirmation
        '''
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        old_quantity = self.check_quantity(name)

        if quantity > old_quantity:
            return self.add_medicine(name, quantity - old_quantity)
        elif quantity < old_quantity:
            return self.remove_medicine(name, old_quantity - quantity)
        else:
            return False


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


    def dashboard_info(self):
        '''Returns the data for the dashboard

        Returns:
            dict: A dictionary of all the medicines
        '''
        return self.medicines["medicines"]


    def update_quantity(self):
        '''Updates the quantity remaining. Sends data to update() to update the JSON
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

                self.update(medicine)
        else:
            for medicine in self.medicines["medicines"]:
                self.update(medicine)


    def update(self, name: str):
        '''Modify JSON so it reflect correct dates

        Args:
            name (str): Name of the medication to be updated
        '''
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        modifier = self.medicines["medicines"][name]["modifier"]
        today = datetime.datetime.today().strptime(
            datetime.datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        remaining_days = float(
            self.medicines["medicines"][name]["quantity"]) // modifier
        end_date = today + datetime.timedelta(days=remaining_days)

        self.medicines["last_check"] = str(today)
        self.medicines["medicines"][name]["remaining_days"] = remaining_days
        self.medicines["medicines"][name]["end_date"] = str(end_date)
        self.write_JSON()

    def check_modifier(self, name:str) -> int:
        '''Check the modifier for the specified medication

        Args:
            name (str): Name of the medication

        Returns:
            (str): A string for confirmation
        '''
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        return int(self.medicines['medicines'][name]['modifier'])


    def change_modifier(self, name: str, amount: int) -> str:
        '''Change the modifier value

        Args:
            name (str): Name of medicine
            amount (int): New modifier amount

        Returns:
            (str): A string to confirm
        '''
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        old = self.check_modifier(name)

        if amount == old:
            return False
        
        if amount < 0:
            return False

        self.medicines["medicines"][name]["modifier"] = amount
        self.write_JSON()
        self.update_quantity()
        return f"\n{name} modifier {old} changed to {amount}\n"


    def add_new(self, name: str, quantity: int, modifier: int) -> str:
        name = name.upper()
        self.medicines["medicines"][name] = {
            "quantity": quantity,
            "end_date": "0000-00-00 00:00:00",
            "remaining_days": 0,
            "modifier": modifier
        }

        self.update(name)

        return f"\nadded medication {name} with quantity {quantity}\n"


    def delete_medicine(self, name:str) -> bool:
        '''Delete the specified medication

        Args:
            name (str): Name of the medication

        Returns:
            (bool): True if successful, False if not
        '''
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return False

        self.medicines["medicines"].pop(name)

        self.write_JSON()
        self.update_quantity()
        return True
    
a = Medicine()