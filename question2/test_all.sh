#!/bin/bash
# Austin Hunt
# 11/19/2021
# Bash script to obtain results for the following configurations:
# Number of map tasks varied as: 10 and 20
# Number of Reduce tasks varied as: 2 and 3
# Number of racks varied as 1, 2 and 3
# Total combinations = 2 * 2 * 3 = 12
sleepTime=5
iters=5
cd /vagrant 

for mapTasks in 10 20; do
    for reduceTasks in 2 3; do
        for racks in 1 2 3; do
            # This will create the appropriate topology.
            echo "Cleaning network..."
            sudo mn -c
            metricsfile="metrics/${mapTasks}-map-${reduceTasks}-reduce-${racks}-racks.csv"
            echo "Running map reduce with ${racks} racks, ${reduceTasks} reduce tasks, and ${mapTasks} map tasks; writing to metrics file ${metricsfile}"
            sudo python3 mr_mininet.py -i ${iters} -M $mapTasks -R $reduceTasks -r $racks big.txt --metricsfile ${metricsfile}
            echo "sleeping for ${sleepTime} seconds"
            sleep $sleepTime
        done
    done
done
