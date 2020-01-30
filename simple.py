import sys

PRINT_BEEJ = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4
PRINT_REGISTER = 5
ADD = 6

memory = [
    PRINT_BEEJ,
    SAVE, #saves the value
    65,
    2, #register number to save to
    SAVE,
    20,
    3,
    ADD, #ADD r2 += r3
    2,
    3 ,
    PRINT_REGISTER,
    2,
    HALT
]

register = [0] * 8


pc = 0 #program counter
running = True

while running:
    #execute instructions in memory

    command = memory[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1

    elif command == PRINT_NUM:
        num = memory[pc+1]
        print(num)
        pc += 2

    elif command == HALT:
        running = False
        pc += 1

    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3
    
    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3

    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2
    
    else:
        print(f"Error unknown command: {command}")
        sys.exit(1)
        pc += 1


