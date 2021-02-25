# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Decoder: Process 32-bits instruction into their corresponding instruction object.

from sdvs.constants import *


class Instruction:
    """
    Instruction structure to hold the decoded parts of the 32-bits instruction.
    """

    def __init__(self, op_code, cfg_mask=0b00, inst_type=0b00,
                 rd=0b0000, ra=0b0000, rb=0b0000,
                 imma=0b00000000000, immb=0b00000000000,
                 addr=0b000000000000000000000000):
        self.op_code = op_code
        self.cfg_mask = cfg_mask
        self.rd = rd
        self.ra = ra
        self.rb = rb
        self.imma = imma
        self.immb = immb
        self.addr = addr
        self.type = inst_type

    def __eq__(self, other):
        return (self.op_code == other.op_code and
                self.cfg_mask == other.cfg_mask and
                self.rd == other.rd and
                self.ra == other.ra and
                self.rb == other.rb and
                self.imma == other.imma and
                self.immb == other.immb and
                self.addr == other.addr and
                self.type == other.type)

    def __str__(self):
        return "Instruction object OP_CODE={} rd={}\ncfg_mask={} type={}\n imma={} immb={}\n addr={}".format(
            self.op_code,
            self.rd,
            self.cfg_mask,
            self.type,
            self.ra,
            self.rb,
            self.imma,
            self.immb,
            self.addr
        )


class Decoder:
    """
    Decode a 32-bits instruction into its structure counterpart.
    """

    def __init__(self, bit_instructions):
        self.bit_instructions = bit_instructions
        self.current_instruction = 0

    def decode(self, bitInstruction):
        """
        Process the bit instruction with several bit-masks and fills an
        Instruction object.
        :param bitInstruction: 32-bits instruction to decode
        :return: filled instruction object
        """
        op_code = (bitInstruction & 0xF0000000) >> 28  # 1111 0000 0000 0000 0000 0000 0000 0000
        instruction = Instruction(op_code)
        if op_code == OP_NOT:
            instruction.rd = (bitInstruction & 0x0F000000) >> 24  # 0000 1111 0000 0000 0000 0000 0000 0000
            instruction.ra = (bitInstruction & 0x0000000F)  # 0000 0000 0000 0000 0000 0000 0000 1111

        elif op_code == OP_LOAD:
            instruction.cfg_mask = (bitInstruction & 0x0C000000) >> 26  # 0000 1100 0000 0000 0000 0000 0000 0000
            instruction.rd = (bitInstruction & 0x00F00000) >> 20  # 0000 0000 1111 0000 0000 0000 0000 0000
            if instruction.cfg_mask == LOAD_REG:
                instruction.ra = (bitInstruction & 0x0000000F)  # 0000 0000 0000 0000 0000 0000 0000 1111
            elif instruction.cfg_mask == LOAD_IMM:
                instruction.imma = (bitInstruction & 0x000007FF)  # 0000 0000 0000 0000 0000 0111 1111 1111
            elif instruction.cfg_mask == LOAD_ADR:
                instruction.type = (bitInstruction & 0x03000000) >> 24  # 0000 0011 0000 0000 0000 0000 0000 0000
                instruction.addr = (bitInstruction & 0x000FFFFF)  # 0000 0000 0000 1111 1111 1111 1111 1111
            elif instruction.cfg_mask == LOAD_RAA:
                instruction.type = (bitInstruction & 0x03000000) >> 24  # 0000 0011 0000 0000 0000 0000 0000 0000
                instruction.ra = (bitInstruction & 0x0000000F)  # 0000 0000 0000 0000 0000 0000 0000 1111

        elif op_code == OP_STORE:
            instruction.cfg_mask = (bitInstruction & 0x0C000000) >> 26  # 0000 1100 0000 0000 0000 0000 0000 0000
            instruction.rd = (bitInstruction & 0x00F00000) >> 20  # 0000 0000 1111 0000 0000 0000 0000 0000
            if instruction.cfg_mask == STORE_ADR:
                instruction.type = (bitInstruction & 0x03000000) >> 24  # 0000 0011 0000 0000 0000 0000 0000 0000
                instruction.addr = (bitInstruction & 0x000FFFFF)  # 0000 0000 0000 1111 1111 1111 1111 1111
            elif instruction.cfg_mask == STORE_RAA:
                instruction.type = (bitInstruction & 0x03000000) >> 24  # 0000 0011 0000 0000 0000 0000 0000 0000
                instruction.ra = (bitInstruction & 0x0000000F)  # 0000 0000 0000 0000 0000 0000 0000 1111

        elif op_code == OP_JMP:
            instruction.rd = (bitInstruction & 0x0F000000) >> 24  # 0000 1111 0000 0000 0000 0000 0000 0000
            instruction.addr = (bitInstruction & 0x00FFFFFF)  # 0000 0000 1111 1111 1111 1111 1111 1111

        else:  # Binary operation
            instruction.cfg_mask = (bitInstruction & 0x0C000000) >> 26  # 0000 1100 0000 0000 0000 0000 0000 0000
            instruction.rd = (bitInstruction & 0x03C00000) >> 22  # 0000 0011 1100 0000 0000 0000 0000 0000
            # Switch on the configuration
            if instruction.cfg_mask == CFG_RR:
                instruction.ra = (bitInstruction & 0x00007800) >> 11  # 0000 0000 0000 0000 0111 1000 0000 0000
                instruction.rb = (bitInstruction & 0x0000000F)  # 0000 0000 0000 0000 0000 0000 0000 1111
            elif instruction.cfg_mask == CFG_RI:
                instruction.ra = (bitInstruction & 0x00007800) >> 11  # 0000 0000 0000 0000 0111 1000 0000 0000
                instruction.immb = (bitInstruction & 0x000007FF)  # 0000 0000 0000 0000 0000 0111 1111 1111
            elif instruction.cfg_mask == CFG_IR:
                instruction.imma = (bitInstruction & 0x003FF800) >> 11  # 0000 0000 0011 1111 1111 1000 0000 0000
                instruction.rb = (bitInstruction & 0x0000000F)  # 0000 0000 0000 0000 0000 0000 0000 1111
            elif instruction.cfg_mask == CFG_II:
                instruction.imma = (bitInstruction & 0x003FF800) >> 11  # 0000 0000 0011 1111 1111 1000 0000 0000
                instruction.immb = (bitInstruction & 0x000007FF)  # 0000 0000 0000 0000 0000 0111 1111 1111

        return instruction

    def decode_next(self):
        """
        Create a generator out of the 32-bits instructions list and decode it when needed.
        :return: next instruction to be decoded
        """
        decoded_instruction = self.decode(self.bit_instructions[self.current_instruction])
        self.current_instruction += 1
        return decoded_instruction
