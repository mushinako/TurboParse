#!/usr/bin/env python3
import os
import re

import const

# This file specifies in escf parsing

def parse_escf(path, num_of_excited, mo_parse, verbose):
    if os.path.isdir(path):
        file = os.path.join(path, 'escf.out')
        if os.path.isfile(file):
            with open(file) as f:
                data = f.read()
            # Get ground state energy
            data = data.partition('Ground')[2]
            data = data.partition('Total')[2]
            grnd = const.re_float.search(data).group(1)
            if verbose:
                print('  Ground energy:', grnd)
            # Get excited state information
            # Note num_of_excited has already been added 1
            for i in range(1, num_of_excited):
                data = data.partition('{} singlet'.format(i))[2]
                if data:
                    # Energy in eV
                    data = data.partition('Excitation energy / eV:')[2]
                    ev = const.re_float.search(data).group(1)
                    # Energy in nm
                    data = data.partition('Excitation energy / nm:')[2]
                    nm = const.re_float.search(data).group(1)
                    # Oscillator length
                    data = data.partition('length representation:')[2]
                    ln = const.re_float.search(data).group(1)
                    data = data.partition('occ. orbital')[2]
                    # Molecular orbitals
                    data = data.partition('\n')[2]
                    mo, _, data = data.partition('Change of electron number:')
                    # TODO: Everything
                    if verbose:
                        print('  Excitation state ', '{}:'.format(i))
                        print('    Energy (eV):', ev)
                        print('    Energy (nm):', nm)
                        print('    Oscil. len.:', ln)
                    continue
                print('  No excitation', i, 'and beyond!')
                num_of_excited = i - 1
                break
            return True  # Return the parsed result
        print('No escf.out in folder', path + '!')
    else:
        print('No folder', path + '!')
    return False


# Main escf parsing function
def escf(parsee, num_of_excited, mo_parse, verbose):
    # MO parsing has not been implemented yet for escf
    if mo_parse:
        print('Molecular orbital parsing has not been implemented for escf!')
        return False
    data = []
    for name, path in parsee.items():
        if verbose:
            print('\nCurrently parsing', name + '...')
        parsed = parse_escf(path, num_of_excited, mo_parse, verbose)
        if parsed:
            # TODO: Do something about parsed data
            continue
        print('Parsing error for', path)
        return False
    return True
