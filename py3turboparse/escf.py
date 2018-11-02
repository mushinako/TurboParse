#!/usr/bin/env python3
# This file specifies in escf parsing
import os
import sys
import const


# Convert mo data to lists
def mo_data_2_lists(mo):
    trans = []
    coeff = []
    for x in mo.split('\n'):
        y = x.strip()
        if len(y):
            # MO coefficient
            tmp_coeff = const.re_udeci_e.search(y).group(1)
            if float(tmp_coeff) >= 10:
                coeff.append(tmp_coeff)
                # Initial MO
                moi = const.re_uint_s.search(y).group(1)
                # MO pair [initial, final]
                y = y.partition(moi)[2]
                trans.append([int(const.re_uint.search(y).group(1)), int(moi)])
    return [trans, coeff]


# Excited state parsing
def excited(data, num_of_excited, mo_parse, verbose):
    l_nm = []
    l_ev = []
    l_trans = []
    l_coeff = []
    l_ln = []
    # For each excited state...
    for i in range(1, num_of_excited + 1):
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
            # Convert mo to lists
            trans, coeff = mo_data_2_lists(mo)
            if verbose:
                print('  Excitation state {}:'.format(i))
                print('    Energy (nm):', nm)
                print('    Energy (eV):', ev)
                print('    MO trans.  :', trans)
                print('    MO coeff.  :', coeff)
                print('    Oscil. len.:', ln)
            l_nm.append(nm)
            l_ev.append(ev)
            l_trans.append(trans)
            l_coeff.append(coeff)
            l_ln.append(ln)
            continue
        print('  No excitation', i, 'and beyond!')
        break
    # Convert mo to list of strings
    l_mo = const.mo_lists_2_strings(l_trans, l_coeff, l_ln, mo_parse, verbose)
    return [l_nm, l_ev, l_mo, l_ln]


# escf main function
def escf(path, num_of_excited, mo_parse, verbose):
    # Read escf.out
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
        exct = excited(data, num_of_excited, mo_parse, verbose)
        # Return ground energy and excited energy
        return [[grnd] * len(exct[0])] + exct
    print('No escf.out in folder', path + '!')
    return False
