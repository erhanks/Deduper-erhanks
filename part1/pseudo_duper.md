## Files:
```
input_sam_file - sorted by chromosome with samtools before putting through script
output_sam_file - will be in chromosome order
umi_file - one umi per line
```

## Functions:
```
def soft_check(cigar: string) -> int: 
''' 
To extract the number of soft clipped bases from a CIGAR string
'''
    if first letter in cigar is S:
        return number before it
    else
        return 0
```
### Examples
```
soft_check("2S4M") -> 2
soft_check("4M") -> 0
soft_check("4M2S") -> 0
```


## Main Script
```
-- Initializing variables & file --
current_chrom_dict = {}
all_umi = set() # in a set for faster lookup

with open output_sam_file (writing to new file) as out_sam: # To write over the previous output_sam_file if there was one to not cause problems with appending later, and to add headers if needed
    add headers

-- Dealing with umi file --
with open umi_file:
    for line in umi_file:
        line = line.strip
        all_umi.add(line)
    
with open input_sam_file:
    for line in input_sam_file:
        if line.starts_with("@") == False
            line = line.strip.split
            chrom = line[2]
            cigar = line[5]
            start = line[3] - soft_check(cigar) # moving the start point as far back as the soft check is
            umi = split line[0] at the colons and take the last entry of that list

            if chrom != curr chrom: # Only dealing with one chromosome at a time to minimize memory usage
                append current_chrom_dict to output_sam_file
                current_chrom_dict = {}
                curr_chrom = chrom
            else:
                continue 

            if (start,umi) not in current_chrom_dict and umi in all_umi:
                current_chrom_dict[(start,umi)] = line
            else:
                continue
```