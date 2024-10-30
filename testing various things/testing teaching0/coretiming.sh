#!/bin/bash
#list numbers to iterate over
corenumbers="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16"
runs="1 2 3 4 5 6 7 8 9 10"

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
    #run over i runs
    for i in $runs
    do
	OMP_NUM_THREADS=$N python3 coretiming.py >> summary.txt
	echo "done "$i"/10"
    done
    echo ":" >> summary.txt

done
