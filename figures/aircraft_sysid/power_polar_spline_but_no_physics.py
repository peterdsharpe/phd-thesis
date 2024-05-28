from common import *

_, airspeed = simple_read("airspeed")
_, baro_alt = simple_read("baro_alt")
_, voltage = simple_read("voltage")
_, current = simple_read("current")

from aerosandbox.tools.statistics import time_series_uncertainty_quantification as tsuq

fig, ax = plt.subplots(figsize=(7,4))

x = airspeed
y = voltage * current

plt.plot(
    x, y,
    ".k",
    markersize=5,
    markeredgewidth=0,
    alpha=0.25,
    label="Raw Data"
)

p.plot_with_bootstrapped_uncertainty(
    x, y,
    x_stdev=None,
    y_stdev=tsuq.estimate_noise_standard_deviation(y[np.argsort(x)]),
    ci=[0.75, 0.95],
    color="orangered",
    n_bootstraps=100000,
    ci_to_alpha_mapping=lambda ci: 0.8 *(1 - ci) ** 0.4,
    draw_data=False,
)
plt.xlim(x.min(), x.max())
plt.ylim(-10, 800)
p.set_ticks(1, 0.25, 100, 25)
plt.legend(
    loc="lower right"
)
p.show_plot(
    xlabel="Airspeed [m/s]",
    ylabel="Electrical\nPower Consumed\n[Watts]",
    # title="Raw Data",
    legend=False,
    # dpi=300
    savefig="power_polar_spline_but_no_physics.pdf"
)