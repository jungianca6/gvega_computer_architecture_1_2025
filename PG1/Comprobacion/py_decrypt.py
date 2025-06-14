import struct

# Constantes
DELTA = 0x9e3779b9
KEY = [0xdeadbeef, 0xdeadbeef, 0xdeadbeef, 0xdeadbeef]

def select_file():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    file_path = filedialog.askopenfilename(title="Selecciona un archivo para descifrar")
    return file_path

# Función de descifrado TEA para un bloque de 64 bits
def decrypt_block(v, k):
    v0, v1 = v
    sum = (DELTA * 32) & 0xFFFFFFFF
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]))) & 0xFFFFFFFF
        sum = (sum - DELTA) & 0xFFFFFFFF
    return struct.pack('>2I', v0, v1)

def main():
    input_file = select_file()
    if not input_file:
        print("No se seleccionó ningún archivo.")
        return

    # Leer el archivo cifrado
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()

    # Descifrar los datos bloque por bloque
    decrypted_data = bytearray()
    for i in range(0, len(encrypted_data), 8):
        block = encrypted_data[i:i+8]
        if len(block) < 8:
            break  # Ignorar bloque incompleto
        v = struct.unpack('>2I', block)
        decrypted_data.extend(decrypt_block(v, KEY))

    # Guardar los datos descifrados en un nuevo archivo
    output_file = 'Comprobacion/decrypted_image.dec'
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

    print(f"Descifrado completo. Archivo guardado como {output_file}.")

if __name__ == "__main__":
    main()
