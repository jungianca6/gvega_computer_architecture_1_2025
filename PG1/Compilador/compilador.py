# compilador.py
import os

from Compilador.asm_parser import parsed_program
from Compilador.lexer import tokens
from Compilador.isa_traductor import traducir_instrucciones_a_binario


# Insertar NOPs por dependencias
def insertar_nops_por_dependencias(instrucciones_limpias):
    print("Instrucciones limpias:", instrucciones_limpias)
    def get_destinos(instr):
        op = instr[0]

        # Operaciones aritméticas (escriben en el primer operando)
        if op in ('MOV', 'MOVI', 'ADD', 'ADDI', 'SUB', 'SUBI',
                  'MUL', 'MULI', 'XOR', 'XORI', 'XOR3',
                  'SHL', 'SHR', 'BSHL', 'BSHR',
                  'LDR', 'LDRI'):
            return [instr[1]]

        # Comparaciones no escriben en ningún registro
        elif op in ('CMP', 'CMPI'):
            return []

        # STR, STRI, BSTRH, BSTRL no escriben en registros (solo memoria o bóveda)
        elif op in ('STR', 'STRI', 'BSTRH', 'BSTRL'):
            return []

        # Branches, saltos y NOP tampoco escriben en registros
        elif op in ('BEQ', 'BNE', 'BLT', 'BGT', 'JUMP', 'NOP', 'END'):
            return []

        # Por defecto, no asumimos que escribe
        return []

    def get_fuentes(instr):
        op = instr[0]

        # --- Aritméticas Reg-Registro ---
        if op in ('ADD', 'SUB', 'MUL', 'XOR'):
            return [instr[2], instr[3]]  # RS1, RS2
        elif op == 'XOR3':
            return [instr[2], instr[3], instr[4]]  # RS1, RS2, RS3
        elif op in ('SHL', 'SHR', 'CMP'):
            return [instr[1], instr[2]]  # RD (o comparado), RS1
        elif op == 'MOV':
            return [instr[2]]  # RS1

        # --- Aritméticas Reg-Inmediato ---
        elif op in ('ADDI', 'SUBI', 'MULI', 'XORI', 'SHLI', 'SHRI'):
            return [instr[2]]  # RS1
        elif op == 'MOVI':
            return []  # Solo inmediato, no fuente de registro
        elif op == 'CMPI':
            return [instr[1]]  # Registro comparado

        # --- Memoria ---
        elif op in ('LDR', 'STR'):
            return [instr[2]] if len(instr) == 3 else [instr[1]]  # Base address RS1
        elif op == 'LDRI':
            return []  # Solo inmediato
        elif op == 'STRI':
            return [instr[1]]  # R0 es la fuente

        # --- Bóveda (Key Shifts) ---
        elif op in ('BSHL', 'BSHR'):
            return [instr[1]]  # RS1

        # --- Branches y control ---
        elif op in ('BEQ', 'BNE', 'BLT', 'BGT'):
            return [instr[1]]  # Condición (Z, etc.)
        elif op == 'JUMP':
            return []  # Solo inmediato

        # --- Bóveda (Key Store) ---
        elif op in ('BSTRH', 'BSTRL'):
            return []  # Solo inmediato

        # --- NOP y END ---
        elif op in ('NOP', 'END'):
            return []

        # Por defecto
        return []

    instrucciones_finales = []

    for instr in instrucciones_limpias:
            # Insertar NOPs después de branches (BEQ/BNE/BLT/BGT/JUMP)
        if instr[0] in ('BEQ', 'BNE', 'BLT', 'BGT', 'JUMP'):
            instrucciones_finales.append(instr)
            instrucciones_finales.append(('NOP',))  # 1 NOP es suficiente en tu arquitectura
            continue

        fuentes = set(get_fuentes(instr))

        nops_a_insertar = 0
        for lookback in range(1, 4):
            if len(instrucciones_finales) < lookback:
                break
            instr_anterior = instrucciones_finales[-lookback]
            if instr_anterior[0] == 'NOP':
                continue
            destinos_anterior = set(get_destinos(instr_anterior))

            if fuentes & destinos_anterior:
                nops_necesarios = max(0, 4 - lookback)
                if nops_necesarios > nops_a_insertar:
                    nops_a_insertar = nops_necesarios

        for _ in range(nops_a_insertar):
            instrucciones_finales.append(('NOP',))

        instrucciones_finales.append(instr)
    print("Instrucciones finales:", instrucciones_finales)
    return instrucciones_finales


def compilar_programa(secciones_lista):
    parsed = {nombre: contenido for nombre, contenido in secciones_lista}

    vault_section = parsed.get('.vault', [])
    data_section = parsed.get('.data', [])
    text_section = parsed.get('.text', [])

    memoria_instrucciones = []
    memoria_datos = {}
    etiquetas = {}
    tabla_variables = {}
    direccion_actual = 0

    # 1. Expandir la sección .vault
    if vault_section:
        tipo, nombre, valores = vault_section[0]
        if tipo == 'word':
            for i, val in enumerate(valores):
                k = f'K{i}'
                parte_alta = (val >> 16) & 0xFFFF
                parte_baja = val & 0xFFFF
                memoria_instrucciones.append(('BSTRH', k, f'#{parte_alta}'))
                memoria_instrucciones.append(('BSTRL', k, f'#{parte_baja}'))
                direccion_actual += 2

    # 2. Asignar direcciones a .data
    direccion_datos = 0x0000

    for item in data_section:
        if isinstance(item, tuple):
            tipo, nombre, valores = item

            if tipo == 'word':
                size = valores[0]
                tabla_variables[nombre] = direccion_datos
                for _ in range(size):
                    memoria_datos[direccion_datos] = 0
                    direccion_datos += 4

    # 3. Procesar sección .text y recolectar etiquetas
    instrucciones_con_etiquetas = memoria_instrucciones.copy()
    for item in text_section:
        if isinstance(item, str):
            etiquetas[item] = direccion_actual
        else:
            instrucciones_con_etiquetas.append(item)
            direccion_actual += 1

    # 4. Función para limpiar argumentos
    def limpiar_argumentos(instr):
        nuevo = [instr[0]]
        for arg in instr[1:]:
            if isinstance(arg, str):
                if arg in {',', '='}:
                    continue
                if arg.startswith('#'):
                    try:
                        nuevo.append(int(arg[1:]))
                    except ValueError:
                        nuevo.append(arg)
                else:
                    nuevo.append(arg)
            else:
                nuevo.append(arg)
        return tuple(nuevo)

    instrucciones_limpias = [limpiar_argumentos(instr) for instr in instrucciones_con_etiquetas]

    # 5. Insertar NOPs por dependencias
    instrucciones_limpias = insertar_nops_por_dependencias(instrucciones_limpias)

    # 6. Actualizar etiquetas en las instrucciones limpias
    etiquetas_actualizadas = {}
    indice_actual = 0  # posición en instrucciones_limpias

    for item in text_section:
        if isinstance(item, str):
            # Es una etiqueta, guardamos la dirección actual
            etiquetas_actualizadas[item.rstrip(':')] = indice_actual
        else:
            # Es una instrucción real, avanzamos en instrucciones_limpias hasta que la encontremos
            while instrucciones_limpias[indice_actual] != limpiar_argumentos(item):
                indice_actual += 1
            indice_actual += 1

    # 7. Reemplazar referencias de etiquetas en las instrucciones
    instrucciones_finales = []
    for instr in instrucciones_limpias:
        if isinstance(instr, str):  # Por si quedó alguna etiqueta
            continue
        opcode = instr[0]
        argumentos = list(instr[1:])
        for i, arg in enumerate(argumentos):
            if isinstance(arg, str):
                if arg in tabla_variables:
                    argumentos[i] = f'{tabla_variables[arg]}'
                elif arg in etiquetas_actualizadas:
                    argumentos[i] = f'{etiquetas_actualizadas[arg]}'
        instrucciones_finales.append((opcode, *argumentos))

    return instrucciones_finales


def compilar(filename="files/isa_code.txt"):
    with open(filename, "r") as f:
        data = f.read()

    secciones = parsed_program(data)
    instrucciones = compilar_programa(secciones)
    inst_binarias = traducir_instrucciones_a_binario(instrucciones)

    # Guardar el resultado en un archivo, tal y como está cada instrucción
    file_compilated = os.path.join(os.path.dirname(os.getcwd()), "PG1/Compilador/compilacion_sin_binario.txt")
    with open(file_compilated, "w") as f:
        for instr in instrucciones:
            f.write(' '.join(map(str, instr)) + '\n')

    # Guardar el resultado binario en un archivo
    file_compi_binary = os.path.join(os.path.dirname(os.getcwd()), "PG1/Compilador/mem_instructions.txt")
    with open(file_compi_binary, "w") as f:

        #Versión con bloques de 8 bits, para facilitar la lectura
        for instr in inst_binarias:
            # Dividir en bloques de 8 bits
            bloques = [instr[i:i + 8] for i in range(0, len(instr), 8)]
            f.write(' '.join(bloques) + '\n')

        ##Versión sin espacios
        #for instr in inst_binarias:
        #    f.write(instr + '\n')

    return inst_binarias


if __name__ == "__main__":
    filepath = os.path.join(os.path.dirname(os.getcwd()), "tea_encrypt.txt")
    instrucciones = compilar(filepath)

    print("=== Memoria de Instrucciones ===")
    for i, instr in enumerate(instrucciones):
        print(f"{i:03X}: {instr}")
