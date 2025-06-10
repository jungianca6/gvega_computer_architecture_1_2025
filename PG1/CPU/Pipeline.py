from CPU.vault import Vault
import time


class Pipeline:
    def __init__(self, pc, instruction_memory, register_file, data_memory, alu, decoder, control_unit):
        self.pc = pc
        self.instruction_memory = instruction_memory
        self.register_file = register_file
        self.data_memory = data_memory
        self.alu = alu
        self.decoder = decoder
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

        self.if_instr = None
        self.id_instr = None
        self.ex_instr = None
        self.mem_instr = None
        self.wb_instr = None

        self.instrucciones_completadas = 0

    def fetch(self):
        """
        Etapa de Fetch: Obtiene la instrucción desde la memoria de instrucciones.
        """
        if self.if_id is None:
            instruction = self.instruction_memory.fetch(self.pc.value)
            self.if_instr = instruction  # Guardar la instrucción para el debug
            if instruction is not None:
                # print(f"Fetch: Instrucción {instruction:032b} en PC={self.pc.value}")
                self.if_id = {"instruction": instruction, "pc": self.pc.value, "instruction_pipeline": instruction}
                # print(f"[DEBUG] PC en fetch: 0x{self.pc.value}")
                self.pc.increment()

        return self.if_instr

    def decode(self):
        self.id_instr = self.if_instr
        if self.if_id and self.id_ex is None:
            if self.if_id["instruction"] is None:  # Verificar si es un estado de flush
                # print("Decode: Estado de flush detectado, no se procesa instrucción.")
                self.if_id = None
                return

            instruction = self.if_id["instruction"]
            decoded = self.decoder.decode(instruction)

            if 'error' in decoded:
                # print(f"Decode Error: {decoded['error']}")
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

            # print(f"Decode: PC={self.if_id['pc']}: Instrucción={instruction:032b} -> Decodificación={decoded}")

            # Actualizar el registro del pipeline para la etapa id_ex
            self.id_ex = {"decoded": decoded,
                          "control_signals": control_signals,
                          "pc": self.if_id["pc"],
                          "instruction_pipeline": decoded.get("instruction_pipeline", f"Instr {instruction:08x}")
                          }
            self.if_id = None

        return self.id_instr

    def execute(self):
        self.ex_instr = self.id_instr

        if self.id_ex and self.ex_mem is None:
            decoded = self.id_ex["decoded"]
            signals = self.id_ex["control_signals"]
            old_pc = self.id_ex["pc"]
            alu_result = 0  # Valor por defecto

            instruction_pipeline = self.id_ex["instruction_pipeline"]
            # print(f"Control Signals en execute {signals}")

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

            # Memoria
            elif decoded["type"] == "Memoria":
                if "imm" in decoded:
                    alu_result = decoded["imm"]  # Dirección directa
                else:
                    alu_result = self.alu.operate(rs1_val, 0, signals['ALUOp'])

            # Saltos (BEQ, BNE, etc.)
            elif decoded["type"] == "Control":
                if signals["Branch"]:
                    alu_result = 1 if rs1_val == rs2_val else 0
                    if alu_result == 1:  # Salto tomado
                        self.pc.set(decoded["imm"])
                        # print(f"Branch Taken: PC <- {decoded['imm']}")

            # Bóveda
            elif decoded["type"] == "VAULT":
                # Aquí sí usas tu Vault
                ks = decoded["ks"]
                h_l = decoded["hl"]
                immediate = decoded["immediate"]

                if h_l == 1:
                    self.vault.store_high(ks, immediate)
                else:
                    self.vault.store_low(ks, immediate)

                alu_result = 0  # No hace operación en ALU

            # Boveda - Shift
            elif decoded["type"] == "VAULT_SHIFT":
                ks = decoded["ks"]
                shift_amount = decoded["imm"]

                # Leer la llave actual (HIGH + LOW como 16 bits)
                high, low = self.vault.get_key(ks)

                # Combinar en 64 bits
                key_value = (high << 16) | low

                # Realizar el shift
                if decoded["name"] == "BSHL":
                    alu_temp = self.alu.operate(rs1_val, shift_amount, 0b0110)  # SHRI
                    alu_temp = self.alu.operate(alu_temp, key_value, 0b0001)  # ADD
                else:  # BSHR
                    alu_temp = self.alu.operate(rs1_val, shift_amount, 0b0111)  # SHLI
                    alu_temp = self.alu.operate(alu_temp, key_value, 0b0001)  # ADD

                alu_result = alu_temp

            # Escribir en ex_mem
            self.ex_mem = {
                "alu_result": alu_result,
                "decoded": decoded,
                "control_signals": signals,
                "instruction_pipeline": instruction_pipeline
            }
            self.id_ex = None

        return self.ex_instr

    def memory(self):
        self.mem_instr = self.ex_instr

        if self.ex_mem and self.mem_wb is None:
            decoded = self.ex_mem["decoded"]
            signals = self.ex_mem["control_signals"]
            alu_result = self.ex_mem["alu_result"]
            instruction_pipeline = self.ex_mem["instruction_pipeline"]

            # Operaciones de Memoria (LDR/STR)
            if decoded["type"] == "Memoria":
                if signals["MemRead"]:  # LDR/LDRI
                    mem_data = self.data_memory.read(alu_result)
                    self.mem_wb = {
                        "memory_data": mem_data,
                        "decoded": decoded,
                        "result": mem_data,  # Para writeback
                        "instruction_pipeline": instruction_pipeline
                    }
                    # print(f"Memory Read @ {alu_result}: {mem_data}")

                elif signals["MemWrite"]:  # STR/STRI
                    data = self.register_file.read(decoded["rs2"]) if "rs2" in decoded else 0
                    self.data_memory.write(alu_result, data)
                    self.mem_wb = {"decoded": decoded,
                                   "instruction_pipeline": instruction_pipeline}  # No hay writeback
                    # print(f"Memory Write @ {alu_result}: {data}")

            # Otras instrucciones (pasan el resultado de execute)
            else:
                self.mem_wb = {
                    "result": alu_result,  # Resultado de ALU o bóveda
                    "decoded": decoded,
                    "instruction_pipeline": instruction_pipeline
                }

            self.ex_mem = None
        return self.mem_instr

    def writeback(self):
        self.wb_instr = self.mem_instr

        if self.mem_wb:
            decoded = self.mem_wb["decoded"]
            instr_str = self.mem_wb.get("instruction_pipeline", "<unknown>")

            # Solo escribe si RegWrite está activo y hay un registro destino
            if self.mem_wb.get("control_signals", {}).get("RegWrite", 0) and "rd" in decoded:
                data = self.mem_wb.get("memory_data", self.mem_wb.get("result", 0))
                self.register_file.write(decoded["rd"], data)
                # print(f"Writeback: {instr_str} → R{decoded['rd']} = {data}")
            self.mem_wb = None

        return self.wb_instr

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

    def step(self):
        print(f"\nClock Cycle: {self.clock_cycle + 1}")
        wbInstr = self.writeback()
        memInstr = self.memory()
        exInstr = self.execute()
        idInstr = self.decode()
        ifInstr = self.fetch()
        self.clock_cycle += 1

        pipe_stages = {
            "IF": ifInstr,
            "ID": idInstr,
            "EX": exInstr,
            "MEM": memInstr,
            "WB": wbInstr
        }

        return pipe_stages, self.clock_cycle

    def is_pipeline_empty(self):
        instrucciones_terminadas = (
                self.pc.value >= len(self.instruction_memory.instructions) * 4
        )
        etapas_vacias = all(
            stage is None for stage in [self.if_id, self.id_ex, self.ex_mem, self.mem_wb]
        )
        return instrucciones_terminadas and etapas_vacias
