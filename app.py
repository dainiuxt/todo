from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

todos = [{"task": "take out the trash", "done": False}]

@app.route("/")
def index():
    return render_template("layout.html", todos=todos)


# Do form input
@app.route("/add", methods=["POST"])
def add():
    task = request.form['task']
    todos.append({"task": task, "done": False})
    return redirect(url_for("index", todos=todos))

@app.route("/edit")
def edit():
    pass

@app.route("/complete")
def complete():
    pass

@app.route("/delete")
def delete():
    pass

if __name__ == "__main__":
    app.run(debug=True)