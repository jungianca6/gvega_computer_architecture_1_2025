# isa_traductor.py

opcodes = {
    'system': '000',
    'arithmetic': '001',
    'memory': '010',
    'control': '011',
    'vault_key': '100',
    'vault_shift': '101'
}

# Codificación de registros: R0-R15, K0-K3
registros = {f'R{i}': format(i, '04b') for i in range(16)}
registros.update({f'K{i}': format(i, '02b') for i in range(4)})

# Mapeo de instrucciones a (tipo, operación binaria, formato)
instrucciones = {
    'NOP':    ('system',     '0', None),
    'END':    ('system',     '1', None),

    'MOV':    ('arithmetic', '0000', 'R2R'),
    'ADD':    ('arithmetic', '0001', 'R3R'),
    'SUB':    ('arithmetic', '0010', 'R3R'),
    'MUL':    ('arithmetic', '0011', 'R3R'),
    'XOR':    ('arithmetic', '0100', 'R3R'),
    'XOR3':   ('arithmetic', '0101', 'R4R'),
    'SHL':    ('arithmetic', '0110', 'RRI'),
    'SHR':    ('arithmetic', '0111', 'RRI'),
    'CMP':    ('arithmetic', '1000', 'R2R'),

    'MOVI':   ('arithmetic', '0000', 'RI'),
    'ADDI':   ('arithmetic', '0001', 'RRI'),
    'SUBI':   ('arithmetic', '0010', 'RRI'),
    'MULI':   ('arithmetic', '0011', 'RRI'),
    'XORI':   ('arithmetic', '0100', 'RRI'),
    'SHLI':   ('arithmetic', '0110', 'RRI'),
    'SHRI':   ('arithmetic', '0111', 'RRI'),
    'CMPI':   ('arithmetic', '1000', 'RI'),

    'LDR':    ('memory',     '0',    'MM'),
    'LDRI':   ('memory',     '0',    'MI'),
    'STR':    ('memory',     '1',    'MM'),
    'STRI':   ('memory',     '1',    'MI'),

    'BEQ':    ('control',    '000',  'J'),
    'BNE':    ('control',    '001',  'J'),
    'BLT':    ('control',    '010',  'J'),
    'BGT':    ('control',    '011',  'J'),
    'JUMP':   ('control',    '110',  'J'),

    'BSTRH':  ('vault_key',  '1',    'VK'),
    'BSTRL':  ('vault_key',  '0',    'VK'),

    'BSHL':   ('vault_shift','0',    'VS'),
    'BSHR':   ('vault_shift','1',    'VS'),
}

def bin_pad(val, bits):
    return format(int(val), f'0{bits}b')

def traducir_instrucciones_a_binario(asm_code):
    instrucciones_binarias = []
    etiquetas = {}
    linea_actual = 0

    # Primera pasada: recolectar etiquetas
    for linea in asm_code:
        if isinstance(linea, str):
            etiquetas[linea] = linea_actual
        else:
            linea_actual += 1

    # Segunda pasada: traducir a binario
    for linea in asm_code:
        if isinstance(linea, str):
            continue

        op, *args = linea
        if op not in instrucciones:
            raise ValueError(f"Instrucción no reconocida: {op}")

        tipo, operacion, formato = instrucciones[op]
        opcode = opcodes[tipo]

        if tipo == 'system':
            bin_instr = opcode + operacion + '0' * 28

        elif tipo == 'arithmetic':
            imm_flag = '1' if 'I' in op else '0'
            if formato == 'R3R':
                rd, rs1, rs2 = map(lambda r: registros[r], args)
                bin_instr = opcode + operacion + imm_flag + rd + rs1 + rs2 + '0000' + '0'*8
            elif formato == 'R4R':
                rd, rs1, rs2, rs3 = map(lambda r: registros[r], args)
                bin_instr = opcode + operacion + '0' + rd + rs1 + rs2 + rs3 + '0'*8
            elif formato == 'RRI':
                rd, rs1, imm = args
                bin_instr = opcode + operacion + '1' + registros[rd] + registros[rs1] + bin_pad(imm, 16)
            elif formato == 'RI':
                rd, imm = args
                bin_instr = opcode + operacion + '1' + registros[rd] + '0000' + bin_pad(imm, 16)
            elif formato == 'R2R':
                rd, rs1 = map(lambda r: registros[r], args)
                bin_instr = opcode + operacion + '0' + rd + rs1 + '0000' + '0000' + '0'*8

        elif tipo == 'memory':
            rd = registros[args[0]]
            op_bit = operacion
            if formato == 'MM':
                rs1 = registros[args[1]]
                imm_flag = '0'
                imm = bin_pad(args[2] if len(args) > 2 else 0, 19)
            elif formato == 'MI':
                rs1 = '0000'
                imm_flag = '1'
                imm = bin_pad(args[1], 19)
            bin_instr = opcode + op_bit + imm_flag + rd + rs1 + imm

        elif tipo == 'control':
            target = args[0]

            try:
                # Si es un número (literal), lo usamos directo
                addr = int(target)
            except ValueError:
                # Si no, buscamos si es una etiqueta
                addr = etiquetas.get(target)
                if addr is None:
                    raise ValueError(f"Etiqueta '{target}' no encontrada en etiquetas")

            bin_instr = opcode + operacion + bin_pad(addr, 26)

        elif tipo == 'vault_key':
            ks = registros[args[0]]
            high = operacion
            imm = bin_pad(args[1], 16)
            bin_instr = opcode + ks + high + '0'*10 + imm

        elif tipo == 'vault_shift':
            op_bit = operacion
            rd = registros[args[0]]
            rs1 = registros[args[1]]
            ks = registros[args[2]]
            imm = bin_pad(args[3], 18)
            bin_instr = opcode + op_bit + rd + rs1 + ks + imm

        instrucciones_binarias.append(bin_instr)

    return instrucciones_binarias

