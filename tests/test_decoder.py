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


class TestDecoder(unittest.TestCase):

    @patch('builtins.open', mock_open(read_data=mock_file))
    def setUp(self):
        self.asm = ASM()
        self.bit_instructions = self.asm.process_file("path/to/mock/file")
        self.decoder = Decoder(self.bit_instructions)

    def test_decode_next(self):
        self.assertEqual()
