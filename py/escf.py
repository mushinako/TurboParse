#!/usr/bin/env python3
import os
import sys
import re

def process_file(file, num, verbose):
    if os.path.isfile(file):
        with open(file, 'r') as rf:
            data = rf.read()

        csv = []

        for i in range(1, num):
            if verbose:
                print()

            data = data.partition('{} singlet a excitation'.format(i))[2]

            if data:
                data = data.partition('Excitation energy / eV:')[2]
                re_ev = re.compile('\s(\d+\.\d*(E(\-)?\d+)?)\s')
                ev = re_ev.search(data).group(1)

                data = data.partition('Excitation energy / nm:')[2]
                re_nm = re.compile('\s(\d+\.\d*(E(\-)?\d+)?)\s')
                nm = re_nm.search(data).group(1)

                data = data.partition('length representation:')[2]
                re_leng = re.compile('\s(\d+\.\d*(E(\-)?\d+)?)\s')
                leng = re_leng.search(data).group(1)

                data = data.partition('occ. orbital')[2]
                data = data.partition('\n')[2]
                mo, _, data = data.partition('Change of electron number:')

                l_mo_trans = []
                l_coeff = []

                for x in mo.split('\n'):
                    if len(x) and not x.isspace():
                        y = x.strip()

                        re_moi = re.compile('^(\d+)\s')
                        moi = re_moi.search(y).group(1)

                        y = y.partition(moi)[2]
                        re_mof = re.compile('\s(\d+)\s')

                        re_coef = re.compile('\s(\d+\.\d+)$')
                        l_coeff.append(re_coef.search(y).group(1))

                        l_mo_trans.append(
                            re_mof.search(y).group(1) + '←' + moi
                            )

                mo_trans = (' ' * 5).join(l_mo_trans)
                coeff = (' ' * 5).join(l_coeff)

                if verbose:
                    print('Singlet', i)
                    print('  ev:', ev)
                    print('  nm:', nm)
                    print('  leng:', leng)
                    print('  mo_trans:', mo_trans)
                    print('  coeff:', coeff)

                if len(l_mo_trans) != len(l_coeff):
                    print('Error!')

                csv.append(','.join((nm, ev, mo_trans, leng, coeff)))

            else:
                print('No excitation {} and beyond!'.format(i))
                break

        return csv

    else:
        print('Incorrect file path!')
        print(HELP)


def escf(path, num_of_excited, mo_parse, verbose):
    pass


def main():
    if len(sys.argv) in [4, 5]:
        verbose = False
        if len(sys.argv) == 5:
            if sys.argv[4] == '-v':
                verbose = True
            else:
                print(HELP)
                return

        try:
            num = int(sys.argv[3]) + 1
        except ValueError:
            print('Invalid number of excitations!')
            print(HELP)
            return

        if sys.argv[1] == '-o':
            csv = [('Lambda max (nm),'
                    'Energy (eV),'
                    'MO Number,'
                    'Oscilator Strength (length),'
                    'Contribution (%)')]
            file = sys.argv[2]
            p = process_file(file, num, verbose)
            if not p:
                sys.exit()
            csv += p

            with open(file + '.csv', 'w') as wf:
                wf.write('\n'.join(csv))

        elif sys.argv[1] == '-l':
            csv = [('Name,'
                    'Lambda max (nm),'
                    'Energy (eV),'
                    'MO Number,'
                    'Oscilator Strength (length),'
                    'Contribution (%)')]
            file_list = sys.argv[2]

            if os.path.isfile(file_list):
                with open(file_list, 'r') as f:
                    files = f.read().split('\n')

                for file_data in files:
                    if file_data and file_data[0] != '#':
                        x = file_data.split()
                        if len(x) != 2:
                            print('Error in List File!')
                            return
                        file, name = x
                        p = process_file(file, num, verbose)
                        if not p:
                            sys.exit()
                        csv += [name + ',' + x for x in p]

                with open(file_list + '.csv', 'w') as wf:
                    wf.write('\n'.join(csv))

            else:
                print('Incorrect file path!')
                print(HELP)

        else:
            print(HELP)

    else:
        print(HELP)


if __name__ == '__main__':
    main()
