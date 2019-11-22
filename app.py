from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_mysqldb import MySQL
import os
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle
from reportlab.lib.pagesizes import letter, inch

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'msc2019'

mysql = MySQL(app)

@app.route('/')
def getEmpleados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM empleados")
    data = cur.fetchall()
    cur.close()
    return render_template('index2.html', empleados=data )

@app.route('/postempleado', methods = ['POST'])
def postEmpleado():
    if request.method == "POST":
        flash("Empleado registrado correctamente")
        nombre = request.form['nombre']
        sueldo = request.form['sueldo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO empleados (nombre, sueldo) VALUES (%s, %s)", (nombre, sueldo))
        mysql.connection.commit()
        return redirect(url_for('getEmpleados'))

@app.route('/delete/<string:clave>', methods = ['GET'])
def deleteEmpleado(clave):
    flash("Empleado eliminado")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM empleados WHERE clave=%s", (clave,))
    mysql.connection.commit()
    return redirect(url_for('getEmpleados'))

@app.route('/putempleado',methods=['POST','GET'])
def putEmpleado():
    if request.method == 'POST':
        clave = request.form['clave']
        nombre = request.form['nombre']
        sueldo = request.form['sueldo']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE empleados
               SET nombre=%s, sueldo=%s
               WHERE clave=%s
            """, (nombre, sueldo, clave))
        flash("Empleado editado correctamente")
        mysql.connection.commit()
        return redirect(url_for('getEmpleados'))

@app.route('/reporte')
def getReporte():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM empleados")
    data = cur.fetchall()
    cur.close()
    stylesheet = getSampleStyleSheet()
    x = datetime.datetime.now()
    doc = SimpleDocTemplate("templates/Reporte_Empleados.pdf", pagesize=letter)
    colwidths = [2*inch, 2*inch, 2*inch]
    elements = []
    elements.append(Paragraph('Reporte de Empleados', stylesheet['Title']))
    elements.append(Spacer(1,12))
    data = [list(i) for i in data]
    data.insert(0,["Clave","Nombre","Sueldo"])
    t = Table(data, colwidths)
    t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
    elements.append(t)
    doc.build(elements)
    return send_file("templates/Reporte_Empleados.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
