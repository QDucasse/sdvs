# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# GUI: The graphical interface of the project
import os
import tkinter as tk
from tkinter import ttk

from binary_reader import BinaryReader
from constants import *
from decoder import Decoder
from memory import Memory
from core import Core


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
        self.simulator = Core(Decoder(bin_instructions), memory)

        # Frame definitions
        self.left_frame = tk.Frame(parent, width=100)  # top left
        self.instruction_title_frame = tk.Frame(self.left_frame)
        self.instruction_data_frame = tk.Frame(self.left_frame)
        self.right_frame = tk.Frame(parent, width=200)  # top right
        self.memory_frame = tk.Frame(self.right_frame)  # top memory
        self.memory_title_frame = tk.Frame(self.memory_frame)
        self.memory_data_frame = tk.Frame(self.memory_frame)
        self.registers_frame = tk.Frame(self.right_frame)  # top registers
        self.registers_title_frame = tk.Frame(self.registers_frame)
        self.registers_data_frame = tk.Frame(self.registers_frame)
        self.buttons_frame = tk.Frame(self.right_frame)

        # Instruction Variables
        self.pc = tk.StringVar()
        self.op_code = tk.StringVar()
        self.cfg_mask = tk.StringVar()
        self.rd = tk.StringVar()
        self.ra = tk.StringVar()
        self.rb = tk.StringVar()
        self.imma = tk.StringVar()
        self.immb = tk.StringVar()
        self.address = tk.StringVar()
        self.type = tk.StringVar()
        self.clear_instruction()
        # Instruction Values
        self.label_pc_value = tk.Label(self.instruction_data_frame, textvariable=self.pc)
        self.label_op_code_value = tk.Label(self.instruction_data_frame, textvariable=self.op_code)
        self.label_cfg_mask_value = tk.Label(self.instruction_data_frame, textvariable=self.cfg_mask)
        self.label_type_value = tk.Label(self.instruction_data_frame, textvariable=self.type)
        self.label_rd_value = tk.Label(self.instruction_data_frame, textvariable=self.rd)
        self.label_ra_value = tk.Label(self.instruction_data_frame, textvariable=self.ra)
        self.label_rb_value = tk.Label(self.instruction_data_frame, textvariable=self.rb)
        self.label_imma_value = tk.Label(self.instruction_data_frame, textvariable=self.imma)
        self.label_immb_value = tk.Label(self.instruction_data_frame, textvariable=self.immb)
        self.label_address_value = tk.Label(self.instruction_data_frame, textvariable=self.address)

        # Memory variables
        self.memory = tk.StringVar()
        self.memory.set("0")
        self.label_memory_value = tk.Label(self.memory_frame, textvariable=self.memory)

        # Registers variables
        self.registers = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(),
                          tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(),
                          tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(),
                          tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.clear_registers()
        self.label_r0_value = tk.Label(self.registers_data_frame, textvariable=self.registers[0])
        self.label_r1_value = tk.Label(self.registers_data_frame, textvariable=self.registers[1])
        self.label_r2_value = tk.Label(self.registers_data_frame, textvariable=self.registers[2])
        self.label_r3_value = tk.Label(self.registers_data_frame, textvariable=self.registers[3])
        self.label_r4_value = tk.Label(self.registers_data_frame, textvariable=self.registers[4])
        self.label_r5_value = tk.Label(self.registers_data_frame, textvariable=self.registers[5])
        self.label_r6_value = tk.Label(self.registers_data_frame, textvariable=self.registers[6])
        self.label_r7_value = tk.Label(self.registers_data_frame, textvariable=self.registers[7])
        self.label_r8_value = tk.Label(self.registers_data_frame, textvariable=self.registers[8])
        self.label_r9_value = tk.Label(self.registers_data_frame, textvariable=self.registers[9])
        self.label_r10_value = tk.Label(self.registers_data_frame, textvariable=self.registers[10])
        self.label_r11_value = tk.Label(self.registers_data_frame, textvariable=self.registers[11])
        self.label_r12_value = tk.Label(self.registers_data_frame, textvariable=self.registers[12])
        self.label_r13_value = tk.Label(self.registers_data_frame, textvariable=self.registers[13])
        self.label_r14_value = tk.Label(self.registers_data_frame, textvariable=self.registers[14])
        self.label_r15_value = tk.Label(self.registers_data_frame, textvariable=self.registers[15])
        self.register_labels = [
            self.label_r0_value, self.label_r1_value, self.label_r2_value, self.label_r3_value,
            self.label_r4_value, self.label_r5_value, self.label_r6_value, self.label_r7_value,
            self.label_r8_value, self.label_r9_value, self.label_r10_value, self.label_r11_value,
            self.label_r12_value, self.label_r13_value, self.label_r14_value, self.label_r15_value
        ]

        # Buttons
        self.step_button = ttk.Button(self.buttons_frame, text="Step", command=self.process_one_instruction)
        self.step_button.pack()

        self.close_button = ttk.Button(self.buttons_frame, text="Quit", command=parent.quit)
        self.close_button.pack()

        # Widgets and layout - Instruction
        self.left_frame.grid(row=0, column=0, sticky=tk.W)
        self.instruction_title_frame.grid(row=0, column=0)
        self.instruction_data_frame.grid(row=1, column=0)
        self.fill_instruction_frame()
        # Widgets and layout - Memory / Registers
        self.right_frame.grid(row=0, column=1, sticky=tk.N)
        # Memory
        self.memory_frame.grid(row=0, column=0, sticky=tk.N)
        self.memory_title_frame.grid(row=0)
        self.memory_data_frame.grid(row=1)
        self.fill_memory_frame()
        # Registers
        self.registers_frame.grid(row=1, column=0, sticky=tk.N)
        self.registers_title_frame.grid(row=0)
        self.registers_data_frame.grid(row=1)
        self.fill_registers_frame()
        # Buttons
        self.buttons_frame.grid(row=2, column=0, sticky=tk.S)

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
            reg.set(hex(0))

    # -----------
    # FRAME SETUP
    # -----------

    # Instruction
    def fill_instruction_frame(self):
        label_title = tk.Label(self.instruction_title_frame, text="Current Instruction")
        label_title.grid(row=0, sticky=tk.W)
        # PC
        label_pc = tk.Label(self.instruction_data_frame, text="PC: ")
        label_pc.grid(row=1, sticky=tk.W)
        # Op Code
        label_op_code = tk.Label(self.instruction_data_frame, text="Op Code: ")
        label_op_code.grid(row=2, sticky=tk.W)
        # Cfg Mask
        label_cfg_mask = tk.Label(self.instruction_data_frame, text="Config: ")
        label_cfg_mask.grid(row=3, sticky=tk.W)
        # Type
        label_type = tk.Label(self.instruction_data_frame, text="Type: ")
        label_type.grid(row=4, sticky=tk.W)
        # Rd
        label_rd = tk.Label(self.instruction_data_frame, text="RD: ")
        label_rd.grid(row=5, sticky=tk.W)
        # Ra
        label_ra = tk.Label(self.instruction_data_frame, text="RA: ")
        label_ra.grid(row=6, sticky=tk.W)
        # Rb
        label_rb = tk.Label(self.instruction_data_frame, text="RB: ")
        label_rb.grid(row=7, sticky=tk.W)
        # Imma
        label_imma = tk.Label(self.instruction_data_frame, text="IMMA: ")
        label_imma.grid(row=8, sticky=tk.W)
        # Immb
        label_immb = tk.Label(self.instruction_data_frame, text="IMMB: ")
        label_immb.grid(row=9, sticky=tk.W)
        # Address
        label_address = tk.Label(self.instruction_data_frame, text="Address: ")
        label_address.grid(row=10, sticky=tk.W)
        # Layout of values
        self.label_pc_value.grid(row=1, column=1, sticky=tk.W)
        self.label_op_code_value.grid(row=2, column=1, sticky=tk.W)
        self.label_cfg_mask_value.grid(row=3, column=1, sticky=tk.W)
        self.label_type_value.grid(row=4, column=1, sticky=tk.W)
        self.label_rd_value.grid(row=5, column=1, sticky=tk.W)
        self.label_ra_value.grid(row=6, column=1, sticky=tk.W)
        self.label_rb_value.grid(row=7, column=1, sticky=tk.W)
        self.label_imma_value.grid(row=8, column=1, sticky=tk.W)
        self.label_immb_value.grid(row=9, column=1, sticky=tk.W)
        self.label_address_value.grid(row=10, column=1, sticky=tk.W)

    # Memory
    def fill_memory_frame(self):
        label_title = tk.Label(self.memory_title_frame, text="Memory Representation")
        label_title.grid(row=0)
        # Memory
        self.label_memory_value.grid(row=1, column=0, sticky=tk.N)

    # Registers
    def fill_registers_frame(self):
        label_title = tk.Label(self.registers_title_frame, text="Registers")
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
        self.display_registers()
        self.display_memory()
        self.display_colors()

    def display_instruction(self, instruction):
        self.clear_instruction()
        self.pc.set(str(self.simulator.decoder.next_instruction_index))
        self.op_code.set(instruction.op_str())
        self.cfg_mask.set(instruction.cfg_str())
        self.type.set(instruction.type_str())
        self.rd.set(str(instruction.rd))
        # LOAD
        if instruction.op_code == OP_LOAD:
            if instruction.cfg_mask == LOAD_ADR:
                self.address.set(str(instruction.address))
            elif instruction.cfg_mask == LOAD_RAA:
                self.ra.set(str(instruction.ra))
            elif instruction.cfg_mask == LOAD_REG:
                self.ra.set(str(instruction.ra))
            elif instruction.cfg_mask == LOAD_IMM:
                self.imma.set(str(instruction.imma))
        # STORE
        elif instruction.op_code == OP_STORE:
            if instruction.cfg_mask == STORE_ADR:
                self.address.set(str(instruction.address))
            elif instruction.cfg_mask == STORE_RAA:
                self.ra.set(str(instruction.ra))
        # NOT
        elif instruction.op_code == OP_NOT:
            self.ra.set(str(instruction.ra))
        # JMP
        elif instruction.op_code == OP_JMP:
            self.address.set(str(instruction.address))
        # BINARY OPERATION
        else:
            if instruction.cfg_mask == CFG_RR:
                self.ra.set(str(instruction.ra))
                self.rb.set(str(instruction.rb))
            elif instruction.cfg_mask == CFG_RI:
                self.ra.set(str(instruction.ra))
                self.immb.set(str(instruction.immb))
            elif instruction.cfg_mask == CFG_IR:
                self.imma.set(str(instruction.imma))
                self.rb.set(str(instruction.rb))
            elif instruction.cfg_mask == CFG_II:
                self.imma.set(str(instruction.imma))
                self.immb.set(str(instruction.immb))

    def display_memory(self):
        self.memory.set(hex(self.simulator.memory.raw_memory))

    def display_registers(self):
        for reg in self.simulator.registers:
            self.registers[reg.number].set(hex(reg.value))

    def clear_colors(self):
        for label in self.register_labels:
            label.config(fg="black")
        self.label_rd_value.config(fg="black")
        self.label_ra_value.config(fg="black")
        self.label_rb_value.config(fg="black")
        self.label_imma_value.config(fg="black")
        self.label_immb_value.config(fg="black")
        self.label_address_value.config(fg="black")

    def change_reg_color(self, number, color):
        self.register_labels[number].config(fg=color)

    def color_rd(self, color):
        self.change_reg_color(self.simulator.current_instruction.rd, color)
        self.label_rd_value.config(fg=color)

    def color_ra(self, color):
        self.change_reg_color(self.simulator.current_instruction.ra, color)
        self.label_ra_value.config(fg=color)

    def color_rb(self, color):
        self.change_reg_color(self.simulator.current_instruction.rb, color)
        self.label_rb_value.config(fg=color)

    def display_colors(self):
        self.clear_colors()
        # Registers
        op_code = self.simulator.current_instruction.op_code
        cfg_mask = self.simulator.current_instruction.cfg_mask
        if op_code == OP_STORE:
            self.color_rd("green")
            self.label_address_value.config(fg="red")
        elif op_code == OP_JMP:
            self.color_rd("green")
            self.label_address_value.config(fg="red")
        elif op_code == OP_LOAD:
            self.color_rd("red")
            if cfg_mask == LOAD_REG or cfg_mask == LOAD_RAA:
                self.color_ra("green")
            elif cfg_mask == LOAD_IMM:
                self.label_imma_value.config(fg="green")
            elif cfg_mask == LOAD_ADR:
                self.label_address_value.config(fg="green")
        elif op_code == OP_NOT:
            self.color_rd("red")
            self.color_ra("green")
        else:
            if cfg_mask == CFG_RR:
                self.color_ra("green")
                self.color_rb("green")
            elif cfg_mask == CFG_RI:
                self.color_ra("green")
                self.label_immb_value.config(fg="green")
            elif cfg_mask == CFG_IR:
                self.label_imma_value.config(fg="green")
                self.color_rb("green")
            elif cfg_mask == CFG_II:
                self.label_imma_value.config(fg="green")
                self.label_immb_value.config(fg="green")
            self.color_rd("red")


if __name__ == "__main__":
    root = tk.Tk()
    my_gui = GUI(root, bin_file="../sdve-beem-benchmark/bin/adding.6.out")
    print([hex(elt) for elt in my_gui.simulator.decoder.bit_instructions])
    my_gui.simulator.memory = Memory(256, 0x0000000000000000000000000000000000010001000000050000000400000003)
    root.mainloop()
