#!/usr/bin/env bash

FILE=./part1/in_test.sam
FILE_S=$FILE.sorted.sam
OUT=./part1/hanks_deduper_out.sam
UMI=./STL96.txt


#pixi run samtools sort -o $FILE_S -O sam $FILE 
#/usr/bin/time -v 
pixi run ./hanks_deduper.py -f $FILE -o $OUT -u $UMI