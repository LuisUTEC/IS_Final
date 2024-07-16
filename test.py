from objects import CuentaUsuario,Operacion
import unittest


class TestCuentaUsuario(unittest.TestCase):
    
    def setUp(self):
        self.cuenta1 = CuentaUsuario("Alice", "123456", 1000.0, [("Bob", "654321"), ("Charlie", "789012")])
        self.cuenta2 = CuentaUsuario("Bob", "654321", 500.0, [("Alice", "123456")])

    def test_listarContactos(self):
        contactos = self.cuenta1.listarContactos()
        self.assertEqual(contactos, [("Bob", "654321"), ("Charlie", "789012")])

    def test_transferir(self):
        result = self.cuenta1.transferir("654321", 200.0)
        self.assertTrue(result)
        self.assertEqual(self.cuenta1.Saldo, 800.0)
        self.assertEqual(self.cuenta2.Saldo, 700.0)
        
        result = self.cuenta1.transferir("000000", 100.0)
        self.assertFalse(result)

        result = self.cuenta1.transferir("654321", 10000.0)
        self.assertFalse(result)

    def test_historialOperaciones(self):
        self.cuenta1.transferir("654321", 200.0)
        operaciones = self.cuenta1.historialOperaciones()
        self.assertEqual(len(operaciones), 1)
        self.assertEqual(operaciones[0].Valor, 200.0)
        self.assertEqual(operaciones[0].Origen.Numero, "123456")
        self.assertEqual(operaciones[0].Destino.Numero, "654321")

    def test_mostrarHistorial(self):
        self.cuenta1.transferir("654321", 200.0)
        historial = self.cuenta1.mostrarHistorial()
        self.assertEqual(historial['Saldo'], 800.0)
        self.assertEqual(len(historial['Operaciones']), 1)
        self.assertEqual(historial['Operaciones'][0].Valor, 200.0)

if __name__ == '__main__':
    unittest.main()
