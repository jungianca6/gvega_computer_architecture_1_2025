import hashlib

def calcular_md5(nombre_archivo):
    try:
        with open(nombre_archivo, 'rb') as f:
            contenido = f.read()
            md5_hash = hashlib.md5(contenido).hexdigest()
            print(f"MD5 de '{nombre_archivo}': {md5_hash}")
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no existe.")

def select_file():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    file_path = filedialog.askopenfilename(title="Selecciona un archivo para cifrar")
    return file_path 

if __name__ == "__main__":
    archivo = select_file()
    if archivo:
        calcular_md5(archivo)
