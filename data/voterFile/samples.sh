#! bin/bash

find . -name "*.csv"|while read fname; do
  echo $fname
  head -n 100 $fname > $fname.sample 
done
find . -name "*.CSV"|while read fname; do
  echo $fname
  head -n 100 $fname > $fname.sample 
done

find . -name "*.TXT"|while read fname; do
  echo $fname
  head -n 100 $fname > $fname.sample 
done
#find . -name "*.txt"|while read fname; do
#  echo $fname
#  head -n 100 $fname > $fname.sample 
#done
#
#
