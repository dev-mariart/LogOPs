from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import psycopg2
from datetime import date
from functools import wraps

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"  # Cambia esto por una clave secreta segura

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    database="logOps_db",
    user="postgres",
    password="root1603",
    host="localhost",
    port="5432"
)

# Decorador para verificar la autenticación
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
            numero_empleado = int(request.form["employee_number"])
            password = request.form["password"]

            cur = conn.cursor()
            cur.execute("SELECT numero_empleado, nombre, apellido FROM empleados WHERE numero_empleado = %s", (numero_empleado,))
            usuario = cur.fetchone()
            cur.close()

            if usuario and str(usuario[0]) == password:
                session['logged_in'] = True
                session['user_id'] = numero_empleado
                return redirect(url_for("dashboard", numero_empleado=numero_empleado))
            else:
                error = "Los datos son incorrectos. Por favor, inténtelo de nuevo."
        except ValueError:
            error = "El número de empleado debe ser un número."

    return render_template("login.html", error=error)

@app.route("/dashboard/<int:numero_empleado>")
@login_required
def dashboard(numero_empleado):
    cur = conn.cursor()
    cur.execute("SELECT nombre, apellido FROM empleados WHERE numero_empleado = %s", (numero_empleado,))
    empleado_info = cur.fetchone()
    cur.close()

    if empleado_info:
        nombre, apellido = empleado_info
        return render_template("dashboard.html", nombre=nombre, apellido=apellido, numero_empleado=numero_empleado)
    else:
        return "Error: Información del empleado no encontrada."

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/marcar/<int:numero_empleado>/<tipo_marca>", methods=["POST"])
@login_required
def marcar(numero_empleado, tipo_marca):
    try:
        # Verifica si ya existe una marca para el tipo y el empleado en el día actual
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM marcas_horario WHERE numero_empleado = %s AND tipo_marca = %s AND timestamp::date = %s",
                    (numero_empleado, tipo_marca, date.today()))
        marca_existente = cur.fetchone()[0]
        cur.close()

        if marca_existente > 0:
            mensaje_error = "Ya has marcado hoy."
            return jsonify({"error": mensaje_error}), 400

        data = request.get_json()
        fecha_hora_marca = data.get("fecha_hora_marca")
        fecha_marca = fecha_hora_marca.split()[0]
        hora_marca = fecha_hora_marca.split()[1]

        cur = conn.cursor()
        cur.execute("INSERT INTO marcas_horario (numero_empleado, tipo_marca, timestamp, hora_marca) VALUES (%s, %s, %s, %s)",
                    (numero_empleado, tipo_marca, fecha_marca, hora_marca))
        conn.commit()
        cur.close()

        mensaje_exito = "Marca registrada correctamente."
        return jsonify({"message": mensaje_exito}), 200
    except Exception as e:
        return jsonify({"error": f"Error al marcar: {str(e)}"}), 500
    

if __name__ == "__main__":
    app.run(debug=True)