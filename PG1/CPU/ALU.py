class ALU:
    def __init__(self):
        self.result = 0  # Resultado de la operación
        self.zero = 0b0  # Indicador de cero
        self.neg = 0b0  # Indicador de negativo
        pass

    def operate(self, input1, input2, ALUOp, input3=None):
        if ALUOp == 0b0000:  # MOV/MOVI (OP=0000)
            self.result = input2
            self.update_flags()
        elif ALUOp == 0b0001:  # ADD/ADDI (OP=0001)
            self.result = input1 + input2
            self.update_flags()
        elif ALUOp == 0b0010:  # SUB/SUBI (OP=0010)
            self.result = input1 - input2
            self.update_flags()
        elif ALUOp == 0b0011:  # MUL/MULI (OP=0011)
            self.result = input1 * input2
            self.update_flags()
        elif ALUOp == 0b0100:  # XOR/XORI (OP=0100)
            self.result = input1 ^ input2
            self.update_flags()
        elif ALUOp == 0b0101:  # XOR3 (OP=0101)
            self.result = input1 ^ input2 ^ input3
            self.update_flags()
        elif ALUOp == 0b0110:  # SHL/SHLI (OP=0110)
            self.result = input1 << input2
            self.update_flags()
        elif ALUOp == 0b0111:  # SHR/SHRI (OP=0111)
            self.result = input1 >> input2
            self.update_flags()
        elif ALUOp == 0b1000:  # CMP/CMPI (OP=1000)
            self.result = input1 - input2
            self.update_flags()
            self.result = 0  # CMP returns 0 as result
        else:
            self.result = 0  # NOP/END or undefined operation
            self.update_flags()

        self.flags = {
            "zero": self.zero,
            "neg": self.neg
        }
        return self.result, self.flags

    def update_flags(self):
        # Actualiza los indicadores de cero y negativo basados en el resultado
        if self.result == 0:
            self.zero = 0b1
        else:
            self.zero = 0b0

        if self.result < 0:
            self.neg = 0b1
        else:
            self.neg = 0b0
