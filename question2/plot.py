""" Run this script after running the containers via docker-compose
Usage:
python plot.py
"""

import numpy as np
import matplotlib.pyplot as plt
import csv

def plot_config_by_completion_time():
    avg_completion_times = []
    configurations = []
    d = {

    }
    for num_map_workers in [10, 20]:
        d[num_map_workers] = {}
        for num_reduce_workers in [2, 3]:
            d[num_map_workers][num_reduce_workers] = {}
            for num_racks in [1, 2, 3]:
                d[num_map_workers][num_reduce_workers][num_racks] = []
                fname = f'metrics/{num_map_workers}-map-{num_reduce_workers}-reduce-{num_racks}-racks.csv'
                with open(fname, 'r') as f:
                    reader = csv.reader(f)
                    next(reader) # skip header
                    for line in reader: # only interested in total completion time, last item
                        d[num_map_workers][num_reduce_workers][num_racks].append(float(line[-1]))
                    configurations.append(f'{num_map_workers}-{num_reduce_workers}-{num_racks}')
                    avg_completion_times.append(
                        sum(d[num_map_workers][num_reduce_workers][num_racks]) /
                            len(d[num_map_workers][num_reduce_workers][num_racks])
                    )
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.subplots_adjust(bottom=0.15)
    ax.set_title('Average MapReduce \nCompletion Times of Various Network Configurations')
    ax.plot(configurations, avg_completion_times)
    ax.set_xlabel('Configuration (# Map Workers-# Reduce Workers-# Racks)')
    ax.set_xticklabels(configurations, rotation='vertical', fontsize=7)
    ax.set_ylabel('Completion Time (s)')
    plt.savefig('plots/config-by-completiontime.png')

def get_data_for_combo(num_racks, num_map_workers, num_reduce_workers):
    with open(f'metrics/{num_map_workers}-map-{num_reduce_workers}-reduce-{num_racks}-racks.csv','r') as f:
        reader = csv.reader(f)
        next(reader)
        return [float(line[-1]) for line in reader]

def get_data_for_num_map_workers(num_map_workers):
    results = []
    for num_racks in [1, 2, 3]:
        for num_reduce_workers in [2, 3]:
            with open(f'metrics/{num_map_workers}-map-{num_reduce_workers}-reduce-{num_racks}-racks.csv','r') as f:
                reader = csv.reader(f)
                next(reader)
                for line in reader:
                    results.append(float(line[-1]))
    return results

def get_data_for_num_reduce_workers(num_reduce_workers):
    results = []
    for num_racks in [1, 2, 3]:
        for num_map_workers in [10, 20]:
            with open(f'metrics/{num_map_workers}-map-{num_reduce_workers}-reduce-{num_racks}-racks.csv','r') as f:
                reader = csv.reader(f)
                next(reader)
                for line in reader:
                    results.append(float(line[-1]))
    return results

def get_data_for_num_racks(num_racks):
    results = []
    for num_map_workers in [10, 20]:
        for num_reduce_workers in [2, 3]:
            with open(f'metrics/{num_map_workers}-map-{num_reduce_workers}-reduce-{num_racks}-racks.csv','r') as f:
                reader = csv.reader(f)
                next(reader)
                for line in reader:
                    results.append(float(line[-1]))
    return results

def plot_cdf_per_num_racks():
    """ Create one CDF plot per # racks; one line per map-reduce combo (4 lines total)
    10M-2R
    10M-3R
    20M-2R
    20M-3R
    """
    for num_racks in [1,2,3]:
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_xlabel('$time (s)$')
        ax.set_ylabel('$p$')
        ax.set_title(f'Completion Time CDF Curve\nfor {num_racks} Racks')
        for mr_combo in [[10,2],[10,3],[20,2],[20,3]]:
            # Get and sort results for this combination
            data = np.sort(get_data_for_combo(num_racks, mr_combo[0],mr_combo[1]))
            # calculate the proportional values of samples
            # p = 1. * np.arange(len(data)) / (len(data) - 1)
            p = np.linspace(0, 1, len(data), endpoint=False)
            # Plot the percentiles
            _90th_percentile = round(np.percentile(data, 90),2)
            _95th_percentile = round(np.percentile(data, 95),2)
            _99th_percentile = round(np.percentile(data, 99),2)
            ax.plot(data, p, label=f"MapWorkers={mr_combo[0]},ReduceWorkers={mr_combo[1]}; \n90th={_90th_percentile};\n95th={_95th_percentile};\n99th={_99th_percentile}")
        plt.legend(bbox_to_anchor=(1.05, 1.0, 0.4, 0.1), loc='upper left')
        plt.tight_layout()
        plt.savefig(f'plots/cdf-{num_racks}-racks.png')
        plt.close()

def plot_cdf_one_line_per_num_racks():
    """ Create one CDF plot with one line per num racks
    """
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel('$time (s)$')
    ax.set_ylabel('$p$')
    ax.set_title(f'Completion Time CDF Curve\nfor 1, 2, and 3 Mininet Racks')
    for num_racks in [1,2,3]:
        data = np.sort(get_data_for_num_racks(num_racks=num_racks))
        # calculate the proportional values of samples
        # p = 1. * np.arange(len(data)) / (len(data) - 1)
        p = np.linspace(0, 1, len(data), endpoint=False)
        # Plot the percentiles
        _90th_percentile = round(np.percentile(data, 90),2)
        _95th_percentile = round(np.percentile(data, 95),2)
        _99th_percentile = round(np.percentile(data, 99),2)
        ax.plot(data, p, label=f"# Racks={num_racks}; \n90th={_90th_percentile};\n95th={_95th_percentile};\n99th={_99th_percentile}")
    plt.legend(bbox_to_anchor=(1.05, 1.0, 0.4, 0.1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f'plots/cdf-all-num-racks.png')
    plt.close()

def plot_cdf_one_line_per_num_map_workers():
    """ Create one CDF plot with one line per num map workers
    """
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel('$time (s)$')
    ax.set_ylabel('$p$')
    ax.set_title(f'Completion Time CDF Curve\nfor 10 and 20 Map Workers')
    for map_workers in [10, 20]:
        data = np.sort(get_data_for_num_map_workers(num_map_workers=map_workers))
        # calculate the proportional values of samples
        # p = 1. * np.arange(len(data)) / (len(data) - 1)
        p = np.linspace(0, 1, len(data), endpoint=False)
        # Plot the percentiles
        _90th_percentile = round(np.percentile(data, 90),2)
        _95th_percentile = round(np.percentile(data, 95),2)
        _99th_percentile = round(np.percentile(data, 99),2)
        ax.plot(data, p, label=f"# Map Workers={map_workers}; \n90th={_90th_percentile};\n95th={_95th_percentile};\n99th={_99th_percentile}")
    plt.legend(bbox_to_anchor=(1.05, 1.0, 0.4, 0.1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f'plots/cdf-all-num-map-workers.png')
    plt.close()

def plot_cdf_one_line_per_num_reduce_workers():
    """ Create one CDF plot with one line per num reduce workers
    """
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel('$time (s)$')
    ax.set_ylabel('$p$')
    ax.set_title(f'Completion Time CDF Curve\nfor 2 and 3 Reduce Workers')
    for reduce_workers in [2, 3]:
        data = np.sort(get_data_for_num_reduce_workers(num_reduce_workers=reduce_workers))
        # calculate the proportional values of samples
        # p = 1. * np.arange(len(data)) / (len(data) - 1)
        p = np.linspace(0, 1, len(data), endpoint=False)
        # Plot the percentiles
        _90th_percentile = round(np.percentile(data, 90),2)
        _95th_percentile = round(np.percentile(data, 95),2)
        _99th_percentile = round(np.percentile(data, 99),2)
        ax.plot(data, p, label=f"# Reduce Workers={reduce_workers}; \n90th={_90th_percentile};\n95th={_95th_percentile};\n99th={_99th_percentile}")
    plt.legend(bbox_to_anchor=(1.05, 1.0, 0.4, 0.1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f'plots/cdf-all-num-reduce-workers.png')
    plt.close()




if __name__ == "__main__":
    plot_config_by_completion_time()
    plot_cdf_per_num_racks()
    plot_cdf_one_line_per_num_racks()
    plot_cdf_one_line_per_num_map_workers()
    plot_cdf_one_line_per_num_reduce_workers()