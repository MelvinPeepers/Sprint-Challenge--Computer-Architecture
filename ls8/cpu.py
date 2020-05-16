"""CPU functionality."""
# LambdaSchool-8 computer

import sys

# found these in the program = []
HLT = 0b00000001  # 1 - Step 4 Add the HLT instruction definition
# 130 Step 5 Add the LDI instruction See the LS-8 spec for the details of what this instructions does and its opcode value.
LDI = 0b10000010  # 130
PRN = 0b01000111  # 71 - Step 6 Add the PRN instruction

ADD = 0b10100000  # 160
SUB = 0b10100001  # 161
MUL = 0b10100010  # 162
DIV = 0b10100011  # 163

POP = 0b01000110  # 70
PUSH = 0b01000101  # 69
CALL = 0b01010000  # 80
RET = 0b00010001  # 17

CMP = 0b10100111  # 167
JMP = 0b01010100  # 84
JEQ = 0b01010101  # 85
JNE = 0b01010110  # 86
# Doubled checked this numbers to ensure they are correct

SP = 7  # register location that holds top of stack address
# store the top of memory into Register 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Step 1 add list properties to the CPU class to hold 256 bytes of memory
        # and 8 general-purpose registers. Also add properties for any internal
        # registers you need, e.g. PC
        self.ram = [0] * 256  # memory
        self.reg = [0] * 8  # register
        self.pc = 0
        #self.reg[SP] = len(self.ram) - 1

        # Step 2
        # You don't need to add the MAR or MDR to your CPU class,
        # but they would make handy parameter names for ram_read()
        # and ram_write(), if you wanted.
    def ram_read(self, mar):
        # Step 2 should accept the address to read and return the value stored there.
        # The MAR contains the address that is being read or written to
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        # Step 2 should accept a value to write, and the address to write it to.
        # The MDR contains the data that was read or the data to write.
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""
        # reset the memory
        address = 0
        # get the filename from arguments
        # print('starting step 7')
        print(sys.argv[0])
        print(sys.argv[1])

        if len(sys.argv) != 2:
            print("Need proper file name passed")
            sys.exit(1)

        filename = sys.argv[1]
        with open(filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()
                # print(line)
                if line == "":
                    continue

                self.ram[address] = int(line, 2)
                address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #    # From print8.ls8
        #    0b10000010,  # LDI R0,8
        #    0b00000000,
        #    0b00001000,
        #    0b01000111,  # PRN R0
        #    0b00000000,
        #    0b00000001,  # HLT
        # ]

        # for instruction in program:
        #    self.ram[address] = instruction
        #    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":  # subtract
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":  # multiply
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":  # division
            self.reg[reg_a] /= self.reg[reg_b]

        elif op == "CMP":
            """
            Compare the values in two registers.

            If they are equal, set the Equal E flag to 1, otherwise set it to 0.

            If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.

            If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
            """
            # FL bits: 00000LGE
            # L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise. 00000100
            # G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.00000010
            # E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise. 00000001

            # if reg_a is equal to reg_b 00000001
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001

            # if reg_a is less then reg_b 00000100
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100

            # if reg_a is greater then to reg_b 00000010
            if self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # needs to read the memory address that's stored in register PC,
        # and store that result in IR, the Instruction Register. This can
        # just be a local variable in run().

        running = True

        while running:
            ir = self.ram[self.pc]  # similiar to command = memory[pc]
            # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into
            # variables operand_a and operand_b in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif ir == HLT:
                running = False
                self.pc += 1

            elif ir == ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3

            elif ir == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3

            elif ir == PUSH:
                reg = operand_a
                self.reg[SP] -= 1  # decrement the Stack Pointer (SP)
                # read the next value for register location
                reg_value = self.reg[reg]
                # take the value in that register and add to stack
                self.ram[self.reg[SP]] = reg_value
                self.pc += 2

            elif ir == POP:
                # POP value of stack at location SP
                value = self.ram[self.reg[SP]]
                reg = operand_a
                self.reg[reg] = value
                self.reg[SP] += 1  # increment the Stack Pointer (SP)
                self.pc += 2

            elif ir == CALL:
                # store the next line to execute onto the stack
                # this will be the line we will return to after our subroutine
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.pc + 2
                # read which register stores our next line passed with CALL
                reg = operand_a
                # set the PC to that value
                self.pc = self.reg[reg]

            elif ir == RET:
                # pop the current value off stack
                # this SHOULD be the return address
                return_address = self.ram[self.reg[SP]]
                # Increment the stack pointer (move back up the stack)
                self.reg[SP] += 1
                # set the PC to that value
                self.pc = return_address

            elif ir == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

            elif ir == JMP:
                # Jump to the address stored in the given register.
                # Set the PC to the address stored in the given register.
                self.pc = self.reg[operand_a]

            elif ir == JEQ:
                # If equal flag is set (true), jump to the address stored in the given register.
                # 00000001
                if self.flag == 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            elif ir == JNE:
                # If E flag is clear (false, 0), jump to the address stored in the given register.
                # 00000001
                if self.flag != 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            else:
                # if command is non recognizable
                print(ir)
                print("Unknown instruction")
                sys.exit(1)
                # lets crash :(
