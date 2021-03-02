# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# GUI: The graphical interface of the project
import os
from tkinter import Label, Button, Tk, StringVar, IntVar, Frame, W, N, E

from binary_reader import BinaryReader
from constants import *
from decoder import Decoder
from memory import Memory
from simulator import Simulator


class GUI:

    def __init__(self, parent, mem_file=None, bin_file=None):
        self.parent = parent
        parent.title("SDVS")
        bin_instructions = []
        memory = Memory(0, 0)
        if bin_file and os.path.exists(bin_file):
            bin_instructions = BinaryReader.read_instructions(bin_file)
        if mem_file and os.path.exists(mem_file):
            raw_memory = BinaryReader.read_memory(mem_file)
            memory = Memory(raw_memory.bit_length(), raw_memory)
        self.simulator = Simulator(Decoder(bin_instructions), memory)

        # Frame definitions
        self.instruction_frame = Frame(parent)  # top left
        self.instruction_title_frame = Frame(self.instruction_frame)
        self.instruction_data_frame = Frame(self.instruction_frame)
        self.memory_reg_frame = Frame(parent)  # top right
        self.memory_frame = Frame(self.memory_reg_frame)  # top memory
        self.memory_title_frame = Frame(self.memory_frame)
        self.memory_data_frame = Frame(self.memory_frame)
        self.registers_frame = Frame(self.memory_reg_frame)  # top registers
        self.registers_title_frame = Frame(self.registers_frame)
        self.registers_data_frame = Frame(self.registers_frame)

        # Instruction Variables
        self.op_code = StringVar()
        self.cfg_mask = StringVar()
        self.rd = StringVar()
        self.ra = StringVar()
        self.rb = StringVar()
        self.imma = StringVar()
        self.immb = StringVar()
        self.address = StringVar()
        self.type = StringVar()
        self.clear_instruction()
        # Instruction Values
        self.label_op_code_value = Label(self.instruction_data_frame, textvariable=self.op_code)
        self.label_cfg_mask_value = Label(self.instruction_data_frame, textvariable=self.cfg_mask)
        self.label_type_value = Label(self.instruction_data_frame, textvariable=self.type)
        self.label_rd_value = Label(self.instruction_data_frame, textvariable=self.rd)
        self.label_ra_value = Label(self.instruction_data_frame, textvariable=self.ra)
        self.label_rb_value = Label(self.instruction_data_frame, textvariable=self.rb)
        self.label_imma_value = Label(self.instruction_data_frame, textvariable=self.imma)
        self.label_immb_value = Label(self.instruction_data_frame, textvariable=self.immb)
        self.label_address_value = Label(self.instruction_data_frame, textvariable=self.address)

        # Memory variables
        self.memory = StringVar()
        self.memory.set("0")
        self.label_memory_value = Label(self.memory_frame, textvariable=self.memory)

        # Registers variables
        self.registers = [IntVar()] * REG_NUMBER
        self.clear_registers()
        self.label_r0_value = Label(self.registers_data_frame, textvariable=self.registers[0])
        self.label_r1_value = Label(self.registers_data_frame, textvariable=self.registers[1])
        self.label_r2_value = Label(self.registers_data_frame, textvariable=self.registers[2])
        self.label_r3_value = Label(self.registers_data_frame, textvariable=self.registers[3])
        self.label_r4_value = Label(self.registers_data_frame, textvariable=self.registers[4])
        self.label_r5_value = Label(self.registers_data_frame, textvariable=self.registers[5])
        self.label_r6_value = Label(self.registers_data_frame, textvariable=self.registers[6])
        self.label_r7_value = Label(self.registers_data_frame, textvariable=self.registers[7])
        self.label_r8_value = Label(self.registers_data_frame, textvariable=self.registers[8])
        self.label_r9_value = Label(self.registers_data_frame, textvariable=self.registers[9])
        self.label_r10_value = Label(self.registers_data_frame, textvariable=self.registers[10])
        self.label_r11_value = Label(self.registers_data_frame, textvariable=self.registers[11])
        self.label_r12_value = Label(self.registers_data_frame, textvariable=self.registers[12])
        self.label_r13_value = Label(self.registers_data_frame, textvariable=self.registers[13])
        self.label_r14_value = Label(self.registers_data_frame, textvariable=self.registers[14])
        self.label_r15_value = Label(self.registers_data_frame, textvariable=self.registers[15])

        # Widgets and layout - Instruction
        self.instruction_frame.grid(row=0, column=0, sticky=W)
        self.instruction_title_frame.grid(row=0, column=0)
        self.instruction_data_frame.grid(row=1, column=0)
        self.fill_instruction_frame()
        # Widgets and layout - Memory / Registers
        self.memory_reg_frame.grid(row=0, column=1, sticky=N)
        # Memory
        self.memory_frame.grid(row=0, column=0, sticky=N)
        self.memory_title_frame.grid(row=0)
        self.memory_data_frame.grid(row=1)
        self.fill_memory_frame()
        # Registers
        self.registers_frame.grid(row=1, column=0, sticky=N)
        self.registers_title_frame.grid(row=0)
        self.registers_data_frame.grid(row=1)
        self.fill_registers_frame()

    # -----------
    # CLEAR VARS
    # -----------

    def clear_instruction(self):
        self.op_code.set("-")
        self.cfg_mask.set("-")
        self.rd.set("-")
        self.ra.set("-")
        self.rb.set("-")
        self.imma.set("-")
        self.immb.set("-")
        self.address.set("-")
        self.type.set("-")

    def clear_registers(self):
        for reg in self.registers:
            reg.set(0)

    # -----------
    # FRAME SETUP
    # -----------

    # Instruction
    def fill_instruction_frame(self):
        label_title = Label(self.instruction_title_frame, text="Current Instruction")
        label_title.grid(row=0, sticky=W)
        # Op Code
        label_op_code = Label(self.instruction_data_frame, text="Op Code: ")
        label_op_code.grid(row=1, sticky=W)
        # Cfg Mask
        label_cfg_mask = Label(self.instruction_data_frame, text="Config: ")
        label_cfg_mask.grid(row=2, sticky=W)
        # Type
        label_type = Label(self.instruction_data_frame, text="Type: ")
        label_type.grid(row=3, sticky=W)
        # Rd
        label_rd = Label(self.instruction_data_frame, text="RD: ")
        label_rd.grid(row=4, sticky=W)
        # Ra
        label_ra = Label(self.instruction_data_frame, text="RA: ")
        label_ra.grid(row=5, sticky=W)
        # Rb
        label_rb = Label(self.instruction_data_frame, text="RB: ")
        label_rb.grid(row=6, sticky=W)
        # Imma
        label_imma = Label(self.instruction_data_frame, text="IMMA: ")
        label_imma.grid(row=7, sticky=W)
        # Immb
        label_immb = Label(self.instruction_data_frame, text="IMMB: ")
        label_immb.grid(row=8, sticky=W)
        # Address
        label_address = Label(self.instruction_data_frame, text="Address: ")
        label_address.grid(row=9, sticky=W)
        # Layout of values
        self.label_op_code_value.grid(row=1, column=1, sticky=W)
        self.label_cfg_mask_value.grid(row=2, column=1, sticky=W)
        self.label_type_value.grid(row=3, column=1, sticky=W)
        self.label_rd_value.grid(row=4, column=1, sticky=W)
        self.label_ra_value.grid(row=5, column=1, sticky=W)
        self.label_rb_value.grid(row=6, column=1, sticky=W)
        self.label_imma_value.grid(row=7, column=1, sticky=W)
        self.label_immb_value.grid(row=8, column=1, sticky=W)
        self.label_address_value.grid(row=9, column=1, sticky=W)

    # Memory
    def fill_memory_frame(self):
        label_title = Label(self.memory_title_frame, text="Memory Representation")
        label_title.grid(row=0)
        # Memory
        self.label_memory_value.grid(row=1, column=0, sticky=N)

    # Registers
    def fill_registers_frame(self):
        label_title = Label(self.registers_title_frame, text="Registers")
        label_title.grid(column=2)
        # Registers - 0 to 3
        self.label_r0_value.grid(row=1, column=0)
        self.label_r1_value.grid(row=1, column=1)
        self.label_r2_value.grid(row=1, column=2)
        self.label_r3_value.grid(row=1, column=3)
        # Registers - 4 to 7
        self.label_r4_value.grid(row=2, column=0)
        self.label_r5_value.grid(row=2, column=1)
        self.label_r6_value.grid(row=2, column=2)
        self.label_r7_value.grid(row=2, column=3)
        # Registers - 8 to 11
        self.label_r8_value.grid(row=3, column=0)
        self.label_r9_value.grid(row=3, column=1)
        self.label_r10_value.grid(row=3, column=2)
        self.label_r11_value.grid(row=3, column=3)
        # Registers - 12 to 15
        self.label_r12_value.grid(row=4, column=0)
        self.label_r13_value.grid(row=4, column=1)
        self.label_r14_value.grid(row=4, column=2)
        self.label_r15_value.grid(row=4, column=3)

    # Actual simulation
    def process_one_instruction(self):
        self.simulator.process_one_instruction()
        self.display_instruction(self.simulator.current_instruction)
        print(self.simulator.memory)
        self.simulator.print_registers()

    def display_instruction(self, instruction):
        self.clear_instruction()
        self.op_code = instruction.op_str()
        self.cfg_mask = instruction.cfg_str()
        self.type = instruction.type_str()
        self.rd = str(instruction.rd)

        if instruction.op_code == OP_LOAD:
            if instruction.cfg_mask ==

        elif instruction.
        self.ra = instruction.ra
        self.rb = instruction.rb
        self.imma = instruction.imma
        self.immb = instruction.immb
        self.address = instruction.address

    def display_memory(self):
        pass

    def display_registers(self):
        pass

if __name__ == "__main__":
    root = Tk()
    my_gui = GUI(root, "../sdvc/bin/adding.6.out")
    root.mainloop()
