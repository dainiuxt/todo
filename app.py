from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.PasswordType)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f"<User {self.name}>"


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created = db.Column(db.DateTime)
    content = db.Column(db.String(255))
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Task {self.content}>"


class UsersTasks(db.Model):
    __tablename__ = "users_tasks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))

    def __repr__(self):
        return f"<UsersTasks {self.user_id} - {self.task_id}>"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
