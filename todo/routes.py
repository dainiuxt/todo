from flask import render_template, redirect, request, url_for, flash

# Used for hashing passwords and checking if correct
from todo.helpers.hash.hash import get_salt, hash_password, check_password

# Render forms quickly and get additional validation from wtforms
from .forms import RegisterForm, LoginForm

todos = [{"task": "take out the trash", "done": False}]

def register_routes(app, db):
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
    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegisterForm()

        # Means that request was POST and form is valid
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # Hash to protect password
            # Salt so figuring out hash function is harder
            hashed_pw = hash_password(password, get_salt())

            # check if user doesnt already exist

            # Successful registry
            flash("You successfuly registered!")
            return render_template("register.html", form=form)

        return render_template("register.html", error=False, form=form)

    # Login
    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()

        # Means that request was POST and form is valid
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # check if correct password and user exists

            # Successful login
            return redirect(url_for('index'))
        
        return render_template("login.html", form=form)