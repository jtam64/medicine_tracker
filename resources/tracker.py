import json
import datetime

'''A simple medication tracker using python
'''


class Medicine():
    def __init__(self):
        self.medicines = {}
        self.read_JSON()
        self.update_quantity()


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


    def add_medicine(self, name: str, quantity: float) -> str:
        '''Increase quantity for the specified medication

        Args:
            name (str): Name of the medication
            quantity (float): Number to increase by

        Returns:
            (str): A string for confirmation
        '''
        quantity = round(quantity, 1)
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return f"{name} is not registered in the database"

        if quantity < 0:
            return f"Cannot add negative quantity to {name}"

        self.medicines["medicines"][name]["quantity"] += quantity
        self.write_JSON()
        self.update_quantity()
        return f"Added {quantity} to {name}\n"


    def remove_medicine(self, name: str, quantity: float) -> str:
        '''Decrease quantity for the specified medication

        Args:
            name (str): Name of the medication
            quantity (float): Number to decrease by

        Returns:
            (str): A string for confirmation
        '''
        quantity = round(quantity, 1)
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        if quantity < 0:
            return "Cannot remove negative quantity from {name}"

        self.medicines["medicines"][name]["quantity"] -= quantity
        self.write_JSON()
        self.update_quantity()
        return f"Removed {quantity} from {name}\n"


    def check_quantity(self, name: str) -> float:
        '''Check the quantity for the specified medication

        Args:
            name (str): Name of the medication

        Returns:
            (str): A string for confirmation
        '''
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        return float(self.medicines['medicines'][name]['quantity'])


    def medicine_quantity(self, name: str, quantity: float) -> bool:
        '''Update the quantity for the specified medication

        Args:
            name (str): Name of the medication
            quantity (float): Number to update to

        Returns:
            (str): A string for confirmation
        '''
        quantity = round(quantity, 1)
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        old_quantity = self.check_quantity(name)

        if quantity > old_quantity:
            return self.add_medicine(name, quantity - old_quantity)
        elif quantity < old_quantity:
            return self.remove_medicine(name, old_quantity - quantity)
        else:
            return ""


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
        return dict((sorted(self.medicines["medicines"].items(), key=lambda x: x[1]["remaining_days"])))


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

    def check_modifier(self, name:str) -> float:
        '''Check the modifier for the specified medication

        Args:
            name (str): Name of the medication

        Returns:
            (str): A string for confirmation
        '''
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        return float(self.medicines['medicines'][name]['modifier'])


    def change_modifier(self, name: str, amount: float) -> str:
        '''Change the modifier value

        Args:
            name (str): Name of medicine
            amount (float): New modifier amount

        Returns:
            (str): A string to confirm
        '''
        amount = round(amount, 1)
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return (f"{name} is not registered in the database")

        old = self.check_modifier(name)

        if float(amount) == float(old):
            return ""
        
        if amount < 0:
            return f"{amount} is not a valid modifier"

        self.medicines["medicines"][name]["modifier"] = amount
        self.write_JSON()
        self.update_quantity()
        return f"{name} modifier {old} changed to {amount}"


    def add_new(self, name: str, quantity: float, modifier: float) -> str:
        '''Add new medication 

        Args:
            name (str): Name of medication
            quantity (float): Quantity to be added
            modifier (float): How many pills are taken per day

        Returns:
            str: Confirmation string
        '''
        quantity = round(quantity, 1)
        name = name.upper()
        self.medicines["medicines"][name] = {
            "quantity": quantity,
            "end_date": "0000-00-00 00:00:00",
            "remaining_days": 0,
            "modifier": modifier
        }

        self.update(name)

        return f"Added medication {name} with quantity {quantity}\n"


    def delete_medicine(self, name:str) -> bool:
        '''Delete the specified medication

        Args:
            name (str): Name of the medication

        Returns:
            (bool): True if successful, False if not
        '''
        name = name.upper()
        if name not in self.medicines["medicines"].keys():
            return f"{name} is not registered in the database"

        self.medicines["medicines"].pop(name)

        self.write_JSON()
        self.update_quantity()
        return f"Deleted {name} from the database"
    
    def change_name(self, old_name: str, new_name: str) -> bool:
        '''Change the name of the medication

        Args:
            old_name (str): Old name of the medication
            new_name (str): New name of the medication

        Returns:
            (bool): True if successful, False if not
        '''
        old_name = old_name.upper()
        new_name = new_name.upper()
        if old_name not in self.medicines["medicines"].keys():
            return f"{old_name} is not registered in the database"

        self.medicines["medicines"][new_name] = self.medicines["medicines"].pop(old_name)
        self.write_JSON()
        self.update_quantity()
        return f"Changed name from {old_name} to {new_name}"
    
a = Medicine()