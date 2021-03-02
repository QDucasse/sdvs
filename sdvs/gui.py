# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# GUI: The graphical interface of the project
import os
from tkinter import Label, Button, Tk, StringVar, IntVar

from binary_reader import BinaryReader
from decoder import Decoder
from simulator import Simulator


class GUI:

    def __init__(self, parent, filename=None):
        self.parent = parent
        parent.title("SDVS")
        bin_instructions = []
        if filename and os.path.exists(filename):
            bin_instructions = BinaryReader.read_file(filename)
        self.simulator = Simulator(Decoder(bin_instructions))

        # Instruction variables
        self.op_code = StringVar()
        self.cfg_mask = StringVar()
        self.rd = IntVar()
        self.ra = IntVar()
        self.rb = IntVar()
        self.imma = IntVar()
        self.immb = IntVar()
        self.address = IntVar()
        self.type = StringVar()

        # Memory variables

        # Registers variables

        # Widgets and layout
        self.create_instruction_frame()
        self.create_memory_frame()
        self.create_registers_frame()

    # -----------
    # FRAME SETUP
    # -----------

    # Instruction
    def create_instruction_frame(self):
        pass

    # Memory
    def create_memory_frame(self):
        pass

    # Registers
    def create_registers_frame(self):
        pass

    # Actual simulation
    def process_one_instruction(self):
        pass

    def display_instruction(self):
        pass


if __name__ == "__main__":
    root = Tk()
    my_gui = GUI(root, "../sdvc/bin/adding.6.out")
    root.mainloop()
