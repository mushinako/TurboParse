#!/usr/bin/env python3
import os
import const


def excited(data, num_of_excited, mo_parse, verbose):
    return False


def ricc2(path, num_of_excited, mo_parse, verbose):
    # Check ricc2.out and spectrum
    file = os.path.join(path, 'ricc2.out')
    spec_file = os.path.join(path, 'spectrum')
    if os.path.isfile(file) and os.path.isfile(spec_file):
        # Read spectrum
        spec_data = []
        with open(spec_file) as f:
            for x in f.read().split('\n'):
                if x:
                    if x[0] == '#':
                        spec_data = []
                    else:
                        spec_data.append(x.split()[1])
        # num_of_excited cannot be larger than number of spectrum data
        if num_of_excited > len(spec_data):
            num_of_excited = len(spec_data)
            print('No excitation data', num_of_excited, 'and beyond!')
        # Read ricc2.out
        with open(file) as f:
            data = f.read()
        # Get ground state energy
        data = data.partition('Final CC2 energy')[2]
        grnd = const.re_deci.search(data).group(1)
        if verbose:
            print('  Ground energy:', grnd)
        # Get excited state information
        exct = excited(data, num_of_excited, mo_parse, verbose)
        # Return ground energy and excited energy
        return False # Return result
    if not os.path.isfile(file):
        print('No ricc2.out in folder', path + '!')
    if not os.path.isfile(spec_file):
        print('No spectrum in folder', path + '!')
    return False
