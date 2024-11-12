#!/usr/bin/env python

import os
import re
import glob
import argparse


def getArgs():
    parser = argparse.ArgumentParser(
        description="Generate a multiple species plot for all OMArk folder in a given path.")
    parser.add_argument('-i', '--input',dest="omarkDir", type=str, help="Folder with OMArk results", required=False, default="datasets/omark")
    
    arg = parser.parse_args()

    return arg

def main(args):
    # 1 - Find summary
    shortSum = glob.glob(args.omarkDir+"/*.sum")

    # 2 - Open output files
    f = open("omark-merged.tsv", "w")
    f.write("Filename\tProteins\tSingle\tDuplicated\tMissing\tConsistent\tInconsistent\tContaminant\tUnknown\n")

    cp = open('omark-completeness.R.tsv', 'w')
    cp.write('Filename\tScore\tCategory\n')

    cs = open('omark-consistency.R.tsv', 'w')
    cs.write('Filename\tScore\tCategory\n')

    po = open('omark-proteins-count.R.tsv', 'w')
    po.write('Filename\tProteins\n')

    # 3 - Open each file and extract results
    for sum in shortSum:
        with open(sum, 'r') as omaqsum:
            in_cont = False
            FAA = os.path.splitext(os.path.basename(sum))[0]
            for line in omaqsum.readlines():
                if not in_cont:
                    protein_nr_line = re.search(r"On the whole proteome, there \w+ ([0-9]+) proteins", line)
                    if protein_nr_line:
                        PROTEINS = int(protein_nr_line.group(1))
                    #S:Single:S, D:Duplicated[U:Unexpected,E:Expected],M:Missing
                    resultline = re.search(r"S:([-0-9.]+)%,D:([-0-9.]+)%\[U:([-0-9.]+)%,E:([-0-9.]+)%\],M:([-0-9.]+)", line)
                    if resultline:
                        COMPLETE = float(resultline.group(1)) + float(resultline.group(2))
                        SINGLE = float(resultline.group(1))
                        DUPLICATED = float(resultline.group(2))
                        EXPECTED_DUPLICATED = float(resultline.group(3))
                        UNEXPECTED_DUPLICATED = float(resultline.group(4))
                        MISSING = float(resultline.group(5))
                    #C:Placements in correct lineage [P:Partial hits, F:Fragmented], E: Erroneous placement [P:Partial hits, F:Fragmented], N: no mapping
                    conservline = re.search(r"A:([-0-9.]+)%\[P:([-0-9.]+)%,F:([-0-9.]+)%\],I:([-0-9.]+)%\[P:([-0-9.]+)%,F:([-0-9.]+)%\],C:([-0-9.]+)%\[P:([-0-9.]+)%,F:([-0-9.]+)%\],U:([-0-9.]+)%", line)
                    if conservline:
                        CONSISTENT = float(conservline.group(1))
                        CONSISTENT_PARTIALLY_MAPPING = float(conservline.group(2))
                        CONSISTENT_FRAGMENTS = float(conservline.group(3))
                        CONSISTENT_STRUCTURALLY_CONSISTENT = float(conservline.group(1)) - float(conservline.group(2)) - float(conservline.group(3))
                        INCONSISTENT = float(conservline.group(4))
                        INCONSISTENT_PARTIALLY_MAPPING = float(conservline.group(5))
                        INCONSISTENT_FRAGMENTS = float(conservline.group(6))
                        INCONSISTENT_STRUCTURALLY_CONSISTENT = float(conservline.group(4)) - float(conservline.group(5)) - float(conservline.group(6))
                        CONTAMINANT = float(conservline.group(7))
                        CONTAMINANT_PARTIALLY_MAPPING = float(conservline.group(8))
                        CONTAMINANT_FRAGMENTS = float(conservline.group(9))
                        CONTAMINANT_STRUCTURALLY_CONSISTENT = float(conservline.group(7)) - float(conservline.group(8)) - float(conservline.group(9))
                        UNKNOWN = float(conservline.group(10))
                    if line == '#From HOG placement, the detected species are:\n':
                        in_cont = True
                else:
                    if line[0] == '#' or line == '\n':
                        continue

            f.write(f'{FAA}\t{PROTEINS}\t{SINGLE}\t{DUPLICATED}\t{MISSING}\t{CONSISTENT}\t{INCONSISTENT}\t{CONTAMINANT}\t{UNKNOWN}\n')
            cp.write(f'{FAA}\t{SINGLE}\tSingle\n{FAA}\t{DUPLICATED}\tDuplicated\n{FAA}{MISSING}\tMissing\n')
            cs.write(f'{FAA}\t{CONSISTENT}\tConsistent\n{FAA}\t{INCONSISTENT}\tInconsistent\n{FAA}\t{CONTAMINANT}\tContaminant\n{FAA}\t{UNKNOWN}\tUnknowm\n')
            po.write(f'{FAA}\t{PROTEINS}\n')


    # 4 - Close open file(s)
    f.close()
    cp.close()
    cs.close()
    po.close()

if __name__ == '__main__':
    args = getArgs()
    main(args)
