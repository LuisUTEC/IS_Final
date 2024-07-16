from datetime import datetime
from typing import List

class Operacion:
    def __init__(self, origen, destino, valor):
        self.Origen = origen
        self.Destino = destino
        self.Valor = valor
        self.Fecha = datetime.now()

class CuentaUsuario:
    def __init__(self, nombre: str , numero: str, saldo: float, numeros_contacto: List[str]):
        self.Nombre = nombre
        self.Numero = numero
        self.Saldo = saldo
        self.NumerosContacto = numeros_contacto
        self.operaciones = []

    def historialOperaciones(self):
        return self.operaciones

    def transferir(self, destino, valor: float):
        if self.Saldo >= valor:
            self.Saldo -= valor
            for d in range(0,len(self.NumerosContacto)):
                if self.NumerosContacto[d].second == destino:
                    self.NumerosContacto[d].Saldo += valor
            operacion = Operacion(self, destino, valor)
            self.operaciones.append(operacion)
            destino.operaciones.append(operacion)
            return True
        else:
            return False

