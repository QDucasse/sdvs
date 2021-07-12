# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Command Line Interface: Command-line arguments parser and routine.

import argparse
import subprocess

from memory import Memory
from simulator import Simulator


class Parser(argparse.ArgumentParser):

    def __init__(self):
        super(Parser, self).__init__(description="SDVE binary execution simulator")
        self.add_parse_arguments()

    def add_parse_arguments(self):
        """
        Define arguments to parse.
        """
        self.add_argument("--source", "-s", help="SDVE model source file.")
        self.add_argument("--compiler", "-c", default="/usr/bin/sdvc", help="SDVC path.")
        self.add_argument("--ncores", "-n", help="Number of cores.")
        self.add_argument("--gui", "-g", default=False, action="store_true", help="Trigger the GUI.")
        self.add_argument("--outputfile", "-o", default="execstats.csv", help="CSV file to store the results")


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
        if self.args.gui:
            if self.args.ncores == 1:
                pass # Process GUI
            else:
                print("GUI is not available with more than one core.")
        else: # No GUI
            # Compile file
            subprocess.run([self.args.compiler, "-c", self.args.source, "-o", "bin/a.out", "-n", self.args.ncores])
            # Setup simulator
            import os
            print(os.getcwd())
            binaries = ["bin/a.out." + str(i) for i in range(int(self.args.ncores))]
            with open(self.args.source[:-5]+".cfg", "r") as f:
                init_cfg = f.readline().strip()
            simulator = Simulator(binaries, len(init_cfg)*4)
            # Launch checking with initial config
            exec_time, cfgs = simulator.launch_checking(int(init_cfg, 16))
            # Print and write results
            print("Model executed for {} cycles.".format(exec_time))
            print("{} configs encountered:".format(len(cfgs)))

            model_name = self.args.source.split("/")[-1][:-5]
            # Model name, nb of cores, init config,nb of cycles, nb of cfgs
            fields = [model_name, self.args.ncores, str(exec_time), str(len(cfgs))]

            import csv
            with open(self.args.outputfile, "a") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(fields)






