from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb

app = Flask(__name__,template_folder='template')


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)




#hacemos que mysql inicie la conexion
mysql.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')   

@app.route('/acceso-login', methods= ["GET", "POST"])
def login():
   
    if request.method == 'POST' and 'Admin_Correo' in request.form and 'Admin_Pass' in request.form:
       
        _correo = request.form['Admin_Correo']
        _password = request.form['Admin_Pass']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM administrador WHERE Admin_Correo = %s AND Admin_Pass = %s', (_correo, _password,))
        account = cur.fetchone()
      
        if account:
            session['logueado'] = True
            session['Admin_Id'] = account['Admin_Id']
            session['Admin_Rol'] = account['Admin_Rol']
            
            if session['Admin_Rol']==1:
                return render_template("admin2.html")
            elif session['Admin_Rol']==2:
                return render_template("admin.html")
        else:
            return render_template('index.html',mensaje="Usuario O Contraseña Incorrectas")

    
if __name__ == '__main__':
   app.secret_key = "pinchellave"
   app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
