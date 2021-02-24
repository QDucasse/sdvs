# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Constants and codes used in the project

# Register constants
REG_NUMBER = 16
REG_SIZE = 32

# Op codes
OP_ADD = 0b0000
OP_SUB = 0b0001
OP_MUL = 0b0010
OP_DIV = 0b0011
OP_MOD = 0b0100
OP_AND = 0b0101
OP_OR = 0b0110
OP_LT = 0b0111
OP_GT = 0b1000
OP_EQ = 0b1001
OP_NOT = 0b1010
OP_JMP = 0b1011
OP_STORE = 0b1100
OP_LOAD = 0b1101

# Binary configs
CFG_RR = 0b00
CFG_RI = 0b01
CFG_IR = 0b10
CFG_II = 0b11

# Load configs
LOAD_REG = 0b00
LOAD_IMM = 0b01
LOAD_ADR = 0b10
LOAD_RAA = 0b11

# Store configs
STORE_ADR = 0b00
STORE_RAA = 0b01

# Types configs
VAL_BOOL = 0b00
VAL_BYTE = 0b01
VAL_INT = 0b10
VAL_STATE = 0b11

