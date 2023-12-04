from flask import Blueprint, render_template, request, redirect, send_from_directory, current_app, flash
from flaskext.mysql import MySQL
import os
from datetime import datetime
from flask import Flask
from flask import render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = MySQL()

empleados_blueprint = Blueprint('empleados', __name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema'

mysql.init_app(app)

@empleados_blueprint.record_once
def on_load(state):
    global CARPETA
    CARPETA = os.path.join('uploads')
    state.app.config['CARPETA'] = CARPETA

@empleados_blueprint.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    carpeta = current_app.config['CARPETA']
    return send_from_directory(current_app.config['CARPETA'], nombreFoto)

def generate_hashed_password(raw_password):
    return bcrypt.generate_password_hash(raw_password).decode('utf-8')

def register_user(Usua_Correo, Usua_Pass, Usua_Nombre, Usua_Rol=2):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "INSERT INTO `usuarios` (`Usua_Nombre`, `Usua_Pass`, `Usua_Correo`, `Usua_Rol`) VALUES (%s, %s, %s, %s);"
    hashed_password = generate_hashed_password(Usua_Pass)
    data = (Usua_Nombre, hashed_password, Usua_Correo, Usua_Rol)

    cursor.execute(sql, data)
    conn.commit()

    conn.close()

@empleados_blueprint.route('/vista')
def index():
    sql = "SELECT * FROM empleados;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()
    conn.commit()

    return render_template('/Dashboard-Admin/empleados/index.html', empleados=empleados)


@empleados_blueprint.route('/destroy/<string:Emp_Id>')
def destroy(Emp_Id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT Emp_Foto FROM empleados WHERE Emp_Id=%s", Emp_Id)
    fila = cursor.fetchall()

    os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM empleados WHERE Emp_Id=%s", (Emp_Id,))
    conn.commit()
    return redirect('/empleados/vista')

@empleados_blueprint.route('/edit/<string:Emp_Id>')
def edit(Emp_Id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE Emp_Id=%s", (Emp_Id,))
    empleados = cursor.fetchall()
    conn.commit()

    print("Empleados:", empleados)  

    return render_template('/Dashboard-Admin/empleados/edit.html', empleados=empleados)

@empleados_blueprint.route('/update', methods=['POST'])
def update():

    _Emp_Id = request.form['EDocumento']
    _Emp_Nombre = request.form['ENombre']
    _Emp_Apellido = request.form['EApellido']
    _Emp_TipoDoc = request.form['ETipoDoc']
    _Emp_Correo = request.form['ECorreo']
    _Emp_Sexo = request.form['ESexo']
    _Emp_FechaNac = request.form['EFechaNac']
    _Emp_Telefono = request.form['ETelefono']
    _Emp_Direccion = request.form['EDireccion']
    _Emp_Estado = request.form['EEstado']
    _Emp_Foto = request.files['foto']

    sql = "UPDATE `empleados` SET Emp_Nombre=%s, Emp_Apellido=%s, Emp_TipoDoc=%s, Emp_Correo=%s, Emp_Sexo=%s, Emp_FechaNac=%s, Emp_Telefono=%s, Emp_Direccion=%s, Emp_Estado=%s WHERE Emp_Id=%s;"
    datos = (_Emp_Nombre, _Emp_Apellido, _Emp_TipoDoc, _Emp_Correo, _Emp_Sexo, _Emp_FechaNac, _Emp_Telefono, _Emp_Direccion, _Emp_Estado, _Emp_Id)

    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _Emp_Foto.filename != '':
        nuevoNombreFoto = tiempo + _Emp_Foto.filename
        _Emp_Foto.save("uploads/" + nuevoNombreFoto)

        cursor.execute("SELECT Emp_Foto FROM empleados WHERE Emp_Id=%s", _Emp_Id)
        fila = cursor.fetchall()

        os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE empleados SET Emp_Foto=%s WHERE Emp_Id=%s", (nuevoNombreFoto, _Emp_Id))
        conn.commit()

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/empleados/vista')

@empleados_blueprint.route('/create')
def create():
    return render_template('/Dashboard-Admin/empleados/create.html')

@empleados_blueprint.route('/store', methods=['POST'])
def storage():
    _Emp_Id = request.form['EDocumento']
    _Emp_Nombre = request.form['ENombre']
    _Emp_Apellido = request.form['EApellido']
    _Emp_TipoDoc = request.form['ETipoDoc']
    _Emp_Correo = request.form['ECorreo']
    _Emp_Sexo = request.form['ESexo']
    _Emp_FechaNac = request.form['EFechaNac']
    _Emp_Telefono = request.form['ETelefono']
    _Emp_Direccion = request.form['EDireccion']
    _Emp_Estado = request.form['EEstado']
    _Emp_Foto = request.files['foto']

    sql = "INSERT INTO `empleados` (`Emp_Id`, `Emp_Nombre`, `Emp_Apellido`, `Emp_TipoDoc`, `Emp_Correo`, `Emp_Sexo`, `Emp_FechaNac`, `Emp_Telefono`, `Emp_Direccion`, `Emp_Estado`, `Emp_Foto`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    datos = (_Emp_Id, _Emp_Nombre, _Emp_Apellido, _Emp_TipoDoc, _Emp_Correo, _Emp_Sexo, _Emp_FechaNac, _Emp_Telefono, _Emp_Direccion, _Emp_Estado, _Emp_Foto.filename)

    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _Emp_Foto.filename != '':
        nuevoNombreFoto = tiempo + _Emp_Foto.filename
        _Emp_Foto.save("uploads/" + nuevoNombreFoto)

        cursor.execute("UPDATE empleados SET Emp_Foto=%s WHERE Emp_Id=%s", (nuevoNombreFoto, _Emp_Id))

    cursor.execute(sql, datos)
    conn.commit()

    # Registra al usuario
    register_user(_Emp_Correo, _Emp_Id, _Emp_Nombre)  # Correo como nombre de usuario, ID como contraseña

    conn.close()

    return redirect('/empleados/vista')