from dis import Instruction

from CPU.Cpu import Cpu

if __name__ == "__main__":
    cpu = Cpu()

    # Aquí puedes cargar instrucciones o realizar otras configuraciones necesarias
    instruction = [
        '10000100000000001101111010101101',  # BSTRH K0 57005
        '10000000000000001011111011101111',  # BSTRL K0 48879
        '00100001000000000000000000000000',  # MOVI R0 0
        '00000000000000000000000000000000',  # NOP
        '00000000000000000000000000000000',  # NOP
        '00000000000000000000000000000000',  # NOP
        '01000000100000000000000000000000',  # LDR R1 R0
        '01000001000000000000000000000100',  # LDR R2 R0 4
        '00000000000000000000000000000000',  # NOP
        '00000000000000000000000000000000',  # NOP
        '10110100000100000000000000000100',  # BSHR R4 R1 K0 4
        '10100101001000000000000000000100',  # BSHL R5 R2 K0 4
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
