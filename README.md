# Simple DiVine Simulator (SDVS)

The Simple DiVine Simulator (SDVS) simulates the behavior of the processing unit ([SDVU](https://github.com/QDucasse/sdvu)) and was used to co-design this processing unit and check the correct processing of instructions. It provides a way to understand instructions compiled by the compiler ([SDVC](https://github.com/QDucasse/sdvc)). The ISA is presented [here](https://github.com/QDucasse/sdvc/blob/main/docs/isa.md) and is handmade to fit the language the best. The language itself is a transformation of DiVinE to a single static assignment form (Simple DiVinE).

### Installation and Usage

The project can be setup by cloning the repository and installing with:
```bash
$ cd <install_directory>
$ git clone git@github.com:QDucasse/sdvs
$ cd sdvs
$ python setup.py install
```

You can then run the simulation with:
```bash
$ python sdvs/main.py
usage: main.py [-h] [--source SOURCE] [--compiler COMPILER] [--ncores NCORES]
               [--gui] [--outputfile OUTPUTFILE]

SDVE binary execution simulator

optional arguments:
  -h, --help            show this help message and exit
  --source SOURCE, -s SOURCE
                        SDVE model source file.
  --compiler COMPILER, -c COMPILER
                        SDVC path.
  --ncores NCORES, -n NCORES
                        Number of cores.
  --gui, -g             Trigger the GUI.
  --outputfile OUTPUTFILE, -o OUTPUTFILE
                        CSV file to store the results
```

The project contains 200~ tests that can be run with `pytest`:
```bash
$ pytest
==================================================================================== test session starts =====================================================================================
platform linux -- Python 3.7.6, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: /home/quentin/Desktop/GitProjects/model checking/sdvs
collected 197 items                                                                                                                                                                          

tests/test_asm.py ..................                                                                                                                                                   [  9%]
tests/test_binary_reader.py .                                                                                                                                                          [  9%]
tests/test_core.py ........................................................................................................................................                            [ 78%]
tests/test_decoder.py .........................                                                                                                                                        [ 91%]
tests/test_memory.py .................                                                                                                                                                 [100%]

==================================================================================== 197 passed in 0.30s =====================================================================================
```
