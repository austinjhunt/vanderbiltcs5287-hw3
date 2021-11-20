import csv
import math
def get_results_list_from_matrix_dimension(cpu_count, matrix_dimension):
    d = {
        1 : '1',
        0.5 : '0p5',
        0.25 : '0p25'
    }
    filename = f'cpu{d[cpu_count]}results/{matrix_dimension}.csv'
    results = []
    with open(filename) as f:
        reader = csv.reader(f)
        for line in reader:
            time = line[1]
            results.append(float(time))
    return results

def get_standard_deviation(values):
    mean = sum(values) / len(values)
    variance = sum([((x - mean) ** 2) for x in values]) / len(values)
    return variance ** 0.5

def get_results_for_cpu_count(cpu_count):
    results = {}
    for matrixDimension in [1000, 1500, 2000, 2500, 3000]:
        results[matrixDimension] = get_results_list_from_matrix_dimension(cpu_count, matrixDimension)
    return results

def percentile_rank(all_times, current_time):
    count = 0
    for t in all_times:
        if t <= current_time:
            count += 1
    percentile_rank = 100.0 * count / len(all_times)
    return percentile_rank

def cdf(all_times, current_time):
    """ compute the fraction of the values in the all times distribution that are less than or equal to current time """
    count = 0.0
    for t in all_times:
        if t <= current_time:
            count += 1
    return count / len(all_times)

cpu_1_results = get_results_for_cpu_count(1)
cpu_0p5_results = get_results_for_cpu_count(0.5)
cpu_0p25_results = get_results_for_cpu_count(0.25)
