# Vanderbilt University CS 5287 Principles of Cloud Computing Homework 3
## Due 11/19/2021

Please refer to the below sections for the locations of the deliverables for Homework Assignment 3 questions 1 and 2.

### Question 1
For this question, I created a [docker-compose.yml file](question1/docker-compose.yml) to automatically spin up an environment consisting of a docker container with 1 CPU, 0.5 CPUs, and 0.25 CPUs, respectively named cpu1, cpu0p5, and cpu0p25.

I modified the Dockerfile to include the directive `ADD hw3.sh /`, so that `hw3.sh`, seen below, can be executed within containers built from that image.
```
#!/bin/bash
## hw3.sh
## Austin Hunt

# Execute this within a given Docker container
# to automate execution of matinv.py for each matrix dimension

for matrixDimension in 1000 1500 2000 2500 3000; do
    resultsFile="/results/${matrixDimension}.csv"
    python3 matinv.py -i 50 -d ${matrixDimension} ${resultsFile}
done

```

With the inclusion of hw3.sh in the / folder of the image, I provide the command `bash /hw3.sh` to each of the services `cpu1`, `cpu0p5`, and `cpu0p25` to automate the execution of matinv.py for each matrix dimension within each differently allocated container. I also use the `volumes` key in the docker-compose file to mount each container's `/results` folder to a respective folder on the host, so that I do not have to copy files out of the containers before removing them.

These host folders are the `cpu*results` folders, each containing 5 CSV files, one per matrix dimension.

Lastly, I created a `plot.py` file that uses `numpy` and `matplotlib` to plot the following using those results files:
1. CPU count by Matrix Dimension by Average Time in 3D ([One plot](question1/plots/cpu-by-matrixdim-time-avg.png))
2. CPU count by Matrix Dimension by Standard Deviation of Time in 3D ([One plot](plots/../question1/plots/cpu-by-matrixdim-time-stddev.png))
3. One CDF curve per (CPU Count, Matrix Dimension) combo (15 plots total; [example here](plots/../question1/plots/cdf-cc-0.25-md-1000.png))
4. One CDF plot per matrix dimension containing one line per CPU count (5 plots total; [example here](plots/../question1/plots/cdf-matrixdim-1000.png))


### Question 2
For this question, I used Vagrant with the `ubuntu/focal64` box provisioned with a SHELL provisioner to speed up the process of creating a VM with the necessary packages installed (mininet, Python, etc.).
I also made sure to sync the Vagrantfile folder with the `/vagrant` path inside the VM for the purpose of easy file sharing.

Once the VM was created (with `vagrant init` and `vagrant up --provision`), I ran the commands as indicated in the instructions manually (after trying and failing to get the full automation of the data collection to work, as evidenced by my [test_all.sh](question2/test_all.sh) Bash script and my customized [mr_mininet.py](question2/mr_mininet.py) Python module).

All data was collected into the `question2/metrics` folder ([example here](question2/metrics/10-map-2-reduce-1-racks.csv) ). I have one CSV per 3-combination of `# map workers`, `# reduce workers`, and `# racks`, where each CSV contains 5 records (i.e., iterations), totaling 12 files, and totaling 60 iterations.

After the data was collected, I wrote a new plotting script using (again) `matplotlib` and `numpy`. This module handles the creation of the following plots:
1. A simple "configuration by completion time" 2-dimensional line graph, showing the relationship between average map reduce completion times and the respective 3-combinations of (# map workers, # reduce workers, and # racks), totaling 12 combinations. [Plot is here.](question2/plots/config-by-completiontime.png)
2. One CDF plot per # Mininet Racks configured (including 1, 2, and 3 mininet racks). Each plot contains 4 lines corresponding to 4 different combinations of (# map workers, # reduce workers) for that rack configuration. [Example here of 1 mininet rack](question2/plots/cdf-1-racks.png)
3. One CDF Plot with one line per number of mininet racks configured. [Plot is here](question2/plots/cdf-all-num-racks.png)
4. One CDF Plot with one line per number of map workers configured. [Plot is here](question2/plots/cdf-all-num-map-workers.png)
5. One CDF Plot with one line per number of reduce workers configured. [Plot is here](question2/plots/cdf-all-num-reduce-workers.png)

### Patterns Observed
- Based on the plots, it is not 100% clear that adding racks to an emulated topology increases average completion time. This is a result I was expecting because of the fact that switch-to-switch communication carries longer delay than host-to-switch communciation. However, plots such as [this one](question2/plots/cdf-all-num-racks.png) blur that correlation a bit.
- Adding more map workers (i.e. 20 vs 10) provides for shorter average completion time ([proof](question2/plots/cdf-all-num-map-workers.png))
- Adding more reduce workers (i.e. 3 vs 2) provides for shorter average completion time ([proof](question2/plots/cdf-all-num-reduce-workers.png)
- Based on [this plot](question2/plots/config-by-completiontime.png), I would argue that adding a rack to a topology has a greater negative impact (causing longer completion time) when there are 10 map workers and 2 reduce workers than with any other config. Just based on the slop of the line in the leftmost 10-2-* section, it seems like this is the configuration impacted by rack addition the most.

