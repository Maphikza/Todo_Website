from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
import uuid

db = SQLAlchemy()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY_APP")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


class Todos(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    todo_item = db.Column(db.String(250), nullable=False)
    item_id = db.Column(db.String(250), nullable=True, unique=True)


with app.app_context():
    db.create_all()

year = datetime.now().year
month = datetime.now().month
day = datetime.now().day


@app.route('/', methods=["GET", "POST"])
def home():
    todo_list = db.session.query(Todos.todo_item, Todos.item_id, Todos.id).all()
    return render_template("index.html", year=year, month=month, day=day, todo_list=todo_list)


@app.route('/add', methods=["GET", "POST"])
def add_todo():
    if request.method == "POST":
        todo = request.form.get("todo")
        unique_id = uuid.uuid1()
        new_todo = Todos(todo_item=todo, item_id=str(unique_id))
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/delete/<todo_id>")
def delete_todo(todo_id):

    todo_item_to_delete = Todos.query.get(todo_id)
    db.session.delete(todo_item_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
