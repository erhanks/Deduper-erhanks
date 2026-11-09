#!/usr/bin/env bash

FILE_NAME=C1_SE_uniqAlign.sam
FILE=/projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam
FILE_S=./$FILE_NAME.sorted.sam
OUT=./part1/hanks_deduper_out.sam
UMI=./STL96.txt


pixi run samtools sort -o $FILE_S -O sam $FILE 
/usr/bin/time -v pixi run ./hanks_deduper.py -f $FILE_S -o $OUT -u $UMI