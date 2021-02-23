# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Binary reader: Handles the binary file and produces a list of 32-bits instructions.
# Test file!

import unittest
from unittest.mock import patch, mock_open
from sdvs.binary_reader import BinaryReader

mock_file = b'\x80\x80\x90\x1c\xde\xa3\x12\x14'


class TestBinaryReader(unittest.TestCase):

    @patch('builtins.open', mock_open(read_data=mock_file))
    def testReadFile(self):
        instructions = BinaryReader.read_file("path/to/mock/file")
        self.assertEqual(instructions[0], 0x8080901c)
        self.assertEqual(instructions[1], 0xdea31214)
