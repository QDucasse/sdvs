# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Command Line Interface: Command-line arguments parser and routine.

import argparse


class Parser(argparse.ArgumentParser):

    def __init__(self):
        super(Parser, self).__init__(description="SDVE binary execution simulator")
        self.add_parse_arguments()

    def add_parse_arguments(self):
        """
        Define arguments to parse.
        """
        self.add_argument("--step", action="store_true", help="Trigger step execution.")

    def parse(self, args):
        """
        Parse the arguments defined in add_parse_arguments from the command line options.
        :param args: command line arguments
        :return: dictionary with the corresponding values for each argument.
        """
        return self.parse_args(args)


class ObjDict(dict):
    """
    Provide an object interface to a dictionary: dict['key'] becomes dict.key.
    """

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


class CLI:
    """
    Command Line Interface linking the parser to the simulator.
    """

    def __init__(self, command_line_args):
        # Parse the command line arguments
        self.parser = Parser()
        args = self.parser.parse(command_line_args)

        self.args = ObjDict(args.__dict__)

    def main(self):
        # Use arguments to trigger simulation
        pass
