import unittest
from app import app, get_db_connection

class TestBilletera(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM historial")
        cursor.execute("UPDATE cuentas SET saldo = 200 WHERE numero = '21345'")
        cursor.execute("UPDATE cuentas SET saldo = 400 WHERE numero = '123'")
        cursor.execute("UPDATE cuentas SET saldo = 300 WHERE numero = '456'")
        conn.commit()
        cursor.close()
        conn.close()

    def test_contactos(self):
        response = self.app.get('/billetera/contactos?minumero=21345')
        self.assertEqual(response.status_code, 200)
        self.assertIn('123', response.json)
        self.assertIn('456', response.json)

    def test_pagar_success(self):
        response = self.app.get('/billetera/pagar?minumero=21345&numerodestino=123&valor=100')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Transacción realizada con éxito', response.json['message'])

    def test_pagar_insufficient_balance(self):
        response = self.app.get('/billetera/pagar?minumero=21345&numerodestino=123&valor=300')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Saldo insuficiente', response.json['error'])

    def test_pagar_invalid_contact(self):
        response = self.app.get('/billetera/pagar?minumero=21345&numerodestino=789&valor=100')
        self.assertEqual(response.status_code, 400)
        self.assertIn('El destino no es un contacto válido', response.json['error'])

    def test_historial(self):
        self.app.get('/billetera/pagar?minumero=21345&numerodestino=123&valor=100')
        response = self.app.get('/billetera/historial?minumero=21345')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Arnaldo', response.json['nombre'])
        self.assertEqual(response.json['saldo'], 100)
        self.assertEqual(len(response.json['operaciones']), 1)

if __name__ == '__main__':
    unittest.main()
