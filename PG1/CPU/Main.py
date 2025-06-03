
from ControlUnit import ControlUnit
from InstructionDecoder import InstructionDecoder
from RegisterFile import RegisterFile
from Extend import Extend
from ALU import ALU
from InstructionMemory import InstructionMemory
from ProgramCounter import ProgramCounter
from DataMemory import DataMemory
from Pipeline import Pipeline
from DataMemory import DataMemory

if __name__ == "__main__":
    # Instancias necesarias
    pc = ProgramCounter()
    instruction_memory = InstructionMemory()
    data_memory = DataMemory()  # Instancia de la memoria de datos
    decoder = InstructionDecoder()
    control_unit = ControlUnit()
    register_file = RegisterFile()
    alu = ALU()
    extend = Extend()

    # Instrucciones de ejemplo
    instructions = [
        "Aca se pueden poner instrucciones de ejemplo"
    ]
    instruction_memory.loadInstructions(instructions)

    # Crear el pipeline
    pipeline = Pipeline(pc, instruction_memory, register_file, data_memory, alu, decoder, extend, control_unit)
