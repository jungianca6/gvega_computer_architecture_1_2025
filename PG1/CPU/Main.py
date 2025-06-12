from dis import Instruction

from CPU.Cpu import Cpu

if __name__ == "__main__":
    cpu = Cpu()

    # Aquí puedes cargar instrucciones o realizar otras configuraciones necesarias
    instruction = [
                   '01010001100000000000000000001000',  # LDR R4 16
                   '01001010000000000000000000010000',  # LDR R5 20
                   '01001010100000000000000000010100',  # XOR R6, R5, R4
                   '00000000000000000000000000000000',  # NOP
                   '00000000000000000000000000000000',  # NOP
                   '00000000000000000000000000000000',  # NOP
                   '01011011000000000000000000011000',  # STR R6 24
                   '00010000000000000000000000000000'  # END
                   ]

    cpu.setInstructions(instruction)

    while True:
        pipe_stages, pipe_cycle, registers, memory = cpu.runCPU()
        print(f"Pipeline Stages: {pipe_stages}")
        print(f"Pipeline Cycle: {pipe_cycle}")
        print(f"Registers: {registers}")
        print(f"Memory: {memory}")
        cpu.pipeline.vault.debug_print()
        if all(stage is None for stage in pipe_stages.values()):
            print("No more instructions to execute.")
            break

    print("CPU execution completed.")
