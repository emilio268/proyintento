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

servicios_blueprint = Blueprint('servicios', __name__)

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PORT']=3306
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
#hacemos que mysql inicie la conexion
mysql.init_app(app)



@servicios_blueprint.record_once
def on_load(state):
    global CARPETA
    CARPETA = os.path.join('uploads')
    state.app.config['CARPETA'] = CARPETA


@servicios_blueprint.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    carpeta = current_app.config['CARPETA']
    return send_from_directory(current_app.config['CARPETA'], nombreFoto)

@servicios_blueprint.route('/vista')
def index():
    sql = "SELECT * FROM servicios;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    servicios = cursor.fetchall()
    conn.commit()

    return render_template('/index.html', servicios=servicios)

@servicios_blueprint.route('/destroy/<int:Serv_ID>')
def destroy(Serv_ID):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT Serv_Foto FROM servicios WHERE Serv_ID=%s", Serv_ID)
    fila = cursor.fetchall()

    os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM servicios WHERE Serv_ID=%s", (Serv_ID))
    conn.commit()
    return redirect('/servicios/vista')

@servicios_blueprint.route('/edit/<int:Serv_ID>')
def edit(Serv_ID):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicios WHERE Serv_ID=%s", (Serv_ID))
    servicios = cursor.fetchall()
    conn.commit()

    return render_template('Dashboard-Admin/servicios/edit.html', servicios=servicios)

@servicios_blueprint.route('/update', methods=['POST'])
def update():
    _Serv_Nombre = request.form['SNombre']
    _Serv_Desc = request.form['SCorreo']
    _Serv_Foto = request.files['SFoto']
    _Serv_ID = request.form['SID']

    sql = "UPDATE `servicios` SET Serv_Nombre=%s, Serv_Desc=%s WHERE Serv_ID=%s;"
    datos = (_Serv_Nombre, _Serv_Desc, _Serv_ID)

    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _Serv_Foto.filename != '':
        nuevoNombreFoto = tiempo + _Serv_Foto.filename
        _Serv_Foto.save("uploads/" + nuevoNombreFoto)

        cursor.execute("SELECT Serv_Foto FROM servicios WHERE Serv_ID=%s", _Serv_ID)
        fila = cursor.fetchall()

        os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE servicios SET Serv_Foto=%s WHERE Serv_ID=%s", (nuevoNombreFoto, _Serv_ID))
        conn.commit()

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/servicios/vista')

@servicios_blueprint.route('/create')
def create():
    return render_template('Dashboard-Admin/servicios/create.html')

@servicios_blueprint.route('/store', methods=['POST'])
def storage():
    _Serv_Nombre = request.form['SNombre']
    _Serv_Desc = request.form['SCorreo']
    _Serv_Foto = request.files['SFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _Serv_Foto.filename != '':
        nuevoNombreFoto = tiempo + _Serv_Foto.filename
        _Serv_Foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO `servicios` (`Serv_ID`, `Serv_Nombre`, `Serv_Desc`, `Serv_Foto`) VALUES (NULL, %s, %s, %s);"

    datos = (_Serv_Nombre, _Serv_Desc, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/servicios/vista')

@app.route('/inicio')
def incio():
    return render_template('/index.html')