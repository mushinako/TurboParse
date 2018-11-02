#!/usr/bin/env python3
# This file holds the main interface for the whole parser
import os
import sys
import argparse
import escf
import ricc2

METHODS = ['escf', 'ricc2']


# Check list file
def is_list_file(parser, path):
    if os.path.isfile(path):
        parsee = {}
        with open(path) as f:
            for line in f:
                if line:
                    path_line = [s.strip() for s in line.split(',')]
                    if len(path_line) == 2:
                        parsee[path_line[1]] = path_line[0]
                    else:
                        parser.error('List file format error!')
        return [path, parsee]
    parser.error('No file at {}!'.format(path))


# Parse arguments from stdin
def parse_args():
    # A quirk for WSL
    args = sys.argv[1:]
    args[-1] = args[-1].replace('\r', '')
    # Arguments:
    #   Function (escf/ricc2)
    #   PATH
    #   NUM of excited states
    #   Optional arguments
    parser = argparse.ArgumentParser(description='Parse TURBOMOLE(TM) outputs')
    parser.add_argument('func', metavar='METHOD', choices=METHODS,
                        help='method to parse')
    parser.add_argument('parsee', metavar='PATH', help='path of list file',
                        type=lambda x: is_list_file(parser, x))
    parser.add_argument('num_of_excited', metavar='NUM', type=int,
                        help='number of excited states to parse')
    parser.add_argument('-m', action='store_true', dest='mo_parse',
                        help='parse HOMO-LUMO orbitals')
    parser.add_argument('-v', action='store_true', dest='verbose',
                        help='verbose')
    return parser.parse_args(args)


# Main parsing function
def parse_main(func, parsee, num_of_excited, mo_parse, verbose):
    data = [('Name,Ground energy,Lambda max (nm),Energy (eV),Decomposition,'
             'Oscilator Strength (length)')]
    for name, path in sorted(parsee.items()):
        if verbose:
            print('\nCurrently parsing', name + '...')
        if os.path.isdir(path):
            parse_func = getattr(__import__(func), func)
            try:
                prsd = parse_func(path, num_of_excited,
                                                 mo_parse, verbose)
            except Exception as e:
                print('An error occured!')
                print(e)
            else:
                if prsd:
                    data += [','.join(x)
                             for x in zip([name] * len(prsd[0]), *prsd)]
                    continue
            print('Parsing error for', path)
        else:
            print('No folder', path + '!')
        return False
    return data


# Main thing
def main():
    args = parse_args()
    # cd to list for relative path
    file_path, args.parsee = args.parsee
    path, file = os.path.split(file_path)
    os.chdir(path)
    # Check parsing result
    success = parse_main(**vars(args))
    if success:
        file = os.path.splitext(file)[0]
        if args.mo_parse:
            file += '-mo'
        csv = file + '.csv'
        with open(csv, 'w') as f:
            f.write('\n'.join(success))
        print('Data successfully extracted and written to', csv + '!')
    else:
        print('Parser has encountered an error!')
    return


if __name__ == '__main__':
    main()
