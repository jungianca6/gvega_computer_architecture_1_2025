import tkinter as tk
from GUI.Components.Label import Label


class MemoryFrame(tk.Frame):
    def __init__(self, master=None, memory=None, **kwargs):
        self.block_size = 256
        super().__init__(master, **kwargs)
        self.memories = memory if memory else [0] * self.block_size
        self.index = 0  # Start index of the block to display
        self.labels = []
        self.config(bg="#3B5998")

        for _ in range(self.block_size):
            label = Label(self, text="", style_type="List")
            label.pack(fill="x", padx=5, pady=2)
            self.labels.append(label)

        self.UpdateMemories(self.memories, self.index)

    def UpdateMemories(self, new_values, index=0):
        self.memories = new_values
        self.index = index * self.block_size
        for i in range(self.block_size):
            mem_index = self.index + i
            if mem_index < len(self.memories):
                value = self.memories[mem_index]
                self.labels[i].SetText(f"0x{mem_index*4:04X}\t| 0x{value:08X}")
            else:
                self.labels[i].SetText("")
