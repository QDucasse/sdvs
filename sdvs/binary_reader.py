# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Binary reader: Handles the binary file and produces a list of 32-bits instructions.

class BinaryReader:

    @classmethod
    def read_instructions(cls, file_name):
        """
        Reads a binary file and returns a list with the processed instructions.
        :return: 32-bits instructions list
        """
        instructions = []
        with open(file_name, "rb") as file:
            instruction = file.read(4)  # read(1) processes 1 byte, we need 4 for an instruction
            while instruction:
                instructions.append(int.from_bytes(instruction, "little"))
                instruction = file.read(4)
        instructions.append(0x00000000)
        return instructions

    @classmethod
    def read_memory(cls, file_name):
        """
        Reads a binary file with the memory representation of the globals configuration.
        :return: raw memory
        """
        with open(file_name, "rb") as file:
            content = int.from_bytes(file.read(), "big")
        return content

    @classmethod
    def write_text_file(cls, file_name, instructions):
        """
        Write the result in a one instruction per line
        :param instructions:
        :param file_name:
        :return:
        """
        hex_instructions = ["{0:0{1}X}".format(instruction, 8) for instruction in instructions]
        with open(file_name, "w") as file:
            file.write("\n".join(hex_instructions))


if __name__ == "__main__":
    bin_instructions = BinaryReader.read_instructions("../sdve-beem-benchmark/bin/adding.6.out")
    hex_instructions = [hex(instruction) for instruction in bin_instructions]
    print("\n".join(hex_instructions))
    BinaryReader.write_text_file("../sdvu/cfg/prg_mem.ini", bin_instructions)