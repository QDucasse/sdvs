# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Assembler: Process textual assembler to generate instructions.

import unittest
from sdvs.asm import *
from sdvs.constants import *


class TestASM(unittest.TestCase):

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
