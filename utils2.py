import csv
import numpy as np
import os
import matplotlib.pyplot as plt
from libs.rvms import idfStudent


def confidence_interval(alpha, n, l) -> float:
    sigma = np.std(l, ddof=1)
    if n > 1:
        t = idfStudent(n - 1, 1 - alpha / 2)
        return (t * sigma) / np.sqrt(n - 1)
    else:
        return 0.0


def batch_means(data, batch_size):
    n = len(data)
    num_batches = n // batch_size
    batch_means = []

    for i in range(num_batches):
        batch = data[i * batch_size: (i + 1) * batch_size]
        batch_means.append(np.mean(batch))

    return batch_means


def write_on_csv(input_list):
    with open("acs.dat", mode='w', newline='') as file:
        writer = csv.writer(file)
        for element in input_list:
            writer.writerow([element])


def append_on_csv(input_data, file):
    # response_time_mean = event_list.completed[server_index_completed].event_time - event.event_time
    #append_on_csv(response_time_mean, CSV_RESPONSE_TIME)

    with open(file, mode = 'a', newline= '') as f:
        writer = csv.writer(f)
        writer.writerow(input_data)


def cumulative_mean(data):
    # Computes the cumulative mean for an array of data
    return np.cumsum(data) / np.arange(1, len(data) + 1)


def plot_cumulative_means(cumulative_means, stationary_value, ylabel, title, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_means, label=ylabel)
    plt.xlabel('Batch Number')

    # Plot a horizontal line for the stationary value
    plt.axhline(stationary_value, color='orange', label='Mean of means')

    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # Create folder 'plots' if it doesn't exist
    if not os.path.exists('plots'):
        os.makedirs('plots')

    # Save plots
    plt.savefig(f'plots/{filename}.png')
    plt.close()