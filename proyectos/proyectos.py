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

proyectos_blueprint = Blueprint('proyectos', __name__)

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PORT']=3306
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
#hacemos que mysql inicie la conexion
mysql.init_app(app)


@proyectos_blueprint.record_once
def on_load(state):
    global CARPETA
    CARPETA = os.path.join('uploads')
    state.app.config['CARPETA'] = CARPETA


@proyectos_blueprint.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    carpeta = current_app.config['CARPETA']
    return send_from_directory(current_app.config['CARPETA'], nombreFoto)

@proyectos_blueprint.route('/vista')
def index():
    sql = "SELECT * FROM proyectos;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    proyectos = cursor.fetchall()
    conn.commit()

    return render_template('Dashboard-Admin/proyectos/index.html', proyectos=proyectos)

@proyectos_blueprint.route('/destroy/<int:Proy_Id>')
def destroy(Proy_Id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT Proy_Foto FROM proyectos WHERE Proy_Id=%s", Proy_Id)
    fila = cursor.fetchall()

    os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM proyectos WHERE Proy_Id=%s", (Proy_Id))
    conn.commit()
    return redirect('/proyectos/vista')

@proyectos_blueprint.route('/edit/<int:Proy_Id>')
def edit(Proy_Id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proyectos WHERE Proy_Id=%s", (Proy_Id))
    proyectos = cursor.fetchall()
    conn.commit()

    return render_template('Dashboard-Admin/proyectos/edit.html', proyectos=proyectos)

@proyectos_blueprint.route('/update', methods=['POST'])
def update():
    _Proy_Nombre = request.form['PNombre']
    _Proy_Desc = request.form['PCorreo']
    _Proy_Foto = request.files['PFoto']
    _Proy_Id = request.form['PID']

    sql = "UPDATE `proyectos` SET Proy_Nombre=%s, Proy_Desc=%s WHERE Proy_Id=%s;"
    datos = (_Proy_Nombre, _Proy_Desc, _Proy_Id)

    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _Proy_Foto.filename != '':
        nuevoNombreFoto = tiempo + _Proy_Foto.filename
        _Proy_Foto.save("uploads/" + nuevoNombreFoto)

        cursor.execute("SELECT Proy_Foto FROM proyectos WHERE Proy_Id=%s", _Proy_Id)
        fila = cursor.fetchall()

        os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE proyectos SET Proy_Foto=%s WHERE Proy_Id=%s", (nuevoNombreFoto, _Proy_Id))
        conn.commit()

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/proyectos/vista')

@proyectos_blueprint.route('/create')
def create():
    return render_template('Dashboard-Admin/proyectos/create.html')

@proyectos_blueprint.route('/store', methods=['POST'])
def storage():
    _Proy_Nombre = request.form['PNombre']
    _Proy_Correo = request.form['PCorreo']
    _Proy_Foto = request.files['PFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _Proy_Foto.filename != '':
        nuevoNombreFoto = tiempo + _Proy_Foto.filename
        _Proy_Foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO `proyectos` (`Proy_Id`, `Proy_nombre`, `Proy_Desc`, `Proy_Foto`) VALUES (NULL, %s, %s, %s);"

    datos = (_Proy_Nombre, _Proy_Correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/proyectos/vista')

@app.route('/inicio')
def incio():
    return render_template('/index.html')