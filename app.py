import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos desde el .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Certificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class AlumnoCertificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'), nullable=False)
    certificacion_id = db.Column(db.Integer, db.ForeignKey('certificacion.id'), nullable=False)
    calificacion = db.Column(db.Numeric(5, 2), nullable=False)
    alumno = db.relationship('Alumno', backref='certificaciones')
    certificacion = db.relationship('Certificacion', backref='alumnos')

@app.route('/')
def index():
    alumnos = Alumno.query.all()
    certificaciones = Certificacion.query.all()
    relaciones = AlumnoCertificacion.query.all()
    return render_template('index.html', alumnos=alumnos, certificaciones=certificaciones, relaciones=relaciones)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        nombre = request.form['nombre']
        alumno = Alumno(nombre=nombre)
        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/add_certificacion', methods=['GET', 'POST'])
def add_certificacion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cert = Certificacion(nombre=nombre)
        db.session.add(cert)
        db.session.commit()
        return redirect(url_for('ver_certificaciones'))
    return render_template('add_certificacion.html')

@app.route('/ver_certificaciones')
def ver_certificaciones():
    certificaciones = Certificacion.query.all()
    return render_template('ver_certificaciones.html', certificaciones=certificaciones)

@app.route('/asignar_certificacion', methods=['GET', 'POST'])
def asignar_certificacion():
    alumnos = Alumno.query.all()
    certificaciones = Certificacion.query.all()
    if request.method == 'POST':
        alumno_id = request.form['alumno_id']
        certificacion_id = request.form['certificacion_id']
        calificacion = request.form['calificacion']
        relacion = AlumnoCertificacion(alumno_id=alumno_id, certificacion_id=certificacion_id, calificacion=calificacion)
        db.session.add(relacion)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('asignar_certificacion.html', alumnos=alumnos, certificaciones=certificaciones)

@app.route('/relacion/editar/<string:alumno>/<string:certificacion>')
def editar_relacion(alumno, certificacion):
    # lógica para editar
    return f"Editar {alumno} - {certificacion}"

@app.route('/relacion/eliminar/<int:alumno_id>/<int:certificacion_id>', methods=['POST'])
def eliminar_relacion(alumno_id, certificacion_id):
    relacion = AlumnoCertificacion.query.filter_by(alumno_id=alumno_id, certificacion_id=certificacion_id).first()
    if relacion:
        db.session.delete(relacion)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
