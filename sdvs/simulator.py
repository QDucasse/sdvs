# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Simulator: Process instructions one by one and show the results of their execution

from sdvs.decoder import Instruction
from sdvs.constants import *

class Register:
    def __init__(self, number, size):
        self.number = number
        self.value = 0
        self.type = None
        self.size = size


class Simulator:

    def __init__(self, decoder):
        self.decoder = decoder
        self.current_instruction = None
        self.memory = None
        self.registers = []
        for i in range(REG_NUMBER + 1):
            self.registers.append(Register(i, REG_SIZE))

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
        self.current_instruction = self.decoder.decode_next()
        self.PROCESS_FUNCTIONS[self.current_instruction.op_code](self)

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
                                   left_operand and right_operand)

    def process_or(self):
        """
        Process the OR operation
        Assign left operand or right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand or right_operand)

    def process_less_than(self):
        """
        Process the LT operation
        Assign left operand < right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand < right_operand)

    def process_greater_than(self):
        """
        Process the GT operation
        Assign left operand > right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand > right_operand)

    def process_equal(self):
        """
        Process the EQ operation
        Assign left operand == right operand in the destination register
        """
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand == right_operand)

    def process_not(self):
        """
        Process the NOT operation
        Assign not(ra) in the destination register
        """
        self.assign_register_value(self.current_instruction.rd,
                                   not(self.retrieve_register_value(self.current_instruction.ra)))

    def process_jmp(self):
        """
        Change the decoder current instruction to the given one if the
        condition in rd is true
        """
        if self.retrieve_register_value(self.current_instruction.rd):
            self.decoder.next_instruction_index = self.current_instruction.addr / INSTRUCTION_SIZE

    def process_store(self):
        """
        Store the content of a given register in memory
        """
        # Get value from rd
        value = self.retrieve_register_value(self.current_instruction.rd)
        if self.current_instruction.cfg_mask == STORE_ADR:
            # Store in memory
            self.memory.set_at_address(value, self.current_instruction.address,
                                       self.current_instruction.type)
        elif self.current_instruction.cfg_mask == STORE_RAA:
            # Get address out of register
            address = self.retrieve_register_value(self.current_instruction.ra)
            # Store in memory
            self.memory.set_at_address(value, address, self.current_instruction.type)

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
        OP_LOAD: process_load
    }