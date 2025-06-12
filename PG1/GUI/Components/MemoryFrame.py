import tkinter as tk
from GUI.Components.Label import Label


class MemoryFrame(tk.Frame):
    def __init__(self, master=None, memory=None, **kwargs):
        super().__init__(master, **kwargs)
        self.memories = memory if memory else [0] * 128
        self.labels = []
        self.config(bg="#3B5998")

        for i, value in enumerate(self.memories):
            label = Label(self, text=f"0x{i*4:04X}\t| 0x{value:08X}", style_type="List")
            label.pack(fill="x", padx=5, pady=2)
            self.labels.append(label)

    def UpdateMemories(self, new_values):
        self.memories = new_values
        for i, value in enumerate(self.memories):
            self.labels[i].SetText(f"0x{i*4:04X}\t| 0x{value:08X}")

