# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Decoder: Process 32-bits instruction into their corresponding instruction object.
# Test file!

import unittest
from unittest.mock import patch, mock_open
from sdvs.decoder import Decoder, Instruction
from sdvs.asm import ASM
from sdvs.constants import *

mock_file = """
add r3 r1 r2
sub r3 r1 122
mod r3 122 r2
eq r3 123 124
not r3 r1
jmp r3 234
mov r3 r1
mov r3 234
loadbool r3 r1
loadbool r3 234
loadbyte r3 r1
loadbyte r3 234
loadint r3 r1
loadint r3 234
loadstate r3 r1
loadstate r3 234
storebool r3 r1
storebool r3 234
storebyte r3 r1
storebyte r3 234
storeint r3 r1
storeint r3 234
storestate r3 r1
storestate r3 234
"""


class TestDecoder(unittest.TestCase):

    @patch('builtins.open', mock_open(read_data=mock_file))
    def setUp(self):
        self.asm = ASM()
        self.bit_instructions = self.asm.process_file("path/to/mock/file")
        self.decoder = Decoder(self.bit_instructions)

    def test_decode_next(self):
        # add r3 r1 r2
        expected_instruction_add = Instruction(OP_ADD, rd=3, ra=1, rb=2, cfg_mask=CFG_RR)
        self.assertEqual(expected_instruction_add, self.decoder.decode_next())
        self.assertEqual(1, self.decoder.current_instruction)
        # sub r3 r1 122
        expected_instruction_sub = Instruction(OP_SUB, rd=3, ra=1, immb=122, cfg_mask=CFG_RI)
        self.assertEqual(expected_instruction_sub, self.decoder.decode_next())
        self.assertEqual(2, self.decoder.current_instruction)

    def test_decode_bin_RR(self):
        # add r3 r1 r2
        expected_instruction = Instruction(OP_ADD, rd=3, ra=1, rb=2, cfg_mask=CFG_RR)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[0]))

    def test_decode_bin_RI(self):
        # sub r3 r1 122
        expected_instruction = Instruction(OP_SUB, rd=3, ra=1, immb=122, cfg_mask=CFG_RI)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[1]))

    def test_decode_bin_IR(self):
        # mod r3 122 r2
        expected_instruction = Instruction(OP_MOD, rd=3, imma=122, rb=2, cfg_mask=CFG_IR)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[2]))

    def test_decode_bin_II(self):
        # eq r3 123 124
        expected_instruction = Instruction(OP_EQ, rd=3, imma=123, immb=124, cfg_mask=CFG_II)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[3]))

    def test_decode_not(self):
        # not r3 r1
        expected_instruction = Instruction(OP_NOT, rd=3, ra=1)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[4]))

    def test_decode_jmp(self):
        # jmp r3 234
        expected_instruction = Instruction(OP_JMP, rd=3, addr=234)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[5]))

    def test_decode_mov_reg(self):
        # mov r3 r1
        expected_instruction = Instruction(OP_LOAD, cfg_mask=LOAD_REG, rd=3, ra=1)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[6]))

    def test_decode_mov_imm(self):
        # mov r3 234
        expected_instruction = Instruction(OP_LOAD, cfg_mask=LOAD_IMM, rd=3, imma=234)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[7]))

    def test_decode_load_bool_raa(self):
        # loadbool r3 r1
        expected_instruction = Instruction(OP_LOAD, cfg_mask=LOAD_RAA, rd=3, ra=1, inst_type=VAL_BOOL)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[8]))

    def test_decode_load_bool_adr(self):
        # loadbool r3 234
        expected_instruction = Instruction(OP_LOAD, cfg_mask=LOAD_ADR, rd=3, addr=234, inst_type=VAL_BOOL)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[9]))

    def test_decode_load_byte_raa(self):
        # loadbyte r3 r1
        expected_instruction = Instruction(OP_LOAD, cfg_mask=LOAD_RAA, rd=3, ra=1, inst_type=VAL_BYTE)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[10]))

    def test_decode_load_byte_adr(self):
        # loadbyte r3 234
        expected_instruction = Instruction(OP_LOAD, cfg_mask=LOAD_ADR, rd=3, addr=234, inst_type=VAL_BYTE)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[11]))

    def test_decode_load_int_raa(self):
        # loadint r3 r1
        expected_instruction = Instruction(OP_LOAD, cfg_mask=LOAD_RAA, rd=3, ra=1, inst_type=VAL_INT)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[12]))

    def test_decode_load_int_adr(self):
        # loadint r3 234
        expected_instruction = Instruction(OP_LOAD, cfg_mask=LOAD_ADR, rd=3, addr=234, inst_type=VAL_INT)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[13]))

    def test_decode_load_state_raa(self):
        # loadstate r3 r1
        expected_instruction = Instruction(OP_LOAD, cfg_mask=LOAD_RAA, rd=3, ra=1, inst_type=VAL_STATE)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[14]))

    def test_decode_load_state_adr(self):
        # loadstate r3 234
        expected_instruction = Instruction(OP_LOAD, cfg_mask=LOAD_ADR, rd=3, addr=234, inst_type=VAL_STATE)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[15]))

    def test_decode_store_bool_raa(self):
        # storebool r3 r1
        expected_instruction = Instruction(OP_STORE, cfg_mask=STORE_RAA, rd=3, ra=1, inst_type=VAL_BOOL)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[16]))

    def test_decode_store_bool_adr(self):
        # storebool r3 234
        expected_instruction = Instruction(OP_STORE, cfg_mask=STORE_ADR, rd=3, addr=234, inst_type=VAL_BOOL)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[17]))

    def test_decode_store_byte_raa(self):
        # storebyte r3 r1
        expected_instruction = Instruction(OP_STORE, cfg_mask=STORE_RAA, rd=3, ra=1, inst_type=VAL_BYTE)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[18]))

    def test_decode_store_byte_adr(self):
        # storebyte r3 234
        expected_instruction = Instruction(OP_STORE, cfg_mask=STORE_ADR, rd=3, addr=234, inst_type=VAL_BYTE)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[19]))

    def test_decode_store_int_raa(self):
        # storeint r3 r1
        expected_instruction = Instruction(OP_STORE, cfg_mask=STORE_RAA, rd=3, ra=1, inst_type=VAL_INT)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[20]))

    def test_decode_store_int_adr(self):
        # storeint r3 234
        expected_instruction = Instruction(OP_STORE, cfg_mask=STORE_ADR, rd=3, addr=234, inst_type=VAL_INT)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[21]))

    def test_decode_store_state_raa(self):
        # storestate r3 r1
        expected_instruction = Instruction(OP_STORE, cfg_mask=STORE_RAA, rd=3, ra=1, inst_type=VAL_STATE)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[22]))

    def test_decode_store_state_adr(self):
        # storestate r3 234
        expected_instruction = Instruction(OP_STORE, cfg_mask=STORE_ADR, rd=3, addr=234, inst_type=VAL_STATE)
        self.assertEqual(expected_instruction, self.decoder.decode(self.bit_instructions[23]))
