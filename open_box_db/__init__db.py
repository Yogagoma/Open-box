from base import Base, engine
from models.employee import Employee
from models.athlete import Athlete
from models.shift import Shift
from models.plan import Plan

print('Creating tables')
Base.metadata.create_all(bind=engine)
print('Finish')

