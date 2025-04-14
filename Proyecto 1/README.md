# gvega_computer_architecture_1_2025
# Proyecto Individual
# Desarrollo de una aplicación para la generación de gráficos y texto

El proyecto consiste en un programa que convierte una imagen a escala de grises, divide la imagen en 16 cuadrantes iguales, y realiza una interpolación bilineal al cuadrante escogido. 
Se utilizó la arquitectura x86 para el código ensamblador que realiza la interpolación, el lenguaje Python como la interfaz de alto nivel, y se realizó en el sistema operativo Ubuntu Linux 24.04 

##  Herramientas utilizadas

| Herramienta     | Descripción |
|-----------------|-------------|
| `NASM`          | Ensamblador para x86-64 (GNU/Linux) |
| `GDB`           | Depurador para programas en bajo nivel |
| `Python 3.13`   | Lenguaje de alto nivel para la interfaz gráfica |
| `Tkinter`       | Biblioteca estándar de GUI en Python |
| `Pillow (PIL)`  | Manejo de imágenes en escala de grises |
| `NumPy`         | Manipulación de datos binarios y arreglos |
| `Linux 24.04`   | Sistema operativo base para desarrollo |
| `subprocess `   | Biblioteca que permite realizar los subprocesos de terminal como compilación, enlace y ejecución de forma automática |
| `Git`           | Control de versiones y gestión del repositorio (se utilizó Github Desktop) |

##  Importante 
Es esencial que este código se ejecute en sistema operativo Linux. El proyecto fue diseñado y programado en Ubuntu Linux 24.04, por lo que se desconoce si se encontrarán problemas al usar versiones anteriores.

##  Instrucciones de uso (terminal)

Si se desea correr el código por terminal, y no por una IDE como Pycharm o Visual Studio, se deben realizar previamente los siguientes pasos:

1. Instalar Python 3.13:
  ```bash
   sudo apt update && sudo apt upgrade 
   ```
   ```bash
   sudo apt install python3.13 python3-pip
   ```

2. Instalar las librerías de Python necesarias:
   ```bash
   pip3 install pillow numpy
   pip3 install numpy
   ```
3. Para ejecutar el código, se abre una terminal en el directorio donde se encuentra el proyecto, o se utiliza "cd" en la terminal para llegar ahí. De cualquier forma, se ejecuta el código así:
  ```bash
   python3.13 GUI.py
  ```
Donde se abrirá la interfaz en Python.

Como se mencionó anteriormente, se puede utilizar una IDE y correr el código por medio de ella. Solo hay que asegurarse de que Numpy y Pillow estén instalados en el intérprete del IDE. 

##  Instrucciones de uso (general)
Ya sea que se utilice la terminal o un IDE, los siguientes pasos para ambos son los mismos. 
### Instalar NASM:
```bash
sudo apt install nasm 
```
### Instalar GDB:
```bash
sudo apt install gdb 
```
Es necesario que NASM esté instalado en el sistema, para que el código de Python pueda realizar la compilación, enlace y ejecución de forma automática por medio de la librería "subprocess". El gdb se utiliza para depuración y simulación. 

Una vez que se tiene todo instalado, y se ha corrido el código, se procede a la interfaz como tal. 

![Interfaz en su estado inicial](https://github.com/user-attachments/assets/957404f1-2b41-453a-aeef-b7d06a52cb4c)

La imagen muestra lo que se debería ver una vez que se ejecuta el código de Python, si no hay errores con las librerías previamente mencionadas. Como se aprecia en la imagen, se encuentra una cuadrícula encima de la imagen original. Esta demuestra la división de cuadrículas. Los botones son los que permiten escoger cual cuadrícula se va a interpolar.
Una vez que se presiona el botón, la interpolación se realizará por medio del código ensamblador, y se permitirá ver en la misma interfaz. 

![Cuadrícula interpolada](https://github.com/user-attachments/assets/7ecedef2-2677-4a2f-a34c-40f6fab0fb2e)




