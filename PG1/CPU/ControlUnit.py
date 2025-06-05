class ControlUnit:
    def __init__(self):
        # Señales de control
        self.RegWrite = 0
        self.MemRead = 0
        self.MemWrite = 0
        self.ALUOp = 0
        self.Branch = 0
        self.Jump = 0
        self.MemToReg = 0
        self.ALUSrc = 0
        self.PCSrc = 0
        self.PCWrite = 1  # Inicializado en 1 para permitir la escritura en PC

    def generateSignals(self, opcode, funct3, funct7):
        # Resetear señales
        self.RegWrite = self.MemRead = self.MemWrite = 0
        self.ALUOp = self.Branch = self.Jump = self.MemToReg = 0
        self.ALUSrc = self.PCSrc = 0
        self.PCWrite = 1  # PC puede ser modificado

         # Tipo Sistema (NOP/END)
        if opcode == 0b000:
            if funct3 == 0b1:  # END
                self.PCWrite = 0  # Detiene el PC
            # NOP no necesita acciones

            # Tipo Memoria (LDR/STR)
        elif opcode == 0b010:
            if funct3 == 0b0:  # LDR
                self.RegWrite = 1
                self.MemRead = 1
                self.MemToReg = 1
            else: # STR
                self.MemWrite = 1


        elif opcode == 0b0010011:  # ADDI (Add Immediate)
            self.RegWrite = 1
            self.ALUSrc = 1
            self.ALUOp = 0b00  # ALU Add
        elif opcode == 0b1100011:  # BEQ (Branch if Equal)
            self.Branch = 1
            self.ALUSrc = 0
            self.ALUOp = 0b01  # ALU
            self.PCSrc = 1  # Activar Branch
        elif opcode == 0b1101111:  # JAL (Jump and Link)
            self.Jump = 1
            self.RegWrite = 1
            self.PCSrc = 1  # Cambiar PC para salto
        elif opcode == 0b0110011:  # R-type (ADD, SUB, AND, OR, SLT, etc.)
            self.RegWrite = 1
            self.ALUSrc = 0  # Los dos operandos vienen de registros
            if funct3 == 0b000:
                if funct7 == 0b0000000:  # ADD
                    self.ALUOp = 0b00
                elif funct7 == 0b0100000:  # SUB
                    self.ALUOp = 0b01
            elif funct3 == 0b111:  # AND
                self.ALUOp = 0b10
            elif funct3 == 0b110:  # OR
                self.ALUOp = 0b11
            elif funct3 == 0b010:  # SLT (Set Less Than)
                self.ALUOp = 0b100
            elif funct3 == 0b001:  # XOR
                self.ALUOp = 0b101

        elif opcode == 0b100 or opcode == 0b101:
            # Instrucciones de bóveda → no tocan registros ni memoria normal
            self.RegWrite = 0
            self.MemRead = 0
            self.MemWrite = 0
            self.ALUOp = 0
            self.Branch = 0
            self.Jump = 0
            self.MemToReg = 0
            self.ALUSrc = 0
            self.PCSrc = 0
            self.PCWrite = 1

            # Tipo Control (BEQ/JUMP)
        elif opcode == 0b011:
            if funct3 != 0b110:  # BEQ/BNE/BLT/BGT
                self.Branch = 1
                self.PCSrc = 1
            else:  # JUMP
                self.Jump = 1
                self.PCSrc = 1

    def __str__(self):
        return f"RegWrite: {self.RegWrite}, MemRead: {self.MemRead}, MemWrite: {self.MemWrite}, ALUOp: {self.ALUOp}, Branch: {self.Branch}, Jump: {self.Jump}, MemToReg: {self.MemToReg}, ALUSrc: {self.ALUSrc}, PCSrc: {self.PCSrc}"
