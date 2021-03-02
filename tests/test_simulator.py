# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Simulator: Process instructions one by one and show the results of their execution
# Test File!

import unittest
from unittest.mock import patch, mock_open

from asm import ASM
from constants import *
from decoder import Decoder, Instruction
from memory import Memory
from simulator import Simulator

# Instructions file setup
ADD_INDEX = 0
SUB_INDEX = 4
MUL_INDEX = 8
DIV_INDEX = 12
MOD_INDEX = 16
AND_INDEX = 20
OR_INDEX = 24
LT_INDEX = 28
GT_INDEX = 32
EQ_INDEX = 36
NOT_INDEX = 40
JMP_INDEX = 41
MOV_INDEX = 42
LOADBOOL_INDEX = 44
LOADBYTE_INDEX = 46
LOADINT_INDEX = 48
LOADSTATE_INDEX = 50
STOREBOOL_INDEX = 52
STOREBYTE_INDEX = 54
STOREINT_INDEX = 56
STORESTATE_INDEX = 58

binops = ["add", "sub", "mul", "div", "mod",
          "and", "or", "lt", "gt", "eq"]

mock_file = """not r3 r1
jmp r3 32
mov r3 r1
mov r3 234
loadbool r3 r1
loadbool r3 8
loadbyte r3 r1
loadbyte r3 8
loadint r3 r1
loadint r3 8
loadstate r3 r1
loadstate r3 8
storebool r3 r1
storebool r3 8
storebyte r3 r1
storebyte r3 8
storeint r3 r1
storeint r3 8
storestate r3 r1
storestate r3 8
"""


def append_bin_mock_file(mock_file):
    bin_mock_file = """"""
    for op in binops:
        bin_mock_file += op + " r3 r1 r2\n"
        bin_mock_file += op + " r3 r1 122\n"
        bin_mock_file += op + " r3 122 r2\n"
        bin_mock_file += op + " r3 123 124\n"
    return bin_mock_file + mock_file


mock_file = append_bin_mock_file(mock_file)


# Dummy instruction setup
def setUpInstruction(op_code, cfg, data_type=VAL_BOOL):
    instruction = Instruction(op_code)
    instruction.cfg_mask = cfg
    instruction.rd = 1
    instruction.ra = 2
    instruction.rb = 3
    instruction.imma = 122
    instruction.immb = 123
    instruction.address = 124
    instruction.type = data_type
    return instruction


class TestSimulator(unittest.TestCase):

    @patch('builtins.open', mock_open(read_data=mock_file))
    def setUp(self):
        asm = ASM()
        bit_instructions = asm.process_file("path/to/mock/file")
        decoder = Decoder(bit_instructions)
        memory = Memory(0, 0)
        self.simulator = Simulator(decoder, memory)

    def testAssignRegisterValue(self):
        for reg in self.simulator.registers:
            self.assertEqual(0, reg.value)
        self.simulator.assign_register_value(7, 32)
        for reg in self.simulator.registers:
            if reg.number == 7:
                self.assertEqual(32, reg.value)
            else:
                self.assertEqual(0, reg.value)

    def testRetrieveRegisterValue(self):
        self.simulator.registers[7].value = 32
        for i, reg in enumerate(self.simulator.registers):
            if reg.number == 7:
                self.assertEqual(32, self.simulator.retrieve_register_value(i))
            else:
                self.assertEqual(0, self.simulator.retrieve_register_value(i))

    def testProcessBinaryOperandsRR(self):
        self.simulator.registers[2].value = 2
        self.simulator.registers[3].value = 4
        for op in range(OP_EQ + 1):
            self.simulator.current_instruction = setUpInstruction(op, CFG_RR)
            left_operand, right_operand = self.simulator.process_binary_operands()
            self.assertEqual(2, left_operand)
            self.assertEqual(4, right_operand)

    def testProcessBinaryOperandsRI(self):
        self.simulator.registers[2].value = 2
        for op in range(OP_EQ + 1):
            self.simulator.current_instruction = setUpInstruction(op, CFG_RI)
            left_operand, right_operand = self.simulator.process_binary_operands()
            self.assertEqual(2, left_operand)
            self.assertEqual(123, right_operand)

    def testProcessBinaryOperandsIR(self):
        self.simulator.registers[3].value = 4
        for op in range(OP_EQ + 1):
            self.simulator.current_instruction = setUpInstruction(op, CFG_IR)
            left_operand, right_operand = self.simulator.process_binary_operands()
            self.assertEqual(122, left_operand)
            self.assertEqual(4, right_operand)

    def testProcessBinaryOperandsII(self):
        for op in range(OP_EQ + 1):
            self.simulator.current_instruction = setUpInstruction(op, CFG_II)
            left_operand, right_operand = self.simulator.process_binary_operands()
            self.assertEqual(122, left_operand)
            self.assertEqual(123, right_operand)

    # --------------
    # ADD OPERATIONS
    # --------------

    def testProcessAddRR(self):
        self.simulator.decoder.next_instruction_index = ADD_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_add()
        self.assertEqual(1 + 2, self.simulator.registers[3].value)

    def testProcessAddRI(self):
        self.simulator.decoder.next_instruction_index = ADD_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.process_add()
        self.assertEqual(1 + 122, self.simulator.registers[3].value)

    def testProcessAddIR(self):
        self.simulator.decoder.next_instruction_index = ADD_INDEX + 2
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[2].value = 2
        self.simulator.process_add()
        self.assertEqual(122 + 2, self.simulator.registers[3].value)

    def testProcessAddII(self):
        self.simulator.decoder.next_instruction_index = ADD_INDEX + 3
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_add()
        self.assertEqual(123 + 124, self.simulator.registers[3].value)

    def testProcessOneInstructionAddRR(self):
        self.simulator.decoder.next_instruction_index = ADD_INDEX
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(1 + 2, self.simulator.registers[3].value)

    def testProcessOneInstructionAddRI(self):
        self.simulator.decoder.next_instruction_index = ADD_INDEX + 1
        self.simulator.registers[1].value = 1
        self.simulator.process_one_instruction()
        self.assertEqual(1 + 122, self.simulator.registers[3].value)

    def testProcessOneInstructionAddIR(self):
        self.simulator.decoder.next_instruction_index = ADD_INDEX + 2
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(122 + 2, self.simulator.registers[3].value)

    def testProcessOneInstructionAddII(self):
        self.simulator.decoder.next_instruction_index = ADD_INDEX + 3
        self.simulator.process_one_instruction()
        self.assertEqual(123 + 124, self.simulator.registers[3].value)

    # --------------
    # SUB OPERATIONS
    # --------------

    def testProcessSubRR(self):
        self.simulator.decoder.next_instruction_index = SUB_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_sub()
        self.assertEqual(1 - 2, self.simulator.registers[3].value)

    def testProcessSubRI(self):
        self.simulator.decoder.next_instruction_index = SUB_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.process_sub()
        self.assertEqual(1 - 122, self.simulator.registers[3].value)

    def testProcessSubIR(self):
        self.simulator.decoder.next_instruction_index = SUB_INDEX + 2
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[2].value = 2
        self.simulator.process_sub()
        self.assertEqual(122 - 2, self.simulator.registers[3].value)

    def testProcessSubII(self):
        self.simulator.decoder.next_instruction_index = SUB_INDEX + 3
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_sub()
        self.assertEqual(123 - 124, self.simulator.registers[3].value)

    def testProcessOneInstructionSubRR(self):
        self.simulator.decoder.next_instruction_index = SUB_INDEX
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(1 - 2, self.simulator.registers[3].value)

    def testProcessOneInstructionSubRI(self):
        self.simulator.decoder.next_instruction_index = SUB_INDEX + 1
        self.simulator.registers[1].value = 1
        self.simulator.process_one_instruction()
        self.assertEqual(1 - 122, self.simulator.registers[3].value)

    def testProcessOneInstructionSubIR(self):
        self.simulator.decoder.next_instruction_index = SUB_INDEX + 2
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(122 - 2, self.simulator.registers[3].value)

    def testProcessOneInstructionSubII(self):
        self.simulator.decoder.next_instruction_index = SUB_INDEX + 3
        self.simulator.process_one_instruction()
        self.assertEqual(123 - 124, self.simulator.registers[3].value)

    # --------------
    # MUL OPERATIONS
    # --------------

    def testProcessMulRR(self):
        self.simulator.decoder.next_instruction_index = MUL_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_mul()
        self.assertEqual(1 * 2, self.simulator.registers[3].value)

    def testProcessMulRI(self):
        self.simulator.decoder.next_instruction_index = MUL_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.process_mul()
        self.assertEqual(1 * 122, self.simulator.registers[3].value)

    def testProcessMulIR(self):
        self.simulator.decoder.next_instruction_index = MUL_INDEX + 2
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[2].value = 2
        self.simulator.process_mul()
        self.assertEqual(122 * 2, self.simulator.registers[3].value)

    def testProcessMulII(self):
        self.simulator.decoder.next_instruction_index = MUL_INDEX + 3
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_mul()
        self.assertEqual(123 * 124, self.simulator.registers[3].value)

    def testProcessOneInstructionMulRR(self):
        self.simulator.decoder.next_instruction_index = MUL_INDEX
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(1 * 2, self.simulator.registers[3].value)

    def testProcessOneInstructionMulRI(self):
        self.simulator.decoder.next_instruction_index = MUL_INDEX + 1
        self.simulator.registers[1].value = 1
        self.simulator.process_one_instruction()
        self.assertEqual(1 * 122, self.simulator.registers[3].value)

    def testProcessOneInstructionMulIR(self):
        self.simulator.decoder.next_instruction_index = MUL_INDEX + 2
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(122 * 2, self.simulator.registers[3].value)

    def testProcessOneInstructionMulII(self):
        self.simulator.decoder.next_instruction_index = MUL_INDEX + 3
        self.simulator.process_one_instruction()
        self.assertEqual(123 * 124, self.simulator.registers[3].value)

    # --------------
    # DIV OPERATIONS
    # --------------

    def testProcessDivRR(self):
        self.simulator.decoder.next_instruction_index = DIV_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_div()
        self.assertEqual(1 / 2, self.simulator.registers[3].value)

    def testProcessDivRI(self):
        self.simulator.decoder.next_instruction_index = DIV_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.process_div()
        self.assertEqual(1 / 122, self.simulator.registers[3].value)

    def testProcessDivIR(self):
        self.simulator.decoder.next_instruction_index = DIV_INDEX + 2
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[2].value = 2
        self.simulator.process_div()
        self.assertEqual(122 / 2, self.simulator.registers[3].value)

    def testProcessDivII(self):
        self.simulator.decoder.next_instruction_index = DIV_INDEX + 3
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_div()
        self.assertEqual(123 / 124, self.simulator.registers[3].value)

    def testProcessOneInstructionDivRR(self):
        self.simulator.decoder.next_instruction_index = DIV_INDEX
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(1 / 2, self.simulator.registers[3].value)

    def testProcessOneInstructionDivRI(self):
        self.simulator.decoder.next_instruction_index = DIV_INDEX + 1
        self.simulator.registers[1].value = 1
        self.simulator.process_one_instruction()
        self.assertEqual(1 / 122, self.simulator.registers[3].value)

    def testProcessOneInstructionDivIR(self):
        self.simulator.decoder.next_instruction_index = DIV_INDEX + 2
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(122 / 2, self.simulator.registers[3].value)

    def testProcessOneInstructionDivII(self):
        self.simulator.decoder.next_instruction_index = DIV_INDEX + 3
        self.simulator.process_one_instruction()
        self.assertEqual(123 / 124, self.simulator.registers[3].value)

    # --------------
    # MOD OPERATIONS
    # --------------

    def testProcessModRR(self):
        self.simulator.decoder.next_instruction_index = MOD_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_mod()
        self.assertEqual(1 % 2, self.simulator.registers[3].value)

    def testProcessModRI(self):
        self.simulator.decoder.next_instruction_index = MOD_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.process_mod()
        self.assertEqual(1 % 122, self.simulator.registers[3].value)

    def testProcessModIR(self):
        self.simulator.decoder.next_instruction_index = MOD_INDEX + 2
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[2].value = 2
        self.simulator.process_mod()
        self.assertEqual(122 % 2, self.simulator.registers[3].value)

    def testProcessModII(self):
        self.simulator.decoder.next_instruction_index = MOD_INDEX + 3
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_mod()
        self.assertEqual(123 % 124, self.simulator.registers[3].value)

    def testProcessOneInstructionModRR(self):
        self.simulator.decoder.next_instruction_index = MOD_INDEX
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(1 % 2, self.simulator.registers[3].value)

    def testProcessOneInstructionModRI(self):
        self.simulator.decoder.next_instruction_index = MOD_INDEX + 1
        self.simulator.registers[1].value = 1
        self.simulator.process_one_instruction()
        self.assertEqual(1 % 122, self.simulator.registers[3].value)

    def testProcessOneInstructionModIR(self):
        self.simulator.decoder.next_instruction_index = MOD_INDEX + 2
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(122 % 2, self.simulator.registers[3].value)

    def testProcessOneInstructionModII(self):
        self.simulator.decoder.next_instruction_index = MOD_INDEX + 3
        self.simulator.process_one_instruction()
        self.assertEqual(123 % 124, self.simulator.registers[3].value)

    # --------------
    # AND OPERATIONS
    # --------------

    def testProcessAndRR(self):
        self.simulator.decoder.next_instruction_index = AND_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_and()
        self.assertEqual(1 and 2, self.simulator.registers[3].value)

    def testProcessAndRI(self):
        self.simulator.decoder.next_instruction_index = AND_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.process_and()
        self.assertEqual(1 and 122, self.simulator.registers[3].value)

    def testProcessAndIR(self):
        self.simulator.decoder.next_instruction_index = AND_INDEX + 2
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[2].value = 2
        self.simulator.process_and()
        self.assertEqual(122 and 2, self.simulator.registers[3].value)

    def testProcessAndII(self):
        self.simulator.decoder.next_instruction_index = AND_INDEX + 3
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_and()
        self.assertEqual(123 and 124, self.simulator.registers[3].value)

    def testProcessOneInstructionAndRR(self):
        self.simulator.decoder.next_instruction_index = AND_INDEX
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(1 and 2, self.simulator.registers[3].value)

    def testProcessOneInstructionAndRI(self):
        self.simulator.decoder.next_instruction_index = AND_INDEX + 1
        self.simulator.registers[1].value = 1
        self.simulator.process_one_instruction()
        self.assertEqual(1 and 122, self.simulator.registers[3].value)

    def testProcessOneInstructionAndIR(self):
        self.simulator.decoder.next_instruction_index = AND_INDEX + 2
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(122 and 2, self.simulator.registers[3].value)

    def testProcessOneInstructionAndII(self):
        self.simulator.decoder.next_instruction_index = AND_INDEX + 3
        self.simulator.process_one_instruction()
        self.assertEqual(123 and 124, self.simulator.registers[3].value)

    # --------------
    # OR OPERATIONS
    # --------------

    def testProcessOrRR(self):
        self.simulator.decoder.next_instruction_index = OR_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_or()
        self.assertEqual(1 or 2, self.simulator.registers[3].value)

    def testProcessOrRI(self):
        self.simulator.decoder.next_instruction_index = OR_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.process_or()
        self.assertEqual(1 or 122, self.simulator.registers[3].value)

    def testProcessOrIR(self):
        self.simulator.decoder.next_instruction_index = OR_INDEX + 2
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[2].value = 2
        self.simulator.process_or()
        self.assertEqual(122 or 2, self.simulator.registers[3].value)

    def testProcessOrII(self):
        self.simulator.decoder.next_instruction_index = OR_INDEX + 3
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_or()
        self.assertEqual(123 or 124, self.simulator.registers[3].value)

    def testProcessOneInstructionOrRR(self):
        self.simulator.decoder.next_instruction_index = OR_INDEX
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(1 or 2, self.simulator.registers[3].value)

    def testProcessOneInstructionOrRI(self):
        self.simulator.decoder.next_instruction_index = OR_INDEX + 1
        self.simulator.registers[1].value = 1
        self.simulator.process_one_instruction()
        self.assertEqual(1 or 122, self.simulator.registers[3].value)

    def testProcessOneInstructionOrIR(self):
        self.simulator.decoder.next_instruction_index = OR_INDEX + 2
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(122 or 2, self.simulator.registers[3].value)

    def testProcessOneInstructionOrII(self):
        self.simulator.decoder.next_instruction_index = OR_INDEX + 3
        self.simulator.process_one_instruction()
        self.assertEqual(123 or 124, self.simulator.registers[3].value)

    # --------------
    # LT OPERATIONS
    # --------------

    def testProcessLtRR(self):
        self.simulator.decoder.next_instruction_index = LT_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_less_than()
        self.assertEqual(1 < 2, self.simulator.registers[3].value)

    def testProcessLtRI(self):
        self.simulator.decoder.next_instruction_index = LT_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.process_less_than()
        self.assertEqual(1 < 122, self.simulator.registers[3].value)

    def testProcessLtIR(self):
        self.simulator.decoder.next_instruction_index = LT_INDEX + 2
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[2].value = 2
        self.simulator.process_less_than()
        self.assertEqual(122 < 2, self.simulator.registers[3].value)

    def testProcessLtII(self):
        self.simulator.decoder.next_instruction_index = LT_INDEX + 3
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_less_than()
        self.assertEqual(123 < 124, self.simulator.registers[3].value)

    def testProcessOneInstructionLtRR(self):
        self.simulator.decoder.next_instruction_index = LT_INDEX
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(1 < 2, self.simulator.registers[3].value)

    def testProcessOneInstructionLtRI(self):
        self.simulator.decoder.next_instruction_index = LT_INDEX + 1
        self.simulator.registers[1].value = 1
        self.simulator.process_one_instruction()
        self.assertEqual(1 < 122, self.simulator.registers[3].value)

    def testProcessOneInstructionLtIR(self):
        self.simulator.decoder.next_instruction_index = LT_INDEX + 2
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(122 < 2, self.simulator.registers[3].value)

    def testProcessOneInstructionLtII(self):
        self.simulator.decoder.next_instruction_index = LT_INDEX + 3
        self.simulator.process_one_instruction()
        self.assertEqual(123 < 124, self.simulator.registers[3].value)

    # --------------
    # GT OPERATIONS
    # --------------

    def testProcessGtRR(self):
        self.simulator.decoder.next_instruction_index = GT_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_greater_than()
        self.assertEqual(1 > 2, self.simulator.registers[3].value)

    def testProcessGtRI(self):
        self.simulator.decoder.next_instruction_index = GT_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.process_greater_than()
        self.assertEqual(1 > 122, self.simulator.registers[3].value)

    def testProcessGtIR(self):
        self.simulator.decoder.next_instruction_index = GT_INDEX + 2
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[2].value = 2
        self.simulator.process_greater_than()
        self.assertEqual(122 > 2, self.simulator.registers[3].value)

    def testProcessGtII(self):
        self.simulator.decoder.next_instruction_index = GT_INDEX + 3
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_greater_than()
        self.assertEqual(123 > 124, self.simulator.registers[3].value)

    def testProcessOneInstructionGtRR(self):
        self.simulator.decoder.next_instruction_index = GT_INDEX
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(1 > 2, self.simulator.registers[3].value)

    def testProcessOneInstructionGtRI(self):
        self.simulator.decoder.next_instruction_index = GT_INDEX + 1
        self.simulator.registers[1].value = 1
        self.simulator.process_one_instruction()
        self.assertEqual(1 > 122, self.simulator.registers[3].value)

    def testProcessOneInstructionGtIR(self):
        self.simulator.decoder.next_instruction_index = GT_INDEX + 2
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(122 > 2, self.simulator.registers[3].value)

    def testProcessOneInstructionGtII(self):
        self.simulator.decoder.next_instruction_index = GT_INDEX + 3
        self.simulator.process_one_instruction()
        self.assertEqual(123 > 124, self.simulator.registers[3].value)

    # --------------
    # EQ OPERATIONS
    # --------------

    def testProcessEqRR(self):
        self.simulator.decoder.next_instruction_index = EQ_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_equal()
        self.assertEqual(1 == 2, self.simulator.registers[3].value)

    def testProcessEqRI(self):
        self.simulator.decoder.next_instruction_index = EQ_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 1
        self.simulator.process_equal()
        self.assertEqual(1 == 122, self.simulator.registers[3].value)

    def testProcessEqIR(self):
        self.simulator.decoder.next_instruction_index = EQ_INDEX + 2
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[2].value = 2
        self.simulator.process_equal()
        self.assertEqual(122 == 2, self.simulator.registers[3].value)

    def testProcessEqII(self):
        self.simulator.decoder.next_instruction_index = EQ_INDEX + 3
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_equal()
        self.assertEqual(123 == 124, self.simulator.registers[3].value)

    def testProcessOneInstructionEqRR(self):
        self.simulator.decoder.next_instruction_index = EQ_INDEX
        self.simulator.registers[1].value = 1
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(1 == 2, self.simulator.registers[3].value)

    def testProcessOneInstructionEqRI(self):
        self.simulator.decoder.next_instruction_index = EQ_INDEX + 1
        self.simulator.registers[1].value = 1
        self.simulator.process_one_instruction()
        self.assertEqual(1 == 122, self.simulator.registers[3].value)

    def testProcessOneInstructionEqIR(self):
        self.simulator.decoder.next_instruction_index = EQ_INDEX + 2
        self.simulator.registers[2].value = 2
        self.simulator.process_one_instruction()
        self.assertEqual(122 == 2, self.simulator.registers[3].value)

    def testProcessOneInstructionEqII(self):
        self.simulator.decoder.next_instruction_index = EQ_INDEX + 3
        self.simulator.process_one_instruction()
        self.assertEqual(123 == 124, self.simulator.registers[3].value)

    # --------------
    # NOT OPERATIONS
    # --------------

    def testProcessNot(self):
        self.simulator.decoder.next_instruction_index = NOT_INDEX
        self.simulator.registers[1].value = 23
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_not()
        self.assertEqual(not 23, self.simulator.registers[3].value)

    def testProcessOneInstructionNot(self):
        self.simulator.decoder.next_instruction_index = NOT_INDEX
        self.simulator.registers[1].value = 23
        self.simulator.process_one_instruction()
        self.assertEqual(not 23, self.simulator.registers[3].value)

    # --------------
    # JMP OPERATIONS
    # --------------

    def testProcessJmpTrue(self):
        self.simulator.decoder.next_instruction_index = JMP_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[3].value = 1 # True
        self.simulator.process_jmp()
        self.assertEqual(8, self.simulator.decoder.next_instruction_index)

    def testProcessOneInstructionJmpTrue(self):
        self.simulator.decoder.next_instruction_index = JMP_INDEX
        self.simulator.registers[3].value = 1  # True
        self.simulator.process_one_instruction()
        self.assertEqual(8, self.simulator.decoder.next_instruction_index)

    def testProcessJmpFalse(self):
        self.simulator.decoder.next_instruction_index = JMP_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[3].value = 0  # False
        self.simulator.process_jmp()
        self.assertEqual(JMP_INDEX + 1, self.simulator.decoder.next_instruction_index)

    def testProcessOneInstructionJmpFalse(self):
        self.simulator.decoder.next_instruction_index = JMP_INDEX
        self.simulator.registers[3].value = 0  # False
        self.simulator.process_one_instruction()
        self.assertEqual(JMP_INDEX + 1, self.simulator.decoder.next_instruction_index)

    # --------------
    # MOV OPERATIONS
    # --------------

    def testProcessMovReg(self):
        self.simulator.decoder.next_instruction_index = MOV_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.registers[1].value = 32
        self.simulator.process_load()
        self.assertEqual(32, self.simulator.registers[3].value)

    def testProcessMovImm(self):
        self.simulator.decoder.next_instruction_index = MOV_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.process_load()
        self.assertEqual(234, self.simulator.registers[3].value)

    def testProcessOneInstructionMovReg(self):
        self.simulator.decoder.next_instruction_index = MOV_INDEX
        self.simulator.registers[1].value = 32
        self.simulator.process_one_instruction()
        self.assertEqual(32, self.simulator.registers[3].value)

    def testProcessOneInstructionMovImm(self):
        self.simulator.decoder.next_instruction_index = MOV_INDEX + 1
        self.simulator.process_one_instruction()
        self.assertEqual(234, self.simulator.registers[3].value)

    # ---------------
    # LOAD OPERATIONS
    # ---------------

    def testProcessLoadBoolRAA(self):
        self.simulator.decoder.next_instruction_index = LOADBOOL_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeeeee01ee)
        self.simulator.registers[1].value = 8     # address
        self.simulator.process_load()
        self.assertEqual(1, self.simulator.registers[3].value)

    def testProcessLoadBoolADR(self):
        self.simulator.decoder.next_instruction_index = LOADBOOL_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeeeee01ee)
        self.simulator.process_load()
        self.assertEqual(1, self.simulator.registers[3].value)

    def testProcessOneInstructionLoadBoolRAA(self):
        self.simulator.decoder.next_instruction_index = LOADBOOL_INDEX
        self.simulator.memory = Memory(40, 0xeeeeee01ee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.process_one_instruction()
        self.assertEqual(1, self.simulator.registers[3].value)

    def testProcessOneInstructionLoadBoolADR(self):
        self.simulator.decoder.next_instruction_index = LOADBOOL_INDEX + 1
        self.simulator.memory = Memory(40, 0xeeeeee01ee)
        self.simulator.process_one_instruction()
        self.assertEqual(1, self.simulator.registers[3].value)

    def testProcessLoadByteRAA(self):
        self.simulator.decoder.next_instruction_index = LOADBYTE_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeeeee24ee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.process_load()
        self.assertEqual(0x24, self.simulator.registers[3].value)

    def testProcessLoadByteADR(self):
        self.simulator.decoder.next_instruction_index = LOADBYTE_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeeeee24ee)
        self.simulator.process_load()
        self.assertEqual(0x24, self.simulator.registers[3].value)

    def testProcessOneInstructionLoadByteRAA(self):
        self.simulator.decoder.next_instruction_index = LOADBYTE_INDEX
        self.simulator.memory = Memory(40, 0xeeeeee24ee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.process_one_instruction()
        self.assertEqual(0x24, self.simulator.registers[3].value)

    def testProcessOneInstructionLoadByteADR(self):
        self.simulator.decoder.next_instruction_index = LOADBYTE_INDEX + 1
        self.simulator.memory = Memory(40, 0xeeeeee24ee)
        self.simulator.process_one_instruction()
        self.assertEqual(0x24, self.simulator.registers[3].value)

    def testProcessLoadIntRAA(self):
        self.simulator.decoder.next_instruction_index = LOADINT_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(48, 0xee12341234ee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.process_load()
        self.assertEqual(0x12341234, self.simulator.registers[3].value)

    def testProcessLoadIntADR(self):
        self.simulator.decoder.next_instruction_index = LOADINT_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(48, 0xee12341234ee)
        self.simulator.process_load()
        self.assertEqual(0x12341234, self.simulator.registers[3].value)

    def testProcessOneInstructionLoadIntRAA(self):
        self.simulator.decoder.next_instruction_index = LOADINT_INDEX
        self.simulator.memory = Memory(48, 0xee12341234ee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.process_one_instruction()
        self.assertEqual(0x12341234, self.simulator.registers[3].value)

    def testProcessOneInstructionLoadIntADR(self):
        self.simulator.decoder.next_instruction_index = LOADINT_INDEX + 1
        self.simulator.memory = Memory(48, 0xee12341234ee)
        self.simulator.process_one_instruction()
        self.assertEqual(0x12341234, self.simulator.registers[3].value)

    def testProcessLoadStateRAA(self):
        self.simulator.decoder.next_instruction_index = LOADSTATE_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeee1234ee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.process_load()
        self.assertEqual(0x1234, self.simulator.registers[3].value)

    def testProcessLoadStateADR(self):
        self.simulator.decoder.next_instruction_index = LOADSTATE_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeee1234ee)
        self.simulator.process_load()
        self.assertEqual(0x1234, self.simulator.registers[3].value)

    def testProcessOneInstructionLoadStateRAA(self):
        self.simulator.decoder.next_instruction_index = LOADSTATE_INDEX
        self.simulator.memory = Memory(40, 0xeeee1234ee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.process_one_instruction()
        self.assertEqual(0x1234, self.simulator.registers[3].value)

    def testProcessOneInstructionLoadStateADR(self):
        self.simulator.decoder.next_instruction_index = LOADSTATE_INDEX + 1
        self.simulator.memory = Memory(40, 0xeeee1234ee)
        self.simulator.process_one_instruction()
        self.assertEqual(0x1234, self.simulator.registers[3].value)

    # ----------------
    # STORE OPERATIONS
    # ----------------

    def testProcessStoreBoolRAA(self):
        self.simulator.decoder.next_instruction_index = STOREBOOL_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[1].value = 8     # address
        self.simulator.registers[3].value = 0x01  # value
        self.simulator.process_store()
        self.assertEqual(0xeeeeee01ee, self.simulator.memory.raw_memory)

    def testProcessStoreBoolADR(self):
        self.simulator.decoder.next_instruction_index = STOREBOOL_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[3].value = 0x01  # value
        self.simulator.process_store()
        self.assertEqual(0xeeeeee01ee, self.simulator.memory.raw_memory)

    def testProcessOneInstructionStoreBoolRAA(self):
        self.simulator.decoder.next_instruction_index = STOREBOOL_INDEX
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.registers[3].value = 0x01  # value
        self.simulator.process_one_instruction()
        self.assertEqual(0xeeeeee01ee, self.simulator.memory.raw_memory)

    def testProcessOneInstructionStoreBoolADR(self):
        self.simulator.decoder.next_instruction_index = STOREBOOL_INDEX + 1
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[3].value = 0x01  # value
        self.simulator.process_one_instruction()
        self.assertEqual(0xeeeeee01ee, self.simulator.memory.raw_memory)

    def testProcessStoreByteRAA(self):
        self.simulator.decoder.next_instruction_index = STOREBYTE_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.registers[3].value = 0x24  # value
        self.simulator.process_store()
        self.assertEqual(0xeeeeee24ee, self.simulator.memory.raw_memory)

    def testProcessStoreByteADR(self):
        self.simulator.decoder.next_instruction_index = STOREBYTE_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[3].value = 0x24  # value
        self.simulator.process_store()
        self.assertEqual(0xeeeeee24ee, self.simulator.memory.raw_memory)

    def testProcessOneInstructionStoreByteRAA(self):
        self.simulator.decoder.next_instruction_index = STOREBYTE_INDEX
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.registers[3].value = 0x24  # value
        self.simulator.process_one_instruction()
        self.assertEqual(0xeeeeee24ee, self.simulator.memory.raw_memory)

    def testProcessOneInstructionStoreByteADR(self):
        self.simulator.decoder.next_instruction_index = STOREBYTE_INDEX + 1
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[3].value = 0x24  # value
        self.simulator.process_one_instruction()
        self.assertEqual(0xeeeeee24ee, self.simulator.memory.raw_memory)

    def testProcessStoreIntRAA(self):
        self.simulator.decoder.next_instruction_index = STOREINT_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(48, 0xeeeeeeeeeeee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.registers[3].value = 0x12341234  # value
        self.simulator.process_store()
        self.assertEqual(0xee12341234ee, self.simulator.memory.raw_memory)

    def testProcessStoreIntADR(self):
        self.simulator.decoder.next_instruction_index = STOREINT_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(48, 0xeeeeeeeeeeee)
        self.simulator.registers[3].value = 0x12341234  # value
        self.simulator.process_store()
        self.assertEqual(0xee12341234ee, self.simulator.memory.raw_memory)

    def testProcessOneInstructionStoreIntRAA(self):
        self.simulator.decoder.next_instruction_index = STOREINT_INDEX
        self.simulator.memory = Memory(48, 0xeeeeeeeeeeee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.registers[3].value = 0x12341234  # value
        self.simulator.process_one_instruction()
        self.assertEqual(0xee12341234ee, self.simulator.memory.raw_memory)

    def testProcessOneInstructionStoreIntADR(self):
        self.simulator.decoder.next_instruction_index = STOREINT_INDEX + 1
        self.simulator.memory = Memory(48, 0xeeeeeeeeeeee)
        self.simulator.registers[3].value = 0x12341234  # value
        self.simulator.process_one_instruction()
        self.assertEqual(0xee12341234ee, self.simulator.memory.raw_memory)

    def testProcessStoreStateRAA(self):
        self.simulator.decoder.next_instruction_index = STORESTATE_INDEX
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.registers[3].value = 0x1234  # value
        self.simulator.process_store()
        self.assertEqual(0xeeee1234ee, self.simulator.memory.raw_memory)

    def testProcessStoreStateADR(self):
        self.simulator.decoder.next_instruction_index = STORESTATE_INDEX + 1
        self.simulator.current_instruction = self.simulator.decoder.decode_next()
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.registers[3].value = 0x1234  # value
        self.simulator.process_store()
        self.assertEqual(0xeeee1234ee, self.simulator.memory.raw_memory)

    def testProcessOneInstructionStoreStateRAA(self):
        self.simulator.decoder.next_instruction_index = STORESTATE_INDEX
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[1].value = 8  # address
        self.simulator.registers[3].value = 0x1234  # value
        self.simulator.process_one_instruction()
        self.assertEqual(0xeeee1234ee, self.simulator.memory.raw_memory)

    def testProcessOneInstructionStoreStateADR(self):
        self.simulator.decoder.next_instruction_index = STORESTATE_INDEX + 1
        self.simulator.memory = Memory(40, 0xeeeeeeeeee)
        self.simulator.registers[3].value = 0x1234  # value
        self.simulator.process_one_instruction()
        self.assertEqual(0xeeee1234ee, self.simulator.memory.raw_memory)
