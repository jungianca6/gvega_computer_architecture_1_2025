import tkinter as tk
from GUI.Components.Label import Label


class MemoryList(tk.Frame):
    def __init__(self, master=None, memory=None, **kwargs):
        super().__init__(master, **kwargs)
        self.memories = memory if memory else [0] * 256
        self.labels = []
        self.config(bg="#3B5998")

        for i, value in enumerate(self.memories):
            label = Label(self, text=f"{hex(i * 4)}\t| {value}", style_type="List")
            label.pack(fill="x", padx=5, pady=2)
            self.labels.append(label)

    def UpdateMemories(self, new_values):
        self.memories = new_values
        for i, value in enumerate(self.memories):
            self.labels[i].SetText(f"{hex(i * 4)}\t| {value}")

