from memoria.cache import Cache
from CPU.isa import Instruction

class Pipeline:
    def __init__(self, program, cache_type="direct", cache_lines=8, block_size=4, associativity=1):
        self.program = program
        self.pc = 0
        self.cycles = 0
        self.halted = False
        self.registers = [0 for _ in range(8)]
        self.memory = [0] * 256
        self.stall = False

        # Pipeline registers
        self.IF = {"instr": None, "pc": 0}
        self.ID = {"instr": None}
        self.EX = {"instr": None}
        self.MEM = {"instr": None}
        self.WB = {"instr": None}

        # Caché real
        self.cache = Cache(size=cache_lines*block_size, block_size=block_size, associativity=associativity)

        # E/S e interrupciones
        self.io_stats = {"io_reads": 0, "io_writes": 0, "interrupts": 0}
        self.interrupt_pending = False
        self.interrupt_cycle = 10  # Simula una interrupción en el ciclo 10

    def _get_forwarded_value(self, reg_idx, stage_instrs):
        for stage in stage_instrs:
            instr = stage["instr"]
            if instr and hasattr(instr, "rd"):
                rd = int(instr.rd[1]) if instr.rd.startswith("R") else int(instr.rd)
                if rd == reg_idx and hasattr(instr, "result"):
                    return instr.result
        return None

    def run_cycle(self):
        # WB
        instr = self.WB["instr"]
        if instr:
            if instr.op in ("ADD", "SUB", "MUL", "LOAD"):
                rd = int(instr.rd[1]) if instr.rd.startswith("R") else int(instr.rd)
                self.registers[rd] = instr.result
            elif instr.op == "IN":
                rd = int(instr.rd[1]) if instr.rd.startswith("R") else int(instr.rd)
                self.registers[rd] = 42  # Simula lectura de dispositivo
                self.io_stats["io_reads"] += 1
            elif instr.op == "OUT":
                self.io_stats["io_writes"] += 1
            elif instr.op == "INT":
                print(f"Interrupción atendida en ciclo {self.cycles}")
                self.io_stats["interrupts"] += 1
        self.WB["instr"] = None

        # MEM
        instr = self.MEM["instr"]
        if instr:
            if instr.op == "LOAD":
                instr.result = self.cache.read(instr.addr, self.memory)
            elif instr.op == "STORE":
                idx = int(instr.rs1[1]) if instr.rs1.startswith("R") else int(instr.rs1)
                self.cache.write(instr.addr, self.registers[idx], self.memory)
            self.WB["instr"] = instr
        self.MEM["instr"] = None

        # EX (con forwarding)
        instr = self.EX["instr"]
        if instr:
            if instr.op in ("ADD", "SUB", "MUL"):
                rs1 = int(instr.rs1[1]) if instr.rs1.startswith("R") else int(instr.rs1)
                rs2 = int(instr.rs2[1]) if instr.rs2.startswith("R") else int(instr.rs2)
                # Forwarding desde MEM y WB
                val_rs1 = self._get_forwarded_value(rs1, [self.MEM, self.WB])
                val_rs2 = self._get_forwarded_value(rs2, [self.MEM, self.WB])
                v1 = val_rs1 if val_rs1 is not None else self.registers[rs1]
                v2 = val_rs2 if val_rs2 is not None else self.registers[rs2]
                if instr.op == "ADD":
                    instr.result = v1 + v2
                elif instr.op == "SUB":
                    instr.result = v1 - v2
                elif instr.op == "MUL":
                    instr.result = v1 * v2
            self.MEM["instr"] = instr
        self.EX["instr"] = None

        # ID (hazard detection y stalling)
        instr = self.ID["instr"]
        if instr:
            hazard = False
            if instr.op in ("ADD", "SUB", "MUL", "LOAD", "STORE"):
                sources = []
                if hasattr(instr, "rs1"):
                    sources.append(int(instr.rs1[1]) if instr.rs1.startswith("R") else int(instr.rs1))
                if hasattr(instr, "rs2"):
                    sources.append(int(instr.rs2[1]) if instr.rs2.startswith("R") else int(instr.rs2))
                for stage in [self.EX, self.MEM, self.WB]:
                    prev = stage["instr"]
                    if prev and hasattr(prev, "rd"):
                        rd = int(prev.rd[1]) if prev.rd.startswith("R") else int(prev.rd)
                        if rd in sources:
                            hazard = True
            if hazard:
                self.stall = True
                return
            else:
                self.stall = False
                self.EX["instr"] = instr
        self.ID["instr"] = None

        # IF (con interrupción)
        if self.cycles == self.interrupt_cycle and not self.interrupt_pending:
            self.interrupt_pending = True

        if self.interrupt_pending:
            self.ID["instr"] = Instruction("INT")
            self.IF["instr"] = None
            self.interrupt_pending = False
        elif self.pc < len(self.program):
            instr = self.program[self.pc]
            self.ID["instr"] = instr
            self.IF["instr"] = instr
            self.IF["pc"] = self.pc
            self.pc += 1
        else:
            self.ID["instr"] = None
            self.IF["instr"] = None

        # Halt si todas las etapas están vacías
        if not any([self.IF["instr"], self.ID["instr"], self.EX["instr"], self.MEM["instr"], self.WB["instr"]]):
            self.halted = True

        self.cycles += 1