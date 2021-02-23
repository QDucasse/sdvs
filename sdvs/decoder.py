# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Decoder: Process 32-bits instruction into their corresponding instruction object.

from constants import *


class Instruction:
    """
    Instruction structure to hold the decoded parts of the 32-bits instruction.
    """

    def __init__(self, op_code):
        self.op_code = op_code
        self.cfg_mask = 0
        self.rd = 0
        self.ra = 0
        self.rb = 0
        self.imma = 0
        self.immb = 0
        self.addr = 0
        self.type = 0


class Decoder:
    """
    Decode a 32-bits instruction into its structure counterpart.
    """

    def __init__(self, bit_instructions):
        self.bit_instructions = bit_instructions

    def decode(self, bitInstruction):
        op_code = (bitInstruction & 0xF0000000) >> 28  # 1111 0000 0000 0000 0000 0000 0000 0000
        instruction = Instruction(op_code)
        if op_code == OP_NOT:
            instruction.rd = (bitInstruction & 0x0F000000) >> 24  # 0000 1111 0000 0000 0000 0000 0000 0000
            instruction.ra = (bitInstruction & 0x0000000F)  # 0000 0000 0000 0000 0000 0000 0000 1111

        elif op_code == OP_LOAD or op_code == OP_STORE:
            instruction.cfg_mask = (bitInstruction & 0x0C000000) >> 26  # 0000 1100 0000 0000 0000 0000 0000 0000
            instruction.type = (bitInstruction & 0x03000000) >> 24  # 0000 0011 0000 0000 0000 0000 0000 0000
            instruction.rd = (bitInstruction & 0x00F00000) >> 20  # 0000 0000 1111 0000 0000 0000 0000 0000
            instruction.ra = (bitInstruction & 0x0000000F)  # 0000 0000 0000 0000 0000 0000 0000 1111
            instruction.imma = (bitInstruction & 0x000007FF)  # 0000 0000 0000 0000 0000 0111 1111 1111
            instruction.addr = (bitInstruction & 0x000FFFFF)  # 0000 0000 0000 1111 1111 1111 1111 1111

        elif op_code == OP_JMP:
            instruction.rd = (bitInstruction & 0x0F000000) >> 24  # 0000 1111 0000 0000 0000 0000 0000 0000
            instruction.addr = (bitInstruction & 0x00FFFFFF)  # 0000 0000 1111 1111 1111 1111 1111 1111

        else:  # Binary operation
            instruction.cfg_mask = (bitInstruction & 0x0C000000) >> 26  # 0000 1100 0000 0000 0000 0000 0000 0000
            instruction.rd = (bitInstruction & 0x03C00000) >> 22  # 0000 0011 1100 0000 0000 0000 0000 0000
            instruction.ra = (bitInstruction & 0x00007800) >> 11  # 0000 0000 0000 0000 0111 1000 0000 0000
            instruction.imma = (bitInstruction & 0x003FF800) >> 11  # 0000 0000 0011 1111 1111 1000 0000 0000
            instruction.immb = (bitInstruction & 0x000007FF)  # 0000 0000 0000 0000 0000 0111 1111 1111

        return instruction

    def decode_next(self):
        """
        Create a generator out of the 32-bits instructions list and decode it when needed.
        :return: next instruction to be decoded
        """
        instructions = (self.decode(bitInstruction) for bitInstruction in self.bit_instructions)
        for instruction in instructions:
            yield instruction
