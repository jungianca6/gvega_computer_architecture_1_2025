import os
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import messagebox

from GUI.Components.Button import Button
from GUI.Components.Label import Label
from GUI.Components.TextEditor import TextEditor
from GUI.Components.RegisterFrame import RegisterFrame
from GUI.Components.MemoryFrame import MemoryFrame
from GUI.Components.StateFrame import StateFrame
from GUI.Components.Combobox import Combobox

from Compilador.compilador import compilar

from CPU.Cpu import Cpu
import threading


class MainGUI:
    def __init__(self):
        # Configuración de la ventana principal
        self.xSize = 1600
        self.ySize = 900
        # Inicialización de variables
        self.cpu = Cpu()
        self.registers = self.cpu.register_file.getRegisters()
        self.instructions = None
        self.memory = self.cpu.data_memory.getMemory()
        self.processor_running = False

        # Ruta del archivo de ejecutable
        self.code_path = os.path.join(os.path.dirname(os.getcwd()), "PG1/files/isa_code.txt")

        # fondos: #1976D2, secundario: #64B5F6, detales: #BBDEFB, advertencias: #0D47A1

        # Inicialización de la ventana principal
        self.root = tk.Tk()
        self.root.title("ISA - Aplicaciones de Seguridad Informática")
        self.root.geometry(f"{self.xSize}x{self.ySize}")
        self.root.resizable(False, False)

        self.root_canvas = tk.Canvas(self.root, width=1600, height=900, bg="#1976D2",
                                     bd=0, highlightthickness=0)
        self.root_canvas.pack()

        # Botones y etiquetas
        # Botón de salir
        self.btn_exit = Button(self.root_canvas, text="✘", command=self.ExitBtn,
                               tooltip_text="Exit")
        self.btn_exit.place(x=(self.xSize - 10), y=10, anchor='ne')

        # Etiqueta de título
        self.lb_title = Label(self.root_canvas, text="ISA - Aplicaciones de Seguridad Informática", style_type="Title")
        self.lb_title.place(x=(self.xSize / 2), y=10, anchor='n')

        # Editor de código
        self.code_editor = TextEditor(self.root_canvas)
        self.code_editor.place(x=50, y=100, width=700, height=750, anchor='nw')

        # Botones de acción
        # Botón de ejecución por ciclo
        self.btn_run_cycle = Button(self.root_canvas, text="▶", command=self.RunCycleBtn,
                                    tooltip_text="Execute per Cycle")
        self.btn_run_cycle.place(x=680, y=60, anchor='ne')

        # Botón de ejecución del procesador
        self.btn_run_processor = Button(self.root_canvas, text="▶▶", command=self.RunProcessorBtn,
                                        tooltip_text="Execute Processor")
        self.btn_run_processor.place(x=750, y=60, anchor='ne')

        # Botones de archivo
        # Botón de subir archivo
        self.btn_upload_file = Button(self.root_canvas, text="Open", command=self.UploadFile,
                                      tooltip_text="Upload File")
        self.btn_upload_file.place(x=50, y=60, anchor='nw')

        # Botón de guardar archivo
        self.btn_save_file = Button(self.root_canvas, text="Save", command=self.SaveFile,
                                    tooltip_text="Save File")
        self.btn_save_file.place(x=150, y=60, anchor='nw')

        # Botón de compilar archivo
        self.btn_compile_file = Button(self.root_canvas, text="Compile", command=self.CompileFile,
                                       tooltip_text="Compile File")
        self.btn_compile_file.place(x=250, y=60, anchor='nw')

        # Inicialización de registros y memoria
        # Marco de registros
        self.reg_canvas = tk.Canvas(self.root_canvas, width=350, height=500, bg="#3B5998",
                                    bd=0, highlightthickness=0)
        self.reg_canvas.place(x=(self.xSize / 2), y=350, anchor='nw')
        lb_reg = Label(self.root_canvas, text="Registers:", style_type="Subtitle")
        lb_reg.place(x=(self.xSize / 2), y=350, anchor='sw')
        self.registerFrame = None
        self.PlaceRegisterList()

        # Marco de memoria
        self.memory_canvas = tk.Canvas(self.root_canvas, width=350, height=500, bg="#3B5998",
                                       bd=0, highlightthickness=0)
        self.memory_canvas.place(x=(self.xSize / 2) + 370, y=350, anchor='nw')
        self.lb_memory = Label(self.root_canvas, text="Memory:", style_type="Subtitle")
        self.lb_memory.place(x=(self.xSize / 2) + 370, y=350, anchor='sw')
        self.memoryFrame = None
        self.PlaceMemoryList()

        self.btn_memory = Button(self.root_canvas, text="MEM", command=self.SetMemBlock,
                                 tooltip_text="Charge Memory Block")
        self.btn_memory.place(x=(self.xSize / 2) + 650, y=345, anchor='sw')
        self.txt_mem = tk.Text(self.root_canvas, height=1, width=10, bg="#BBDEFB", font=("Arial", 12))
        self.txt_mem.place(x=(self.xSize / 2) + 650, y=345, width=75, height=30, anchor='se')

        # Marco de estado del procesador
        self.state_canvas = tk.Canvas(self.root_canvas, width=750, height=100, bg="#3B5998",
                                      bd=0, highlightthickness=0)
        self.state_canvas.place(x=(self.xSize / 2), y=200, anchor='nw')
        self.lb_state = Label(self.root_canvas, text="State:", style_type="Subtitle")
        self.lb_state.place(x=(self.xSize / 2), y=200, anchor='sw')
        self.stateFrame = StateFrame(self.state_canvas, pipe_stages=None)
        self.stateFrame.place(x=0, y=0, width=750, height=200, anchor='nw')

        self.lb_cycle = Label(self.root_canvas, text="Cycle: --", style_type="Subtitle")
        self.lb_cycle.place(x=(self.xSize / 2), y=100, anchor='nw')

        self.delay_options = {
            "1 s": 1000,
            "0,5 s": 500,
            "0,1 s": 100,
            "50 ms": 50,
            "10 ms": 10,
            "5 ms": 5,
            "1 ms": 1,
            "0.1 ms": 0
        }

        self.cb_cycle = Combobox(
            self.root_canvas,
            values=list(self.delay_options.keys()),
            default="1 ms")
        self.cb_cycle.place(x=(self.xSize / 2 + 200), y=100, anchor='nw')

    def run(self):
        # Ejecutar la ventana principal
        self.root.mainloop()
        return None

    def ExitBtn(self):
        # Cerrar la ventana y salir de la aplicación
        self.root.destroy()
        print("Exiting application...")
        return None

    def RunCycleBtn(self):
        # Ejecutar un ciclo de la CPU
        print("Running cycle...")

        pipe_stages, pipe_cycle, registers, memory = self.cpu.runCPU()
        self.lb_cycle.SetText(f"Cycle: {pipe_cycle}")
        if all(stage is None for stage in pipe_stages.values()):
            messagebox.showinfo("Finished", "No more instructions to execute.")
            return None

        # print(f"Pipeline Stages: {pipe_stages}, Cycle: {pipe_cycle}")
        self.stateFrame.update_values(pipe_stages)
        self.registers = registers
        self.memory = memory
        self.memoryFrame.UpdateMemories(memory)
        self.registerFrame.UpdateRegisters(registers)
        return None
    def RunProcessorBtn(self):
        print("Running processor...")
        if not self.processor_running:
            self.processor_running = True
            self.btn_run_processor.SetText("⏸")
            # Ejecutar el ciclo del procesador en un hilo aparte
            threading.Thread(target=self._run_processor_step, daemon=True).start()
        else:
            self.processor_running = False
            self.btn_run_processor.SetText("▶▶")

    def _run_processor_step(self):
        delay = self.delay_options[self.cb_cycle.get()]
        if not self.processor_running:
            return
        pipe_stages, pipe_cycle, registers, memory = self.cpu.runCPU()
        self.lb_cycle.SetText(f"Cycle: {pipe_cycle}")
        if all(stage is None for stage in pipe_stages.values()):
            messagebox.showinfo("Finished", "No more instructions to execute.")
            self.processor_running = False
            self.btn_run_processor.SetText("▶▶")
            return
        self.stateFrame.update_values(pipe_stages)
        self.registers = registers
        self.memory = memory
        self.memoryFrame.UpdateMemories(memory)
        self.registerFrame.UpdateRegisters(registers)
        self._run_processor_step()

    def UploadFile(self):
        # Abrir un diálogo para seleccionar un archivo
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
        # Guardar el contenido del editor de código en un archivo
        dir_path = os.path.dirname(self.code_path)
        print(f"Saving to: {self.code_path}")  # Depuración
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        try:
            content = self.code_editor.get("1.0", tk.END)
            # print(f"Content to save:\n{content}")  # Debug: content
            with open(self.code_path, 'w', encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Success", f"File saved")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
        return None

    def CompileFile(self):
        # Guarda y compila el archivo
        self.SaveFile()
        self.cpu.resetCPU()
        self.lb_cycle.SetText("Cycle: --")
        try:
            self.instructions = compilar(self.code_path)
            if self.instructions is not None:
                # Cargar las instrucciones en el CPU
                self.cpu.setInstructions(self.instructions)
                print(f"{self.instructions}")
                messagebox.showinfo("Compilation Success", "File compiled successfully!")

        except Exception as e:
            messagebox.showerror("Compilation Error", f"An error occurred during compilation: {e}")
            return None

        return None

    def PlaceRegisterList(self):
        reg_scrollbar = tk.Scrollbar(self.root_canvas, orient="vertical",
                                     command=self.reg_canvas.yview)
        reg_scrollbar.place(x=(self.xSize / 2) + 350, y=350, height=500, anchor='nw')
        self.reg_canvas.configure(yscrollcommand=reg_scrollbar.set)

        reg_frame = tk.Frame(self.reg_canvas, bg="#1976D2")
        self.reg_canvas.create_window((0, 0), window=reg_frame, anchor='nw')

        self.registerFrame = RegisterFrame(reg_frame, registers=self.registers)
        self.registerFrame.pack(fill="x", expand=True)

        reg_frame.bind(
            "<Configure>",
            lambda event: self.reg_canvas.configure(scrollregion=self.reg_canvas.bbox("all"))
        )

    def PlaceMemoryList(self):
        memory_scrollbar = tk.Scrollbar(self.root_canvas, orient="vertical",
                                        command=self.memory_canvas.yview)
        memory_scrollbar.place(x=(self.xSize / 2) + 720, y=350, height=500, anchor='nw')
        self.memory_canvas.configure(yscrollcommand=memory_scrollbar.set)

        memory_frame = tk.Frame(self.memory_canvas, bg="#1976D2")
        self.memory_canvas.create_window((0, 0), window=memory_frame, anchor='nw')

        self.memoryFrame = MemoryFrame(memory_frame, memory=self.memory)
        self.memoryFrame.pack(fill="x", expand=True)

        memory_frame.bind(
            "<Configure>",
            lambda event: self.memory_canvas.configure(scrollregion=self.memory_canvas.bbox("all"))
        )

    def SetMemBlock(self):
        index = self.txt_mem.get("1.0", tk.END).strip()
        if index.isdigit() and not self.processor_running:
            if int(index) < self.cpu.data_memory.size:
                index = int(index)
                self.cpu.data_memory.resetDM(index)
                self.memory = self.cpu.data_memory.getMemory()
                self.memoryFrame.UpdateMemories(self.memory)
                messagebox.showinfo("Memory Block", f"Memory block set to index {index}.")
            else:
                messagebox.showerror("Memory Block Error", f"Memory block set to index {index}.")
        else:
            if not index.isdigit():
                messagebox.showerror("Error", "Invalid index. Please enter a valid number.")
            elif self.processor_running:
                messagebox.showerror("Error", "Cannot set memory block while the processor is running.")
        return None
