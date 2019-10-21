#!/bin/bash

./word2vec -train ../Sequence/Sequence_$1 -output feature_$1 -cbow 0 -size 100 -window 5 -negative 0 -hs 1 > logFeature
sed -i "s/ /	/g" feature_$1
sed -i "s/	$//g" feature_$1
sed -i "1,2d" feature_$1
rm logFeature
