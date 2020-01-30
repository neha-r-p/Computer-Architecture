"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256 #holds values 0 to 255

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


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

        #opcodes
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111

        while running:
            ir = self.ram_read(self.pc)
            opcode = ir
            operand_a = self.ram_read(self.pc + 1) #if instruction needs 1 ahead
            operand_b = self.ram_read(self.pc + 2) #if instruction needs 2 ahead

            if opcode == HLT:
                running = False #exits the loop
                self.pc += 1

            if opcode == LDI: #sets specified reg to specified value
                self.reg[operand_a] = operand_b
                self.pc += 3

            if opcode == PRN: #Print numeric value stored in the given register
                print(self.reg[operand_a])
                self.pc +=2 
