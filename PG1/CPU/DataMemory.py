import os
from files.Txt import txt_to_mem, mem_to_txt


class DataMemory:
    def __init__(self):
        self.memory = txt_to_mem()  # Cargar memoria desde el archivo txt
        self.index = 0
        self.num_block = len(self.memory) // 256  # Número de bloques en que se puede dividir la memoria

        self.update_callback = None  # Callback para notificar cambios

        # self.resetDM(self.index)

    def set_update_callback(self, callback):
        """Asigna un callback para notificar actualizaciones en la memoria."""
        self.update_callback = callback

    def read(self, address):
        """Lee un bloque de 4 bytes desde la dirección especificada."""
        index = address // 4  # Calcular la posición en el array
        if 0 <= index < len(self.memory):
            return self.memory[index]
        else:
            print(f"Error: Dirección de memoria fuera de rango: {address}")
            return None

    def write(self, address, data):
        """Escribe un bloque de 4 bytes en la dirección especificada."""
        index = address // 4  # Calcular la posición en el array
        if 0 <= index < len(self.memory):
            self.memory[index] = data & 0xFFFFFFFF  # Aseguramos que el valor sea de 32 bits
            if self.update_callback:
                self.update_callback(address, data)
        else:
            print(f"Error: Dirección de memoria fuera de rango: {address}")

    def dump(self):
        """Devuelve una lista con todas las direcciones y sus valores."""
        result = []
        for i in range(len(self.memory)):
            address = i * 4  # Calcular la dirección real
            result.append((address, self.memory[i]))
        return result

    def resetDM(self, index=None):
        """Reinicia toda la memoria de datos a 0."""
        mem_to_txt(self.memory)

        if self.update_callback:
            for address in range(0, len(self.memory) * 4, 4):
                self.update_callback(address, 0)

    def getMemory(self):
        """Devuelve una copia de la memoria."""
        return self.memory.copy()
