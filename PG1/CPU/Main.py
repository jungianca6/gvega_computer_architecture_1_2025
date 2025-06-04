
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

    # Crear el pipeline
    pipeline = Pipeline(pc, instruction_memory, register_file, data_memory, alu, decoder, extend, control_unit)

    # Instrucciones de prueba de la bóveda
    instruction_memory.loadInstructions([
        # BSTRH K0, 0xAAAA
        (0b100 << 29) | (0b00 << 27) | (1 << 26) | (0 << 16) | 0xAAAA,

        # BSTRL K0, 0x5555
        (0b100 << 29) | (0b00 << 27) | (0 << 26) | (0 << 16) | 0x5555,

        # BSTRH K1, 0xDEAD
        (0b100 << 29) | (0b01 << 27) | (1 << 26) | (0 << 16) | 0xDEAD,

        # BSTRL K1, 0xBEEF
        (0b100 << 29) | (0b01 << 27) | (0 << 26) | (0 << 16) | 0xBEEF,
    ])

    # Ejecutar el pipeline paso a paso
    pipeline.set_mode("no_hazard")  # No necesitamos hazards para bóveda

    while not pipeline.is_pipeline_empty():
        pipeline.step()

    # Imprimir el estado de la bóveda
    pipeline.vault.debug_print()
