# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Binary reader: Handles the binary file and produces a list of 32-bits instructions.

class BinaryReader:

    @classmethod
    def read_file(cls, file_name):
        """
        Reads a binary file and returns a list with the processed instructions.
        :return: 32-bits instructions list
        """
        instructions = []
        with open(file_name, "rb") as file:
            instruction = file.read(4)  # read(1) processes 1 byte, we need 4 for an instruction
            while instruction:
                instructions.append(int.from_bytes(instruction, "big"))
                instruction = file.read(4)
        return instructions
