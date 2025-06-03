import os
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import messagebox

from GUI.Components.Button import Button
from GUI.Components.Label import Label
from GUI.Components.TextEditor import TextEditor
from GUI.Components.RegisterList import RegisterList
from GUI.Components.MemoryList import MemoryList


class MainGUI:
    def __init__(self):
        self.xSize = 1600
        self.ySize = 900
        self.registers = None

        self.code_path = os.path.join(os.getcwd(), "files", "isa_code.txt")

        # fondos: #1976D2, secundario: #64B5F6, detales: #BBDEFB, advertencias: #0D47A1

        self.root = tk.Tk()
        self.root.title("ISA - Aplicaciones de Seguridad Informática")
        self.root.geometry(f"{self.xSize}x{self.ySize}")
        self.root.resizable(False, False)

        self.root_canvas = tk.Canvas(self.root, width=1600, height=900, bg="#1976D2",
                                     bd=0, highlightthickness=0)
        self.root_canvas.pack()

        self.btn_exit = Button(self.root_canvas, text="✘", command=self.ExitBtn,
                               tooltip_text="Exit")
        self.btn_exit.place(x=(self.xSize - 10), y=10, anchor='ne')

        self.lb_title = Label(self.root_canvas, text="ISA - Aplicaciones de Seguridad Informática", style_type="Title")
        self.lb_title.place(x=(self.xSize / 2), y=10, anchor='n')

        self.code_editor = TextEditor(self.root_canvas)
        self.code_editor.place(x=50, y=100, width=700, height=750, anchor='nw')

        self.btn_run_cycle = Button(self.root_canvas, text="▶", command=self.RunCycleBtn,
                                    tooltip_text="Execute per Cycle")
        self.btn_run_cycle.place(x=(self.xSize / 2), y=60, anchor='nw')

        self.btn_run_processor = Button(self.root_canvas, text="▶▶", command=self.RunProcessorBtn,
                                        tooltip_text="Execute Processor")
        self.btn_run_processor.place(x=(self.xSize / 2) + 50, y=60, anchor='nw')

        self.btn_upload_file = Button(self.root_canvas, text="Open", command=self.UploadFile,
                                      tooltip_text="Upload File")
        self.btn_upload_file.place(x=50, y=60, anchor='nw')

        self.btn_save_file = Button(self.root_canvas, text="Save", command=self.SaveFile,
                                    tooltip_text="Save File")
        self.btn_save_file.place(x=150, y=60, anchor='nw')

        self.registers = [i ** 2 for i in range(16)]

        self.reg_canvas = tk.Canvas(self.root_canvas, width=300, height=500, bg="#3B5998",
                                    bd=0, highlightthickness=0)
        self.reg_canvas.place(x=(self.xSize / 2), y=350, anchor='nw')
        lb_reg = Label(self.root_canvas, text="Registers:", style_type="Subtitle")
        lb_reg.place(x=(self.xSize / 2), y=350, anchor='sw')
        self.PlaceRegisterList()

        self.memory_canvas = tk.Canvas(self.root_canvas, width=300, height=500, bg="#3B5998",
                                  bd=0, highlightthickness=0)
        self.memory_canvas.place(x=(self.xSize / 2) + 320, y=350, anchor='nw')
        self.lb_memory = Label(self.root_canvas, text="Memory:", style_type="Subtitle")
        self.lb_memory.place(x=(self.xSize / 2) + 320, y=350, anchor='sw')
        self.PlaceMemoryList()

    def run(self):
        self.root.mainloop()

        return None

    def ExitBtn(self):
        self.root.destroy()
        print("Exiting application...")

        return None

    def RunCycleBtn(self):
        print("Running cycle...")

        return None

    def RunProcessorBtn(self):
        print("Running processor...")

        return None

    def UploadFile(self):
        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            self.code_editor.delete("1.0", tk.END)
            self.code_editor.insert(tk.END, content)

        return None

    def SaveFile(self):
        if not os.path.exists(os.path.dirname(self.code_path)):
            os.makedirs(os.path.dirname(self.code_path))
        try:
            with open(self.code_path, 'w', encoding="utf-8") as f:
                content = self.code_editor.get("1.0", tk.END)
                f.write(content)
            messagebox.showinfo("Success", f"File saved")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

        return None

    def PlaceRegisterList(self):
        reg_scrollbar = tk.Scrollbar(self.root_canvas, orient="vertical",
                                     command=self.reg_canvas.yview)
        reg_scrollbar.place(x=(self.xSize / 2) + 300, y=350, height=500, anchor='nw')
        self.reg_canvas.configure(yscrollcommand=reg_scrollbar.set)

        reg_frame = tk.Frame(self.reg_canvas, bg="#1976D2")
        self.reg_canvas.create_window((0, 0), window=reg_frame, anchor='nw')

        registers_list = RegisterList(reg_frame, registers=self.registers)
        registers_list.pack(fill="x", expand=True)

        reg_frame.bind(
            "<Configure>",
            lambda event: self.reg_canvas.configure(scrollregion=self.reg_canvas.bbox("all"))
        )

    def PlaceMemoryList(self):
        memory_scrollbar = tk.Scrollbar(self.root_canvas, orient="vertical",
                                        command=self.memory_canvas.yview)
        memory_scrollbar.place(x=(self.xSize / 2) + 620, y=350, height=500, anchor='nw')
        self.memory_canvas.configure(yscrollcommand=memory_scrollbar.set)

        memory_frame = tk.Frame(self.memory_canvas, bg="#1976D2")
        self.memory_canvas.create_window((0, 0), window=memory_frame, anchor='nw')

        memory_list = MemoryList(memory_frame)
        memory_list.pack(fill="x", expand=True)

        memory_frame.bind(
            "<Configure>",
            lambda event: self.memory_canvas.configure(scrollregion=self.memory_canvas.bbox("all"))
        )
