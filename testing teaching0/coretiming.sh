#!/bin/bash
#list numbers to iterate over
corenumbers="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16"

#remove summary if it already exists
rm -f summary.txt

#print header
echo "N t" >> summary.txt

#loop over numbers
for N in $corenumbers
do
    #run with N cores
    echo "Running with " $N "cores"
    echo $N >> summary.txt
    OMP_NUM_THREADS=$N python3 coretiming.py >> summary.txt
done
