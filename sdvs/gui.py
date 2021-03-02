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

        # Widgets and layout
        self.create_instruction_frame()
        self.create_memory_frame()
        self.create_registers_frame()

    # -----------
    # FRAME SETUP
    # -----------

    # Instruction
    def create_instruction_frame(self):
        self.create_instruction_variables()
        self.create_instruction_widgets()
        self.create_instruction_layout()

    def create_instruction_variables(self):
        pass

    def create_instruction_widgets(self):
        pass

    def create_instruction_layout(self):
        pass

    # Memory
    def create_memory_frame(self):
        self.create_memory_variables()
        self.create_memory_widgets()
        self.create_memory_layout()

    def create_memory_variables(self):
        pass

    def create_memory_widgets(self):
        pass

    def create_memory_layout(self):
        pass

    # Registers
    def create_registers_frame(self):
        self.create_registers_variables()
        self.create_registers_widgets()
        self.create_registers_layout()

    def create_registers_variables(self):
        pass

    def create_registers_widgets(self):
        pass

    def create_registers_layout(self):
        pass

    # Actual simulation
    def process_one_instruction(self):
        pass

    def display_instruction(self):
        pass


if __name__ == "__main__":
    root = Tk()
    my_gui = GUI(root, "../sdvc/bin/anderson.8.out")
    root.mainloop()
