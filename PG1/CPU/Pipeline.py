from vault import Vault
import time

class Pipeline:
    def __init__(self, pc, instruction_memory, register_file, data_memory, alu, decoder, extend, control_unit):
        self.pc = pc
        self.instruction_memory = instruction_memory
        self.register_file = register_file
        self.data_memory = data_memory
        self.alu = alu
        self.decoder = decoder
        self.extend = extend
        self.control_unit = control_unit
        self.vault = Vault()

        # Inicializar las etapas del pipeline como vacías
        self.fetch_stage = None
        self.decode_stage = None
        self.execute_stage = None
        self.memory_stage = None
        self.writeback_stage = None

        self.latency = {
            "IF": 0.1 * 1e-12,  # 0.1 segundos en picosegundos
            "ID": 0.1 * 1e-12,  # 0.1 segundos en picosegundos
            "EX": 0.2 * 1e-12,  # 0.2 segundos en picosegundos
            "MEM": 0.3 * 1e-12,  # 0.3 segundos en picosegundos
            "WB": 0.1 * 1e-12  # 0.1 segundos en picosegundos
        }

        self.stage_timestamps = {
            "IF": 0,
            "ID": 0,
            "EX": 0,
            "MEM": 0,
            "WB": 0
        }

        self.clock_cycle = 0
        self.if_id = None
        self.id_ex = None
        self.ex_mem = None
        self.mem_wb = None

        self.instrucciones_completadas = 0

    def fetch(self):
        """
        Etapa de Fetch: Obtiene la instrucción desde la memoria de instrucciones.
        """
        if self.if_id is None:
            instruction = self.instruction_memory.fetch(self.pc.value)
            if instruction is not None:
                print(f"Fetch: Instrucción {instruction:032b} en PC={self.pc.value}")
                self.if_id = {"instruction": instruction, "pc": self.pc.value, "instruction_pipeline": instruction}
                print(f"[DEBUG] PC en fetch: 0x{self.pc.value}")
                self.pc.increment()

    def decode(self):
        if self.if_id and self.id_ex is None:
            if self.if_id["instruction"] is None:  # Verificar si es un estado de flush
                print("Decode: Estado de flush detectado, no se procesa instrucción.")
                self.if_id = None
                return

            instruction = self.if_id["instruction"]
            decoded = self.decoder.decode(instruction)

            if 'error' in decoded:
                print(f"Decode Error: {decoded['error']}")
                self.if_id = None
                return

            # Incluir la instrucción original en el diccionario decodificado
            decoded['instruction'] = instruction

            self.control_unit.generateSignals(
                opcode=decoded["opcode"],
                instruction_type=decoded["type"],  # Ej: "Aritmetica (R-R)", "Memoria", etc.
                instruction_name=decoded["name"]  # Ej: "ADD", "MOVI", "BEQ"
            )

            # Extraer señales de control como diccionario
            control_signals = self.extract_control_signals()

            print(f"Decode: PC={self.if_id['pc']}: Instrucción={instruction:032b} -> Decodificación={decoded}")

            # Actualizar el registro del pipeline para la etapa id_ex
            self.id_ex = {"decoded": decoded,
                          "control_signals": control_signals,
                          "pc": self.if_id["pc"]}
            self.if_id = None

    def execute(self):
        if self.id_ex and self.ex_mem is None:
            decoded = self.id_ex["decoded"]
            signals = self.id_ex["control_signals"]
            pc = self.id_ex["pc"]

            instruction_pipeline = self.id_ex["instruction_pipeline"]
            print(f"Control Signals en execute {signals}")

            # Leer registros (si existen)
            rs1_val = self.register_file.read(decoded["rs1"]) if "rs1" in decoded else 0
            rs2_val = self.register_file.read(decoded["rs2"]) if "rs2" in decoded else 0
            rs3_val = self.register_file.read(decoded["rs3"]) if "rs3" in decoded else 0

            # Operaciones Aritméticas
            if "Aritmetica" in decoded["type"]:
                imm = decoded.get("imm", 0)  # Inmediato ya extendido por el compilador
                alu_result = self.alu.operate(
                    rs1_val,
                    rs2_val if "(R-R)" in decoded["type"] else imm,  # Usa RS2 o inmediato
                    signals["ALUOp"],
                    rs3_val if decoded["name"] == "XOR3" else None
                )

                # Saltos (BEQ, JUMP, etc.)
            elif decoded["type"] == "Control":
                alu_result = 1 if rs1_val == rs2_val else 0  # Para BEQ/BNE
                if signals["Branch"] and alu_result == 1:  # Salto tomado
                    self.pc.set(decoded["imm"])  # Dirección absoluta


            self.ex_mem = {
                "alu_result": alu_result,
                "decoded": decoded,
                "control_signals": signals
            }
            self.id_ex = None

            if decoded["type"] == "VAULT":
                # Aquí sí usas tu Vault
                ks = decoded["ks"]
                h_l = decoded["hl"]
                immediate = decoded["immediate"]

                if h_l == 1:
                    self.vault.store_high(ks, immediate)
                else:
                    self.vault.store_low(ks, immediate)

                alu_result = 0  # No hace operación en ALU
            
            elif decoded["type"] == "VAULT_SHIFT":
                ks = decoded["ks"]
                shift_amount = decoded["imm"]

                # Leer la llave actual (HIGH + LOW como 128 bits)
                high, low = self.vault.get_key(ks)

                # Combinar en 128 bits
                key_value = (high << 64) | low

                # Realizar el shift
                if decoded["name"] == "BSHL":
                    shifted = (key_value << shift_amount) & ((1 << 128) - 1)  # Mantener 128 bits
                else:  # BSHR
                    shifted = key_value >> shift_amount

                # Separar en HIGH y LOW de nuevo
                new_high = (shifted >> 64) & 0xFFFFFFFFFFFFFFFF
                new_low = shifted & 0xFFFFFFFFFFFFFFFF

                # Guardar en la bóveda usando store_high / store_low
                self.vault.store_high(ks, new_high)
                self.vault.store_low(ks, new_low)

                print(f"[Vault] Shift {'LEFT' if decoded['name']=='BSHL' else 'RIGHT'} K{ks}: amount={shift_amount}")
                print(f"[Vault] New HIGH: {hex(new_high)}, New LOW: {hex(new_low)}")

                alu_result = 0  # No hay resultado ALU


            print(f"ALU Result: {alu_result}")
            print(f"[Execute] ALU Result: {alu_result}, Control Signals: {signals}")

            # Escribir en ex_mem
            self.ex_mem = {
                "alu_result": alu_result,
                "decoded": decoded,
                "control_signals": signals
            }
            self.id_ex = None

    def memory(self):
        if self.ex_mem and self.mem_wb is None:
            decoded = self.ex_mem["decoded"]
            control_signals = self.ex_mem["control_signals"]
            alu_result = self.ex_mem["alu_result"]
            instruction_pipeline = self.ex_mem["instruction_pipeline"]

            if control_signals['MemRead']:
                memory_data = self.data_memory.read(alu_result)
                print(f"Memory read: Dirección={alu_result}, Valor={memory_data}")
                self.mem_wb = {"memory_data": memory_data, "decoded": decoded,
                               "instruction_pipeline": instruction_pipeline}
            elif control_signals['MemWrite']:
                if "rs2" in decoded:
                    data_to_write = self.register_file.read(decoded["rs2"])
                    self.data_memory.write(alu_result, data_to_write)
                    print(f"Memory write: Escritura en dirección={alu_result}, valor={data_to_write}")
                self.mem_wb = {"decoded": decoded, "instruction_pipeline": instruction_pipeline}
            else:
                self.mem_wb = {"alu_result": alu_result, "decoded": decoded,
                               "instruction_pipeline": instruction_pipeline}

            self.ex_mem = None

    def writeback(self):
        if self.mem_wb:
            decoded = self.mem_wb["decoded"]
            instruction_pipeline = self.mem_wb.get("instruction_pipeline")

            # Si es instrucción de bóveda o shift, no realiza escritura
            if decoded["type"] in ["VAULT", "VAULT_SHIFT"]:
                print("WriteBack: No se realizó escritura (instrucción de bóveda o shift).")
            else:
                # Verificar si la instrucción actual tiene un destino válido (rd)
                if "rd" in decoded and decoded["rd"] is not None:
                    # Manejar escritura para LW
                    if "memory_data" in self.mem_wb and decoded["name"] == "LW":
                        self.register_file.write(decoded["rd"], self.mem_wb["memory_data"])
                        print(f"WriteBack (LW): Escrito {self.mem_wb['memory_data']} en R{decoded['rd']}")

                    # Manejar escritura para ADD o instrucciones tipo R
                    elif "alu_result" in self.mem_wb and decoded["name"] == "ADD":
                        self.register_file.write(decoded["rd"], self.mem_wb["alu_result"])
                        print(f"WriteBack (ADD): Escrito {self.mem_wb['alu_result']} en R{decoded['rd']}")

                    # Escritura general para cualquier otra instrucción con `alu_result`
                    elif "alu_result" in self.mem_wb:
                        self.register_file.write(decoded["rd"], self.mem_wb["alu_result"])
                        print(f"WriteBack: Escrito {self.mem_wb['alu_result']} en R{decoded['rd']}")
                else:
                    print("WriteBack: No se realizó escritura (instrucción sin registro destino).")

            # Registrar la etapa de writeback para interfaz o depuración
            self.writeback_stage = {"instruction_pipeline": instruction_pipeline}
            # Limpiar mem_wb para la siguiente instrucción
            self.mem_wb = None
        else:
            self.writeback_stage = None  # Para mantener la interfaz coherente


    def no_op_instruction(self):
        return {
            'opcode': 0,
            'funct3': 0,
            'funct7': 0,
            'type': 'NOP',
            'name': 'NOP',
            'rd': None,
            'rs1': None,
            'rs2': None,
            'imm': 0,
            'instruction': 0,
        }

    def default_control_signals(self):
        """
        Retorna un diccionario con valores neutros para todas las señales de control.
        Esto se utiliza para manejar NOPs.
        """
        return {
            'RegWrite': 0,
            'MemRead': 0,
            'MemWrite': 0,
            'ALUOp': 0,
            'Branch': 0,
            'Jump': 0,
            'MemToReg': 0,
            'ALUSrc': 0,
            'PCSrc': 0,
            'PCWrite': 1
        }

    def extract_control_signals(self):
        """
        Extrae los valores actuales de las señales de control en `ControlUnit`
        y los convierte en un diccionario.
        """
        return {
            'RegWrite': self.control_unit.RegWrite,
            'MemRead': self.control_unit.MemRead,
            'MemWrite': self.control_unit.MemWrite,
            'ALUOp': self.control_unit.ALUOp,
            'Branch': self.control_unit.Branch,
            'Jump': self.control_unit.Jump,
            'MemToReg': self.control_unit.MemToReg,
            'ALUSrc': self.control_unit.ALUSrc,
            'PCSrc': self.control_unit.PCSrc,
            'PCWrite': self.control_unit.PCWrite
        }
