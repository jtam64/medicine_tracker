from sqlalchemy import Column, Integer, Date, Float, String

class Medicine():
    __tablename__="medicine"
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    quantity = Column(Float,nullable=False)
    remaining_days = Column(Integer,nullable=False)
    modifier = Column(Float,nullable=False)
    end_date = Column(Date,nullable=False)

    def __init__(self, name, quantity, remaining_days, modifier, end_date):
        self.name = name
        self.quantity = quantity
        self.remaining_days = remaining_days
        self.modifier = modifier
        self.end_date = end_date

    def to_dict(self):
        dict = {}
        dict['name'] = self.name
        dict['quantity'] = self.quantity
        dict['remaining_days'] = self.remaining_days
        dict['modifier'] = self.modifier
        dict['end_date'] = self.end_date.strftime("%Y-%m-%d")
        return dict