# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Memory: Holds the configuration and knows how to access the elements providing an address
# Test file!

import unittest
from sdvs.memory import *


class TestMemory(unittest.TestCase):

    def test_gen_bin_number_ones(self):
        self.assertEqual(0xFFF, gen_bin_number_ones(12))
        self.assertEqual(0x3FF, gen_bin_number_ones(10))
        self.assertEqual(0x1, gen_bin_number_ones(1))

    def test_set_bool_at_address(self):
        memory = Memory(24, 0xeeeeee)
        memory.set_bool_at_address(1, 8)
        self.assertEqual(0xee01ee, memory.raw_memory)

    def test_set_bool_at_address_general(self):
        memory = Memory(24, 0xeeeeee)
        memory.set_at_address(VAL_BOOL, 1, 8)
        self.assertEqual(0xee01ee, memory.raw_memory)

    def test_set_byte_at_address(self):
        memory = Memory(48, 0xeeeeeeeeeeee)
        memory.set_byte_at_address(7, 32)
        self.assertEqual(0xee07eeeeeeee, memory.raw_memory)

    def test_set_byte_at_address_general(self):
        memory = Memory(48, 0xeeeeeeeeeeee)
        memory.set_at_address(VAL_BYTE, 7, 32)
        self.assertEqual(0xee07eeeeeeee, memory.raw_memory)

    def test_set_int_at_address(self):
        memory = Memory(80, 0xeeee00000000eeeeeeee)
        memory.set_int_at_address(1234, 32)
        self.assertEqual(0xeeee000004d2eeeeeeee, memory.raw_memory)

    def test_set_int_at_address_general(self):
        memory = Memory(80, 0xeeee00000000eeeeeeee)
        memory.set_at_address(VAL_INT, 1234, 32)
        self.assertEqual(0xeeee000004d2eeeeeeee, memory.raw_memory)

    def test_set_state_at_address(self):
        memory = Memory(56, 0xeeeeeeeeeeeeee)
        memory.set_state_at_address(5, 32)
        self.assertEqual(0xee0005eeeeeeee, memory.raw_memory)

    def test_set_state_at_address_general(self):
        memory = Memory(56, 0xeeeeeeeeeeeeee)
        memory.set_at_address(VAL_STATE, 5, 32)
        self.assertEqual(0xee0005eeeeeeee, memory.raw_memory)

    def test_retrieve_bool_at_address(self):
        memory = Memory(24, 0xee01ee)
        self.assertEqual(1, memory.retrieve_bool_at_address(8))
        self.assertEqual(0xee01ee, memory.raw_memory)

    def test_retrieve_bool_at_address_general(self):
        memory = Memory(24, 0xee01ee)
        self.assertEqual(1, memory.retrieve_at_address(VAL_BOOL, 8))
        self.assertEqual(0xee01ee, memory.raw_memory)

    def test_retrieve_byte_at_address(self):
        memory = Memory(48, 0xee07eeeeeeee)
        self.assertEqual(7, memory.retrieve_byte_at_address(32))
        self.assertEqual(0xee07eeeeeeee, memory.raw_memory)

    def test_retrieve_byte_at_address_general(self):
        memory = Memory(48, 0xee07eeeeeeee)
        self.assertEqual(7, memory.retrieve_at_address(VAL_BYTE, 32))
        self.assertEqual(0xee07eeeeeeee, memory.raw_memory)

    def test_retrieve_int_at_address(self):
        memory = Memory(80, 0xeeee000004d2eeeeeeee)
        self.assertEqual(1234, memory.retrieve_int_at_address(32))
        self.assertEqual(0xeeee000004d2eeeeeeee, memory.raw_memory)

    def test_retrieve_int_at_address_general(self):
        memory = Memory(80, 0xeeee000004d2eeeeeeee)
        self.assertEqual(1234, memory.retrieve_at_address(VAL_INT, 32))
        self.assertEqual(0xeeee000004d2eeeeeeee, memory.raw_memory)

    def test_retrieve_state_at_address(self):
        memory = Memory(56, 0xee0005eeeeeeee)
        self.assertEqual(5, memory.retrieve_state_at_address(32))
        self.assertEqual(0xee0005eeeeeeee, memory.raw_memory)

    def test_retrieve_state_at_address_general(self):
        memory = Memory(56, 0xee0005eeeeeeee)
        self.assertEqual(5, memory.retrieve_at_address(VAL_STATE, 32))
        self.assertEqual(0xee0005eeeeeeee, memory.raw_memory)
