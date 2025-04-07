import tkinter as tk
from PIL import ImageTk, Image
import os
import subprocess
import numpy as np

IMAGE_WIDTH = 390
IMAGE_HEIGHT = 390
GRID_SIZE = 4  # 4x4 = 16 cuadrantes
IMAGE_PATH = "narrador.jpg"
IMG_OUT_PATH = "cuadrante.img"
JPG_OUT_PATH = "cuadrante.jpg"

def extraer_cuadrante(img_array, quadrant_num):
    row = (quadrant_num - 1) // GRID_SIZE
    col = (quadrant_num - 1) % GRID_SIZE

    quad_h = IMAGE_HEIGHT // GRID_SIZE
    quad_w = IMAGE_WIDTH // GRID_SIZE

    start_y = row * quad_h
    end_y = start_y + quad_h
    start_x = col * quad_w
    end_x = start_x + quad_w

    return img_array[start_y:end_y, start_x:end_x]

def guardar_img_cuadrante(cuadrante_array, path):
    cuadrante_array.astype(np.uint8).tofile(path)

def cargar_img_desde_raw(path, shape):
    return np.fromfile(path, dtype=np.uint8).reshape(shape)

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
    originalimg = Image.open(IMAGE_PATH).convert("L") #escala de grises
    original_array = np.array(originalimg)
    originalImgTK = ImageTk.PhotoImage(originalimg)

    # Crear una etiqueta para mostrar la imagen en la ventana
    originalLabel = tk.Label(ventana, image=originalImgTK)
    originalLabel.place(x=75, y=200)

    # Área para la imagen del cuadrante seleccionado
    cuadrante_label = tk.Label(ventana)
    cuadrante_label.place(x=900, y=200)

    def mostrar_cuadrante(num):
        cuadrante = extraer_cuadrante(original_array, num)
        guardar_img_cuadrante(cuadrante, IMG_OUT_PATH)

        # Volver a cargar desde .img
        cargado = cargar_img_desde_raw(IMG_OUT_PATH, cuadrante.shape)
        img_pil = Image.fromarray(cargado, mode='L')
        img_pil.save(JPG_OUT_PATH)

        cuadrante_tk = ImageTk.PhotoImage(img_pil)
        cuadrante_label.config(image=cuadrante_tk)
        cuadrante_label.image = cuadrante_tk  # Evita que se borre de memoria

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
                                   command=lambda num=bNumber: mostrar_cuadrante(num))
                button.pack(side=tk.LEFT, padx=5, pady=5)

    def click(num):
        print(num)


    # Llamar a la función para crear los botones en la posición deseada
    createButtons(ventana, x=550, y=225)


    # Ejecutar el bucle principal de Tkinter
    ventana.mainloop()
GUI()
