#!/bin/bash
python sortingAlgorithms.py > file
j=$(grep ^P file | grep -o '[0-9:]*' | tail -1)
i=$(grep ^seconds.. file | awk 'NF>1{print $NF}')
k=$(grep ^number file | grep -o '[0-9.]*')
l=$(grep ^sortedness file | awk 'NF>1{print $NF}')
echo $j"," $i"," $k"," $l >> insertion_SnowHeight.csv


