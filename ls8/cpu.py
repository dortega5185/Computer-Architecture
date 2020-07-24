"""CPU functionality."""


import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MULT = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.stack_pointer = 7
        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn
        self.branchtable[MULT] = self.mult
        self.branchtable[POP] = self.pop
        self.branchtable[PUSH] = self.push
        self.branchtable[CMP] = self.cmp
        self.branchtable[JMP] = self.jmp
        self.branchtable[JEQ] = self.jeq
        self.branchtable[JNE] = self.jne

        # self.hlt
        
        
    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, word):
        self.ram[pc]= word

    def load(self):
        """Load a program into memory."""

        import sys

        address = 0

        program = []
        with open(sys.argv[-1]) as f:
            for line in f:
                try:
                    line = line.split("#", 1)[0]
                    line = int(line, 2)
                    program.append(line)
                except ValueError:
                    pass

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            # print("MUL is going on", reg_a, reg_b)
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
                self.L = 0
                self.G = 0
            elif reg_a < reg_b:
                self.E = 0
                self.L = 1
                self.G = 0
            elif reg_a > reg_b:
                self.E = 0
                self.L = 0
                self.G = 1
            else:
                self.E = 0
                self.L = 0
                self.G = 0        
   
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def hlt(self): 
        self.running = False
    def ldi(self): 
        # register is program counter + 1
        register = self.ram[self.pc + 1]
        # print(register)
        # for integer value will be, program coutner + 2
        integer = self.ram[self.pc + 2]
        #save integer value at the register at the register specified
        self.reg[register] = integer
        self.pc +=3
        # print(self.reg, self.ram)   
        
    def prn(self): #PRN
        # print(self.reg)
        register = self.ram_read(self.pc + 1)  
        # print(register)             
        print(self.reg[register])
        self.pc +=2   
    def mult(self): #MULT
        # print(self.pc)
        reg_a = self.ram_read(self.pc + 1)
        # self.pc += 1
        reg_b = self.ram_read(self.pc + 2)
        
        self.alu("MUL", reg_a, reg_b)
        # print(reg_a,reg_b)
        self.pc += 3
    def pop(self): #POP
        targ_reg = self.ram[self.pc + 1]
        self.reg[targ_reg] = self.ram[self.reg[self.stack_pointer]]
        self.reg[self.stack_pointer] += 1
        # print("pop")
        self.pc += 2
    def push(self): #PUSH
        targ_reg = self.ram[self.pc + 1]
        #decrement the Stack Pointer
        self.reg[self.stack_pointer] -= 1
        self.ram[self.reg[self.stack_pointer]] = self.reg[targ_reg]
        self.pc += 2
        # print("push")        


    def cmp(self):
        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)

        self.alu("CMP", operand_a, operand_b)
        self.pc += 3
        
    def jmp(self):
        reg_num = self.ram[self.pc+1]
        addr = self.reg[reg_num]
        self.pc = addr
        
    def jeq(self):
        if self.E == 1:
            self.jmp()
        else:
            self.pc += 2
    def jne(self):
        if self.E == 0:
            self.jmp()
        else: self.pc += 2
        
    def run(self):
        """Run the CPU."""
        self.pc = 0
        self.running = True
        while self.running:
            ir = self.pc
            inst = self.ram[ir]
            self.branchtable[inst]()
# import sys
# ​
# memory = [0] * 256
# ​
# address = 0
# ​
# if len(sys.argv) != 2:
#     print("usage: comp.py filename")
#     sys.exit(1)
# ​
# try:
#     with open(sys.argv[1]) as f:
#         for line in f:
#             try:
#                 line = line.split("#",1)[0]
#                 line = int(line, 10)  # int() is base 10 by default
#                 memory[address] = line
#                 address += 1
#             except ValueError:
#                 pass
# ​
# except FileNotFoundError:
#     print(f"Couldn't find file {sys.argv[1]}")
#     sys.exit(1)
# ​
# register = [0] * 8
# ​
# pc = 0  # Program Counter, index into memory of the current instruction
#         # AKA a pointer to the current instruction
# ​
# fl = 0
# ​
# running = True
# ​
# while running:
#     inst = memory[pc]
# ​
#     if inst == 1:  # PRINT_BEEJ
#         print("Beej")
#         pc += 1
# ​
#     elif inst == 2:  # HALT
#         running = False
# ​
#     elif inst == 3:  # SAVE_REG
#         reg_num = memory[pc + 1]
#         value = memory[pc + 2]
# ​
#         register[reg_num] = value
# ​
#         pc += 3
# ​
#     elif inst == 4: # PRINT_REG
#         reg_num = memory[pc + 1]
#         print(register[reg_num])
# ​
#         pc += 2
# ​
#     else:
#         print(f"Unknown instruction {inst}")
#         running = False