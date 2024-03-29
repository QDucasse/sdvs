# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Simulator: Links all elements apart from CLI and GUI.

from sdvs.binary_reader import BinaryReader
from sdvs.checker import Checker
from sdvs.coordinator import Coordinator
from sdvs.core import Core
from sdvs.decoder import Decoder
from sdvs.memory import Memory


class Simulator:

    def __init__(self, bin_paths, cfg_size):
        self.cfg_size = cfg_size
        decoders = []
        for binary in bin_paths:
            bin_instr = BinaryReader.read_instructions(binary)
            decoder = Decoder(bin_instr)
            decoders.append(decoder)
        self.coordinator = Coordinator(decoders, cfg_size)
        self.checker = Checker()
        self.exec_time = 0

    def process_config(self, config):
        # Process actual config
        max_time, new_configs = self.coordinator.process_config(config)
        self.exec_time += max_time
        # Check returned configs
        # print("Obtained configs: [")
        for new_config in new_configs:
            # print(hex(config))
            self.checker.check_config(new_config)
        # print("]")

    def launch_checking(self, init_cfg):
        # print("Checking config " + str(hex(init_cfg.raw_memory)))
        # Memory
        init_memory = init_cfg # Memory(self.cfg_size, init_cfg)
        self.checker.known.add(init_memory)
        self.process_config(init_memory)
        alive = 0
        # while not self.checker.last:
        while len(self.checker.frontier) != 0:
            new_config = self.checker.next_config()
            # print("Checking config " + str(hex(new_config)))
            self.process_config(new_config)
            if alive % 1000 == 999:
                print("{} configs checked.".format(alive+1))
                print("Frontier filled with {} configurations".format(len(self.checker.frontier)))
                print("Encountered {} configurations".format(len(self.checker.known)))
                print("____________________________________________")
            alive += 1
        return self.exec_time, self.checker.known

if __name__ == "__main__":
    binaries = [
        "../../sdvu/cfg/adding.6.out.0",
        "../../sdvu/cfg/adding.6.out.1",
        "../../sdvu/cfg/adding.6.out.2"
    ]
    simulator = Simulator(binaries, 128)
    print(simulator.launch_checking(0x1))
