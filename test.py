import tkinter as tk
import PIL
from PIL import ImageTk, Image
import os
import subprocess

import tkinter as tk

def create_buttons(ventana):
    for i in range(4):
        frame = tk.Frame(ventana)
        frame.pack(side=tk.TOP, padx=5, pady=5)
        for j in range(4):
            button_number = i * 4 + j + 1
            button = tk.Button(frame, font=('Times New Roman', 12), text=str(button_number))
            button.pack(side=tk.LEFT, padx=5, pady=5)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("16 Botones en Tkinter")
ventana.geometry("500x300")
ventana.resizable(False, False)

# Llamar a la función para crear los botones
create_buttons(ventana)

# Ejecutar el bucle principal de Tkinter
ventana.mainloop()
