import struct
import hashlib

DELTA = 0x9E3779B9
NUM_ROUNDS = 32

def tea_encrypt_block(v, k):
    """Encripta un bloque de 64 bits (dos uint32) con TEA"""
    v0, v1 = v
    sum_ = 0
    for _ in range(NUM_ROUNDS):
        sum_ = (sum_ + DELTA) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k[0]) ^ (v1 + sum_) ^ ((v1 >> 5) + k[1]))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k[2]) ^ (v0 + sum_) ^ ((v0 >> 5) + k[3]))) & 0xFFFFFFFF
    return v0, v1

def pad_data(data):
    """Rellenar data para que sea múltiplo de 8 bytes (bloque TEA) con ceros"""
    pad_len = (8 - (len(data) % 8)) % 8
    return data + b'\0' * pad_len

def encrypt_file(input_path, output_path, key):
    with open(input_path, 'rb') as f:
        data = f.read()
    data = pad_data(data)

    encrypted = bytearray()
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        v = struct.unpack('>2I', block)  # Big endian 2 uint32
        enc_v = tea_encrypt_block(v, key)
        encrypted += struct.pack('>2I', *enc_v)

    with open(output_path, 'wb') as f:
        f.write(encrypted)

    print(f"Cifrado terminado:")
    print(f"  nombre: {output_path}")
    print(f"  tamaño: {len(encrypted)} bytes")
    md5 = hashlib.md5(encrypted).hexdigest()
    print(f"  MD5: {md5}")

#funcion que abre una ventana del explorador de archivos para seleccionar el archivo a cifrar
def select_file():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    file_path = filedialog.askopenfilename(title="Selecciona un archivo para cifrar")
    return file_path 

if __name__ == "__main__":
    # Clave fija para ejemplo (puedes cambiarla por tu clave real)
    key = (0xdeadbeef, 0xdeadbeef, 0xdeadbeef, 0xdeadbeef)

    path = select_file()
    if not path:
        print("No se seleccionó ningún archivo.")
    else:
        encrypt_file(path, 'Comprobacion/encrypted_file.enc', key)
        print("Archivo cifrado correctamente.")


