from models import User, db, Posts
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

p1 = Posts(title='Hello!', content='This is a test', user_id=2)
p2 = Posts(title='Hello 2!', content='This is another test', user_id=1)
p3 = Posts(title='Hello 3!', content='This is a 3rd test', user_id=4)
p4 = Posts(title='Hello 4!', content='This is a 4th  test', user_id=5)
p5 = Posts(title='Hello 5!', content='This is a 5th test', user_id=3)

db.session.add_all([p1, p2, p3, p4, p5])
db.session.commit()

