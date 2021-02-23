# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Assembler: Process textual assembler to generate instructions.

from constants import *

def is_reg(string):
    return string.startswith("r")

def expect_reg(string):
    if not(is_reg(string)):
        raise ConfigException


class ConfigException(Exception):
    """
    Wrong configuration for this operation.
    """
    pass

class ASM:

    op_codes = {
        "add": OP_ADD,
        "sub": OP_SUB,
        "mul": OP_MUL,
        "div": OP_DIV,
        "mod": OP_MOD,
        "and": OP_AND,
        "or": OP_OR,
        "lt": OP_LT,
        "gt": OP_GT,
        "eq": OP_EQ,
        "not": OP_NOT,
        "jmp": OP_JMP,
        "storebool": OP_STORE,
        "storebyte": OP_STORE,
        "storeint": OP_STORE,
        "storestate": OP_STORE,
        "loadbool": OP_LOAD,
        "loadbyte": OP_LOAD,
        "loadint": OP_LOAD,
        "loadstate": OP_LOAD,
        "mov": OP_LOAD
    }


    def process_file(self, file_name):
        """
        Reads a textual asm-like file and generates the instructions accordingly
        :param file_name: file to process
        :return: list of instructions
        """
        instructions = []


    def process_line(self, line):
        """
        Process a line in asm into a 32-bits instruction.
        :param line: line to process
        :return: 32-bits instruction
        """
        arguments = line.split(" ")
        op = arguments[0]
        op_code = ASM.op_codes[op]
        bit_instruction = op_code << 28

        if op_code == OP_NOT:
            rd = arguments[1]
            ra = arguments[2]
            try:
                expect_reg(rd)
                expect_reg(ra)
            except ConfigException:
                print("Wrong configuration for not, two registers expected.")
            bit_instruction |= rd << 24
            bit_instruction |= ra

        elif op_code == OP_LOAD:
            if op == "mov":


        elif op_code == OP_JMP:
            pass

        elif op_code == OP_STORE:
            pass

        else:
            pass

        return bit_instruction

    def process_add(self):
        pass


    def process_add(self):
        pass


    def process_add(self):
        pass