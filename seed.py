from models import User, db
from app import app

db.drop_all()
db.create_all()

user1 = User(first_name='Janice', last_name='Michaels')
user2 = User(first_name='Andrew', last_name='Garfield')
user3 = User(first_name='Tina', last_name='Marks')
user4 = User(first_name='Jessica', last_name='Choi')
user5 = User(first_name='Frank', last_name='Button ')

db.session.add_all([user1, user2, user3, user4, user5])
db.session.commit()