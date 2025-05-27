class DispositivoFicticio:
    def __init__(self):
        self.estado = 0

    def leer(self):
        return self.estado

    def escribir(self, valor):
        self.estado = valor