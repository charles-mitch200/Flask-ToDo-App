from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "b'\x1b\xd7K\x1b\xa8\x86\xdd\x9f\xb7\xcc\x98\xfe'"
db = SQLAlchemy(app)

app.app_context().push()

# Create Models
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160))
    complete = db.Column(db.Boolean, default=False)

# Render items in the database on the page
@app.route("/")
def home_page():
    # Grab everything from the table and add it to the todo_list
    todo_list = Todo.query.all()
    # Update the statistics dynamically
    total_todo = Todo.query.count()
    completed_todos = Todo.query.filter_by(complete=True).count()
    pending_todos = Todo.query.filter_by(complete=False).count()
    return render_template('dashboard/home.html', **locals())

# Add new todo to the database(Create)
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    # create a new todo
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home_page"))

# Removing a todo from the database (delete)
@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home_page"))

# Updating a todo
@app.route("/update/<int:id>")
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home_page"))

@app.route("/about")
def about_page():
    return render_template("dashboard/about.html")

# If this is the main app, run it
if __name__ == "__main__":
    app.run(debug=True)