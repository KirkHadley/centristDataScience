#! /bin/bash

touch sources.txt
echo "Downloading DC"

for state in DC CT DE FL GA 
do
    mkdir $state
    if [ $state == "CT" ]
    then
        cd CT
        python ../conn.py -s "http://connvoters.com/download.html" -t True
        cd ..
        echo "CT/*, http://connvoters.com/download.html" >> sources.txt
    fi
    if [ $state == "FL" ]
    then
        cd FL
        python ../conn.py -s "http://flvoters.com/downloads.html" -n 14
        cd ..
        echo "FL/*, http://flvoters.com/download.html" >> sources.txt
    fi
    if [ $state == "DE" ]
    then
        cd DE
        python ../conn.py -s "http://delawarevoters.info/downloads.html" -n 14
        cd ..
        echo "DE/*, http://delawarevoters.info/download.html" >> sources.txt
    fi
    if [ $state == "DC" ]
    then
        mkdir DC/2014_12_18
        mkdir DC/docs
        git clone https://github.com/ajschumacher/dc_voter_reg   
        mv dc_voter_reg/20141218-dc_voters.txt DC/docs/DC_2014_12_18_DOC.txt
        unzip dc_voter_reg/20141218-dc_voters.csv.zip 
        mv dc_voter_reg/20141218-dc_voters.csv DC/2014/DC_2014_12_18_DOC.csv
        rm -rf dc_voter_reg
        echo "DC/*, https://github.com/ajschumacher/dc_voter_reg" >> sources.txt
    fi
    if [ $state == "GA" ]
    then 
        cd GA
        python ../ga.py
        cd ..
        echo "GA/*, http://elections.sos.ga.gov/Elections/voterhistory.do" >> sources.txt
    fi  
done


