from flask import render_template, redirect, request, url_for

from todo.helpers.hash.hash import get_salt, hash_password, check_password

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