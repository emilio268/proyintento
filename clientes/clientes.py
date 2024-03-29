from flask import Blueprint, render_template, request, redirect, send_from_directory, current_app
from flaskext.mysql import MySQL  # O desde 'your_app import mysql', según tu configuración
import os
from datetime import datetime
#modulos que vamos a usar
from flask import Flask
from flask import render_template,request,redirect,url_for
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os

app=Flask(__name__)

mysql= MySQL()

clientes_blueprint = Blueprint('clientes', __name__)

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PORT']=3306
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
#hacemos que mysql inicie la conexion
mysql.init_app(app)


@clientes_blueprint.record_once
def on_load(state):
    global CARPETA
    CARPETA = os.path.join('uploads')
    state.app.config['CARPETA'] = CARPETA

@clientes_blueprint.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    carpeta = current_app.config['CARPETA']
    return send_from_directory(current_app.config['CARPETA'], nombreFoto)
@clientes_blueprint.route('/vista', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rol = request.form.get('rol')
    else:
        rol = request.args.get('rol', 'todos')

    singular_to_plural = {
        'cliente': 'clientes',
        'empleado': 'empleados',
        'administrador': 'administrador'
    }

    campos = {
        'clientes': ['Clie_Id', 'Clie_Nombre', 'Clie_Correo', 'Clie_Foto'],
        'empleados': ['Emp_Id', 'Emp_Nombre', 'Emp_Correo', 'Emp_Foto'],
        'administrador': ['Admin_Id', 'Admin_Nombre', 'Admin_Correo', 'Admin_Foto']
    }

    if rol == 'todos':
        # Combina los resultados de las tres tablas usando UNION
        sql = f"SELECT 'Cliente' AS Rol, {', '.join(campos['clientes'])} FROM clientes " \
              f"UNION ALL " \
              f"SELECT 'Empleado' AS Rol, {', '.join(campos['empleados'])} FROM empleados " \
              f"UNION ALL " \
              f"SELECT 'Administrador' AS Rol, {', '.join(campos['administrador'])} FROM administrador;"
    else:
        if rol in campos:
            sql = f"SELECT '{rol.capitalize()}' AS Rol, {', '.join(campos[rol])} FROM {rol};"
        else:
            return redirect('/clientes/vista')
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    clientes = cursor.fetchall()
    conn.commit()

    return render_template('/Dashboard-Admin/clientes/index.html', clientes=clientes, selected_rol=rol)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    clientes = cursor.fetchall()
    conn.commit()

    return render_template('/Dashboard-Admin/clientes/index.html', clientes=clientes, selected_rol=rol)

@clientes_blueprint.route('/destroy/<int:Clie_Id>')
def destroy(Clie_Id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT Clie_Foto FROM clientes WHERE Clie_Id=%s", Clie_Id)
    fila = cursor.fetchall()

    os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM clientes WHERE Clie_Id=%s", (Clie_Id))
    conn.commit()
    return redirect('/clientes/vista')

@clientes_blueprint.route('/edit/<int:Clie_Id>')
def edit(Clie_Id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE Clie_Id=%s", (Clie_Id))
    clientes = cursor.fetchall()
    conn.commit()

    return render_template('/Dashboard-Admin/clientes/edit.html', clientes=clientes)

@clientes_blueprint.route('/update', methods=['POST'])
def update():
    _Clie_Nombre = request.form['CNombre']
    _Clie_Correo = request.form['CCorreo']
    _Clie_Telefono = request.form['CTelefono']  # Nuevo campo
    _Clie_Direccion = request.form['CDireccion']  # Nuevo campo
    _Clie_Foto = request.files['CFoto']
    _Clie_Id = request.form['CID']

    # Actualiza la sentencia SQL para incluir los nuevos campos
    sql = "UPDATE `clientes` SET Clie_Nombre=%s, Clie_Correo=%s, Clie_Telefono=%s, Clie_Direccion=%s WHERE Clie_Id=%s;"
    datos = (_Clie_Nombre, _Clie_Correo, _Clie_Telefono, _Clie_Direccion, _Clie_Id)


    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _Clie_Foto.filename != '':
        nuevoNombreFoto = tiempo + _Clie_Foto.filename
        _Clie_Foto.save("uploads/" + nuevoNombreFoto)

        cursor.execute("SELECT Clie_Foto FROM clientes WHERE Clie_Id=%s", _Clie_Id)
        fila = cursor.fetchall()

        os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE clientes SET Clie_Foto=%s WHERE Clie_Id=%s", (nuevoNombreFoto, _Clie_Id))
        conn.commit()

    cursor.execute(sql, datos)
    conn.commit()
    

    return redirect('/clientes/vista')

@clientes_blueprint.route('/create')
def create():
    return render_template('/Dashboard-Admin/clientes/create.html')

@clientes_blueprint.route('/store', methods=['POST'])
def storage():
    _Clie_Nombre = request.form['CNombre']
    _Clie_Correo = request.form['CCorreo']
    _Clie_Foto = request.files['CFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _Clie_Foto.filename != '':
        nuevoNombreFoto = tiempo + _Clie_Foto.filename
        _Clie_Foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO `clientes` (`Clie_Id`, `Clie_nombre`, `Clie_Correo`, `Clie_Foto`) VALUES (NULL, %s, %s, %s);"

    datos = (_Clie_Nombre, _Clie_Correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/clientes/vista')
