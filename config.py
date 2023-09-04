#modulos que vamos a usar
from flask import Flask
from flask import render_template,request,redirect,url_for,session, Response
from flask_mysqldb import MySQL,MySQLdb
from flask import send_from_directory
from datetime import datetime
import os
from empleados.empleados import empleados_blueprint
from clientes.clientes import clientes_blueprint
from administrador.administrador import administrador_blueprint

#creamos una aplicacion
app=Flask(__name__)
app.secret_key = "VelaDanAik123"

app.register_blueprint(empleados_blueprint, url_prefix='/dashboard/empleados')
app.register_blueprint(clientes_blueprint, url_prefix='/dashboard/clientes')


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistema'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

