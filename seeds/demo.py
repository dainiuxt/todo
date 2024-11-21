from flask_seeder import Faker, generator
from todo.app import db, User, Task


# Create a new Faker and tell it how to create User objects
users = Faker(
  cls=User,
  init={
    "email": generator.Email(),
    "password": generator.String(),
    "name": generator.Name()
  }
)

# Create 5 users
for user in users.create(5):
    print("Adding user: %s" % user)
    db.session.add(user)

db.session.commit()

# Create a new Faker and tell it how to create Task objects
tasks = Faker(
  cls=Task,
  init={
    "user_id": generator.Random(1, 5),
    "created": generator.Date(),
    "content": generator.Text(),
    "completed": generator.Boolean()
  }
)

# Create 15 tasks
for task in tasks.create(15):
    print("Adding task: %s" % task)
    db.session.add(task)

db.session.commit()


# class User(db.Model):
#     def __init__(self,
#                  id=None,
#                  email=None,
#                  password=None,
#                  name=None):
#         self.id = id
#         self.email = email
#         self.password = password
#         self.name = name


# class Task(db.Model):
#     def __init__(self,
#                  id=None,
#                  user_id=None,
#                  created=None,
#                  content=None,
#                  completed=None):
#         self.id = id
#         self.user_id = user_id
#         self.created = created
#         self.content = content
#         self.completed = completed


# # All seeders inherit from Seeder
# class DemoSeeder(Seeder):

#     # run() will be called by Flask-Seeder
#     def run(self):
#         # Create a new Faker and tell it how to create User objects
#         users = Faker(
#             cls=User,
#             init={
#                 "id": generator.Sequence(),
#                 "email": generator.Email(),
#                 "password": generator.String(),
#                 "name": generator.Name()
#             }
#         )

#         # Create 5 users
#         for user in users.create(5):
#             print("Adding user: %s" % user)
#             self.db.session.add(user)

#         tasks = Faker(
#             cls=Task,
#             init={
#                 "id": generator.Sequence(),
#                 "user_id": generator.Integer(start=1, stop=5),
#                 "created": generator.timestamp(),
#                 "content": generator.String(),
#                 "completed": generator.Boolean()
#             }
#         )

#         # Create 5 tasks
#         for task in tasks.create(5):
#             print("Adding task: %s" % task)
#             self.db.session.add(task)

#         self.db.session.commit()

#         print("Done!")
