from CPU.ControlUnit import ControlUnit
from CPU.InstructionDecoder import InstructionDecoder
from CPU.RegisterFile import RegisterFile
from CPU.ALU import ALU
from CPU.InstructionMemory import InstructionMemory
from CPU.ProgramCounter import ProgramCounter
from CPU.Pipeline import Pipeline
from CPU.DataMemory import DataMemory


def cpu():
    # Instancias necesarias
    pc = ProgramCounter()
    instruction_memory = InstructionMemory()
    data_memory = DataMemory()  # Instancia de la memoria de datos
    decoder = InstructionDecoder()
    control_unit = ControlUnit()
    register_file = RegisterFile()
    alu = ALU()
    RUN_PIPELINE = True  # Ejecuta el pipeline paso a paso

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

    if RUN_PIPELINE:
        while not pipeline.is_pipeline_empty():
            pipeline.step()

        print("=== Simulación completada ===")  # <- solo para claridad

    # Imprimir el estado final de la bóveda
    pipeline.vault.debug_print()
