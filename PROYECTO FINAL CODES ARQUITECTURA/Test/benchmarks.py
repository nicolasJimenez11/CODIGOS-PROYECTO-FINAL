from CPU.isa import Instruction

def load_program1():
    return [
        Instruction("LOAD", rd="R1", addr=0),
        Instruction("ADD", rd="R2", rs1="R1", rs2="R1"),
        Instruction("STORE", rs1="R2", addr=4),
        Instruction("IN", rd="R3"),
        Instruction("OUT", rs1="R3"),
    ]

def load_program2():
    return [
        Instruction("LOAD", rd="R1", addr=8),
        Instruction("MUL", rd="R2", rs1="R1", rs2="R1"),
        Instruction("STORE", rs1="R2", addr=12),
        Instruction("IN", rd="R4"),
        Instruction("OUT", rs1="R4"),
    ]

def load_program3():
    return [
        Instruction("LOAD", rd="R1", addr=16),
        Instruction("SUB", rd="R2", rs1="R1", rs2="R1"),
        Instruction("STORE", rs1="R2", addr=20),
        Instruction("IN", rd="R5"),
        Instruction("OUT", rs1="R5"),
        
    ]
def load_program4():
    return [
        Instruction("LOAD", rd="R1", addr=0),
        Instruction("ADD", rd="R2", rs1="R1", rs2="R1"),
        Instruction("MUL", rd="R3", rs1="R2", rs2="R1"),
        Instruction("SUB", rd="R4", rs1="R3", rs2="R2"),
        Instruction("ADD", rd="R5", rs1="R4", rs2="R1"),
        Instruction("MUL", rd="R6", rs1="R5", rs2="R2"),
        Instruction("SUB", rd="R7", rs1="R6", rs2="R3"),
        Instruction("STORE", rs1="R7", addr=24),
    ]