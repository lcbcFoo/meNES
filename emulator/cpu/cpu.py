import sys

print('oi')
def cpu(lines, output_file):
    # Writes txt file if output_file is set
    if output_file is not None:
        print("Writing file:", output_file)
        with open(output_file, 'w') as f:
            for element in lines:
                f.write("%s\n" % element)
    else:
        print("Printing lines on terminal:")
        for element in lines:
            print(element)
