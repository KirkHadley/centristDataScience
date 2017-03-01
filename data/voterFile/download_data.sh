#! /bin/bash

touch sources.txt
echo "Downloading DC"

for state in DC CT DE FL GA MI NC UT RI OK CO WA 
do
    mkdir $state
    if [ $state == "CT" ]
    then
        cd CT
        python ../conn.py -s "http://connvoters.com/download.html" -n 14 
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
        mv 20141218-dc_voters.csv DC/2014_12_18/DC_2014_12_18_DOC.csv
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
    if [ $state == "MI" ]
    then
        cd MI
        python ../conn.py -s "http://michiganvoters.info/download.html" -n 14
        cd ..
        echo "MI/*, http://michiganvoters.info/download.html" >> sources.txt
    fi
    if [ $state == "UT" ]
    then
        cd UT
        curl https://www.indymedia.org.uk/media/2014/02//515560.zip -o UT_2014.zip
        cd ..
        echo "UT/*, https://www.indymedia.org.uk/en/2014/02/515559.html" >> sources.txt
    fi
    if [ $state == "RI" ]
    then
        cd RI
        curl http://rivoters.com/download/2015-01.txt -O
        curl http://rivoters.com/download/2012-01.txt -O
        cd ..
        echo "RI/*, http://rivoters.com/download/2012-01.txt" >> sources.txt
    fi
    if [ $state == "OK" ]
    then
        cd OK
        python ../conn.py -s "http://oklavoters.com/download.html" -n 14 
        cd ..
        echo "OK/*, http://oklavoters.com/download.html" >> sources.txt
    fi
    if [ $state == "CO" ]
    then
        cd CO
        python ../conn.py -s "http://coloradovoters.info/download.html" -n 14 
        cd ..
        echo "CO/*, http://coloradovoters.info/download.html" >> sources.txt
    fi
    if [ $state == "NC" ]
    then
        cd NC
        python ../nc.py 
        cd ..
        echo "NC/*, https://s3.amazonaws.com/dl.ncsbe.gov?delimiter=%2F&prefix=" >> sources.txt
    fi
    if [ $state == "WA" ]
    then
        cd WA
        wget http://www.sos.wa.gov/elections/vrdb/download/vrdb-current.zip
        cd ..
        echo "WA/*, http://www.sos.wa.gov/elections/vrdb/download/vrdb-current.zip" >> sources.txt
    fi
done

