from common import *

np.random.seed(0)

freq_signal = 100
freq_sample = 1000

##### Synthetic Data Generation #####
t = np.arange(0, 1, 1 / freq_sample)

true_data = np.sin(2 * np.pi * freq_signal * t)

true_noise_standard_deviation = 0.1

noise = np.random.normal(size=len(true_data)) * true_noise_standard_deviation

sensor_data = true_data + noise

import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p

fig, ax = plt.subplots()
plt.plot(t, sensor_data, ".k")
p.show_plot()

##### Noise Variance Reconstruction #####
### Note: there are a few differences between the equation above and this, to prevent overflow
from aerosandbox.tools.statistics import time_series_uncertainty_quantification as tsuq

estimated_noise_standard_deviation = tsuq.estimate_noise_standard_deviation(
    sensor_data,
    estimator_order=4
)

print("True Noise Standard Deviation:", true_noise_standard_deviation)
print("Estimated Noise Standard Deviation:", estimated_noise_standard_deviation)