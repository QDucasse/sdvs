# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Simulator: Process instructions one by one and show the results of their execution

from constants import *
import copy

def bool_to_int(boolean):
    return 1 if boolean else 0


class Register:
    def __init__(self, number, size):
        self.number = number
        self.value = 0
        self.type = None
        self.size = size


class Core:

    def __init__(self, decoder, nb):
        self.nb = nb
        self.decoder = decoder
        self.current_instruction = None
        self.memory = None
        self.init_memory = None
        self.registers = []
        self.executed_cycles = 0
        self.idle = False
        self.new_configs = []
        for i in range(REG_NUMBER):
            self.registers.append(Register(i, REG_SIZE))

    def setup_cfg_memory(self, cfg_memory):
        self.init_memory = cfg_memory
        self.reset_cfg_memory()

    def reset_cfg_memory(self):
        self.memory = copy.deepcopy(self.init_memory)

    def reset_execution(self):
        self.idle = False
        self.decoder.next_instruction_index = 0

    def assign_register_value(self, number, value):
        """
        Assign a value to a given register
        :param number: number of the register to assign
        :param value: value to assign
        """
        self.registers[number].value = value

    def retrieve_register_value(self, number):
        """
        Retrieve the value stored in a given register
        :param number: number of the register to look into
        :return: value held by the register
        """
        return self.registers[number].value

    def process_one_instruction(self):
        """
        Decode the next instruction and dispatch the process function
        """
        # print("Core {} INIT MEMORY IS: {}".format(self.nb, hex(self.memory.raw_memory)))
        # Decode
        self.current_instruction = self.decoder.decode_next()
        # Execute
        self.PROCESS_FUNCTIONS[self.current_instruction.op_code](self)
        # Count cycles
        self.add_exec_cycles()

    def process_binary_operands(self):
        """
        Returns the operands corresponding to the given configuration
        """
        left_operand = None
        right_operand = None
        if self.current_instruction.cfg_mask == CFG_RR:
            left_operand = self.retrieve_register_value(self.current_instruction.ra)
            right_operand = self.retrieve_register_value(self.current_instruction.rb)
        elif self.current_instruction.cfg_mask == CFG_RI:
            left_operand = self.retrieve_register_value(self.current_instruction.ra)
            right_operand = self.current_instruction.immb
        elif self.current_instruction.cfg_mask == CFG_IR:
            left_operand = self.current_instruction.imma
            right_operand = self.retrieve_register_value(self.current_instruction.rb)
        elif self.current_instruction.cfg_mask == CFG_II:
            left_operand = self.current_instruction.imma
            right_operand = self.current_instruction.immb
        return left_operand, right_operand

    def process_add(self):
        """
        Process the ADD operation
        Assign left operand + right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand + right_operand)

    def process_sub(self):
        """
        Process the SUB operation
        Assign left operand - right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand - right_operand)

    def process_mul(self):
        """
        Process the MUL operation
        Assign left operand * right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand * right_operand)

    def process_div(self):
        """
        Process the DIV operation
        Assign left operand / right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand / right_operand)

    def process_mod(self):
        """
        Process the MOD operation
        Assign left operand % right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand % right_operand)

    def process_and(self):
        """
        Process the AND operation
        Assign left operand and right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   bool_to_int(left_operand and right_operand))

    def process_or(self):
        """
        Process the OR operation
        Assign left operand or right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   bool_to_int(left_operand or right_operand))

    def process_less_than(self):
        """
        Process the LT operation
        Assign left operand < right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   bool_to_int(left_operand < right_operand))

    def process_greater_than(self):
        """
        Process the GT operation
        Assign left operand > right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   bool_to_int(left_operand > right_operand))

    def process_equal(self):
        """
        Process the EQ operation
        Assign left operand == right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   bool_to_int(left_operand == right_operand))

    def process_not(self):
        """
        Process the NOT operation
        Assign not(ra) in the destination register
        """
        self.assign_register_value(self.current_instruction.rd,
                                   bool_to_int(not (self.retrieve_register_value(self.current_instruction.ra))))

    def process_jmp(self):
        """
        Change the decoder current instruction to the given one if the
        condition in rd is true
        """
        if self.retrieve_register_value(self.current_instruction.rd) == 0:
            self.decoder.next_instruction_index = self.current_instruction.address

    def process_store(self):
        """
        Store the content of a given register in memory
        """
        # Get value from rd
        value = self.retrieve_register_value(self.current_instruction.rd)
        if self.current_instruction.cfg_mask == STORE_ADR:
            # Store in memory
            self.memory.set_at_address(self.current_instruction.type, value, self.current_instruction.address)
        elif self.current_instruction.cfg_mask == STORE_RAA:
            # Get address out of register
            address = self.retrieve_register_value(self.current_instruction.ra)
            # Store in memory
            self.memory.set_at_address(self.current_instruction.type, value, address)

    def process_load(self):
        """
        Load a variable in a register from memory
        OR
        Change the value of a register (from an immediate or other register)
        """
        if self.current_instruction.cfg_mask == LOAD_ADR:
            # Get value from memory
            value = self.memory.retrieve_at_address(self.current_instruction.type,
                                                    self.current_instruction.address)
            # Assign to the destination register
            self.assign_register_value(self.current_instruction.rd, value)

        elif self.current_instruction.cfg_mask == LOAD_RAA:
            # Get address from register
            address = self.retrieve_register_value(self.current_instruction.ra)
            # Get value from memory
            value = self.memory.retrieve_at_address(self.current_instruction.type, address)
            # Assign to the destination register
            self.assign_register_value(self.current_instruction.rd, value)

        elif self.current_instruction.cfg_mask == LOAD_REG:
            self.assign_register_value(self.current_instruction.rd,
                                       self.retrieve_register_value(self.current_instruction.ra))

        elif self.current_instruction.cfg_mask == LOAD_IMM:
            self.assign_register_value(self.current_instruction.rd, self.current_instruction.imma)

    def process_endga(self):
        """
        Return the stored config memory.
        :return:
        """
        self.new_configs.append(self.memory.raw_memory) # or self.memory
        self.reset_cfg_memory()

    def process_nop(self):
        """
        Wait for a new configuration.
        :return:
        """
        self.idle = True

    def process_instructions(self):
        self.executed_cycles += 2  # Reset routine (2)
        while not self.idle:
            self.executed_cycles += 4  # fetch (2) and decode (2)
            self.process_one_instruction()

    def print_registers(self):
        print("Registers State:")
        for reg in self.registers:
            print("R{}: {}".format(reg.number, hex(reg.value)))
        print("----------------")

    def add_exec_cycles(self):
        if self.current_instruction.op_code != OP_LOAD:
            self.executed_cycles += self.INSTR_CYCLES[self.current_instruction.op_code]
        else:
            if self.current_instruction.cfg_mask == LOAD_ADR:
                self.executed_cycles += 2
            elif self.current_instruction.cfg_mask == LOAD_RAA:
                self.executed_cycles += 3
            else:
                self.executed_cycles += 1

    PROCESS_FUNCTIONS = {
        OP_ADD: process_add,
        OP_SUB: process_sub,
        OP_MUL: process_mul,
        OP_DIV: process_div,
        OP_MOD: process_mod,
        OP_AND: process_and,
        OP_OR: process_or,
        OP_LT: process_less_than,
        OP_GT: process_greater_than,
        OP_EQ: process_equal,
        OP_NOT: process_not,
        OP_JMP: process_jmp,
        OP_STORE: process_store,
        OP_LOAD: process_load,
        OP_ENDGA: process_endga,
        OP_NOP: process_nop
    }

    INSTR_CYCLES = {
        OP_ADD: 3,
        OP_SUB: 3,
        OP_MUL: 3,
        OP_DIV: 3,
        OP_MOD: 3,
        OP_AND: 3,
        OP_OR: 3,
        OP_LT: 3,
        OP_GT: 3,
        OP_EQ: 3,
        OP_NOT: 1,
        OP_JMP: 2,
        OP_STORE: 2,
        OP_ENDGA: 1,
        OP_NOP: 1
    }


if __name__ == "__main__":
    from binary_reader import BinaryReader
    from decoder import Decoder
    from memory import Memory

    bin_instructions = BinaryReader.read_instructions("../../sdvu/cfg/adding.6.out.2")
    for instr in bin_instructions:
        print(hex(instr))
    memory = Memory(128, 0x22221111333333332222222200000001)
    simulator = Core(Decoder(bin_instructions), 2, 128)
    simulator.setup_cfg_memory(memory)
    simulator.process_instructions()
