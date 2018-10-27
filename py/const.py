#!/usr/bin/env python3
import re

re_float = re.compile('\s((\-)?\d+\.\d*(E(\-)?\d+)?)\s')
re_deci_e = re.compile('\s(\d+\.\d+)$')
re_uint = re.compile('\s(\d+)\s')
re_uint_s = re.compile('^(\d+)\s')
