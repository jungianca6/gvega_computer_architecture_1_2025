import tkinter as tk
from PIL import ImageTk, Image
import os
import subprocess
import numpy as np
import cuadrantes

IMAGE_PATH = "narrador.jpg"
IMG_OUT_PATH = "cuadrante.img"
JPG_OUT_PATH = "cuadrante.jpg"


def GUI():
    # Ventana y componentes
    ventana = tk.Tk()
    ventana.title("Interpolación lineal de imagenes")
    ventana.geometry("1400x800")  # Ajustar el tamaño de la ventana si es necesario
    ventana.resizable(None, None)

    canvas= tk.Canvas(ventana, width=1400, height=800, bg="light blue")
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
    originalimg = Image.open(IMAGE_PATH).convert("L") #escala de grises
    originalArray = np.array(originalimg)
    originalImgTK = ImageTk.PhotoImage(originalimg)

    # Crear una etiqueta para mostrar la imagen en la ventana
    originalLabel = tk.Label(ventana, image=originalImgTK)
    originalLabel.place(x=75, y=200)

    # Área para la imagen del cuadrante seleccionado
    cuadranteLabel = tk.Label(ventana)
    cuadranteLabel.place(x=900, y=200)

    def mostrarCuadrante(num):
        cuadrante = cuadrantes.extraerCuadrante(originalArray, num)
        cuadrantes.guardarImg(cuadrante, IMG_OUT_PATH)

        '''
        # Ejecutar ensamblador para interpolar el .img
        try:
            subprocess.run(["nasm", "-felf64", "-o", "InterpolacionBilineal.o", "InterpolacionBilineal.asm"], check=True)
            subprocess.run(["ld", "-o", "InterpolacionBilineal", "InterpolacionBilineal.o"], check=True)
            subprocess.run(["./InterpolacionBilineal"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el ensamblador: {e}")
            return
        '''
        # Volver a cargar desde .img
        cargado = cuadrantes.cargarImg(IMG_OUT_PATH, cuadrante.shape)
        img_pil = Image.fromarray(cargado, mode='L')
        img_pil.save(JPG_OUT_PATH)

        cuadrante_tk = ImageTk.PhotoImage(img_pil)
        cuadranteLabel.config(image=cuadrante_tk)
        cuadranteLabel.image = cuadrante_tk  # Evita que se borre de memoria

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
                                   command=lambda num=bNumber: mostrarCuadrante(num))
                button.pack(side=tk.LEFT, padx=5, pady=5)

    # Llamar a la función para crear los botones en la posición deseada
    createButtons(ventana, x=550, y=225)

    # Ejecutar el bucle principal de Tkinter
    ventana.mainloop()
GUI()
