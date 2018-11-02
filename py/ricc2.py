#!/usr/bin/env python3
import os
import const


# Convert mo lists to list of strings
def mo_data_2_lists(mo):
    trans = []
    coeff = []
    for x in mo.split('\n'):
        x = x.strip()
        if x:
            x = x.split('|')
            tmp_coeff = x[3].strip().split()[1]
            if float(tmp_coeff) >= 10:
                trans.append([int(y.strip().split()[0]) for y in x[2:0:-1]])
                coeff.append(tmp_coeff)
    return [trans, coeff]


# Convert mo lists to list of strings
def mo_lists_2_strings(l_trans, l_coeff, l_ln, mo_parse, verbose):
    pass


# Excited state parsing
def excited(data, num_of_excited, mo_parse, verbose, l_ln):
    l_nm = []
    l_ev = []
    # Parse the table with energies
    data = data.partition('%t1')[2]
    data = data.partition('=')[2]
    for i in range(num_of_excited):
        for _ in range(5):
            data = data.partition('|')[2]
        ev = const.re_ufloat.search(data).group(1)
        l_ev.append(ev)
        l_nm.append(str(round(const.c * const.h / float(ev), 8)))
        data = data.partition('\n')[2]
    # Parse the orbitals
    l_trans = []
    l_coeff = []
    for i in range(num_of_excited):
        data = data.partition('%    |\n')[2]
        data = data.partition('\n')[2]
        # Isolate data table
        mo, _,  data = data.partition('+')
        # Convert mo to lists
        trans, coeff = mo_data_2_lists(mo)
        l_trans.append(trans)
        l_coeff.append(coeff)
    if verbose:
        for i in range(len(l_ln)):
            print('  Excitation state {}:'.format(i+1))
            print('    Energy (nm):', l_nm[i])
            print('    Energy (eV):', l_ev[i])
            print('    MO trans.  :', l_trans[i])
            print('    MO coeff.  :', l_coeff[i])
            print('    Oscil. len.:', l_ln[i])
    # Convert mo to list of strings
    l_mo = const.mo_lists_2_strings(l_trans, l_coeff, l_ln, mo_parse, verbose)
    return [l_nm, l_ev, l_mo]


# ricc2 main function
def ricc2(path, num_of_excited, mo_parse, verbose):
    # Check ricc2.out and spectrum
    file = os.path.join(path, 'ricc2.out')
    spec_file = os.path.join(path, 'spectrum')
    if os.path.isfile(file) and os.path.isfile(spec_file):
        # Read spectrum
        l_ln = []
        with open(spec_file) as f:
            for x in f.read().split('\n'):
                if x:
                    if x[0] == '#':
                        l_ln = []
                    else:
                        l_ln.append(x.split()[1])
        # num_of_excited cannot be larger than number of spectrum data
        if num_of_excited > len(l_ln):
            num_of_excited = len(l_ln)
            print('  No excitation data', num_of_excited, 'and beyond!')
        # Read ricc2.out
        with open(file) as f:
            data = f.read()
        # Get ground state energy
        data = data.partition('Final CC2 energy')[2]
        grnd = const.re_deci.search(data).group(1)
        if verbose:
            print('  Ground energy:', grnd)
        # Get excited state information
        exct = excited(data, num_of_excited, mo_parse, verbose, l_ln)
        # Return ground energy and excited energy
        return [[grnd] * len(l_ln)] + exct + [l_ln]
    if not os.path.isfile(file):
        print('No ricc2.out in folder', path + '!')
    if not os.path.isfile(spec_file):
        print('No spectrum in folder', path + '!')
    return False
