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

    def process_one_instruction(self):
        self.current_instruction = self.decoder.decode_next()

    def process_add(self):
        self.current_instruction

    def process_sub(self, instruction):
        pass

    def process_mul(self, instruction):
        pass

    def process_div(self, instruction):
        pass

    def process_mod(self, instruction):
        pass

    def process_and(self, instruction):
        pass

    def process_or(self, instruction):
        pass

    def process_less_than(self, instruction):
        pass

    def process_greater_than(self, instruction):
        pass

    def process_equal(self, instruction):
        pass

    def process_not(self, instruction):
        pass

    def process_jmp(self, instruction):
        pass

    def process_store(self, instruction):
        pass

    def process_load(self, instruction):
        pass
