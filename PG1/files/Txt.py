import math
import os


def file_to_txt(input_file):
    output_file = os.path.join(os.path.dirname(os.getcwd()), "files/memory.txt")
    with open(input_file, "rb") as f_in, open(output_file, "w") as f_out:
        bytes_leidos = f_in.read()
        # Convierte cada byte a 2 dígitos hexadecimales
        hex_string = bytes_leidos.hex()
        # Guarda en el .txt en bloques de 8 (4 bytes) por línea
        for i in range(0, len(hex_string), 8):
            bloque = hex_string[i:i + 8]
            f_out.write(bloque + "\n")

    return None


def txt_to_mem(i):
    memoria = []
    mem_txt = os.path.join(os.path.dirname(os.getcwd()), "PG1/files/memory.txt")
    with open(mem_txt, "r") as file:
        lines = file.readlines()
    total_lines = len(lines)
    num_blocks = math.ceil(total_lines / 256)
    # Get the block starting at line i
    for line in lines[i:i+256]:
        hex_str = line.strip()
        if hex_str:
            valor = int(hex_str, 16)
            memoria.append(valor)
    return memoria, num_blocks


def mem_to_txt(i, memoria):
    mem_txt = os.path.join(os.path.dirname(os.getcwd()), "PG1/files/memory.txt")
    # Read all lines
    with open(mem_txt, "r") as file:
        lines = file.readlines()
    # Update the block
    for idx, val in enumerate(memoria):
        if i + idx < len(lines):
            lines[i + idx] = f"{val:08x}\n"
        else:
            lines.append(f"{val:08x}\n")
    # Write back
    with open(mem_txt, "w") as file:
        file.writelines(lines)


# in_file = os.path.join(os.path.dirname(os.getcwd()), "TEA/jorge_luis.txt")
# file_to_txt(in_file)
