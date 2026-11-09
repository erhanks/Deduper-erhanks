#!/usr/bin/env python

import argparse as arg

def get_args():
    parser = arg.ArgumentParser(description="Inputs a sorted sam file and outputs a sam file containing the first read of a PCR duplicate")
    parser.add_argument('-f', '--file', type = str, required=True, help = "Input sorted sam file")
    parser.add_argument('-o', '--outfile', type = str, required=True, help = "Name of output file")
    parser.add_argument('-u', '--umi', type = str, required=True, help = "File containing list of UMIs, such that each UMI is on a new line")
    return parser.parse_args()

def soft_check(cgr:str,bits:int,postn:int):
    ''' Takes in a CIGAR string, bitwise flag, and 1-based left most mapping position,
    and returns the start site of the corresponding read.
    '''
    revv = (bits & 16) == 16 # if it is 16, it IS REVERSED
    str_num = ""
    end = False
    length = 0
    end_sc = 0
    begin_sc = 0

    for i in cgr:
        if i.isdigit(): # Collecting digits before letter
            str_num = str_num + str(i)
        else: # Once number is finished, let the letters determine what to do with it
            int_num = int(str_num)
            if i == "S":
                if end:
                    end_sc = int_num # Right soft clipping
                else:
                    begin_sc = int_num # Left soft clipping
                str_num = ""
                int_num = 0
            elif i == "I": # Skipping over insertions
                str_num = ""
                int_num = 0
            else: # All other letters add to length of read
                end = True
                length += int_num
                str_num = ""
                int_num = 0
    if revv:
        strt = postn + length + end_sc-1 
    else:
        strt = postn - begin_sc
    return strt

def check_umi(umii:str,count:dict):
    ''' To check and count the number of wrong UMIs and removed duplicates '''
    if umii not in all_umi:
        count["wrong_umi"] += 1
    elif dict_key in chrom_dict:
        count["dup_rem"] += 1
    else:
        chrom_dict[dict_key] = whole_line
        count["uniq_read"] += 1

args = get_args()
in_file = args.file
out_file = args.outfile
umis = args.umi

chrom_dict: dict[tuple,str] = {}
curr_chrom = 1
all_umi = set() # For fast lookup

# Creating set of UMIs
with open(umis) as umii:
    for line in umii:
        line = line.strip()
        all_umi.add(line)

# To count length of file to know when to add the last dictionary to file            
file_lines = 0 
with open(in_file) as inf:
    for line in inf:
        file_lines += 1

with open(in_file) as inf:
    with open(out_file, "w") as out:
        # Initializing counting variables
        line_num = 0
        seq_lines = 0
        header_lines = 0
        chrom_count = {}
        counting = {"uniq_read":0,"dup_rem":0,"wrong_umi":0}

        for line in inf:
            line_num += 1
            if line.startswith("@"): # If its a header line
                out.write(line)
                header_lines += 1

            else:
                seq_lines += 1
                # Variables from line
                whole_line:str = line
                line = line.strip().split()
                chrom:str = line[2]
                cigar:str = line[5]
                pos:int = int(line[3]) 
                umi:str = line[0].split(":")[-1] 
                bit:int = int(line[1]) # Bitwise flag
                start:int = soft_check(cigar,bit,pos)
                revv:bool = (bit & 16) == 16 # True if strand is reverse
                dict_key:tuple = (start,umi,revv) 
                # Dictionary key contains Start, Umi, and whether or not its reversed, \
                # all things that factor into whether its a duplicate

                if seq_lines == 1: # If this is the first line
                    curr_chrom = chrom
                    check_umi(umi,counting)

                elif line_num == file_lines: # If this is the last line
                    check_umi(umi,counting)
                    for item in chrom_dict.values(): #writing to file
                        out.write(item)
                    chrom_count[curr_chrom] = len(chrom_dict)
                    
                elif chrom != curr_chrom: # If we've finished a chromosome
                    for item in chrom_dict.values():
                        out.write(item)
                    chrom_count[curr_chrom] = len(chrom_dict)

                    if umi in all_umi: # If the UMI is in the set, we add it cause this is the first entry of the chromosome
                        chrom_dict: dict[tuple,str] = {dict_key:whole_line}
                        counting["uniq_read"] +=1 
                    else: # If not, we empty the dictionary
                        chrom_dict: dict[tuple,str] = {}
                        counting["wrong_umi"] += 1
                    curr_chrom = chrom    

                else: # Checking within a chromosome
                    check_umi(umi,counting)

        # Print output values
        print(f"Header lines: {header_lines}; Unique reads: {counting["uniq_read"]}; Wrong UMIs: {counting["wrong_umi"]}; Duplicates removed: {counting["dup_rem"]}")
        for key, value in chrom_count.items():
            print(f"{key}\t{value}")