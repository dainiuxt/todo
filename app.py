from flask import Flask, request, jsonify
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_marshmallow import Marshmallow
from datetime import datetime

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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, metadata=metadata)
ma = Marshmallow(app)
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


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password", "name")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


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


class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "created", "content", "completed")


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
    # čia galima renderinti login/create user


# create a user
@app.route("/create_user", methods=["POST"])
def create_user():
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]

    user = User(email, password, name)
    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user)


@app.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# update a user
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]

    user.email = email
    user.password = password
    user.name = name

    db.session.commit()

    return user_schema.jsonify(user)


@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)


@app.route("/tasks")
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)


# create a task
@app.route("/create_task", methods=["POST"])
def create_task():
    user_id = request.json["user_id"]
    created = datetime.now()
    content = request.json["content"]
    completed = request.json["completed"]

    task = Task(user_id,
                created=created,
                content=content,
                completed=completed)
    db.session.add(task)
    db.session.commit()

    return task_schema.jsonify(task)


# get all tasks for a user
@app.route("/tasks/<int:user_id>", methods=["GET"])
def get_user_tasks(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    result = tasks_schema.dump(tasks)
    return jsonify(result)


# update a task
@app.route("/tasks/<int:user_id>/<int:id>", methods=["PUT"])
def update_task(id, user_id):
    task = Task.query.get(id)
    id = task.id
    user_id = user_id
    content = request.json["content"]

    task.content = content

    db.session.commit()
    return task_schema.jsonify(task)


# complete a task
@app.route("/tasks/<int:user_id>/<int:id>/complete", methods=["PUT"])
def complete_task(id, user_id):
    task = Task.query.get(id)
    id = task.id
    user_id = user_id
    completed = True
    completed = request.json["completed"]

    task.completed = completed

    db.session.commit()
    return task_schema.jsonify(task)
