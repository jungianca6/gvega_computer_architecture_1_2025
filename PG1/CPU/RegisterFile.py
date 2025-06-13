class RegisterFile:
    def __init__(self):
        self.registers = [0] * 16  # Inicializamos 32 registros en 0, el registro 0 no puede escribirse.

        self.registers[3] = 0x9e3779b9   # Quemar DELTA a R3

    def read(self, reg_num):
        """
        Lee el valor de un registro especificado por el número de registro.
        """
        return self.registers[reg_num]

    def write(self, reg_num, value):
        """
        Escribe un valor en un registro, excepto en el registro 0 que es de solo lectura.
        """
        self.registers[reg_num] = value & 0xFFFFFFFF  # Aseguramos que el valor sea de 32 bits

    def resetRegisters(self):
        """Reinicia todos los registros a 0, excepto los valores iniciales que se quieran mantener."""
        self.registers = [0] * 16

        self.registers[3] = 0x9e3779b9  # Quemar DELTA a R3

    def __str__(self):
        """
        Para visualizar los valores de todos los registros.
        """
        return str(self.registers)

    def getRegisters(self):
        """
        Devuelve una copia de los registros.
        """
        return self.registers.copy()
