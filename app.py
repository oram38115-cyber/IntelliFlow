import os
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY is missing. Check your .env file.")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///intelliflow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# User database model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


# Task database model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(30), default="Pending")
    priority = db.Column(db.String(20), default="Medium")
    due_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Automatic task priority
def assign_priority(title, description, due_date=None):
    text = (title + " " + description).lower()

    # Deadline-based priority
    if due_date:
        days_left = (due_date - date.today()).days

        if days_left <= 1:
            return "High"
        elif days_left <= 3:
            return "Medium"

    # Keyword-based priority
    high_words = [
        "urgent", "exam", "deadline", "submission",
        "today", "immediately", "important"
    ]

    medium_words = [
        "project", "assignment", "meeting",
        "report", "presentation", "prepare"
    ]

    if any(word in text for word in high_words):
        return "High"

    if any(word in text for word in medium_words):
        return "Medium"

    return "Low"


# Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.")
        elif len(password) < 8:
            flash("Password must contain at least 8 characters.")
        elif User.query.filter_by(email=email).first():
            flash("This email is already registered.")
        else:
            user = User(
                name=name,
                email=email,
                password=generate_password_hash(password)
            )

            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash("Account created successfully!")
            return redirect(url_for("index"))

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))

        flash("Invalid email or password.")

    return render_template("login.html")


# Logout
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))



# Dashboard
@app.route("/")
@login_required
def index():
    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).order_by(Task.id.desc()).all()

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks if task.status == "Completed"
    )

    pending_tasks = total_tasks - completed_tasks

    # Calculate productivity percentage
    if total_tasks > 0:
        productivity = round(
            (completed_tasks / total_tasks) * 100
        )
    else:
        productivity = 0

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        today=date.today(),
        productivity=productivity
    )


# Add task
@app.route("/add", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    due_date_text = request.form.get("due_date", "").strip()

    if not title:
        flash("Please enter a task title.")
        return redirect(url_for("index"))

    due_date = None

    if due_date_text:
        try:
            due_date = datetime.strptime(
                due_date_text, "%Y-%m-%d"
            ).date()
        except ValueError:
            flash("Please enter a valid deadline.")
            return redirect(url_for("index"))

    task = Task(
        title=title,
        description=description,
        due_date=due_date,
        priority=assign_priority(title, description, due_date),
        user_id=current_user.id
    )

    db.session.add(task)
    db.session.commit()

    flash("Task added successfully!")
    return redirect(url_for("index"))


# Complete task
@app.route("/complete/<int:task_id>")
@login_required
def complete_task(task_id):
    task = db.get_or_404(Task, task_id)

    if task.user_id != current_user.id:
        return redirect(url_for("index"))

    task.status = "Completed"
    db.session.commit()

    return redirect(url_for("index"))


# Edit task
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)

    if task.user_id != current_user.id:
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        due_date_text = request.form.get("due_date", "").strip()

        if not title:
            flash("Task title cannot be empty.")
            return redirect(url_for("edit_task", task_id=task.id))

        due_date = None

        if due_date_text:
            try:
                due_date = datetime.strptime(
                    due_date_text, "%Y-%m-%d"
                ).date()
            except ValueError:
                flash("Please enter a valid deadline.")
                return redirect(url_for("edit_task", task_id=task.id))

        task.title = title
        task.description = description
        task.due_date = due_date
        task.priority = assign_priority(
            title, description, due_date
        )

        db.session.commit()

        flash("Task updated successfully!")
        return redirect(url_for("index"))

    return render_template("edit_task.html", task=task)

# Delete task
@app.route("/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)

    if task.user_id != current_user.id:
        return redirect(url_for("index"))

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("index"))


# Create and update database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        with db.engine.begin() as connection:
            columns = connection.exec_driver_sql(
                "PRAGMA table_info(task)"
            ).fetchall()

            column_names = [column[1] for column in columns]

            if "priority" not in column_names:
                connection.exec_driver_sql(
                    "ALTER TABLE task ADD COLUMN priority "
                    "VARCHAR(20) DEFAULT 'Medium'"
                )

            if "user_id" not in column_names:
                connection.exec_driver_sql(
                    "ALTER TABLE task ADD COLUMN user_id INTEGER"
                )

            if "due_date" not in column_names:
                connection.exec_driver_sql(
                    "ALTER TABLE task ADD COLUMN due_date DATE"
                )

    app.run(debug=True)
