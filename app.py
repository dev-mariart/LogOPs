from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import psycopg2
from datetime import date
from functools import wraps

app = Flask(__name__)
app.secret_key = "your_secret_key" 


conn = psycopg2.connect(
    database="logOps_db",
    user="postgres",
    password="root1603",
    host="localhost",
    port="5432"
)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        try:
            employee_number = int(request.form["employee_number"])
            password = request.form["password"]

            cur = conn.cursor()
            cur.execute("SELECT employee_number, name, last_name FROM employees WHERE employee_number = %s", (employee_number,))
            user = cur.fetchone()
            cur.close()

            if user and str(user[0]) == password:
                session['logged_in'] = True
                session['user_id'] = employee_number
                return redirect(url_for("dashboard", employee_number=employee_number))
            else:
                error = "Incorrect credentials. Please try again."
        except ValueError:
            error = "Employee number should be a number."

    return render_template("login.html", error=error)

@app.route("/dashboard/<int:employee_number>")
@login_required
def dashboard(employee_number):
    cur = conn.cursor()
    cur.execute("SELECT name, last_name FROM employees WHERE employee_number = %s", (employee_number,))
    employee_info = cur.fetchone()
    cur.close()

    if employee_info:
        name, last_name = employee_info
        return render_template("dashboard.html", name=name, last_name=last_name, employee_number=employee_number)
    else:
        return "Error: Employee information not found."

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/mark/<int:employee_number>/<mark_type>", methods=["POST"])
@login_required
def mark(employee_number, mark_type):
    try:
        
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM time_marks WHERE employee_number = %s AND mark_type = %s AND timestamp::date = %s",
                    (employee_number, mark_type, date.today()))
        existing_mark = cur.fetchone()[0]
        cur.close()

        if existing_mark > 0:
            error_message = "You have already marked today."
            return jsonify({"error": error_message}), 400

        data = request.get_json()
        mark_datetime = data.get("mark_datetime")
        mark_date = mark_datetime.split()[0]
        mark_time = mark_datetime.split()[1]

        cur = conn.cursor()
        cur.execute("INSERT INTO time_marks (employee_number, mark_type, timestamp, mark_time) VALUES (%s, %s, %s, %s)",
                    (employee_number, mark_type, mark_date, mark_time))
        conn.commit()
        cur.close()

        success_message = "Mark registered successfully."
        return jsonify({"message": success_message}), 200
    except Exception as e:
        return jsonify({"error": f"Error while marking: {str(e)}"}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
