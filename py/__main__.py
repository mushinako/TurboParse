#!/usr/bin/env python3
# This file holds the main interface for the whole parser
import os
import sys
import escf
import ricc2


METHODS = {
    'escf': escf.escf,
    'ricc2': ricc2.ricc2
    }

HELP = """
USAGE: turboparse [escf/ricc2] PATH NUM [-m] [-v]

PATH: Path of a list file, quoted if contain spaces and special characters
      The list file should contain:
        - Path of folders containing:
            - escf : escf.out,
            - ricc2: ricc2.out and spectrum
        - NAME
      One line for each file, parameters comma separated
NUM : Number of excitations
-m  : Parse HOMO-LUMO orbitals
-v  : Verbose

Result is always in folder of PATH, as PATH.csv
"""


# Parse arguments from stdin
def parse_args():
    mo_parse = False
    verbose = False
    # Arguments:
    #   0 : './py', not useful
    #   1 : Function (escf/ricc2)
    #   2 : PATH
    #   3 : NUM of excited states
    #   4+: Optional arguments
    # At least 4 arguments needed
    if len(sys.argv) > 3:
        func = sys.argv[1]
        # Check argv[1], should be 'escf' or 'ricc2'
        if func in METHODS:
            path = sys.argv[2]
            # Check the existence of a file at PATH
            if os.path.isfile(path):
                # Parse file at PATH
                parsee = {}
                with open(path) as f:
                    for line in f:
                        if line:
                            path_line = [s.strip() for s in line.split(',')]
                            if len(path_line) == 2:
                                parsee[path_line[1]] = path_line[0]
                            else:
                                print('List file format error!')
                                print(HELP)
                                sys.exit()
                try:
                    num_of_excited = int(sys.argv[3]) + 1
                except ValueError:
                    print('Number of excitation not a number!')
                else:
                    args = sys.argv[4:]
                    if '-m' in args:
                        mo_parse = True
                        args.remove('-m')
                    if '-v' in args:
                        verbose = True
                        args.remove('-v')
                    if not len(args):
                        return [path, func, parsee, num_of_excited, mo_parse,
                                verbose]
                    print('Invalid optional arguments!')
            else:
                print('No file at {}!'.format(path))
        else:
            print('Improper method!')
    else:
        print('Invalid arguments!')
    return False


# Main parsing function
def parse_main(method, parsee, num_of_excited, mo_parse, verbose):
    data = [('Name,Ground energy,Lambda max (nm),Energy (eV),Decomposition,'
             'Oscilator Strength (length)')]
    for name, path in sorted(parsee.items()):
        if verbose:
            print('\nCurrently parsing', name + '...')
        if os.path.isdir(path):
            try:
                prsd = METHODS[method](path, num_of_excited, mo_parse, verbose)
            except Exception as e:
                print('An error occured!')
                print(e)
            else:
                if prsd:
                    data += [','.join(x) for x in zip([name] * len(prsd[0]), *prsd)]
                    continue
            print('Parsing error for', path)
        else:
            print('No folder', path + '!')
        return False
    return data


# Main thing
def main():
    args = parse_args()
    # Check if argument parsing is successful
    if args:
        # cd to list for relative path
        path, file = os.path.split(args.pop(0))
        os.chdir(path)
        # Check parsing result
        success = parse_main(*args)
        if success:
            file = os.path.splitext(file)[0]
            if args[-2]:
                file += '-mo'
            csv = file + '.csv'
            with open(csv, 'w') as f:
                f.write('\n'.join(success))
            if args[-1]:
                print('Successfully extracted and written to', csv + '!')
        else:
            print('Parser has encountered an error!')
        return
    print(HELP)


if __name__ == '__main__':
    main()
