from flask import Flask
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)

seeder = FlaskSeeder()
seeder.init_app(app, db)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(50))

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def __repr__(self):
        return f"<User {self.name}>"


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created = db.Column(db.DateTime)
    content = db.Column(db.String(255))
    completed = db.Column(db.Boolean)

    def __init__(self, user_id, created, content, completed):
        self.user_id = user_id
        self.created = created
        self.content = content
        self.completed = completed

    def __repr__(self):
        return f"<Task {self.content}>"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
