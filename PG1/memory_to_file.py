import os

def memory_to_file(input_path='files/memory.txt', output_path='output.bin'):
    if not os.path.exists(input_path):
        print(f"El archivo '{input_path}' no existe.")
        return

    bytes_list = []

    with open(input_path, 'r') as infile:
        for line in infile:
            hex_str = line.strip()
            # Ignorar palabras completamente en cero
            if hex_str == '00000000':
                continue
            # Validar que sea una palabra hexadecimal de 32 bits
            if len(hex_str) == 8:
                try:
                    bytes_out = bytes.fromhex(hex_str)
                    bytes_list.append(bytes_out)
                except ValueError:
                    print(f"Línea inválida (no hexadecimal): {hex_str}")
            else:
                print(f"Línea ignorada (longitud inválida): {hex_str}")

    # Unir todos los bytes y eliminar ceros al final
    all_bytes = b''.join(bytes_list).rstrip(b'\x00')

    with open(output_path, 'wb') as outfile:
        outfile.write(all_bytes)

    print(f"Archivo binario generado sin palabras nulas ni padding final: {output_path}")

if __name__ == "__main__":
    memory_to_file()
