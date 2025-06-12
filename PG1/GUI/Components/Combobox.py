import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


class Combobox(ttk.Combobox):
    def __init__(self, master=None, values=None, default=None, **kwargs):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Combobox",
            fieldbackground="#BBDEFB",  # Fondo del área seleccionada
            background="#64B5F6",       # Fondo del botón desplegable
            foreground="#0D47A1",       # Texto
            font=tkfont.Font(family="Courier", size=16),
            relief="flat"
        )

        super().__init__(
            master,
            values=list(values.keys()) if values else {},
            style="TCombobox",
            font=tkfont.Font(family="Courier", size=16),
            state="readonly",  # para evitar escritura manual
            **kwargs
        )

        if default:
            self.set(default)
