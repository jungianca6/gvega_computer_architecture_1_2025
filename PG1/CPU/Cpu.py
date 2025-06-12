from CPU.ControlUnit import ControlUnit
from CPU.InstructionDecoder import InstructionDecoder
from CPU.RegisterFile import RegisterFile
from CPU.ALU import ALU
from CPU.InstructionMemory import InstructionMemory
from CPU.ProgramCounter import ProgramCounter
from CPU.Pipeline import Pipeline
from CPU.DataMemory import DataMemory


class Cpu:
    def __init__(self, instrs=None):
        self.pc = ProgramCounter()
        self.instruction_memory = InstructionMemory()
        self.data_memory = DataMemory()
        self.decoder = InstructionDecoder()
        self.control_unit = ControlUnit()
        self.register_file = RegisterFile()
        self.alu = ALU()

        self.pipeline = Pipeline(self.pc, self.instruction_memory, self.register_file,
                                 self.data_memory, self.alu, self.decoder, self.control_unit)

    def setInstructions(self, instructions):
        # Convert string instructions to int if needed
        processed_instructions = []
        for instr in instructions:
            if isinstance(instr, str):
                # Assume binary string
                processed_instructions.append(int(instr, 2))
            else:
                processed_instructions.append(instr)
        self.instruction_memory.loadInstructions(processed_instructions)
        self.pc.reset()

    def runCPU(self):
        pipe_stages, pipe_cycle = self.pipeline.step()
        self.pipeline.vault.debug_print()

        return pipe_stages, pipe_cycle, self.register_file.getRegisters(), self.data_memory.getMemory()

    def resetCPU(self):
        self.pc.reset()
        self.pipeline.clock_cycle = 0
        self.instruction_memory.reset()
        self.register_file.resetRegisters()
        # self.data_memory.resetDM()
