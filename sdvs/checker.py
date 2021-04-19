# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Checker: Checks if a configuration is safe then processes
# its successors if not already done

class Checker:

    def __init__(self):
        self.known = {}
        self.frontier = []
        self.last = False

    def check_config(self, config):
        # Apply property
        # Successors already found?
        if not(config in self.known):
            self.known[config] = 1
            self.frontier.append(config)

    def next_config(self):
        new_cfg = self.frontier.pop()
        if len(self.frontier) == 0:
            self.last = True
        return new_cfg

