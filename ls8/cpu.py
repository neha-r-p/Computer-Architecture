"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256 #holds values 0 to 255
        self.sp = 7 #number in reg reserved for sp
        self.reg[self.sp] = 0xF4 #start of empty stack
        self.fl = '00000LGE' #initial flag register


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def push(self, register): #Push the value in the given register on the stack.
        self.reg[self.sp] -= 1 #decrement pointer
        ram_address = self.reg[self.sp]
        self.ram[ram_address] = self.reg[register] #copy value of given reg into address pointed to by sp

    def pop(self, register):
        ram_address = self.reg[self.sp]
        self.reg[register] = self.ram[ram_address] #Copy the value from the address pointed to by SP to the given register.
        self.reg[self.sp] += 1 #Increment SP.

    def load(self, file):
        """Load a program into memory."""
        try:
            address = 0
            with open(file) as f:
                for line in f:
                    #ignore comments
                    comment_split = line.split('#')
                    num = comment_split[0].strip()

                    #ignore blank lines
                    if num == "":
                        continue

                    value = int(num, 2) # convert binary string to int using base 2

                    self.ram[address] = value
                    address += 1
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {file} not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1




    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

        elif op == "CMP":
            if reg_a == reg_b:
                self.fl = 0b00000001
            elif reg_a < reg_b:
                self.fl = 0b00000100
            elif reg_a > reg_b:
                self.fl = 0b00000010

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
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CMP = 0b10100111
        JMP = 0b01010100

        while running:
            ir = self.ram_read(self.pc)
            opcode = ir
            operand_a = self.ram_read(self.pc + 1) #if instruction needs 1 ahead
            operand_b = self.ram_read(self.pc + 2) #if instruction needs 2 ahead

            if opcode == HLT:
                running = False #exits the loop
                self.pc += 1

            elif opcode == LDI: #sets specified reg to specified value
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif opcode == PRN: #Print numeric value stored in the given register
                print(self.reg[operand_a])
                self.pc +=2

            elif opcode == MUL: # Multiply the values in two registers together and store the result in registerA.
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3

            elif opcode == PUSH:
                self.push(operand_a)
                self.pc += 2

            elif opcode == POP:
                self.pop(operand_a)
                self.pc += 2

            elif opcode == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3
            
            elif opcode == JMP:
                reg_address = self.ram[operand_a] #Jump to the address stored in the given register.
