from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

todos = [{"task": "take out the trash", "done": False}]

@app.route("/")
def index():
    return render_template("all.html", todos=todos)

# TODO
@app.route("/active")
def active():
    return render_template("active.html", todos=todos)

# TODO
@app.route("/completed")
def completed():
    return render_template("completed.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    task = request.form['task']
    todos.append({"task": task, "done": False})

    return redirect(url_for("index", todos=todos))

@app.route("/edit")
def edit():
    pass

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    if request.method == "POST":
        if not todos[task_id]['done']:
            todos[task_id]['done'] = True
        else:
            todos[task_id]['done'] = False

    return redirect(url_for("index", todos=todos))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    del todos[task_id]

    return redirect(url_for("index", todos=todos))


if __name__ == "__main__":
    app.run(debug=True)

