from flask import current_app
from flask_mysqldb import MySQL

mysql = MySQL()

def configure_database(app):

    app.config['MYSQL_DATABASE_HOST']='localhost'
    app.config['MYSQL_DATABASE_USER']='root'
    app.config['MYSQL_DATABASE_PORT']=3306
    app.config['MYSQL_DATABASE_PASSWORD']=''
    app.config['MYSQL_DATABASE_DB']='sistema'
    #hacemos que mysql inicie la conexion
    mysql.init_app(app)
