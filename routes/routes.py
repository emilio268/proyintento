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

