import json

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

    def add_medicine(self, name, quantity):
        self.medicines[name]["quantity"] += quantity
    
    def __add__(self, name, quantity):
        self.add_medicine(name, quantity)

    def __str__(self):
        string = ""
        for medicine in self.medicines:
            string += f"{medicine} has {self.medicines[medicine]['quantity']} and will run out on {self.medicines[medicine]['end_date']} \n"
        return(string)

a = Medicine()