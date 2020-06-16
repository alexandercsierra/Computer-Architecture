"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001

    def load(self, program):
        """Load a program into memory."""

        with open(sys.argv[1]) as f:
            for address, instruction in enumerate(f):
                instruction = instruction.split('#')
                try:
                    ins = int(instruction[0],2)
                except ValueError:
                    continue

                self.ram_write(address, ins)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value

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
        while running:
            ir = self.ram[self.pc]
            if ir == self.LDI:
                reg_num = self.ram_read(self.pc+1)
                value = self.ram_read(self.pc+2)
                self.reg[reg_num] = value
                self.pc += 3
            elif ir == self.PRN:
                reg_num = self.ram_read(self.pc+1)
                print(self.reg[reg_num])
                self.pc +=2
            elif ir == self.HLT:
                running = False
                self.pc +=1
            else:
                print(f'Unkown instruction {ir} at address {self.pc}')
                print(self.ram_read(self.pc))
                sys.exit(1)