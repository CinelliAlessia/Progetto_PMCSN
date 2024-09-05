import os

from matplotlib import pyplot as plt
from Simulation import truncate_lognormal


# Esempio di utilizzo:
def plot_truncated_normal(mu, sigma, inf, sup, n=1000):
    """Genera un grafico della distribuzione di probabilità usando la funzione truncate_normal."""
    samples = [truncate_lognormal(mu, sigma, inf, sup) for _ in range(n)]

    plt.figure(figsize=(10, 6))
    plt.hist(samples, bins=50, density=True, alpha=0.6, color='g', label='Campioni')

    plt.title(f'Distribuzione Normale Troncata (media={mu}, sigma={sigma})')
    plt.xlabel('Valori')
    plt.ylabel('Densità di probabilità')
    plt.legend()
    plt.grid(True)
    plt.show()


# Esempio di utilizzo con n = 1000
plot_truncated_normal(mu=15, sigma=3, inf=1e-6, sup=float('inf'), n=1000)


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


