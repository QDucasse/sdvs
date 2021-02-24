# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Assembler: Process textual assembler to generate instructions.

from sdvs.constants import *

# Helper functions
def is_reg(string):
    return string.startswith("r")


def expect_reg(string, error_msg):
    if not (is_reg(string)):
        raise ConfigException(error_msg)


def extract_number(string):
    if is_reg(string):
        return int(string[1:])
    else:
        return int(string)


def determine_bin_cfg(arg1, arg2):
    if is_reg(arg1):
        if is_reg(arg2):
            return CFG_RR
        else:
            return CFG_RI
    else:
        if is_reg(arg2):
            return CFG_IR
        else:
            return CFG_II


def determine_load_cfg(arg):
    if is_reg(arg):
        return LOAD_RAA
    else:
        return LOAD_ADR


def determine_store_cfg(arg):
    if is_reg(arg):
        return STORE_RAA
    else:
        return STORE_ADR


def determine_mov_cfg(arg):
    if is_reg(arg):
        return LOAD_REG
    else:
        return LOAD_IMM


def determine_type(string):
    if string.endswith("bool"):
        return VAL_BOOL
    elif string.endswith("byte"):
        return VAL_BYTE
    elif string.endswith("int"):
        return VAL_INT
    elif string.endswith("state"):
        return VAL_STATE


class ConfigException(Exception):
    """
    Wrong configuration for this operation.
    """
    pass


class ASM:

    def process_file(self, file_name):
        """
        Reads a textual asm-like file and generates the instructions accordingly
        :param file_name: file to process
        :return: list of instructions
        """
        instructions = []
        with open(file_name, "r") as file:
            content = file.readlines()
        for line in content:
            instructions.append(self.process_line(line))


    def process_line(self, line):
        """
        Process a line in asm into a 32-bits instruction.
        :param line: line to process
        :return: 32-bits instruction
        """
        arguments = line.split(" ")
        op = arguments[0]
        op_code, process_function = ASM.OP_CODES[op]
        bit_instruction = op_code << 28
        bit_instruction = process_function(arguments, bit_instruction)
        return bit_instruction

    def process_binary(self, arguments, bit_instruction):
        """
        Process a binary operation (ADD to EQ).
        ex: add r0 r1 245
        """
        # Process the arguments
        if len(arguments) != 4:
            raise ConfigException("Binary operations should hold rd and two arguments")
        else:
            rd, lh, rh = arguments[1:]
        # Determine the config mask
        bit_instruction |= determine_bin_cfg(lh, rh) << 26
        # Expect the first argument to be a register (rd)
        expect_reg(rd, "First argument in Binary Operation should be a destination register")
        bit_instruction |= extract_number(rd) << 22
        # Process left hand and right hand operand
        bit_instruction |= extract_number(lh) << 11
        bit_instruction |= extract_number(rh)
        return bit_instruction

    def process_not(self, arguments, bit_instruction):
        """
        Process a NOT operation.
        ex: not r1 r2
        """
        # Process the arguments
        if len(arguments) != 3:
            raise ConfigException("NOT operation should hold rd and another argument")
        else:
            rd, ra = arguments[1:]
        # Expect the first argument to be a register (rd)
        expect_reg(rd, "First argument in NOT operation should be a destination register")
        bit_instruction |= extract_number(rd) << 24
        # Process ra register
        expect_reg(ra, "Second argument in NOT operation should be a register")
        bit_instruction |= extract_number(ra)
        return bit_instruction

    def process_jmp(self, arguments, bit_instruction):
        """
        Process JMP operation.
        ex: jmp r5 256
        """
        # Process the arguments
        if len(arguments) != 3:
            raise ConfigException("JMP operation should hold rd and an address")
        else:
            rd, address = arguments[1:]
        # Expect the first argument to be a register (rd)
        expect_reg(rd, "First argument in JMP operation should be a condition register")
        bit_instruction |= extract_number(rd) << 24
        # Process address register
        bit_instruction |= extract_number(address)
        return bit_instruction

    def process_mov(self, arguments, bit_instruction):
        """
        Process MOV operation.
        ex: mov r1 r3
        """
        # Process the arguments
        if len(arguments) != 3:
            raise ConfigException("MOV operation should hold rd and an argument")
        else:
            op, rd, lh = arguments
        # Process config and type
        bit_instruction |= determine_mov_cfg(lh) << 26
        bit_instruction |= determine_type(op) << 24
        # Expect the first argument to be a register (rd)
        expect_reg(rd, "First argument in MOV operation should be a destination register")
        bit_instruction |= extract_number(rd) << 20
        # Process address register
        bit_instruction |= extract_number(lh)
        return bit_instruction

    def process_load(self, arguments, bit_instruction):
        """
        Process LOAD operation.
        ex: load r4 356
        """
        # Process the arguments
        if len(arguments) != 3:
            raise ConfigException("LOAD operation should hold rd and an argument")
        else:
            op, rd, lh = arguments
        # Process config and type
        bit_instruction |= determine_load_cfg(lh) << 26
        bit_instruction |= determine_type(op) << 24
        # Expect the first argument to be a register (rd)
        expect_reg(rd, "First argument in LOAD operation should be a destination register")
        bit_instruction |= extract_number(rd) << 20
        # Process address register
        bit_instruction |= extract_number(lh)
        return bit_instruction

    def process_store(self,arguments, bit_instruction):
        """
        Process STORE operation.
        ex: store r4 256
        """
        # Process the arguments
        if len(arguments) != 3:
            raise ConfigException("STORE operation should hold rd and an argument")
        else:
            op, rd, lh = arguments
        # Process config and type
        bit_instruction |= determine_store_cfg(lh) << 26
        bit_instruction |= determine_type(op) << 24
        # Expect the first argument to be a register (rd)
        expect_reg(rd, "First argument in STORE operation should be a destination register")
        bit_instruction |= extract_number(rd) << 20
        # Process address register
        bit_instruction |= extract_number(lh)
        return bit_instruction

    OP_CODES = {
        "add": (OP_ADD, process_binary),
        "sub": (OP_SUB, process_binary),
        "mul": (OP_MUL, process_binary),
        "div": (OP_DIV, process_binary),
        "mod": (OP_MOD, process_binary),
        "and": (OP_AND, process_binary),
        "or": (OP_OR, process_binary),
        "lt": (OP_LT, process_binary),
        "gt": (OP_GT, process_binary),
        "eq": (OP_EQ, process_binary),
        "not": (OP_NOT, process_not),
        "jmp": (OP_JMP, process_jmp),
        "storebool": (OP_STORE, process_store),
        "storebyte": (OP_STORE, process_store),
        "storeint": (OP_STORE, process_store),
        "storestate": (OP_STORE, process_store),
        "loadbool": (OP_LOAD, process_load),
        "loadbyte": (OP_LOAD, process_load),
        "loadint": (OP_LOAD, process_load),
        "loadstate": (OP_LOAD, process_load),
        "mov": (OP_LOAD, process_mov)
    }
