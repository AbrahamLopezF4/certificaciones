from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de alumno
class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    carrera = db.Column(db.String(100), nullable=False)
    certificacion = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Alumno {self.nombre}>'

# Ruta principal - listar alumnos
@app.route('/')
def index():
    alumnos = Alumno.query.all()
    return render_template('index.html', alumnos=alumnos)

# Ruta para agregar un alumno
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        carrera = request.form['carrera']
        certificacion = request.form['certificacion']
        alumno = Alumno(nombre=nombre, carrera=carrera, certificacion=certificacion)
        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Ruta para eliminar alumno
@app.route('/eliminar/<int:id>')
def eliminar(id):
    alumno = Alumno.query.get_or_404(id)
    db.session.delete(alumno)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
