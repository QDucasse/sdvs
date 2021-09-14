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
nop
endga
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
        self.assertEqual(CFG_II, determine_bin_cfg("113", "22348"))

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
        arguments1 = ["add", "r3", "r1", "r2"]
        bit_instruction1 = OP_ADD << 28
        self.assertEqual(0x10c00802, self.asm.process_binary(arguments1, bit_instruction1))
        # Config Register Immediate
        arguments2 = ["sub", "r3", "r1", "122"]
        bit_instruction2 = OP_SUB << 28
        self.assertEqual(0x24c0087a, self.asm.process_binary(arguments2, bit_instruction2))
        # Config Immediate Register
        arguments3 = ["mod", "r3", "122", "r2"]
        bit_instruction3 = OP_MOD << 28
        self.assertEqual(0x58c3d002, self.asm.process_binary(arguments3, bit_instruction3))
        # Config Immediate Immediate
        arguments4 = ["eq", "r3", "123", "124"]
        bit_instruction4 = OP_EQ << 28
        self.assertEqual(0xacc3d87c, self.asm.process_binary(arguments4, bit_instruction4))

    def test_process_not(self):
        arguments = ["not", "r3", "r1"]
        bit_instruction = OP_NOT << 28
        self.assertEqual(0xb3000001, self.asm.process_not(arguments, bit_instruction))

    def test_process_jmp(self):
        arguments = ["jmp", "r3", "234"]
        bit_instruction = OP_JMP << 28
        self.assertEqual(0xc30000ea, self.asm.process_jmp(arguments, bit_instruction))

    def test_process_mov(self):
        # Config LOAD_REG
        arguments1 = ["mov", "r3", "r1"]
        bit_instruction1 = OP_LOAD << 28
        self.assertEqual(0xe0300001, self.asm.process_mov(arguments1, bit_instruction1))
        # Config LOAD_IMM
        arguments2 = ["mov", "r3", "234"]
        bit_instruction2 = OP_LOAD << 28
        self.assertEqual(0xe43000ea, self.asm.process_mov(arguments2, bit_instruction2))

    def test_process_load(self):
        # Config LOAD_RAA - bool
        arguments1 = ["loadbool", "r3", "r1"]
        bit_instruction1 = OP_LOAD << 28
        self.assertEqual(0xec300001, self.asm.process_load(arguments1, bit_instruction1))
        # Config LOAD_ADR - bool
        arguments2 = ["loadbool", "r3", "234"]
        bit_instruction2 = OP_LOAD << 28
        self.assertEqual(0xe83000ea, self.asm.process_load(arguments2, bit_instruction2))
        # Config LOAD_RAA - byte
        arguments1 = ["loadbyte", "r3", "r1"]
        bit_instruction1 = OP_LOAD << 28
        self.assertEqual(0xed300001, self.asm.process_load(arguments1, bit_instruction1))
        # Config LOAD_ADR - byte
        arguments2 = ["loadbyte", "r3", "234"]
        bit_instruction2 = OP_LOAD << 28
        self.assertEqual(0xe93000ea, self.asm.process_load(arguments2, bit_instruction2))
        # Config LOAD_RAA - int
        arguments1 = ["loadint", "r3", "r1"]
        bit_instruction1 = OP_LOAD << 28
        self.assertEqual(0xee300001, self.asm.process_load(arguments1, bit_instruction1))
        # Config LOAD_ADR - int
        arguments2 = ["loadint", "r3", "234"]
        bit_instruction2 = OP_LOAD << 28
        self.assertEqual(0xea3000ea, self.asm.process_load(arguments2, bit_instruction2))
        # Config LOAD_RAA - state
        arguments1 = ["loadstate", "r3", "r1"]
        bit_instruction1 = OP_LOAD << 28
        self.assertEqual(0xef300001, self.asm.process_load(arguments1, bit_instruction1))
        # Config LOAD_ADR - state
        arguments2 = ["loadstate", "r3", "234"]
        bit_instruction2 = OP_LOAD << 28
        self.assertEqual(0xeb3000ea, self.asm.process_load(arguments2, bit_instruction2))

    def test_process_store(self):
        # Config STORE_RAA - bool
        arguments1 = ["storebool", "r3", "r1"]
        bit_instruction1 = OP_STORE << 28
        self.assertEqual(0xd4300001, self.asm.process_store(arguments1, bit_instruction1))
        # Config STORE_ADR - bool
        arguments2 = ["storebool", "r3", "234"]
        bit_instruction2 = OP_STORE << 28
        self.assertEqual(0xd03000ea, self.asm.process_store(arguments2, bit_instruction2))
        # Config STORE_RAA - byte
        arguments1 = ["storebyte", "r3", "r1"]
        bit_instruction1 = OP_STORE << 28
        self.assertEqual(0xd5300001, self.asm.process_store(arguments1, bit_instruction1))
        # Config STORE_ADR - byte
        arguments2 = ["storebyte", "r3", "234"]
        bit_instruction2 = OP_STORE << 28
        self.assertEqual(0xd13000ea, self.asm.process_store(arguments2, bit_instruction2))
        # Config STORE_RAA - int
        arguments1 = ["storeint", "r3", "r1"]
        bit_instruction1 = OP_STORE << 28
        self.assertEqual(0xd6300001, self.asm.process_store(arguments1, bit_instruction1))
        # Config STORE_ADR - int
        arguments2 = ["storeint", "r3", "234"]
        bit_instruction2 = OP_STORE << 28
        self.assertEqual(0xd23000ea, self.asm.process_store(arguments2, bit_instruction2))
        # Config STORE_RAA - state
        arguments1 = ["storestate", "r3", "r1"]
        bit_instruction1 = OP_STORE << 28
        self.assertEqual(0xd7300001, self.asm.process_store(arguments1, bit_instruction1))
        # Config STORE_ADR - state
        arguments2 = ["storestate", "r3", "234"]
        bit_instruction2 = OP_STORE << 28
        self.assertEqual(0xd33000ea, self.asm.process_store(arguments2, bit_instruction2))

    def test_process_nop(self):
        arguments = ["nop"]
        bit_instruction = OP_NOP << 28
        self.assertEqual(0x00000000, self.asm.process_nop(arguments, bit_instruction))

    def test_process_endga(self):
        arguments = ["endga"]
        bit_instruction = OP_ENDGA << 28
        self.assertEqual(0xf0000000, self.asm.process_endga(arguments, bit_instruction))

    def test_process_line(self):
        self.assertEqual(0x10c00802, self.asm.process_line("add r3 r1 r2"))

    @patch('builtins.open', mock_open(read_data=mock_file))
    def test_process_file(self):
        expected_instructions = [
            0x10c00802,  # add r3 r1 r2
            0x24c0087a,  # sub r3 r1 122
            0x58c3d002,  # mod r3 122 r2
            0xacc3d87c,  # eq r3 123 124
            0xb3000001,  # not r3 r1
            0xc30000ea,  # jmp r3 234
            0xe0300001,  # mov r3 r1
            0xe43000ea,  # mov r3 234
            0xec300001,  # loadbool r3 r1
            0xe83000ea,  # loadbool r3 234
            0xed300001,  # loadbyte r3 r1
            0xe93000ea,  # loadbyte r3 234
            0xee300001,  # loadint r3 r1
            0xea3000ea,  # loadint r3 234
            0xef300001,  # loadstate r3 r1
            0xeb3000ea,  # loadstate r3 234
            0xd4300001,  # storebool r3 r1
            0xd03000ea,  # storebool r3 234
            0xd5300001,  # storebyte r3 r1
            0xd13000ea,  # storebyte r3 234
            0xd6300001,  # storeint r3 r1
            0xd23000ea,  # storeint r3 234
            0xd7300001,  # storestate r3 r1
            0xd33000ea,  # storestate r3 234
            0x00000000,  # nop
            0xf0000000   # endga
        ]
        self.assertEqual(expected_instructions, self.asm.process_file("path/to/mock/file"))
