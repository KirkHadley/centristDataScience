#! bin/bash

touch counts_csv

for state in DC CT DE FL GA MI NC UT RI OK CO WA
#for state in DC DE
do
    cd $state
    l=$(find . -name '*.csv' | xargs wc -l | tail -n 1) 
    echo "$state $l"
    echo "$state $l" >> ../counts_csv
    cd ..
done

