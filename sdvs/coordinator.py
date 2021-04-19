# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Coordinator: Coordination between the different cores of the system.

from constants import *
from core import Core


class Coordinator:

    def __init__(self, decoders):
        self.cores = []
        for decoder in decoders:
            self.cores.append(Core(decoder))
        self.executed_cycles = 0

    def process_config(self, config):
        max_exec_time = 0
        new_configs = []
        for core in self.cores:
            core.setup_cfg_memory(config)
            core.process_instructions()
            new_configs += core.new_configs
            max_exec_time = max(core.executed_cycles, max_exec_time)
        return max_exec_time, new_configs


if __name__ == "__main__":
    from binary_reader import BinaryReader
    from memory import Memory
    from decoder import Decoder
    bin_instructions0 = BinaryReader.read_instructions("../../sdvu/cfg/adding.6.out.0")
    bin_instructions1 = BinaryReader.read_instructions("../../sdvu/cfg/adding.6.out.1")
    bin_instructions2 = BinaryReader.read_instructions("../../sdvu/cfg/adding.6.out.2")
    decoder0 = Decoder(bin_instructions0)
    decoder1 = Decoder(bin_instructions1)
    decoder2 = Decoder(bin_instructions2)
    init_cfg = Memory(128, 0x00010001000000010000000100000001)
    add_decoders = [decoder0, decoder1, decoder2]
    coordinator = Coordinator(add_decoders)
    max_time, cfgs = coordinator.process_config(init_cfg)

    print(max_time)
    print(cfgs)


