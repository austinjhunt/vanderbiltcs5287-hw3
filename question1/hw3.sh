#!/bin/bash
## hw3.sh
## Austin Hunt

# Execute this within a given Docker container
# to automate execution of matinv.py for each matrix dimension

for matrixDimension in 1000 1500 2000 2500 3000; do
    resultsFile="/results/${matrixDimension}.csv"
    python3 matinv.py -i 50 -d ${matrixDimension} ${resultsFile}
done