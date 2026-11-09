#!/usr/bin/env python

import argparse as arg

def get_args():
    parser = arg.ArgumentParser(description="")
    parser.add_argument('-f', '--file', type = str, required=True)
    parser.add_argument('-o', '--outfile', type = str, required=True)
    parser.add_argument('-u', '--umi', type = str, required=True)
    return parser.parse_args()

def soft_check(cgr:str,bits:int,postn:int):
    revv = (bits & 16) == 16 # if it is 16, it IS REVERSED

    str_num = ""
    end = False
    length = 0
    end_sc = 0
    begin_sc = 0
    for i in cgr:
        if i.isdigit():
            str_num = str_num + str(i)
        else:
            int_num = int(str_num)
            if i == "S":
                if end:
                    end_sc = int_num
                else:
                    begin_sc = int_num
            else:
                end = True
                length += int_num
                str_num = ""
                int_num = 0

    if revv:
        strt = postn + length + end_sc-1 # and other stuff
    else:
        strt = postn - begin_sc
    #print(strt)
    return strt

def check_umi(umii:str,count:dict):
    if umii not in all_umi:
        count["wrong_umi"] += 1
        #print("wrong umi")
    elif dict_key in chrom_dict:
        count["dup_rem"] += 1
        #print("dup removed")
    else:
        chrom_dict[dict_key] = whole_line
        count["uniq_read"] += 1
        #print("uniq read")

args = get_args()
in_file = args.file
out_file = args.outfile
umis = args.umi

chrom_dict: dict[tuple,str] = {}
curr_chrom = 1
all_umi = set()

with open(umis) as umii:
    for line in umii:
        line = line.strip()
        all_umi.add(line)
    #print(all_umi)
            
file_lines = 0
with open(in_file) as inf:
    for line in inf:
        file_lines += 1

with open(in_file) as inf:
    with open(out_file, "w") as out:
        line_num = 0
        seq_lines = 0
        header_lines = 0
        chrom_count = {}
        counting = {"uniq_read":0,"dup_rem":0,"wrong_umi":0}

        for line in inf:
            line_num += 1

            if line.startswith("@"):
                out.write(line)
                header_lines += 1
            else:

                seq_lines += 1
                whole_line:str = line
                line = line.strip().split()
                chrom:str = line[2]
                cigar:str = line[5]
                pos:int = int(line[3]) 
                umi:str = line[0].split(":")[-1]
                bit:int = int(line[1])
                start:int = soft_check(cigar,bit,pos)
                dict_key:tuple = (start,umi)
                
                #print(f"Chrom: {chrom}; Start: {start}; Umi: {umi}; Current: {curr_chrom}")

                if seq_lines == 1:
                    curr_chrom = chrom
                    check_umi(umi,counting)
                    #print(f"Start of seq lines, chrom is {curr_chrom}, entry is {chrom_dict.keys()}")

                elif line_num == file_lines:
                    check_umi(umi,counting)
                    for item in chrom_dict.values():
                        #print(item)
                        out.write(item)
                    chrom_count[curr_chrom] = len(chrom_dict)
                    
                elif chrom != curr_chrom:
                    #print(chrom_dict.keys())
                    for item in chrom_dict.values():
                        #print(item)
                        out.write(item)

                    chrom_count[curr_chrom] = len(chrom_dict)

                    if umi in all_umi:
                        chrom_dict: dict[tuple,str] = {dict_key:whole_line}
                        counting["uniq_read"] +=1 
                    else:
                        chrom_dict: dict[tuple,str] = {}
                        counting["wrong_umi"] += 1
                    curr_chrom = chrom    
                    #print("Adding lines, reseting values")

                else:
                    check_umi(umi,counting)
        print(f"Header lines: {header_lines}; Unique reads: {counting["uniq_read"]}; Wrong UMIs: {counting["wrong_umi"]}; Duplicates removed: {counting["dup_rem"]}")
        for key, value in chrom_count.items():
            print(f"{key}\t{value}")
        #print(chrom_count)