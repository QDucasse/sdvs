# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Simulator: Links all elements apart from CLI and GUI.

from binary_reader import BinaryReader
from checker import Checker
from coordinator import Coordinator
from core import Core
from decoder import Decoder
from memory import Memory


class Simulator:

    def __init__(self, bin_paths):
        decoders = []
        for binary in bin_paths:
            bin_instr = BinaryReader.read_instructions(binary)
            decoder = Decoder(bin_instr)
            decoders.append(decoder)
        self.coordinator = Coordinator(decoders)
        self.checker = Checker()
        self.exec_time = 0

    def process_config(self, cfg_memory):
        # Process actual config
        max_time, cfgs = self.coordinator.process_config(cfg_memory)
        self.exec_time += max_time
        # Check returned configs
        for cfg in cfgs:
            self.checker.check_config(cfg)

    def launch_checking(self, init_cfg):
        self.process_config(init_cfg)
        while not self.checker.last:
            new_config = self.checker.next_config()
            print("Checking config " + str(hex(new_config)))
            self.process_config(new_config)
        return self.exec_time, self.checker.known

if __name__ == "__main__":
    binaries = [
        "../../sdvu/cfg/adding.6.out.0",
        "../../sdvu/cfg/adding.6.out.1",
        "../../sdvu/cfg/adding.6.out.2"
    ]
    simulator = Simulator(binaries)
    cfg = Memory(128, 0x00010001000000010000000100000001)
    print(simulator.launch_checking(cfg))
