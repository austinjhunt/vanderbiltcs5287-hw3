#!/usr/bin/python
#
# Purpose: Simple MapReduce Wordcount
#
#
# Note that this is standalone main program. Although we can invoke it via
# mininet, you can start it manually from an xterm that you can start on the
# master node from the mininet CLI
#
# Moreover, this code is also now dockerizable
#
# Vanderbilt University Computer Science
# Author: Aniruddha Gokhale
# Course: CS4287-5287 Principles of Cloud Computing
# Created: Fall 2016
# Modified: Nov 2017

# system and time
import os
import sys
import time
import argparse   # argument parser
import re          # regular expression

from mr_framework import MR_Framework # our wordcount MR framework

def parseCmdLineArgs ():
    parser = argparse.ArgumentParser ()
    parser.add_argument ("-i", "--iters", type=int, default=20, help="Number of iterations, default 20")
    parser.add_argument ("-f", "--metricsfile", default="metrics.csv", help="Output file to collect metrics, default metrics.csv")
    parser.add_argument ("-M", "--map", type=int, default=10, help="Number of Map jobs, default 10")
    parser.add_argument ("-R", "--reduce", type=int, default=3, help="Number of Reduce jobs, default 3")
    parser.add_argument ("-p", "--masterport", type=int, default=5556, help="Master node port, default 5556")
    parser.add_argument ("datafile", help="Big data file")
    args = parser.parse_args ()
    return args

def main ():
    print("MapReduce Wordcount Main program")
    parsed_args = parseCmdLineArgs ()

    # now invoke the mapreduce framework. Notice we have slightly changed the way the
    # constructor works and the arguments it takes.
    mrf = MR_Framework (parsed_args)

    # invoke the process
    mrf.solve ()

#----------------------------------------------
if __name__ == '__main__':
    main ()
