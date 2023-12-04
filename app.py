#modulos que vamos a usar
from flask import Flask, flash
from flask import render_template,request,redirect,url_for,session, Response
from flask_mysqldb import MySQL,MySQLdb
from flask import send_from_directory
from datetime import datetime
import os
from login.login import login_blueprint
from empleados.empleados import empleados_blueprint
from clientes.clientes import clientes_blueprint
from proyectos.proyectos import proyectos_blueprint
from administrador.administrador import administrador_blueprint
from servicios.servicios import servicios_blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import Flask, session, render_template, request, redirect, url_for
from flaskext.mysql import MySQL
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash


#creamos una aplicacion
app=Flask(__name__)
app.secret_key = "VelaDanAik123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sistema'  # Reemplaza con tu contraseña si es necesaria
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.register_blueprint(empleados_blueprint, url_prefix='/empleados')
app.register_blueprint(login_blueprint)
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

@app.route('/add', methods=['POST'])
def add_service_to_cart():
    cursor = None
    conn = None  # inicializa también 'conn'
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['Serv_ID']
        # validar los valores recibidos
        if _quantity and _code and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM servicios WHERE Serv_ID=%s", _code)
            row = cursor.fetchone()

            itemArray = {row['Serv_ID']: {'Serv_Nombre': row['Serv_Nombre'], 'Serv_ID': row['Serv_ID'],
                                          'quantity': _quantity, 'Serv_Precio': row['Serv_Precio'],
                                          'Serv_Foto': row['Serv_Foto'], 'total_price': _quantity * row['Serv_Precio']}}

            all_total_price = 0
            all_total_quantity = 0

            session.modified = True
            if 'cart_item' in session:
                if row['Serv_ID'] in session['cart_item']:
                    for key, value in session['cart_item'].items():
                        if row['Serv_ID'] == key:
                            old_quantity = session['cart_item'][key]['quantity']
                            total_quantity = old_quantity + _quantity
                            session['cart_item'][key]['quantity'] = total_quantity
                            session['cart_item'][key]['total_price'] = total_quantity * row['Serv_Precio']
                else:
                    session['cart_item'] = array_merge(session['cart_item'], itemArray)

                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + _quantity * row['Serv_Precio']

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

            return redirect(url_for('products'))
        else:
            return 'Error al agregar el artículo al carrito'
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

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

@app.route('/products')
def mostrar_servicios1():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM servicios")
        rows = cursor.fetchall()
        return render_template('products.html', services=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/products')
def mostrar_servicios():

    return render_template('/products.html')

@app.route('/dashboard-admin')
def mostrar_dashboardadmin():
    # Realiza consultas para obtener las cantidades utilizando SQLAlchemy
    cantidad_clientes = db.session.query(db.func.count()).select_from(db.table('clientes')).scalar()
    cantidad_empleados = db.session.query(db.func.count()).select_from(db.table('empleados')).scalar()
    cantidad_proyectos = db.session.query(db.func.count()).select_from(db.table('proyectos')).scalar()
    cantidad_usuarios = cantidad_clientes + cantidad_empleados  # Calcula la cantidad total de usuarios

    # Establece estas cantidades en la sesión para usarlas en la plantilla HTML
    session['cantidad_empleados'] = cantidad_empleados
    session['cantidad_clientes'] = cantidad_clientes
    session['cantidad_proyectos'] = cantidad_proyectos
    session['cantidad_usuarios'] = cantidad_usuarios

    return render_template('/Dashboard-Admin/admin_Dashboard.html', cantidad_empleados=cantidad_empleados, cantidad_clientes=cantidad_clientes, cantidad_proyectos=cantidad_proyectos, cantidad_usuarios=cantidad_usuarios)
 
@app.route('/dashboard-clie')
def mostrar_dashboardclie():

    return render_template('/Dashboard-Admin/clientes/index.html')

@app.route('/dashboard-clie-create')
def mostrar_dashboardemplecreate():

    return render_template('/Dashboard-Admin/clientes/create.html')

@app.route('/dashboard-emp')
def mostrar_dashboardemp():

    return render_template('/Dashboard-Empleado/Emple-Dashboard.html')

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

app.route('/proceso')
def proceso():
    
    return render_template('')


if __name__== '__main__':
    app.run(debug=True)

    