#!/usr/bin/env python3
import re

# Regexes
re_float = re.compile('\s((\-)?\d+\.\d*([Ee](\-)?\d+)?)\s')
re_ufloat = re.compile('\s(\d+\.\d*([Ee](\-)?\d+)?)\s')
re_deci = re.compile('\s(\-?\d+\.\d*)\s')
re_udeci_e = re.compile('\s(\d+\.\d*)$')
re_uint = re.compile('\s(\d+)\s')
re_uint_s = re.compile('^(\d+)\s')

# Planck Constant in eV.s
h = 4.135667662e-15

# Speed of Light in nm.s
c = 299792458 * 1e9


# Convert mo lists to list of strings
def mo_lists_2_strings(l_trans, l_coeff, l_ln, mo_parse, verbose):
    # Convert mo lists to list of strings
    l_mo = []
    # Parse numbers to HOMO-LUMO?
    if mo_parse:
        # Find HOMO-LUMO
        float_ln = [float(x) for x in l_ln]
        hl_index = float_ln.index(max(float_ln))
        lumo, homo = l_trans[hl_index][0]
        # Check if (LUMO - HOMO) is 1
        if lumo - homo != 1:
            print('HOMO-LUMO Parsing Error!')
            print('Oscil. len.:', l_ln)
            print('HO-LU index:', hl_index)
            print('Trans. list:', l_trans)
            sys.exit()
        # Parse each MO entry to LUMO←HOMO (coeff)
        for i in range(len(l_ln)):
            trans = l_trans[i]
            mo = []
            for j in range(len(trans)):
                lu, ho = trans[j]
                tmp_mo = ''
                # LUMO check
                if lu > lumo:
                    tmp_mo += 'L+{}'.format(lu-lumo)
                elif lu < lumo:
                    tmp_mo += 'L-{}'.format(lumo-lu)
                else:
                    tmp_mo += '    L'
                tmp_mo += '←'
                # HOMO check
                if ho < homo:
                    tmp_mo += 'H-{}'.format(homo-ho)
                elif ho > homo:
                    tmp_mo += 'H+{}'.format(ho-homo)
                else:
                    tmp_mo += 'H   '
                mo.append(tmp_mo + '  ({}%)'.format(l_coeff[i][j]))
            l_mo.append('      '.join(mo))
    else:
        # Parse each MO entry to LUMO←HOMO (coeff)
        for i in range(len(l_ln)):
            trans = l_trans[i]
            mo = []
            for j in range(len(trans)):
                mo.append('{0}←{1}  ({2}%)'.format(*trans[j], l_coeff[i][j]))
            l_mo.append('      '.join(mo))
    return l_mo
