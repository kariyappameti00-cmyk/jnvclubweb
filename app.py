from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)


# ==============================
# DATABASE CONNECTION
# ==============================

def get_db_connection():
    conn = sqlite3.connect("database.db")

    # Allows us to access columns by name
    conn.row_factory = sqlite3.Row

    return conn


# ==============================
# CREATE DATABASE
# ==============================

def create_database():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            college TEXT NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            state TEXT NOT NULL,
            activities TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    conn.close()


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():

    return render_template("project.html")


# ==============================
# REGISTRATION PAGE
# ==============================

@app.route("/registration")
def registration():

    return render_template("registration.html")


# ==============================
# SAVE REGISTRATION
# ==============================

@app.route("/register", methods=["POST"])
def register():

    # Get data from form

    name = request.form["name"]

    email = request.form["email"]

    phone = request.form["phone"]

    college = request.form["college"]

    department = request.form["department"]

    year = request.form["year"]

    state = request.form["state"]

    # Multiple checkbox values

    activities = request.form.getlist("activities")

    # Convert list into a single string

    activities_string = ", ".join(activities)


    # Connect database

    conn = get_db_connection()

    cursor = conn.cursor()


    # Insert student information

    cursor.execute("""
        INSERT INTO students
        (
            name,
            email,
            phone,
            college,
            department,
            year,
            state,
            activities
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        college,
        department,
        year,
        state,
        activities_string
    ))


    conn.commit()

    conn.close()


    # Show successful message

    return render_template(
        "registration.html",
        message="Registration successful! Your details have been saved."
    )


# ==============================
# VIEW REGISTERED STUDENTS
# ==============================

@app.route("/students")
def students():

    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students
    )


# ==============================
# START SERVER
# ==============================

if __name__ == "__main__":

    create_database()

    app.run(debug=True)