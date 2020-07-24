"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print('usage: comp.py + filename')
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        # print('her ', line)
                        line = line.split('#', 1)[0]
                        # print('her ', line)
                        line = int(line, 2)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f'Couldnt find file {sys.argv[1]}')
            sys.exit(1)


        for instruction in self.reg:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""
        running = True

        ops = {
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b00000001: 'HLT'

        }

        while running:
            inst = self.ram_read(self.pc)

            if ops[inst] == 'LDI':
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]

                self.reg[reg_num] = value

                self.pc += 3

            elif ops[inst] == 'PRN':
                reg_num = self.ram[self.pc + 1]
                print(self.reg[reg_num])

                self.pc += 2

            elif ops[inst] == 'HLT':
                running = False

            else:
                print(f'Unknown instruction {inst}')

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