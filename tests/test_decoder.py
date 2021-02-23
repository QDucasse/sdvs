# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Decoder: Process 32-bits instruction into their corresponding instruction object.
# Test file!

import unittest
from sdvs.decoder import Decoder, Instruction


class TestDecoder(unittest.TestCase):

    def setUp(self):
        self.bit_instructions = [0x8080901c]
        self.decoder = Decoder(self.bit_instructions)
