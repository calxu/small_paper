#!/bin/bash

./handle_documents_$1.py > documents_$1

awk -F '\t' '{print $1}' ../train_Checkins | sort -n | uniq > Vocabulary

./handle_map.py documents_$1 > $1.doc

sed -i "s/	$//g" $1.doc

# rm Vocabulary
