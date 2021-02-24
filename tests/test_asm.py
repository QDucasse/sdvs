# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Assembler: Process textual assembler to generate instructions.

import unittest
from unittest.mock import patch, mock_open

from sdvs.asm import *
from sdvs.constants import *

mock_file = """
add r0 r1 r2
sub r0 r1 122
mod r0 122 r2
eq r0 123 124
not r0 r1
jmp r0 2567
mov r0 r1
mov r0 255566
loadbool r0 r1
loadbool r0 255566
loadbyte r0 r1
loadbyte r0 255566
loadint r0 r1
loadint r0 255566
loadstate r0 r1
loadstate r0 255566
storebool r0 r1
storebool r0 255566
storebyte r0 r1
storebyte r0 255566
storeint r0 r1
storeint r0 255566
storestate r0 r1
storestate r0 255566
"""


class TestASM(unittest.TestCase):

    def setUp(self):
        self.asm = ASM()

    def test_is_reg(self):
        self.assertTrue(is_reg("r13"))
        self.assertFalse(is_reg("135"))

    def test_expect_reg(self):
        self.assertRaises(ConfigException, expect_reg, "134", "Should hold reg")

    def test_extract_number(self):
        self.assertEqual(13, extract_number("r13"))
        self.assertEqual(24456778, extract_number("24456778"))

    def test_determine_bin_cfg(self):
        self.assertEqual(CFG_RR, determine_bin_cfg("r3", "r10"))
        self.assertEqual(CFG_RI, determine_bin_cfg("r3", "14578"))
        self.assertEqual(CFG_IR, determine_bin_cfg("323", "r10"))
        self.assertEqual(CFG_II, determine_bin_cfg("113", "225678"))

    def test_determine_load_cfg(self):
        self.assertEqual(LOAD_RAA, determine_load_cfg("r4"))
        self.assertEqual(LOAD_ADR, determine_load_cfg("45687"))

    def test_determine_mov_cfg(self):
        self.assertEqual(LOAD_REG, determine_mov_cfg("r4"))
        self.assertEqual(LOAD_IMM, determine_mov_cfg("45687"))

    def test_determine_store_cfg(self):
        self.assertEqual(STORE_RAA, determine_store_cfg("r4"))
        self.assertEqual(STORE_ADR, determine_store_cfg("45687"))

    def test_determine_type(self):
        self.assertEqual(VAL_BOOL, determine_type("storebool"))
        self.assertEqual(VAL_BOOL, determine_type("loadbool"))
        self.assertEqual(VAL_BYTE, determine_type("storebyte"))
        self.assertEqual(VAL_BYTE, determine_type("loadbyte"))
        self.assertEqual(VAL_INT, determine_type("storeint"))
        self.assertEqual(VAL_INT, determine_type("loadint"))
        self.assertEqual(VAL_STATE, determine_type("storestate"))
        self.assertEqual(VAL_STATE, determine_type("loadstate"))

    def test_process_binary(self):
        # Config Register Register
        arguments1 = ["add", "r0", "r1", "r2"]
        bit_instruction1 = OP_ADD << 28
        self.assertEqual(0x00000802, self.asm.process_binary(arguments1, bit_instruction1))
        # Config Register Immediate
        arguments2 = ["sub", "r0", "r1", "122"]
        bit_instruction2 = OP_SUB << 28
        self.assertEqual(0x1400087a, self.asm.process_binary(arguments2, bit_instruction2))
        # Config Immediate Register
        arguments3 = ["mod", "r0", "122", "r2"]
        bit_instruction3 = OP_MOD << 28
        self.assertEqual(0x4803d002, self.asm.process_binary(arguments3, bit_instruction3))
        # Config Immediate Immediate
        arguments4 = ["eq", "r0", "123", "124"]
        bit_instruction4 = OP_EQ << 28
        self.assertEqual(0x9c03d87c, self.asm.process_binary(arguments4, bit_instruction4))

    def test_process_not(self):
        arguments = ["not", "r0", "r1"]
        bit_instruction = OP_NOT << 28
        self.assertEqual(0xa0000001, self.asm.process_not(arguments, bit_instruction))

    def test_process_jmp(self):
        arguments = ["jmp", "r0", "2567"]
        bit_instruction = OP_JMP << 28
        self.assertEqual(0xb0000a07, self.asm.process_jmp(arguments, bit_instruction))

    def test_process_mov(self):
        # Config LOAD_REG
        arguments1 = ["mov", "r0", "r1"]
        bit_instruction1 = OP_LOAD << 28
        self.assertEqual(0xd0000001, self.asm.process_mov(arguments1, bit_instruction1))
        # Config LOAD_IMM
        arguments2 = ["mov", "r0", "255566"]
        bit_instruction2 = OP_LOAD << 28
        self.assertEqual(0xd403e64e, self.asm.process_mov(arguments2, bit_instruction2))

    def test_process_load(self):
        # Config LOAD_RAA - bool
        arguments1 = ["loadbool", "r0", "r1"]
        bit_instruction1 = OP_LOAD << 28
        self.assertEqual(0xdc000001, self.asm.process_load(arguments1, bit_instruction1))
        # Config LOAD_ADR - bool
        arguments2 = ["loadbool", "r0", "255566"]
        bit_instruction2 = OP_LOAD << 28
        self.assertEqual(0xd803e64e, self.asm.process_load(arguments2, bit_instruction2))
        # Config LOAD_RAA - byte
        arguments1 = ["loadbyte", "r0", "r1"]
        bit_instruction1 = OP_LOAD << 28
        self.assertEqual(0xdd000001, self.asm.process_load(arguments1, bit_instruction1))
        # Config LOAD_ADR - byte
        arguments2 = ["loadbyte", "r0", "255566"]
        bit_instruction2 = OP_LOAD << 28
        self.assertEqual(0xd903e64e, self.asm.process_load(arguments2, bit_instruction2))
        # Config LOAD_RAA - int
        arguments1 = ["loadint", "r0", "r1"]
        bit_instruction1 = OP_LOAD << 28
        self.assertEqual(0xde000001, self.asm.process_load(arguments1, bit_instruction1))
        # Config LOAD_ADR - int
        arguments2 = ["loadint", "r0", "255566"]
        bit_instruction2 = OP_LOAD << 28
        self.assertEqual(0xda03e64e, self.asm.process_load(arguments2, bit_instruction2))
        # Config LOAD_RAA - state
        arguments1 = ["loadstate", "r0", "r1"]
        bit_instruction1 = OP_LOAD << 28
        self.assertEqual(0xdf000001, self.asm.process_load(arguments1, bit_instruction1))
        # Config LOAD_ADR - state
        arguments2 = ["loadstate", "r0", "255566"]
        bit_instruction2 = OP_LOAD << 28
        self.assertEqual(0xdb03e64e, self.asm.process_load(arguments2, bit_instruction2))

    def test_process_store(self):
        # Config STORE_RAA - bool
        arguments1 = ["storebool", "r0", "r1"]
        bit_instruction1 = OP_STORE << 28
        self.assertEqual(0xc4000001, self.asm.process_store(arguments1, bit_instruction1))
        # Config STORE_ADR - bool
        arguments2 = ["storebool", "r0", "255566"]
        bit_instruction2 = OP_STORE << 28
        self.assertEqual(0xc003e64e, self.asm.process_store(arguments2, bit_instruction2))
        # Config STORE_RAA - byte
        arguments1 = ["storebyte", "r0", "r1"]
        bit_instruction1 = OP_STORE << 28
        self.assertEqual(0xc5000001, self.asm.process_store(arguments1, bit_instruction1))
        # Config STORE_ADR - byte
        arguments2 = ["storebyte", "r0", "255566"]
        bit_instruction2 = OP_STORE << 28
        self.assertEqual(0xc103e64e, self.asm.process_store(arguments2, bit_instruction2))
        # Config STORE_RAA - int
        arguments1 = ["storeint", "r0", "r1"]
        bit_instruction1 = OP_STORE << 28
        self.assertEqual(0xc6000001, self.asm.process_store(arguments1, bit_instruction1))
        # Config STORE_ADR - int
        arguments2 = ["storeint", "r0", "255566"]
        bit_instruction2 = OP_STORE << 28
        self.assertEqual(0xc203e64e, self.asm.process_store(arguments2, bit_instruction2))
        # Config STORE_RAA - state
        arguments1 = ["storestate", "r0", "r1"]
        bit_instruction1 = OP_STORE << 28
        self.assertEqual(0xc7000001, self.asm.process_store(arguments1, bit_instruction1))
        # Config STORE_ADR - state
        arguments2 = ["storestate", "r0", "255566"]
        bit_instruction2 = OP_STORE << 28
        self.assertEqual(0xc303e64e, self.asm.process_store(arguments2, bit_instruction2))

    def test_process_line(self):
        self.assertEqual(0x00000802, self.asm.process_line("add r0 r1 r2"))

    @patch('builtins.open', mock_open(read_data=mock_file))
    def test_process_file(self):
        expected_instructions = [
            0x00000802,  # add r0 r1 r2
            0x1400087a,  # sub r0 r1 122
            0x4803d002,  # mod r0 122 r2
            0x9c03d87c,  # eq r0 123 124
            0xa0000001,  # not r0 r1
            0xb0000a07,  # jmp r0 2567
            0xd0000001,  # mov r0 r1
            0xd403e64e,  # mov r0 255566
            0xdc000001,  # loadbool r0 r1
            0xd803e64e,  # loadbool r0 255566
            0xdd000001,  # loadbyte r0 r1
            0xd903e64e,  # loadbyte r0 255566
            0xde000001,  # loadint r0 r1
            0xda03e64e,  # loadint r0 255566
            0xdf000001,  # loadstate r0 r1
            0xdb03e64e,  # loadstate r0 255566
            0xc4000001,  # storebool r0 r1
            0xc003e64e,  # storebool r0 255566
            0xc5000001,  # storebyte r0 r1
            0xc103e64e,  # storebyte r0 255566
            0xc6000001,  # storeint r0 r1
            0xc203e64e,  # storeint r0 255566
            0xc7000001,  # storestate r0 r1
            0xc303e64e   # storestate r0 255566
        ]
        self.assertEqual(expected_instructions, self.asm.process_file("path/to/mock/file"))
