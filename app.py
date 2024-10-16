from flask import Flask, request, jsonify, render_template, url_for,redirect
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_seeder import FlaskSeeder
from flask_marshmallow import Marshmallow
from datetime import datetime

from hash import hash_password, get_salt, check_password

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

# seeder = FlaskSeeder()
# seeder.init_app(app, db)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    # name = db.Column(db.String(50))

    def __init__(self, username, password, salt):
        self.username = username
        self.password = password
        self.salt = salt
        # self.name = name


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "salt")

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


user_schema = UserSchema()
users_schema = UserSchema(many=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


todos = [{"task": "take out the trash", "done": False}]


######################################
############# FRONTEND ###############
######################################

# All tasks
@app.route("/")
def index():
    return render_template("tasks_all.html", todos=todos)

# Active tasks
@app.route("/active")
def active():
    return render_template("tasks_active.html", todos=todos)

# Completed tasks
@app.route("/completed")
def completed():
    return render_template("tasks_completed.html", todos=todos)

# Add task
@app.route("/add", methods=["POST"])
def add():
    task = request.form['task']
    todos.append({"task": task, "done": False})

    return redirect(url_for("index", todos=todos))

# Edit task
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    if request.method == "POST":
        todos[task_id]['task'] = request.form['updated-task']

        return redirect(url_for("index", todos=todos))

    return render_template("tasks_edit_task.html", todo=todos[task_id], id=task_id)

# Mark as completed
@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    if request.method == "POST":
        if not todos[task_id]['done']:
            todos[task_id]['done'] = True
        else:
            todos[task_id]['done'] = False

    return redirect(url_for("index", todos=todos))

# Del task
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    del todos[task_id]

    return redirect(url_for("index", todos=todos))

# Register
#TODO ADD PASSWORD HASH
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get info from form
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["password-confirmation"]
        
        # No input was provided -> Exit
        if not(username and password and confirm_password):
            return render_template("register.html", error=True, error_message="You must enter username and password")
        
        # Hash
        salt = get_salt()
        hashed_pw = hash_password(password, salt)
        hashed_confirm_pw = hash_password(confirm_password, salt)
        
        # Passwords dont match
        if not check_password(hashed_pw, hashed_confirm_pw):
            return render_template("register.html", error=True, error_message="Passwords don't match")
       
       # Successful registry
        return render_template("register.html", success=True, message="You successfuly registered!")

    return render_template("register.html", error=False)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pass
    
    return render_template("login.html")

######################################
############# DATABASE ###############
######################################

# # create a user
# @app.route("/create_user", methods=["POST"])
# def create_user():
#     username = request.json["username"]
#     password = request.json["password"]
#     name = request.json["name"]

#     user = User(username, password, name)
#     db.session.add(user)
#     db.session.commit()

#     return user_schema.jsonify(user)


# @app.route("/users", methods=["GET"])
# def get_users():
#     all_users = User.query.all()
#     result = users_schema.dump(all_users)
#     return jsonify(result)


# @app.route("/users/<int:id>", methods=["GET"])
# def get_user(id):
#     user = User.query.get(id)
#     return user_schema.jsonify(user)


# # update a user
# @app.route("/users/<int:id>", methods=["PUT"])
# def update_user(id):
#     user = User.query.get(id)
#     username = request.json["username"]
#     password = request.json["password"]
#     name = request.json["name"]

#     user.username = username
#     user.password = password
#     user.name = name

#     db.session.commit()

#     return user_schema.jsonify(user)


# @app.route("/users/<int:id>", methods=["DELETE"])
# def delete_user(id):
#     user = User.query.get(id)
#     db.session.delete(user)
#     db.session.commit()
#     return user_schema.jsonify(user)


# @app.route("/tasks")
# def get_tasks():
#     all_tasks = Task.query.all()
#     result = tasks_schema.dump(all_tasks)
#     return jsonify(result)


# # create a task
# @app.route("/create_task", methods=["POST"])
# def create_task():
#     user_id = request.json["user_id"]
#     created = datetime.now()
#     content = request.json["content"]
#     completed = request.json["completed"]

#     task = Task(user_id,
#                 created=created,
#                 content=content,
#                 completed=completed)
#     db.session.add(task)
#     db.session.commit()

#     return task_schema.jsonify(task)


# # get all tasks for a user
# @app.route("/tasks/<int:user_id>", methods=["GET"])
# def get_user_tasks(user_id):
#     tasks = Task.query.filter_by(user_id=user_id).all()
#     result = tasks_schema.dump(tasks)
#     return jsonify(result)


# # update a task
# @app.route("/tasks/<int:user_id>/<int:id>", methods=["PUT"])
# def update_task(id, user_id):
#     task = Task.query.get(id)
#     id = task.id
#     user_id = user_id
#     content = request.json["content"]

#     task.content = content

#     db.session.commit()
#     return task_schema.jsonify(task)


# # complete a task
# @app.route("/tasks/<int:user_id>/<int:id>/complete", methods=["PUT"])
# def complete_task(id, user_id):
#     task = Task.query.get(id)
#     id = task.id
#     user_id = user_id
#     completed = True
#     completed = request.json["completed"]

#     task.completed = completed

#     db.session.commit()
#     return task_schema.jsonify(task)


if __name__ == "__main__":
    app.run(debug=True)

