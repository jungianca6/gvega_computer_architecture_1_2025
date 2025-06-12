from dis import Instruction

from CPU.Cpu import Cpu

if __name__ == "__main__":
    cpu = Cpu()

    # Aquí puedes cargar instrucciones o realizar otras configuraciones necesarias
    instruction = ['00100001000100000000000000000000',  # MOVI R1 0
                   '00000000000000000000000000000000',  # NOP
                   '00000000000000000000000000000000',  # NOP
                   '00000000000000000000000000000000',  # NOP
                   '00100011000100010000000000000001',  # ADDI R1 R1 1
                   '00000000000000000000000000000000',  # NOP
                   '00000000000000000000000000000000',  # NOP
                   '00000000000000000000000000000000',  # NOP
                   '00110001000100000000000000000011',  # CMPI R1 5
                   '01100000000000000000000000110000',  # BEQ 12
                   '00000000000000000000000000000000',  # NOP
                   '01111000000000000000000000001100',  # JUMP 1
                   '00000000000000000000000000000000',  # NOP
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
