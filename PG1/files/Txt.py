import hashlib
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

        total_lines = (len(hex_string) + 7) // 8
        padding_needed = (256 - (total_lines % 256)) % 256
        for _ in range(padding_needed):
            f_out.write("00000000\n")


def txt_to_file(output_file):
    input_file = os.path.join(os.path.dirname(os.getcwd()), "files/memory.txt")
    with open(input_file, "r") as f_in:
        hex_data = ""
        for line in f_in:
            hex_str = line.strip()
            if hex_str and hex_str != "00000000":
                hex_data += hex_str
    # Convert hex string to bytes
    bytes_data = bytes.fromhex(hex_data)
    with open(output_file, "wb") as f_out:
        f_out.write(bytes_data)


def txt_to_mem():
    memoria = []
    mem_txt = os.path.join(os.path.dirname(os.getcwd()), "PG1/files/memory.txt")
    with open(mem_txt, "r") as file:
        lines = file.readlines()
    for line in lines:
        hex_str = line.strip()
        if hex_str:
            valor = int(hex_str, 16)
            memoria.append(valor)
    return memoria


def mem_to_txt(memoria):
    mem_txt = os.path.join(os.path.dirname(os.getcwd()), "PG1/files/memory.txt")
    with open(mem_txt, "w") as file:
        for val in memoria:
            file.write(f"{val:08x}\n")


def md5_of_memory_txt():
    file_path = os.path.join(os.path.dirname(os.getcwd()), "files/memory.txt")
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


if __name__ == "__main__":
    in_file = os.path.join(os.path.dirname(os.getcwd()), "files/jorge_luis.txt")
    # file_to_txt(in_file)

    # md5 =  md5_of_memory_txt()
    # print(md5)
