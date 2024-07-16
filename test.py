import unittest
from app import app, db
from models import Cuenta, Contacto, Operacion
from config import TestConfig

class BilleteraTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(TestConfig)
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            cuenta1 = Cuenta(numero="21345", nombre="Arnaldo", saldo=200)
            cuenta2 = Cuenta(numero="123", nombre="Luisa", saldo=400)
            cuenta3 = Cuenta(numero="456", nombre="Andrea", saldo=300)
            db.session.add_all([cuenta1, cuenta2, cuenta3])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_listar_contactos_exito(self):
        response = self.app.get('/billetera/contactos?numero=21345')
        self.assertEqual(response.status_code, 200)

    def test_realizar_pago_exito(self):
        response = self.app.post('/billetera/pagar', json={
            'minumero': '21345',
            'numerodestino': '123',
            'valor': 100
        })
        self.assertEqual(response.status_code, 200)

    def test_realizar_pago_error_saldo(self):
        response = self.app.post('/billetera/pagar', json={
            'minumero': '21345',
            'numerodestino': '123',
            'valor': 300
        })
        self.assertEqual(response.status_code, 400)

    def test_historial_exito(self):
        response = self.app.get('/billetera/historial?numero=21345')
        self.assertEqual(response.status_code, 200)

    def test_historial_error(self):
        response = self.app.get('/billetera/historial?numero=99999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
