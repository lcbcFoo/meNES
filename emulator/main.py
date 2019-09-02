import sys
import argparse
from cpu import *

def main():
    argParser = argparse.ArgumentParser(description='Arguments for meNES emulator.')

    argParser.add_argument('input_file_path', help='The path to ROM file that the emulator will run.')
    argParser.add_argument('-g', '--debug', help='Run the file on debug mode (prints instructions).')
    # argParser.add_argument('-d', '--display', help='Print the output file on stdout', action='store_true')

    args = argParser.parse_args()
    input_file = args.input_file_path

    # Read all lines in the input file
    with open(input_file, 'r') as i:
        lines = i.readlines()

    # Emulate binary
    cpu(lines)

    # Show on stdout if requested to
    # if args.display:
    #     print(code)

if __name__ == '__main__':
    main()

