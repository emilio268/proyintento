from flask import Flask, flash, Blueprint, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

# Crear una instancia de Flask
app = Flask(__name__)
app.secret_key = "VelaDanAik123"

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sistema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql = MySQL(app)
db = SQLAlchemy(app)

# Blueprint para el login
login_blueprint = Blueprint('login', __name__)

# ...

@login_blueprint.route('/acceso-login', methods=["GET", "POST"])
def login():
    _correo = None
    if request.method == 'POST' and 'Usua_Correo' in request.form and 'Usua_Pass' in request.form:
        _correo = request.form['Usua_Correo']
        _password = request.form['Usua_Pass']

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE Usua_Correo = %s', (_correo,))
    account = cur.fetchone()

    if account:
        if check_password_hash(account['Usua_Pass'], _password):
            session['Usua_Correo'] = _correo
            session['Usua_Nombre'] = account['Usua_Nombre']
            session['Usua_Id'] = account['Usua_Id']
            session['Usua_Foto'] = account['Usua_Foto']
            session['logueado'] = True

        if account['Usua_Rol'] == 1:
            return render_template("/Dashboard-Admin/admin_Dashboard.html")
        elif account['Usua_Rol'] == 2:
            return render_template("/Dashboard-Empleado/Emple-Dashboard.html")
        elif account['Usua_Rol'] == 3:
            return render_template("/Dashboard-Cliente/clie-Dashboard.html")
        elif account['Usua_Rol'] == 4:
            return render_template("/Dashboard-Empleado/Emple-Dashboard.html")
        else:
            print("Contraseña incorrecta")
    else:
        print("Usuario no encontrado")

    flash('Usuario o Contraseña Incorrectos', 'danger')
    return render_template('/login/login.html')


@login_blueprint.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        _correo = request.form['Usua_Correo']
        _contrasena = request.form['Usua_Pass']
        _nombre = request.form['Clie_Nombre']

        cur = mysql.connection.cursor()

        try:
            # Genera un hash seguro de la contraseña
            hashed_password = generate_password_hash(_contrasena).decode('utf-8')

            if _contrasena != request.form['confirm_Pass']:
                flash('Las contraseñas no coinciden', 'danger')
                return redirect(url_for('login.registro'))

            # Insertar en la tabla usuarios
            cur.execute("INSERT INTO usuarios (Usua_Correo, Usua_Pass, Usua_Nombre) VALUES (%s, %s, %s)",
                        (_correo, hashed_password, _nombre))
            mysql.connection.commit()

            Usua_Id = cur.lastrowid

            # Insertar en la tabla clientes y establecer Clie_Correo
            cur.execute("INSERT INTO clientes (Clie_Nombre, Usua_Id, Clie_Correo) VALUES (%s, %s, %s)",
                        (_nombre, Usua_Id, _correo))
            mysql.connection.commit()

            cur.close()

            # Establecer la sesión como autenticada
            session['Usua_Correo'] = _correo
            session['logueado'] = True

            flash('Registro exitoso', 'success')

            # Redirigir al usuario según su rol después del registro
            cur.execute('SELECT Usua_Rol FROM usuarios WHERE Usua_Correo = %s', (_correo,))
            account = cur.fetchone()
            if account:
                if account['Usua_Rol'] == 'administrador':
                    return render_template("/Dashboard-Admin/admin_Dashboard.html")
                elif account['Usua_Rol'] == 'empleado':
                    return render_template("/Dashboard-Empleado/Emple-Dashboard.html")
                elif account['Usua_Rol'] == 'cliente':
                    return render_template("/Dashboard-Cliente/clie-Dashboard.html")
                elif account['Usua_Rol'] == 'empleado-rol':
                    return render_template("/Dashboard-Empleado/Emple-Dashboard.html")

        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    return render_template('login/login.html')

@app.route('/proceso')
def proceso():
    return render_template('')

if __name__ == '__main__':
    app.run(debug=True)
