import psycopg2
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/billetera'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cuenta(db.Model):
    numero = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.String(50))
    nombre = db.Column(db.String(50))
    saldo = db.Column(db.Numeric)
    contactos = db.Column(db.ARRAY(db.String))

class Historial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_origen = db.Column(db.String(50))
    numero_destino = db.Column(db.String(50))
    valor = db.Column(db.Numeric)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def get_db_connection():
    conn = psycopg2.connect(
        dbname="billetera",
        user="user",
        password="password",
        host="localhost"
    )
    return conn

@app.route('/billetera/contactos')
def contactos():
    minumero = request.args.get('minumero')
    cuenta = Cuenta.query.filter_by(numero=minumero).first()
    if cuenta:
        return jsonify(cuenta.contactos)
    else:
        return jsonify({"error": "Número no encontrado"}), 404

@app.route('/billetera/pagar')
def pagar():
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = float(request.args.get('valor'))
    
    cuenta_origen = Cuenta.query.filter_by(numero=minumero).first()
    cuenta_destino = Cuenta.query.filter_by(numero=numerodestino).first()
    
    if not cuenta_origen or not cuenta_destino:
        return jsonify({"error": "Número no encontrado"}), 404
    
    if numerodestino not in cuenta_origen.contactos:
        return jsonify({"error": "El destino no es un contacto válido"}), 400
    
    if cuenta_origen.saldo < valor:
        return jsonify({"error": "Saldo insuficiente"}), 400
    
    cuenta_origen.saldo -= valor
    cuenta_destino.saldo += valor
    
    nueva_operacion = Historial(numero_origen=minumero, numero_destino=numerodestino, valor=valor)
    db.session.add(nueva_operacion)
    db.session.commit()
    
    return jsonify({"message": "Transacción realizada con éxito"}), 200

@app.route('/billetera/historial')
def historial():
    minumero = request.args.get('minumero')
    cuenta = Cuenta.query.filter_by(numero=minumero).first()
    if not cuenta:
        return jsonify({"error": "Número no encontrado"}), 404
    
    operaciones = Historial.query.filter(
        (Historial.numero_origen == minumero) | (Historial.numero_destino == minumero)
    ).all()
    
    historial = [
        {
            "numero_origen": op.numero_origen,
            "numero_destino": op.numero_destino,
            "valor": op.valor,
            "fecha": op.fecha
        }
        for op in operaciones
    ]
    
    return jsonify({
        "nombre": cuenta.nombre,
        "saldo": cuenta.saldo,
        "operaciones": historial
    })

if __name__ == '__main__':
    app.run(debug=True)
