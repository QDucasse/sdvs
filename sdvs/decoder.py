# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Decoder: Process 32-bits instruction into their corresponding instruction object.

from constants import *
from instruction import Instruction


class Decoder:
    """
    Decode a 32-bits instruction into its structure counterpart.
    """

    def __init__(self, bit_instructions):
        self.bit_instructions = bit_instructions
        self.next_instruction_index = 0

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
                instruction.address = (bitInstruction & 0x000FFFFF)  # 0000 0000 0000 1111 1111 1111 1111 1111
            elif instruction.cfg_mask == LOAD_RAA:
                instruction.type = (bitInstruction & 0x03000000) >> 24  # 0000 0011 0000 0000 0000 0000 0000 0000
                instruction.ra = (bitInstruction & 0x0000000F)  # 0000 0000 0000 0000 0000 0000 0000 1111

        elif op_code == OP_STORE:
            instruction.cfg_mask = (bitInstruction & 0x0C000000) >> 26  # 0000 1100 0000 0000 0000 0000 0000 0000
            instruction.rd = (bitInstruction & 0x00F00000) >> 20  # 0000 0000 1111 0000 0000 0000 0000 0000
            if instruction.cfg_mask == STORE_ADR:
                instruction.type = (bitInstruction & 0x03000000) >> 24  # 0000 0011 0000 0000 0000 0000 0000 0000
                instruction.address = (bitInstruction & 0x000FFFFF)  # 0000 0000 0000 1111 1111 1111 1111 1111
            elif instruction.cfg_mask == STORE_RAA:
                instruction.type = (bitInstruction & 0x03000000) >> 24  # 0000 0011 0000 0000 0000 0000 0000 0000
                instruction.ra = (bitInstruction & 0x0000000F)  # 0000 0000 0000 0000 0000 0000 0000 1111

        elif op_code == OP_JMP:
            instruction.rd = (bitInstruction & 0x0F000000) >> 24  # 0000 1111 0000 0000 0000 0000 0000 0000
            instruction.address = (bitInstruction & 0x00FFFFFF)  # 0000 0000 1111 1111 1111 1111 1111 1111

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
        decoded_instruction = self.decode(self.bit_instructions[self.next_instruction_index])
        self.next_instruction_index += 1
        return decoded_instruction


if __name__ == "__main__":
    from binary_reader import BinaryReader
    bin_instructions = BinaryReader.read_file("../sdve-beem-benchmark/bin/adding.6.out")
    print(bin_instructions)
    decoder = Decoder(bin_instructions)
    print(decoder.decode_next())

