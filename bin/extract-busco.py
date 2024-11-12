#!/usr/bin/env python3

import os
import glob
import json
import argparse

def getArgs():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-b',dest="buscoDir",type=str,required=False,default='datasets/busco',help='Folder with BUSCO results (json)')

    arg = parser.parse_args()

    return arg

def main(args):

    # 1 - Find short summary
    shortSum = glob.glob(args.buscoDir+"/*.json")

    # 2 - Open output files
    f = open("busco-merged.tsv", "w")
    f.write("Filename\tDomain\tSingle\tDuplicated\tFragmented\tMissing\n")

    r = open('busco-merged.R.tsv', 'w')
    r.write('Filename\tScore\tCategory\n')
    
    # 3 - Open each file and extract results
    for bjson in shortSum:
        with open(bjson, 'r') as file:
            data = json.load(file)
            # Parameters
            FASTA = os.path.splitext(os.path.basename(data['parameters']['in']))[0]
            DB = data['parameters']['domain']
            # Results
            SG = data['results']['Single copy percentage']
            DUP = data['results']['Multi copy percentage']
            FRAG = data['results']['Fragmented percentage']
            MISS = data['results']['Missing percentage']
            f.write(f'{FASTA}\t{DB}\t{SG}\t{DUP}\t{FRAG}\t{MISS}\n')
            r.write(f'{FASTA}\t{SG}\tSingle\n{FASTA}\t{DUP}\tDuplication\n{FASTA}\t{FRAG}\tFragmented\n{FASTA}\t{MISS}\tMissing\n')

    # 4 - Close open file(s)
    f.close()
    r.close()

if __name__ == '__main__':
    args = getArgs()
    main(args)
