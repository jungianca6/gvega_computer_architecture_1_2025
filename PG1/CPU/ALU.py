class ALU:
    def __init__(self):
        pass

    def operate(self, input1, input2, ALUOp, input3=None):
        if ALUOp == 0b0000:  # MOV/MOVI (OP=0000)
            return input2  # MOV simplemente copia el valor (input2=rs2 o inmediato)

        elif ALUOp == 0b0001:  # ADD/ADDI (OP=0001)
            return input1 + input2

        elif ALUOp == 0b0010:  # SUB/SUBI (OP=0010)
            return input1 - input2

        elif ALUOp == 0b0011:  # MUL/MULI (OP=0011)
            return input1 * input2

        elif ALUOp == 0b0100:  # XOR/XORI (OP=0100)
            return input1 ^ input2

        elif ALUOp == 0b0101:  # XOR3 (OP=0101)
            return input1 ^ input2 ^ input3

        elif ALUOp == 0b0110:  # SHL/SHLI (OP=0110)
            return input1 << input2

        elif ALUOp == 0b0111:  # SHR/SHRI (OP=0111)
            return input1 >> input2

        elif ALUOp == 0b1000:  # CMP/CMPI (OP=1000)
            return 1 if input1 < input2 else 0

        else:
            return 0  # NOP/END o operación no definida