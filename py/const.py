#!/usr/bin/env python3
import re

# Regexes
re_float = re.compile('\s((\-)?\d+\.\d*(E(\-)?\d+)?)\s')
re_deci = re.compile('\s(\-?\d+\.\d+)\s')
re_udeci_e = re.compile('\s(\d+\.\d+)$')
re_uint = re.compile('\s(\d+)\s')
re_uint_s = re.compile('^(\d+)\s')

# Planck Constant in eV.s
h = 4.135667662e-15

# Speed of Light in nm.s
c = 299792458 * 1e9
