import tkinter as tk
import PIL
from PIL import ImageTk, Image
import os
import subprocess

import tkinter as tk

def GUI():
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Interpolación")
    ventana.geometry("700x500")  # Ajustar el tamaño de la ventana si es necesario
    ventana.resizable(None, None)

    def create_buttons(ventana, x, y):
        botones = tk.Frame(ventana)
        botones.place(x=x, y=y)  # Colocar el frame en la posición especificada
        for i in range(4):
            filas = tk.Frame(botones)
            filas.pack(side=tk.TOP, padx=5, pady=5)
            for j in range(4):
                bNumber = i * 4 + j + 1
                button = tk.Button(filas, font=('Times New Roman', 12), text=str(bNumber))
                # command=lambda num=bNumber: click(num)
                button.pack(side=tk.LEFT, padx=5, pady=5)

    # Llamar a la función para crear los botones en la posición deseada
    create_buttons(ventana, x=510, y=100)


    # Ejecutar el bucle principal de Tkinter
    ventana.mainloop()
GUI()
