import tkinter as tk
from GUI.Components.Tooltip import Tooltip


class Button(tk.Button):
    def __init__(self, master=None, text="", command=None, tooltip_text=None, **kwargs):

        super().__init__(master, text=text, command=command, **kwargs)
        self.config(font=("Arial", 12), bg="#3B5998", fg="white", activebackground="#2D4373", activeforeground="white")
        self.command = command

        if tooltip_text:
            self.tooltip = Tooltip(self, tooltip_text)

    def set_text(self, text):
        self.config(text=text)
