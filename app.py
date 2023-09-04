#modulos que vamos a usar
from flask import Flask, flash
from flask import render_template,request,redirect,url_for,session, Response
from flask_mysqldb import MySQL,MySQLdb
from flask import send_from_directory
from datetime import datetime
import os
from empleados.empleados import empleados_blueprint
from clientes.clientes import clientes_blueprint
from proyectos.proyectos import proyectos_blueprint
from administrador.administrador import administrador_blueprint
from servicios.servicios import servicios_blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


#creamos una aplicacion
app=Flask(__name__)
app.secret_key = "VelaDanAik123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sistema'  # Reemplaza con tu contraseña si es necesaria
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.register_blueprint(empleados_blueprint, url_prefix='/empleados')
app.register_blueprint(servicios_blueprint, url_prefix='/servicios')
app.register_blueprint(clientes_blueprint, url_prefix='/clientes')
app.register_blueprint(administrador_blueprint, url_prefix='/administrador')
app.register_blueprint(proyectos_blueprint, url_prefix='/proyectos')


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistema'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
db = SQLAlchemy(app)


@app.route('/')
def inicio():
    return render_template('/index.html')

@app.route('/login')
def mostrar_login():

    return render_template('login/login.html')

@app.route('/dashboard-proyectos')
def mostrar_dashboardproyectos():

    return render_template('/Dashboard-Admin/proyectos/index.html')

@app.route('/dashboard-srv-create')
def mostrar_dashboardservicioscreate():

    return render_template('/Dashboard-Admin/servicios/create.html')

@app.route('/dashboard-proy-create')
def mostrar_dashboardproycreate():

    return render_template('/Dashboard-Admin/proyectos/create.html')

@app.route('/dashboard-admin')
def mostrar_dashboardadmin():

    return render_template('/Dashboard-Admin/admin_Dashboard.html')

@app.route('/dashboard-clie')
def mostrar_dashboardemple():

    return render_template('/Dashboard-Admin/clientes/index.html')

@app.route('/dashboard-clie-create')
def mostrar_dashboardemplecreate():

    return render_template('/Dashboard-Admin/clientes/create.html')

@app.route('/dashboard-emp')
def mostrar_dashboardemp():

    return render_template('/Dashboard-Empleado/index.html')

@app.route('/dashboard-cli')
def mostrar_dashboardcli():

    return render_template('/Dashboard-Cliente/Clie-Dashboard.html')

@app.route('/dashboard-emp-create')
def mostrar_dashboardempcreate():

    return render_template('/Dashboard-Admin/empleados/create.html')

@app.route('/admin-chat')
def mostrar_adminchat():

    return render_template('/Dashboard-Admin/chat.html')

@app.route('/admin-profile')
def mostrar_adminedit():

    return render_template('/Dashboard-Admin/administrador/edit.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('/index.html')

@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    # Consultas para obtener la cantidad de usuarios, empleados, clientes y proyectos
    consulta_usuarios = text("SELECT COUNT(*) FROM usuarios")
    resultado_usuarios = db.session.execute(consulta_usuarios)
    cantidad_usuarios = resultado_usuarios.scalar()

    consulta_empleados = text("SELECT COUNT(*) FROM empleados")
    resultado_empleados = db.session.execute(consulta_empleados)
    cantidad_empleados = resultado_empleados.scalar()

    consulta_clientes = text("SELECT COUNT(*) FROM clientes")
    resultado_clientes = db.session.execute(consulta_clientes)
    cantidad_clientes = resultado_clientes.scalar()

    consulta_proyectos = text("SELECT COUNT(*) FROM proyectos")
    resultado_proyectos = db.session.execute(consulta_proyectos)
    cantidad_proyectos = resultado_proyectos.scalar()

    if request.method == 'POST' and 'Usua_Correo' in request.form and 'Usua_Pass' in request.form:
        _correo = request.form['Usua_Correo']
        _password = request.form['Usua_Pass']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE Usua_Correo = %s AND Usua_Pass = %s', (_correo, _password,))
        account = cur.fetchone()

        if account is not None:
            session['Usua_Correo'] = _correo
            session['Usua_Pass'] = _password
            session['Usua_Nombre'] = account['Usua_Nombre']
            session['Usua_Id'] = account['Usua_Id']
            session['Usua_Foto'] = account['Usua_Foto']

        if account:
            session['logueado'] = True
            session['Usua_Id'] = account['Usua_Id']
            session['Usua_Rol'] = account['Usua_Rol']
            session['Usua_Foto'] = account['Usua_Foto']

            if session['Usua_Rol'] == 1:
                return render_template("/Dashboard-Admin/admin_Dashboard.html", cantidad_usuarios=cantidad_usuarios,
                                       cantidad_empleados=cantidad_empleados, cantidad_clientes=cantidad_clientes,
                                       cantidad_proyectos=cantidad_proyectos)
            elif session['Usua_Rol'] == 2 :
                return render_template("/Dashboard-Empleado/Emple-Dashboard.html")
            elif session['Usua_Rol'] == 3 :
                return render_template("/Dashboard-Cliente/clie-Dashboard.html")
            elif session['Usua_Rol'] == 4 :
                return render_template("/Dashboard-Empleado/Emple-Dashboard.html")
        else:
            return render_template('index.html', mensaje="Usuario O Contraseña Incorrectas")

    # Resto de la vista si no hay solicitud POST
    return render_template('/Dashboard-Empleado/Emple-Dashboard.html', cantidad_usuarios=cantidad_usuarios,
                           cantidad_empleados=cantidad_empleados, cantidad_clientes=cantidad_clientes,
                           cantidad_proyectos=cantidad_proyectos)
  
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        _correo = request.form['Usua_Correo']
        _contrasena = request.form['Usua_Pass']
        _nombre = request.form['Clie_Nombre']

        # Utiliza MySQL para conectar y ejecutar consultas
        cur = mysql.connection.cursor()

        try:
            # Inserta el usuario en la tabla de usuarios
            cur.execute("INSERT INTO usuarios (Usua_Correo, Usua_Pass, Usua_Nombre) VALUES (%s, %s, %s)", (_correo, _contrasena, _nombre))
            mysql.connection.commit()

            # Obtiene el ID del usuario recién registrado
            Usua_Id = cur.lastrowid

            # Inserta el cliente en la tabla de clientes
            cur.execute("INSERT INTO clientes (Clie_Nombre, Usua_Id) VALUES (%s, %s)", (_nombre, Usua_Id))
            mysql.connection.commit()

            cur.close()

            flash('Registro exitoso', 'success')
            return redirect(url_for('/login'))
        except Exception as e:
            # Manejar cualquier excepción que pueda ocurrir durante la inserción
            flash(f'Error: {str(e)}', 'danger')

    return render_template('login/login.html')



app.route('/proceso')
def proceso():
    
    return render_template('')


if __name__== '__main__':
    app.run(debug=True)