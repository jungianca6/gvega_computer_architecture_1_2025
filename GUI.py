import tkinter as tk
from PIL import ImageTk, Image
import os
import subprocess
import numpy as np

def GUI():
    # Ventana y componentes
    ventana = tk.Tk()
    ventana.title("Interpolación lineal de imagenes")
    ventana.geometry("1200x800")  # Ajustar el tamaño de la ventana si es necesario
    ventana.resizable(None, None)

    canvas= tk.Canvas(ventana, width=1200, height=800, bg="light blue")
    canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    #Etiquetas
    cuadriculas = tk.Label(ventana, text="Cuadrantes", font=('Times New Roman', 14),
                           bg='white', fg='black')
    cuadriculas.place(x=550,y=150)

    ogImg = tk.Label(ventana, text="Imagen Original", font=('Times New Roman', 14),
                           bg='white', fg='black')
    ogImg.place(x=75, y=150)

    newImg = tk.Label(ventana, text="Imagen interpolada", font=('Times New Roman', 14),
                     bg='white', fg='black')
    newImg.place(x=900, y=150)


    #Imagen
    originalimg = Image.open("narrador.jpg").convert("L") #escala de grises
    originalImgTK = ImageTk.PhotoImage(originalimg)

    # Crear una etiqueta para mostrar la imagen en la ventana
    originalLabel = tk.Label(ventana, image=originalImgTK)
    originalLabel.place(x=75, y=200)


    def createButtons(ventana, x, y):
        botones = tk.Frame(ventana)
        botones.place(x=x, y=y)  # Colocar el frame en la posición especificada
        #botones.configure(background="light blue")
        for i in range(4):
            filas = tk.Frame(botones)
            filas.pack(side=tk.TOP, padx=5, pady=5)
            for j in range(4):
                bNumber = i * 4 + j + 1
                button = tk.Button(filas, font=('Times New Roman', 11), text=str(bNumber),
                                   command=lambda num=bNumber: click(num))
                button.pack(side=tk.LEFT, padx=5, pady=5)

    def click(num):
        print(num)


    # Llamar a la función para crear los botones en la posición deseada
    createButtons(ventana, x=550, y=225)


    # Ejecutar el bucle principal de Tkinter
    ventana.mainloop()
GUI()
