#!/bin/bash

sed -i '1d' feature_$1
paste ../documents/Vocabulary feature_$1 > feature_$1.bak

mv feature_$1.bak feature_$1
