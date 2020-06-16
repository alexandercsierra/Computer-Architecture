#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
print_eight = [0b10000010,0b00000000,0b00001000,0b01000111,0b00000000,
0b00000001]

cpu = CPU()

cpu.load()
cpu.run()