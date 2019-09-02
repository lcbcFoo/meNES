import sys
import argparse
import os
import subprocess
import binascii
from cpu import *

def main():
    argParser = argparse.ArgumentParser(description='Arguments for meNES emulator.')

    argParser.add_argument('input_file_path', help='The path to ROM file that the emulator will run.')
    argParser.add_argument('-g', '--debug', help='Run the file on debug mode (prints instructions).')
    # argParser.add_argument('-d', '--display', help='Print the output file on stdout', action='store_true')

    args = argParser.parse_args()
    input_file = args.input_file_path

    # Generates binary
    asmDirectory = os.path.dirname(os.path.realpath(input_file))
    status = subprocess.call(["asm6f", input_file],cwd=asmDirectory)

    # Read all lines in the binary file
    
    input_file = input_file.replace(".asm", ".bin")
    print(input_file)
    with open(input_file, 'rb') as i:
        data = i.read()
        hexa = binascii.hexlify(data)
    
    # Emulate binary
    cpu(data)

    # Show on stdout if requested to
    # if args.display:
    #     print(code)

if __name__ == '__main__':
    main()

