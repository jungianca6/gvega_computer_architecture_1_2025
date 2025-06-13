import tkinter as tk
from GUI.Components.Label import Label


class RegisterFrame(tk.Frame):
    def __init__(self, master=None, registers=None, **kwargs):
        super().__init__(master, **kwargs)
        self.registers = registers if registers else [0]*16
        self.labels = []
        self.config(bg="#3B5998")

        for i, value in enumerate(self.registers):
            label = Label(self, text=f"R{i}\t| 0x{value:08X}", style_type="List")
            label.pack(fill="x", padx=5, pady=2)
            self.labels.append(label)

    def UpdateRegisters(self, new_values):
        self.registers = new_values
        for i, value in enumerate(self.registers):
            self.labels[i].SetText(f"R{i}\t| 0x{value:08X}")

