from flask import Flask, request, jsonify
from models import db, Cuenta, Contacto, Operacion
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/billetera/contactos', methods=['GET'])
def listar_contactos():
    numero = request.args.get('minumero')
    cuenta = Cuenta.query.filter_by(numero=numero).first()
    if cuenta:
        contactos = [{"numero": c.numero, "nombre": c.nombre} for c in cuenta.contactos]
        return jsonify(contactos), 200
    return jsonify({"error": "Cuenta no encontrada"}), 404

@app.route('/billetera/pagar', methods=['POST'])
def realizar_pago():
    data = request.get_json()
    minumero = data.get('minumero')
    numerodestino = data.get('numerodestino')
    valor = data.get('valor')
    
    cuenta = Cuenta.query.filter_by(numero=minumero).first()
    cuenta_destino = Cuenta.query.filter_by(numero=numerodestino).first()

    if not cuenta or not cuenta_destino:
        return jsonify({"error": "Cuenta origen o destino no encontrada"}), 404

    if cuenta.saldo < valor:
        return jsonify({"error": "Saldo insuficiente"}), 400

    cuenta.saldo -= valor
    cuenta_destino.saldo += valor

    operacion_envio = Operacion(tipo='envio', cuenta_id=cuenta.id, cuenta_destino=numerodestino, valor=valor)
    operacion_recepcion = Operacion(tipo='recepcion', cuenta_id=cuenta_destino.id, cuenta_destino=minumero, valor=valor)

    db.session.add(operacion_envio)
    db.session.add(operacion_recepcion)
    db.session.commit()

    return jsonify({"mensaje": "Pago realizado con éxito"}), 200

@app.route('/billetera/historial', methods=['GET'])
def historial():
    numero = request.args.get('minumero')
    cuenta = Cuenta.query.filter_by(numero=numero).first()
    if cuenta:
        operaciones = Operacion.query.filter_by(cuenta_id=cuenta.id).all()
        historial = {
            "saldo": cuenta.saldo,
            "operaciones": [{"tipo": op.tipo, "valor": op.valor, "fecha": op.fecha, "cuenta_destino": op.cuenta_destino} for op in operaciones]
        }
        return jsonify(historial), 200
    return jsonify({"error": "Cuenta no encontrada"}), 404
