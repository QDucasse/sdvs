# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Instruction: Holder of the instructions information

from constants import *

class Instruction:
    """
    Instruction structure to hold the decoded parts of the 32-bits instruction.
    """

    OP_CODES_STR = {
        OP_ADD: "OP_ADD",
        OP_SUB: "OP_SUB",
        OP_MUL: "OP_MUL",
        OP_DIV: "OP_DIV",
        OP_MOD: "OP_MOD",
        OP_AND: "OP_AND",
        OP_OR: "OP_OR",
        OP_LT: "OP_LT",
        OP_GT: "OP_GT",
        OP_EQ: "OP_EQ",
        OP_NOT: "OP_NOT",
        OP_JMP: "OP_JMP",
        OP_STORE: "OP_STORE",
        OP_LOAD: "OP_LOAD"
    }

    BIN_CFG_STR = {
        CFG_RR: "CFG_RR",
        CFG_RI: "CFG_RI",
        CFG_IR: "CFG_IR",
        CFG_II: "CFG_II"
    }

    STORE_CFG_STR = {
        STORE_ADR: "STORE_ADR",
        STORE_RAA: "STORE_RAA"
    }

    LOAD_CFG_STR = {
        LOAD_ADR: "LOAD_ADR",
        LOAD_RAA: "LOAD_RAA",
        LOAD_REG: "LOAD_REG",
        LOAD_IMM: "LOAD_IMM"
    }

    TYPE_STR = {
        VAL_BOOL: "BOOL",
        VAL_BYTE: "BYTE",
        VAL_INT: "INT",
        VAL_STATE: "STATE"
    }

    def __init__(self, op_code, cfg_mask=0b00, inst_type=0b00,
                 rd=0b0000, ra=0b0000, rb=0b0000,
                 imma=0b00000000000, immb=0b00000000000,
                 address=0b000000000000000000000000):
        self.op_code = op_code
        self.cfg_mask = cfg_mask
        self.rd = rd
        self.ra = ra
        self.rb = rb
        self.imma = imma
        self.immb = immb
        self.address = address
        self.type = inst_type

    def __eq__(self, other):
        return (self.op_code == other.op_code and
                self.cfg_mask == other.cfg_mask and
                self.rd == other.rd and
                self.ra == other.ra and
                self.rb == other.rb and
                self.imma == other.imma and
                self.immb == other.immb and
                self.address == other.address and
                self.type == other.type)

    def __str__(self):
        return "Instruction {}".format(self.op_str)

    def op_str(self):
        return self.OP_CODES_STR[self.op_code]

    def cfg_str(self):
        if self.op_code == OP_LOAD:
            return self.LOAD_CFG_STR[self.cfg_mask]
        elif self.op_code == OP_STORE:
            return self.STORE_CFG_STR[self.cfg_mask]
        elif self.op_code == OP_JMP | self.op_code == OP_NOT:
            return "-"
        else:
            return self.BIN_CFG_STR[self.cfg_mask]

    def type_str(self):
        return self.TYPE_STR[self.type]