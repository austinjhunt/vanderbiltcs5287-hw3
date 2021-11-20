""" Run this script after running the containers via docker-compose
Usage:
python plot.py
"""

import numpy as np
import matplotlib.pyplot as plt
from util import *


def plot_cdf_per_matrix_dimension():
    """ Create one CDF plot per matrix dimension; one line per CPU count """
    for matrix_dimension in [1000, 1500, 2000, 2500, 3000]:
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_xlabel('$time (s)$')
        ax.set_ylabel('$p$')
        for cpu_count in [0.25, 0.5, 1]:
            # Get and sort results for this combination
            data = np.sort(get_results_list_from_matrix_dimension(cpu_count, matrix_dimension))
            # calculate the proportional values of samples
            # p = 1. * np.arange(len(data)) / (len(data) - 1)
            p = np.linspace(0, 1, len(data), endpoint=False)
            # Plot the percentiles
            _90th_percentile = round(np.percentile(data, 90),2)
            _95th_percentile = round(np.percentile(data, 95),2)
            _99th_percentile = round(np.percentile(data, 99),2)
            ax.plot(data, p, label=f"CPU={cpu_count}; \n90th={_90th_percentile};\n95th={_95th_percentile};\n99th={_99th_percentile}")
        plt.legend(bbox_to_anchor=(1.05, 1.0, 0.4, 0.1), loc='upper left')
        plt.tight_layout()
        plt.savefig(f'plots/cdf-matrixdim-{matrix_dimension}.png')
        plt.close()




def plot_3d_avg():
    """ Plot CPU count by Matrix Dimension by Average Time in 3D (One plot) """
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_title('Computation Time AVG v. CPU Count v. Matrix Dimension')
    cpu_counts = [0.25, 0.5, 1.0]
    matrix_dims = [1000, 1500, 2000, 2500, 3000]
    for cpu_count in cpu_counts:
        # New line for new CPU count
        avgs_for_current_cpu_count = []
        for matrix_dim in matrix_dims:
            # let Z be average time for this CPU count and this Matrix dimension
            results = get_results_for_cpu_count(cpu_count)[matrix_dim]
            avg = round((sum(results) / len(results)), 3)
            avgs_for_current_cpu_count.append(avg)
        ax.scatter([cpu_count] * 5, matrix_dims, avgs_for_current_cpu_count, 'gray')
        ax.set_xlabel('CPU count')
        ax.set_xticks([0.25, 0.5, 1])
        ax.set_ylabel('Matrix Dimension')
        ax.set_zlabel('Average Computation Time (s)')
    plt.savefig(f'plots/cpu-by-matrixdim-time-avg.png')
    plt.close()


def plot_3d_standard_dev():
    """ Plot CPU count by Matrix Dimension by Standard Deviation of Time in 3D (One plot) """
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_title('Computation Time AVG v. CPU Count v. Matrix Dimension')
    cpu_counts = [0.25, 0.5, 1.0]
    matrix_dims = [1000, 1500, 2000, 2500, 3000]
    for cpu_count in cpu_counts:
        # New line for new CPU count
        std_devs_for_current_cpu_count = []
        for matrix_dim in matrix_dims:
            # let Z be average time for this CPU count and this Matrix dimension
            results = get_results_for_cpu_count(cpu_count)[matrix_dim]
            std_devs_for_current_cpu_count.append(get_standard_deviation(results))
        ax.scatter([cpu_count] * 5, matrix_dims, std_devs_for_current_cpu_count, 'gray')
        ax.set_xlabel('CPU count')
        ax.set_xticks([0.25, 0.5, 1])
        ax.set_ylabel('Matrix Dimension')
        ax.set_zlabel('Average Computation Time (s)')
    plt.savefig(f'plots/cpu-by-matrixdim-time-stddev.png')
    plt.close()


def plot_cdf_per_cpu_count_matrix_dim_combo():
    """ Plot one CDF curve per CPU Count + Matrix Dimension Combo (15 plots) """
    cpu_counts = [0.25, 0.5, 1]
    matrix_dimensions = [1000, 1500, 2000, 2500, 3000]
    for cc in cpu_counts:
        for md in matrix_dimensions:
            # one new plot per cc + md pair
            fig = plt.figure()
            ax = fig.add_subplot()
            ax.set_title(f'CDF for CPU Count {cc}, Matrix Dimension {md}')
            data = np.sort(get_results_list_from_matrix_dimension(cpu_count=cc, matrix_dimension=md))
            p = np.linspace(0, 1, len(data), endpoint=False)
            _90th_percentile = round(np.percentile(data, 90),2)
            _95th_percentile = round(np.percentile(data, 95),2)
            _99th_percentile = round(np.percentile(data, 99),2)
            plt.tight_layout()
            ax.set_xlabel('$time (s)$')
            ax.set_ylabel('$p$')
            ax.plot([_90th_percentile] * len(data), np.arange(0, 1, 1. / len(data)), label=f"90th={_90th_percentile}")
            ax.plot([_95th_percentile] * len(data), np.arange(0, 1, 1. / len(data)), label=f"95th={_95th_percentile}")
            ax.plot([_99th_percentile] * len(data), np.arange(0, 1, 1. / len(data)), label=f"99th={_99th_percentile}")
            ax.plot(data, p)
            plt.legend()
            plt.savefig(f'plots/cdf-cc-{cc}-md-{md}.png')
            plt.close()

if __name__ == "__main__":
    plot_3d_avg() # 1 plot
    plot_3d_standard_dev() # 1 plot
    plot_cdf_per_matrix_dimension()  # 5 plots
    plot_cdf_per_cpu_count_matrix_dim_combo() # 15 plots