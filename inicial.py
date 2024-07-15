from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/billetera'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cuenta(db.Model):
    numero = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.String(50))
    saldo = db.Column(db.Numeric)
    contactos = db.Column(db.ARRAY(db.String))

class Historial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_origen = db.Column(db.String(50))
    numero_destino = db.Column(db.String(50))
    valor = db.Column(db.Numeric)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

def initialize_database():
    with app.app_context():
        db.create_all()

        cuenta1 = Cuenta(numero='123456', nombre='Juan Perez', saldo=1000.0, contactos=['789012', '345678'])
        cuenta2 = Cuenta(numero='789012', nombre='Maria Gomez', saldo=1500.0, contactos=['123456'])
        cuenta3 = Cuenta(numero='345678', nombre='Carlos Ruiz', saldo=2000.0, contactos=['123456'])

        historial1 = Historial(numero_origen='123456', numero_destino='789012', valor=100.0)
        historial2 = Historial(numero_origen='789012', numero_destino='123456', valor=50.0)
        historial3 = Historial(numero_origen='123456', numero_destino='345678', valor=200.0)

        db.session.add_all([cuenta1, cuenta2, cuenta3, historial1, historial2, historial3])
        db.session.commit()

if __name__ == '__main__':
    initialize_database()
    print("Base de datos inicializada con datos de prueba.")
