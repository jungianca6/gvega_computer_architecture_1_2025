
from ControlUnit import ControlUnit
from InstructionDecoder import InstructionDecoder
from RegisterFile import RegisterFile
from ALU import ALU
from InstructionMemory import InstructionMemory
from ProgramCounter import ProgramCounter
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

    # Crear el pipeline
    pipeline = Pipeline(pc, instruction_memory, register_file, data_memory, alu, decoder, control_unit)

    # Instrucciones de prueba
    instruction_memory.loadInstructions([
        # BSTRH K0, 0xAAAA
        (0b100 << 29) | (0b00 << 27) | (1 << 26) | (0 << 16) | 0xAAAA,

        # BSTRL K0, 0x5555
        (0b100 << 29) | (0b00 << 27) | (0 << 26) | (0 << 16) | 0x5555,

        # BSHL K0, shift 4
        (0b101 << 29) | (0b0 << 28) | (0 << 24) | (0 << 20) | (0b00 << 18) | (4 & 0x3FFFF),

        # BSHR K0, shift 2
        (0b101 << 29) | (0b1 << 28) | (0 << 24) | (0 << 20) | (0b00 << 18) | (2 & 0x3FFFF),

        # BSTRH K1, 0xDEAD
        (0b100 << 29) | (0b01 << 27) | (1 << 26) | (0 << 16) | 0xDEAD,

        # BSTRL K1, 0xBEEF
        (0b100 << 29) | (0b01 << 27) | (0 << 26) | (0 << 16) | 0xBEEF,

        # BSHL K1, shift 8
        (0b101 << 29) | (0b0 << 28) | (0 << 24) | (0 << 20) | (0b01 << 18) | (8 & 0x3FFFF),

        # BSHR K1, shift 5
        (0b101 << 29) | (0b1 << 28) | (0 << 24) | (0 << 20) | (0b01 << 18) | (5 & 0x3FFFF),
    ])

    # Ejecutar el pipeline paso a paso
    pipeline.set_mode("no_hazard")  # No necesitamos hazards para bóveda

    while not pipeline.is_pipeline_empty():
        pipeline.step()

    # Imprimir el estado final de la bóveda
    pipeline.vault.debug_print()
