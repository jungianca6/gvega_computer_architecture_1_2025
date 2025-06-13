class InstructionDecoder:
    def __init__(self):
        pass

    def decode(self, instruction):

        # EXTRAER CORRECTAMENTE EL TIPO (opcode) PARA TU ISA
        tipo = (instruction >> 29) & 0b111  # Tipo[31:29]

        #Sistema
        if tipo == 0b000:
            op = (instruction >> 28) & 0b1  # OP[28]
            if op == 0b1:
                return {"opcode": tipo, "type": "Sistema", "name": "END"}
            else:
                return {"opcode": tipo, "type": "Sistema", "name": "NOP"}

        if tipo == 0b001:  # Aritmética

            op = (instruction >> 25) & 0b1111  # OP[28:25]
            rd = (instruction >> 20) & 0b1111  # RD[23:20]
            rs1 = (instruction >> 16) & 0b1111  # RS1[19:16]
            rs2 = (instruction >> 12) & 0b1111  # RS2[15:12]
            rs3 = (instruction >> 8) & 0b1111  # RS3[11:8] (para XOR3)
            imm = instruction & 0xFFFF  # Inmediato[15:0] (para instrucciones tipo I)
            I = (instruction >> 24) & 0b1  # OP[24]

            if I == 0b0:
                if op == 0b0000:
                    return {"opcode": tipo, "type": "Aritmetica (R-R)", "name": "MOV", "rd": rd, "rs1": rs1, "rs2": rs2}
                elif op == 0b0001:
                    return {"opcode": tipo, "type": "Aritmetica (R-R)", "name": "ADD", "rd": rd, "rs1": rs1, "rs2": rs2}
                elif op == 0b0010:
                    return {"opcode": tipo, "type": "Aritmetica (R-R)", "name": "SUB", "rd": rd, "rs1": rs1, "rs2": rs2}
                elif op == 0b0011:
                    return {"opcode": tipo, "type": "Aritmetica (R-R)", "name": "MUL", "rd": rd, "rs1": rs1, "rs2": rs2}
                elif op == 0b0100:
                    return {"opcode": tipo, "type": "Aritmetica (R-R)", "name": "XOR", "rd": rd, "rs1": rs1, "rs2": rs2}
                elif op == 0b0101:
                    return {"opcode": tipo, "type": "Aritmetica (R-R)", "name": "XOR3", "rd": rd, "rs1": rs1,
                            "rs2": rs2, "rs3": rs3}
                elif op == 0b0110:
                    return {"opcode": tipo, "type": "Aritmetica (R-R)", "name": "SHL", "rd": rd, "rs1": rs1, "rs2": rs2}
                elif op == 0b0111:
                    return {"opcode": tipo, "type": "Aritmetica (R-R)", "name": "SHR", "rd": rd, "rs1": rs1, "rs2": rs2}
                else:
                    return {"opcode": tipo, "type": "Aritmetica (R-R)", "name": "CMP", "rd": None, "rs1": rd,
                            "rs2": rs1}
            else:
                if op == 0b0000:
                    return {"opcode": tipo, "type": "Aritmetica (R-I)", "name": "MOVI", "rd": rd, "rs1": rs1,
                            "imm": imm}
                elif op == 0b0001:
                    return {"opcode": tipo, "type": "Aritmetica (R-I)", "name": "ADDI", "rd": rd, "rs1": rs1,
                            "imm": imm}
                elif op == 0b0010:
                    return {"opcode": tipo, "type": "Aritmetica (R-I)", "name": "SUBI", "rd": rd, "rs1": rs1,
                            "imm": imm}
                elif op == 0b0011:
                    return {"opcode": tipo, "type": "Aritmetica (R-I)", "name": "MULI", "rd": rd, "rs1": rs1,
                            "imm": imm}
                elif op == 0b0100:
                    return {"opcode": tipo, "type": "Aritmetica (R-I)", "name": "XORI", "rd": rd, "rs1": rs1,
                            "imm": imm}
                elif op == 0b0101:
                    return {"opcode": tipo, "type": "Aritmetica (R-I)", "name": "XOR3", "rd": rd, "rs1": rs1,
                            "imm": imm}
                elif op == 0b0110:
                    return {"opcode": tipo, "type": "Aritmetica (R-I)", "name": "SHLI", "rd": rd, "rs1": rs1,
                            "imm": imm}
                elif op == 0b0111:
                    return {"opcode": tipo, "type": "Aritmetica (R-I)", "name": "SHRI", "rd": rd, "rs1": rs1,
                            "imm": imm}
                else:
                    return {"opcode": tipo, "type": "Aritmetica (R-I)", "name": "CMPI", "rd": None, "rs1": rd,
                            "imm": imm}
                #no lo dejes en else, has otro elif,. Que el else sea un no valido. En todo lo demas igual

        #Memoria
        if tipo == 0b010:
            op = (instruction >> 28) & 0b1  # OP[28]
            rd = (instruction >> 23) & 0b1111  # RD[26:23]
            rs1 = (instruction >> 19) & 0b1111  # RS1[22:19]
            imm = instruction & 0x7FFFF  # imm[18:0]
            I = (instruction >> 27) & 0b1  # OP[27]
            if op == 0b0:
                if I == 0b1:
                    return {"opcode": tipo, "type": "Memoria", "name": "LDRI", "rd": rd, 'imm': imm}
                else:
                    return {"opcode": tipo, "type": "Memoria", "name": "LDR", "rd": rd, "rs1": rs1, 'imm': imm}
            else:
                if I == 0b1:
                    return {"opcode": tipo, "type": "Memoria", "name": "STRI", "rd": rd, 'imm': imm}
                else:
                    return {"opcode": tipo, "type": "Memoria", "name": "STR", "rd": rd, "rs1": rs1, 'imm': imm}

        #Control
        if tipo == 0b011:
            op = (instruction >> 26) & 0b111  # OP[28:26]
            imm = instruction & 0x3FFFFFF  # Inmediato[25:0]
            if op == 0b000:
                return {"opcode": tipo, "type": "Control", "name": "BEQ", 'imm': imm}
            elif op == 0b001:
                return {"opcode": tipo, "type": "Control", "name": "BNE", 'imm': imm}
            elif op == 0b010:
                return {"opcode": tipo, "type": "Control", "name": "BLT", 'imm': imm}
            elif op == 0b011:
                return {"opcode": tipo, "type": "Control", "name": "BGT", 'imm': imm}
            else:
                return {"opcode": tipo, "type": "Control", "name": "JUMP", 'imm': imm}

        # Boveda - Almacenar
        elif tipo == 0b100:
            ks = (instruction >> 27) & 0b11
            h_l = (instruction >> 26) & 0b1
            immediate = instruction & 0xFFFF  # Usar solo los 16 bits bajos (como en el ISA)

            return {
                'opcode': tipo,
                'type': 'VAULT',
                'name': 'BSTRH' if h_l == 1 else 'BSTRL',
                'ks': ks,
                'hl': h_l,
                'immediate': immediate,
                'instruction_pipeline': f"{'BSTRH' if h_l == 1 else 'BSTRL'} K{ks}, {immediate:#06x}"
            }

        # Boveda - Shift
        elif tipo == 0b101:
            op = (instruction >> 28) & 0b1
            rd = (instruction >> 24) & 0b1111
            rs = (instruction >> 20) & 0b1111
            ks = (instruction >> 18) & 0b11
            imm = instruction & 0x3FFFF  # 18 bits

            return {
                'opcode': tipo,
                'type': 'VAULT_SHIFT',
                'name': 'BSHL' if op == 0 else 'BSHR',
                'op': op,
                'rd': rd,
                'rs1': rs,
                'ks': ks,
                'imm': imm,
                'instruction_pipeline': f"{'BSHL' if op == 0 else 'BSHR'} K{ks}, {imm}"
            }

        return {'error': 'Unknown instruction format or opcode'}
