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

    def generateSignals(self, opcode, instruction_type, instruction_name):
        # Resetear señales
        self.RegWrite = self.MemRead = self.MemWrite = 0
        self.ALUOp = self.Branch = self.Jump = self.MemToReg = 0
        self.ALUSrc = self.PCSrc = 0
        self.PCWrite = 1  # PC puede ser modificado

        # Sistema (NOP/END)
        if opcode == 0b000:
            if instruction_name == "END":
                self.PCWrite = 0  # Detener el PC

        # Aritmética (R-R o R-I)
        elif opcode == 0b001:
            self.RegWrite = 1
            self.ALUOp = {
                "MOV": 0b0000, "MOVI": 0b0000, "ADD": 0b0001, "ADDI": 0b0001, "SUB": 0b0010, "SUBI": 0b0010,
                "MUL": 0b0011, "MULI": 0b0011, "XOR": 0b0100, "XORI": 0b0100, "XOR3": 0b0101,
                "SHL": 0b0110, "SHLI": 0b0110, "SHR": 0b0111, "SHRI": 0b0111, "CMP": 0b1000, "CMPI": 0b1000
            }[instruction_name]
            self.ALUSrc = 1 if "(R-I)" in instruction_type else 0

        # Memoria
        elif opcode == 0b010:
            if instruction_name in ["LDR", "LDRI"]:
                self.RegWrite = 1
                self.MemRead = 1
                self.MemToReg = 1
            else:  # STR/STRI
                self.MemWrite = 1
            self.ALUSrc = 1 if instruction_name.endswith("I") else 0

        # Control (Saltos)
        elif opcode == 0b011:
            if instruction_name != "JUMP":
                self.Branch = 1
            else:
                self.Jump = 1
            self.PCSrc = 1

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

    def __str__(self):
        return f"RegWrite: {self.RegWrite}, MemRead: {self.MemRead}, MemWrite: {self.MemWrite}, ALUOp: {self.ALUOp}, Branch: {self.Branch}, Jump: {self.Jump}, MemToReg: {self.MemToReg}, ALUSrc: {self.ALUSrc}, PCSrc: {self.PCSrc}"
