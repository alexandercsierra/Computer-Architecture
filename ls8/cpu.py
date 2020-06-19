"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0,0,0,0,0,0,0,0xf4]
        self.ram = [0] * 256
        self.pc = 0
        self.running = False
        self.sp = 7
        self.flag = 0b00000000
        self.skip_commands = [0b01010000, 0b00010001, 0b01010101, 0b01010110, 0b01010100]
        self.branch_table = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MULT,
            0b10100000: self.ADD,
            0b01100101: self.INC,
            0b01100110: self.DEC,
            0b10000100: self.ST,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE,
            0b01001000: self.PRA,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b01010010: self.INT,
            0b00010011: self.IRET,
            0b00000001: self.HLT
        }


    def LDI(self):
        reg_num = self.ram_read(self.pc+1)
        value = self.ram_read(self.pc+2)
        self.reg[reg_num] = value

    def PRN(self):
        reg_num = self.ram_read(self.pc+1)
        print(self.reg[reg_num])

    def HLT(self):
        self.running = False

    def MULT(self):
        self.alu('MULT', self.pc+1, self.pc+2)

    def ADD(self):
        self.alu('ADD', self.pc+1, self.pc+2)

    def DEC(self):
        self.alu('DEC', self.pc+1, None)

    def INC(self):
        self.alu('INC', self.pc+1, None)
    
    def CMP(self):
        self.alu('CMP', self.pc+1, self.pc+2)
    
    def JEQ(self):
        if self.flag == 0b00000001:
            reg_num = self.ram[self.pc+1]
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2

    def JNE(self):
        if self.flag != 0b00000001:
            reg_num = self.ram[self.pc+1]
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2

    def PUSH(self):
        #decrement register at SP
        self.reg[self.sp] -=1
        #get value from next entry in memory
        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]
        #store it appropriately
        self.ram[self.reg[self.sp]] = value
    
    def POP(self):
        address = self.reg[self.sp]
        value = self.ram[address]
        #go to register listed next in ram
        self.reg[self.ram[self.pc +1 ]] = value
        #increment sp
        self.reg[self.sp] +=1

    def CALL(self):
        return_address = self.pc + 2

        self.reg[self.sp] -=1
        self.ram[self.reg[self.sp]] = return_address

        reg_num = self.ram[self.pc+1]
        destination = self.reg[reg_num]
        self.pc = destination

    def RET(self):
        return_address = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

        self.pc = return_address

    def INT(self):
        pass


    def IRET(self):
        pass
    
    def ST(self):
        reg_a = self.ram[self.pc +1]
        reg_b = self.ram[self.pc +2]

        reg_b_val = self.reg[reg_b]
        self.ram[self.reg[reg_a]] = reg_b_val

    def JMP(self):
        reg_addr = self.ram[self.pc+1]
        self.pc = self.reg[reg_addr]

    def PRA(self):
        reg_addr = self.ram[self.pc+1]
        num = self.reg[reg_addr]
        print(chr(num))

    def load(self):
        """Load a program into memory."""
        address = 0
        with open(sys.argv[1]) as f:
            for instruction in f:
                instruction = instruction.split('#')
                try:
                    ins = int(instruction[0], 2)
                    self.ram_write(address, ins)
                    address += 1
                except ValueError:
                    continue
                
                


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[self.ram[reg_a]] += self.reg[self.ram[reg_b]]
        elif op == "MULT":
            self.reg[self.ram[reg_a]] *= self.reg[self.ram[reg_b]]
        elif op == "CMP":
            value_a = self.reg[self.ram[reg_a]] 
            value_b = self.reg[self.ram[reg_b]]

            if value_a == value_b:
                self.flag = 0b00000001
            elif value_a < value_b:
                self.flag = 0b00000100
            elif value_a > value_b:
                self.flag = 0b00000010
        elif op == "DEC":
            self.reg[reg_a] -= 1
        elif op == "INC":
            self.reg[reg_a] += 1
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
        self.running = True
        while self.running:
            # print('pc', self.pc)
            # print('sp', self.ram[self.reg[self.sp]])
            ir = self.ram[self.pc]
            if ir not in self.branch_table:
                print(f'Unknown instruction {ir} at address {self.pc}')
                
                sys.exit(1)
            self.branch_table[ir]()
            params = (ir & 0b11000000) >> 6
            if ir not in self.skip_commands:
                self.pc += params + 1
                
           
