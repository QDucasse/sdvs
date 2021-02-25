# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Memory: Holds the configuration and knows how to access the elements providing an address
# Test file!

import unittest
from sdvs.constants import *
from sdvs.memory import *


class TestMemory(unittest.TestCase):

    def setUp(self):
        self.memory = Memory()

    def test_gen_bin_number_ones(self):
        self.assertEqual(0xFFF, gen_bin_number_ones(12))
        self.assertEqual(0x3FF, gen_bin_number_ones(10))
        self.assertEqual(0x1, gen_bin_number_ones(1))

    def test_gen_bin_number_zeros(self):
        self.assertEqual(0b000000000000, gen_bin_number_zeros(12))
        self.assertEqual(0x0000000000, gen_bin_number_zeros(10))
        self.assertEqual(0x0, gen_bin_number_zeros(1))

    def test_set_bool_at_address(self):
        self.memory.raw_memory = 0xe0ee
        self.memory.set_bool_at_address(1, 8)
        self.assertEqual(0x01ee, self.memory.raw_memory)

    def test_set_bool_at_address_general(self):
        self.memory.raw_memory = 0xe0ee
        self.memory.set_at_address(VAL_BOOL, 1, 8)
        self.assertEqual(0x01ee, self.memory.raw_memory)

    def test_set_byte_at_address(self):
        self.memory.set_byte_at_address(7, 32)
        self.assertEqual(0x07eeeeeeee, self.memory.raw_memory)

    def test_set_byte_at_address_general(self):
        self.memory.set_at_address(VAL_BYTE, 7, 32)
        self.assertEqual(0x07eeeeeeee, self.memory.raw_memory)

    def test_set_int_at_address(self):
        self.memory.set_int_at_address(1234, 32)
        self.assertEqual(0x04d2eeeeeeee, self.memory.raw_memory)

    def test_set_int_at_address_general(self):
        self.memory.set_at_address(VAL_INT, 1234, 32)
        self.assertEqual(0x04d2eeeeeeee, self.memory.raw_memory)

    def test_set_state_at_address(self):
        self.memory.set_state_at_address(5, 32)
        self.assertEqual(0x05eeeeeeee, self.memory.raw_memory)

    def test_set_state_at_address_general(self):
        self.memory.set_at_address(VAL_STATE, 5, 32)
        self.assertEqual(0x05eeeeeeee, self.memory.raw_memory)

    def test_retrieve_bool_at_address(self):
        self.memory.raw_memory = 0x01ee
        self.assertEqual(1, self.memory.retrieve_bool_at_address(8))
        self.assertEqual(0x01ee, self.memory.raw_memory)

    def test_retrieve_bool_at_address_general(self):
        self.memory.raw_memory = 0x01ee
        self.assertEqual(1, self.memory.retrieve_at_address(VAL_BOOL, 8))
        self.assertEqual(0x01ee, self.memory.raw_memory)

    def test_retrieve_byte_at_address(self):
        self.memory.raw_memory = 0x07eeeeeeee
        self.assertEqual(7, self.memory.retrieve_byte_at_address(32))
        self.assertEqual(0x07eeeeeeee, self.memory.raw_memory)

    def test_retrieve_byte_at_address_general(self):
        self.memory.raw_memory = 0x07eeeeeeee
        self.assertEqual(7, self.memory.retrieve_at_address(VAL_BYTE, 32))
        self.assertEqual(0x07eeeeeeee, self.memory.raw_memory)

    def test_retrieve_int_at_address(self):
        self.memory.raw_memory = 0x04d2eeeeeeee
        self.assertEqual(1234, self.memory.retrieve_int_at_address(32))
        self.assertEqual(0x04d2eeeeeeee, self.memory.raw_memory)

    def test_retrieve_int_at_address_general(self):
        self.memory.raw_memory = 0x04d2eeeeeeee
        self.assertEqual(1234, self.memory.retrieve_at_address(VAL_INT, 32))
        self.assertEqual(0x04d2eeeeeeee, self.memory.raw_memory)

    def test_retrieve_state_at_address(self):
        self.memory.raw_memory = 0x05eeeeeeee
        self.assertEqual(5, self.memory.retrieve_state_at_address(32))
        self.assertEqual(0x05eeeeeeee, self.memory.raw_memory)

    def test_retrieve_state_at_address_general(self):
        self.memory.raw_memory = 0x05eeeeeeee
        self.assertEqual(5, self.memory.retrieve_at_address(VAL_STATE, 32))
        self.assertEqual(0x05eeeeeeee, self.memory.raw_memory)
