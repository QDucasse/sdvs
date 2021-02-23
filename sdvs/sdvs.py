# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# SDVS: SDVE binary execution simulator

import sys
from cli import CLI

if __name__ == "__main__":
    cli = CLI(sys.argv[1:])
    cli.main()
