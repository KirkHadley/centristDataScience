#! bin/bash

touch counts

for state in DC CT DE FL GA MI NC UT RI OK CO WA
#for state in DC DE
do
    cd $state
    l=$(find . -name '*.txt' | xargs wc -l | tail -n 1) 
    echo "$state $l"
    echo "$state $l" >> ../counts
    cd ..
done
