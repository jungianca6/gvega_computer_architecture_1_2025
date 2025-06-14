from files.Txt import txt_to_mem, mem_to_txt


def tea_encrypt_block(v, k, num_rounds=32):
    v0, v1 = v
    delta = 0x9e3779b9
    sum = 0
    for _ in range(num_rounds):
        sum = (sum + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]))) & 0xFFFFFFFF
        print(f"Round {_ + 1}: v0 = {v0:08x}, v1 = {v1:08x}, sum = {sum:08x}")
    return v0, v1


def apply_tea_to_memory(key):
    memoria = txt_to_mem()
    # Encrypt each pair of 32-bit words
    for i in range(0, len(memoria) - 1, 2):
        v = (memoria[i], memoria[i + 1])
        v0, v1 = tea_encrypt_block(v, key)
        memoria[i], memoria[i + 1] = v0, v1
    mem_to_txt(memoria)


# Example usage:
# key = [0x01234567, 0x89abcdef, 0xfedcba98, 0x76543210]
# apply_tea_to_memory(key)

if __name__ == "__main__":
    # Example key for TEA encryption
    key = [0xdeadbeef, 0xdeadbeef, 0xdeadbeef, 0xdeadbeef]
    apply_tea_to_memory(key)
    print("TEA encryption applied to memory.txt")
