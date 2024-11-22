from app import db, ma

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


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "salt")

class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "created", "content", "completed")