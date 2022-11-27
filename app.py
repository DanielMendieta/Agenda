from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
sql = MySQL()


#Conexion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'contactos'
mysql = MySQL(app)


#########################
app.secret_key = 'mysecretkey'

@app.route ('/')
def index():
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM CONTACTO"
    cursor.execute (sql)
    info = cursor.fetchall()
    return render_template('index.html', contacto = info)

@app.route ('/Agregar_Contacto', methods=['POST'])
def Agregar_Contacto():
    if request.method == 'POST':
       nombre = request.form['Nombre_Completo']
       telefono = request.form['Telefono']
       direccion = request.form['Direccion']
       localidad = request.form['Localidad']
       mail = request.form['E_mail']
       cursor = mysql.connection.cursor()
       sql = "INSERT INTO contacto (nombre_completo, telefono, direccion, localidad, e_mail) VALUES ('{0}', {1}, '{2}','{3}', '{4}')".format (nombre, telefono, direccion,localidad, mail)
       cursor.execute (sql)
       mysql.connection.commit()
       flash('Contacto Agregado!')
    return redirect(url_for('index'))
  

@app.route ('/Editar/<id>')
def EditarContacto(id):
    cursor = mysql.connection.cursor()
    sql = 'SELECT * FROM contacto WHERE id = {}'.format (id)
    cursor.execute(sql)
    dato = cursor.fetchall()
    return render_template ('EditarContacto.html', contacto = dato [0])
    #print (dato)
    #return 'HECHO'

@app.route ('/actualizar/<id>', methods = ['POST'])
def actualizarContacto (id):
    if request.method == 'POST':
        nombreCompleto = request.form ['NombreCompleto']
        telefono = request.form ['Telefono']
        direccion = request.form ['Direccion']
        localidad = request.form ['Localidad']
        mail = request.form ['Email']
        cursor = mysql.connection.cursor ()
        sql = """ UPDATE contacto set nombre_completo = '{}', 
        telefono = {},
        direccion = '{}',
        localidad = '{}',
        e_mail = '{}' 
        where id = {} """ . format (nombreCompleto,telefono,direccion,localidad,mail,id)
        cursor.execute (sql)
        mysql.connection.commit()
        flash ('Contacto Actualizado')
        return redirect(url_for('index'))



@app.route('/Eliminar/<string:id>')
def Eliminar(id):
    cursor = mysql.connection.cursor()  
    sql = 'DELETE FROM contacto WHERE id = {0}'.format(id)
    cursor.execute(sql)
    mysql.connection.commit()
    flash ('Contacto Eliminado')
    return redirect(url_for('index'))
   
   

if __name__ == '__main__':
    app.run(port = 3000, debug = True) 