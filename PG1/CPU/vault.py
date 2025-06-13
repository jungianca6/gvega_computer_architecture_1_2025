# === vault.py ===
# Modelo de la bóveda

class Vault:
    def __init__(self):
        # 4 llaves: cada una con parte high y low (32 bits cada parte)
        self.keys = {
            0: {"high": 0, "low": 0},
            1: {"high": 0, "low": 0},
            2: {"high": 0, "low": 0},
            3: {"high": 0, "low": 0},
        }

    def store_high(self, key_selector, value):
        self.keys[key_selector]["high"] = value
        # print(f"[Vault] Stored HIGH for K{key_selector} = {hex(value)}")

    def store_low(self, key_selector, value):
        self.keys[key_selector]["low"] = value
        # print(f"[Vault] Stored LOW for K{key_selector} = {hex(value)}")

    def get_key(self, key_selector):
        return (self.keys[key_selector]["high"], self.keys[key_selector]["low"])

    def debug_print(self):
        print("\n=== Vault State ===")
        for k, v in self.keys.items():
            print(f"K{k}: HIGH = {hex(v['high'])}, LOW = {hex(v['low'])}")
        print("===================\n")
