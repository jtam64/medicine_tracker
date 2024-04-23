from sqlalchemy import Column, Integer, Date
from base import Base

class LastUpdate(Base):
    __tablename__="last_update"
    id = Column(Integer, primary_key=True)
    last_update = Column(Date,nullable=False)

    def __init__(self, last_update):
        self.last_update = last_update

    def to_dict(self):
        dict = {}
        dict['last_update'] = self.last_update.strftime("%Y-%m-%d")
        return dict