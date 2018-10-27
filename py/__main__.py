#!/usr/bin/env python3
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
        - Path of escf.out's,
        - NAME
      One line for each file, parameters comma separated
NUM : Number of excitations
-m  : Parse HOMO-LUMO orbitals
-v  : Verbose

Result is always in folder of PATH, as PATH.csv
"""


# Main thing
def main():
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
                with open(path, 'r') as f:
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
                    num_of_excited = int(sys.argv[3])
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
                    if len(args):
                        print('Invalid optional arguments!')
                    else:
                        # success = METHODS[func](parsee, num_of_excited,
                        #                         mo_parse, verbose)
                        # if success:
                        #     sys.exit('Successfully extracted!')
                        # else:
                        #     sys.exit('Parser has encountered an error!')
                        sys.exit(METHODS[func])     # DEBUG: No actual use
            else:
                print('No file at {}!'.format(path))
        else:
            print('Improper method!')
    else:
        print('Invalid arguments!')
    print(HELP)


if __name__ == '__main__':
    main()
