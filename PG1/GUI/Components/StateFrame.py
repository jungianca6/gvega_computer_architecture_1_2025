import tkinter as tk

from GUI.Components.Label import Label


class StateFrame(tk.Frame):
    def __init__(self, master=None, pipe_stages=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg="#3B5998")
        self.pipe_stages = pipe_stages if pipe_stages else {
            "IF": None,
            "ID": None,
            "EX": None,
            "MEM": None,
            "WB": None
        }

        # Fila de nombres de las etapas
        stages_names = ["Fetch", "Decode", "Execute", "Memory", "Writeback"]
        stages_label = Label(self, text=" | ".join(stages_names), style_type="List"
        )
        stages_label.pack(fill="x", padx=2, pady=2)

        # Fila de valores
        self.values_label = Label(self, text=self._format_values(), style_type="List")
        self.values_label.pack(fill="x", padx=2, pady=2)

    def _format_values(self):
        return " | ".join([
            str(self.pipe_stages.get(stage, ""))
            for stage in ["IF", "ID", "EX", "MEM", "WB"]
        ])

    def update_values(self, new_pipe_stages):
        self.pipe_stages = new_pipe_stages
        self.values_label.config(text=self._format_values())
