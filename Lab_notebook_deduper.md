# Deduper Lab Notebook
### Author: Pen Hanks

### Date created: 10/11/2026

### Description :
Removing PCR duplicates.

# Overview
Updated 11/8/26
Python 3.14
samtools 1.25

## Inputs
- Sorted SAM file
- Name of output SAM file
- Text file containing one UMI on each line

## Outputs
Header lines: 65; Unique reads: 13719048; Wrong UMIs: 0; Duplicates removed: 4467362

### Chromosome specific counts
1       697508 \
10      564903\
11      1220389\
12      359951\
13      467659\
14      387239\
15      437465\
16      360923\
17      517566\
18      290506\
19      571665\
2       2787018\
3       547615\
4       589839\
5       562160\
6       510818\
7       1113183\
8       576463\
9       627488\
MT      202002\
X       317853\
Y       2247\
JH584299.1      3\
GL456233.2      656\
GL456211.1      6\
GL456221.1      4\
GL456354.1      1\
GL456210.1      5\
GL456212.1      4\
JH584304.1      294\
GL456379.1      2\
GL456367.1      3\
GL456239.1      1\
GL456383.1      1\
MU069435.1      5450\
GL456389.1      1\
GL456370.1      21\
GL456390.1      1\
GL456382.1      1\
GL456396.1      17\
GL456368.1      3\
MU069434.1      3\
JH584295.1      111

## usr/bin/time
- pixi run ./hanks_deduper.py -f ./C1_SE_uniqAlign.sam.sorted.sam -o ./part1/hanks_deduper_out.sam -u ./STL96.txt
    - Time
        - User time: 53.05
        - System time (seconds): 8.30
        - Elapsed (wall clock) time (h:mm:ss or m:ss): 1:02.22
    - CPU
        - Percent of CPU this job got: 98%
    - Memory
        - maximum resident set size: 1465380

# Log
## 11/8/26
Turns out, when you sit down and do stuff, it doesn't take that long!

### Soft checking
In my pseudocode, I wasnt checking the direction of the read, so I had to change my soft_check function to account for it. For reversed reads, I  took the position of the read and added the length of the read (Sum of numbers before everything except I and S) and the right soft clipping minus 1. For the forward reads, i took the position of the read and subtracted the left soft clipping. I had some issues because I kept forgetting to make sure I reset the values after I looked at each letter, but once that was resolved, I got the same output as other people!

### Creating system for tracking desired outputs
Once I checked the outputs that I needed to have, I realized I needed to redo the way I was checking whether or not to add a read to the dictionary. Initially, I was just checking that the tuple of unique identifiers wasn't in the dictionary already and that the UMI was in the set of all UMIs at the same time, which doesn't work to count the number of incorrect UMIs and removed duplicates. To adjust for this, I created a function that inputs an UMI and a dictionary that counts the values of unique reads, removed duplicates, and incorrect UMIs, and it would add the current read to the dictionary if it was unique and had a correct UMI, and would update the corresponding dictionary values depending on the situation. 

Counting header lines was easy enough, as I just added a line counter into the portion of the file that was already checking for the header lines. 

### Beginning and end
I was having some issues with handling the beginning and end of the file, which is why ran through the entire file before the main portion of it just to count the number of lines (I thought about using bash to get the number of lines and then hardcoding it in there, but I opted for the better solution of counting the lines in the script itself). This let me check if we had reached the end of the file so I could correctly output the final chromosome dictionary. Similarly, I had an issue initializing the chromosome at the beginning, so I created a sequence line tracker to check if it is the first line so it can be handled separately.  

## 10/20/26
Started on deduper python script and created shell script.

## 10/12/26
Organized pseudocode into sections using markdown, and modified it to go through each chromosome one by one

Created input and output test files, dealing with the cases
- same start and UMI
- same start accounting for soft clipped and same umi
- unknown umi
- same start and umi, different chromosomes
- Same start and different umi

put generated test files and pseudocode into a part1 folder
## 10/11/26
I started drafting pseudocode, and I'm nervous cause its pretty simple, but I think its gonna have everything or a lot of things in memory. I want to try and maybe just go by chromosome and erase everything after one chromosome is output to the sam file