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
        self.registers[number].value = value

    def retrieve_register_value(self, number):
        return self.registers[number].value

    def process_one_instruction(self):
        self.current_instruction = self.decoder.decode_next()
        self.PROCESS_FUNCTIONS[self.current_instruction.op_code]()

    def process_binary_operands(self):
        left_operand = None
        right_operand = None
        if self.current_instruction.cfg_mask == CFG_RR:
            left_operand = self.retrieve_register_value(self.current_instruction.ra)
            right_operand = self.retrieve_register_value(self.current_instruction.rb)
        elif self.current_instruction.cfg_mask == CFG_RI:
            left_operand = self.retrieve_register_value(self.current_instruction.ra)
            right_operand = self.retrieve_register_value(self.current_instruction.immb)
        elif self.current_instruction.cfg_mask == CFG_IR:
            left_operand = self.retrieve_register_value(self.current_instruction.imma)
            right_operand = self.retrieve_register_value(self.current_instruction.rb)
        elif self.current_instruction.cfg_mask == CFG_II:
            left_operand = self.retrieve_register_value(self.current_instruction.imma)
            right_operand = self.retrieve_register_value(self.current_instruction.immb)
        return left_operand, right_operand

    def process_add(self):
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand + right_operand)

    def process_sub(self):
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand - right_operand)

    def process_mul(self):
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand * right_operand)

    def process_div(self):
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand / right_operand)

    def process_mod(self):
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand % right_operand)

    def process_and(self):
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand and right_operand)

    def process_or(self):
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand or right_operand)

    def process_less_than(self):
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand < right_operand)

    def process_greater_than(self):
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand > right_operand)

    def process_equal(self):
        left_operand, right_operand = self.process_binary_operands()
        self.assign_register_value(self.current_instruction.rd,
                                   left_operand == right_operand)

    def process_not(self):
        self.assign_register_value(self.current_instruction.rd,
                                   not(self.retrieve_register_value(self.current_instruction.ra)))

    def process_jmp(self, instruction):
        pass

    def process_store(self, instruction):
        pass

    def process_load(self, instruction):
        pass

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