#!/usr/bin/python

#
# Vanderbilt University, Computer Science
# CS4287-5287: Principles of Cloud Computing
# Author: Aniruddha Gokhale
# Created: Nov 2016
#
# Purpose: The code here is used to demonstrate the homegrown wordcount
# MapReduce framework on a network topology created using Mininet SDN emulator
#
# The mininet part is based on examples from the mininet distribution. The MapReduce
# part has been modified from the earlier thread-based implementation to a more
# process-based implementation required for this sample code
#

import os              # OS level utilities
import sys
import argparse   # for command line parsing
from yaspin import yaspin
from signal import SIGINT
import time

import subprocess

# These are all Mininet-specific
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import CLI
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.util import pmonitor

# This is our topology class created specially for Mininet
from mr_topology import MR_Topo


##################################
# Save the IP addresses of each host in our network
##################################
def saveIPAddresses (hosts, file="ipaddr.txt"):
    # for each host in the list, print its IP address in a file
    # The idea is that this file is now provided to the Wordcount
    # master program so it can use it to find the IP addresses of the
    # Map and Reduce worker machines
    try:
        file = open ("ipaddr.txt", "w")
        for h in hosts:
            file.write (h.IP () + "\n")

        file.close ()

    except:
            print(("Unexpected error:.format{}".sys.exc_info()[0]))
            raise

##################################
# run the entire map reduce set up on the hosts
#
# NOTE: I cannot get this to work properly so we are
# not going to use this approach
##################################
def runMapReduceWordCount (hosts, args):
    try:
        cmds = {}
        # Master
        cmds[hosts[0]] = hosts[0].sendCmd(f'python3 mr_wordcount.py -i {args.iters} -M {args.map} -f {args.metricsfile} -R {args.reduce} -p {args.masterport} {args.datafile}')
        # next run the Map workers
        # do this for as many map jobs as there are. Note that the hosts are organized as follows:
        # 0th entry is master, followed by map hosts, followed by reduce hosts
        for i in range (args.map):
            cmds[hosts[i+1]] = hosts[i+1].sendCmd(f'python3 mr_mapworker.py {hosts[0].IP()} {args.masterport}')

        #  next create the command for the reduce workers
        k = 1 + args.map   # starting index for reducer hosts (master + maps)
        for i in range (args.reduce):
            cmds[hosts[k+i]] = hosts[k+i].sendCmd(f'python3 mr_reduceworker.py {hosts[0].IP ()} {args.masterport}')
    except:
            print("Unexpected error in run mininet:", sys.exc_info()[0])
            raise

def main ():
    "Create and run the Wordcount mapreduce program in Mininet topology"
    parser = argparse.ArgumentParser ()
    parser.add_argument ("-p", "--masterport", type=int, default=5556, help="Wordcount master port number, default 5556")
    parser.add_argument ("-r", "--racks", type=int, choices=[1, 2, 3], default=1, help="Number of racks, choices 1, 2 or 3")
    parser.add_argument ("-i", "--iters", type=int, default=5, help="Number of iterations")
    parser.add_argument ("-M", "--map", type=int, default=10, help="Number of Map jobs, default 10")
    parser.add_argument ("-R", "--reduce", type=int, default=3, help="Number of Reduce jobs, default 3")
    parser.add_argument ("-f", "--metricsfile", default="metrics.csv", help="Output file to collect metrics, default metrics.csv")
    parser.add_argument ("datafile", help="Big data file")
    parsed_args = parser.parse_args ()

    # instantiate our topology
    print("Instantiate topology")
    topo = MR_Topo (Racks=parsed_args.racks, M = parsed_args.map, R = parsed_args.reduce)

    # create the network
    print("Instantiate network")
    net = Mininet (topo, link=TCLink)

    # activate the network
    print("Activate network")
    net.start()

    print("Running MapReduce word count...")
    with yaspin().white.bold.shark.on_blue as sp:
        runMapReduceWordCount (net.hosts, parsed_args)
        for host, line in net.monitor():
            if host:
                print(f'{host} --- {line}')


    print("Cleaning up network")
    # cleanup
    net.stop ()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    main ()
