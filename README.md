# LogOps - Employee Time Tracking System

![Login Page](screenshot/Captura%201.png)

## Description
This project is an employee time tracking system that allows users to log in, view their dashboard, and mark their schedule.

## Prerequisites
- Installed Python 3.x
- Installed and configured PostgreSQL

## Database Configuration

### Creating the database
1. Log in to PostgreSQL: `psql -U your_username -d postgres`
2. Create a new database by executing the SQL command:
    ```sql
    CREATE DATABASE your_database_name;
    ```

### Creating the necessary tables
Run the following SQL commands to create the required tables:

#### 'empleados' Table
```sql
CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    numero_empleado INT UNIQUE
);
 ```

#### 'marcas_horario' Table
```sql
CREATE TABLE marcas_horario (
    id SERIAL PRIMARY KEY,
    numero_empleado INT,
    tipo_marca VARCHAR(50),
    timestamp DATE,
    hora_marca TIME,
    FOREIGN KEY (numero_empleado) REFERENCES empleados(numero_empleado)
);
 ```

## Application Setup

### Steps to configure the application
1. Clone the repository: git clone repository_URL
2. Install dependencies: pip install -r requirements.txt
3. Modify the app.py file:
   - Replace "REPLACE_WITH_SECURE_SECRET_KEY" with your secure secret key.
   - Replace "REPLACE_WITH_DATABASE_NAME", "REPLACE_WITH_USERNAME", "REPLACE_WITH_PASSWORD", "REPLACE_WITH_HOST", and "REPLACE_WITH_PORT" with your PostgreSQL database details.

### Running the application
1. Run the following command: python app.py
2. Access the application in your web browser: http://localhost:5000/

![Login Page](screenshot/gif.gif)

### Folder Structure
- app.py: Main file with Flask application logic.
- login.html: HTML template for the login page.
- dashboard.html: HTML template for the employee dashboard.
- script.js: JavaScript file with client-side interactions.
- styles.css: CSS file for custom styles.

### Credits
This project was developed by [https://github.com/dev-mariart].
