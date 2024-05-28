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

x_plot = np.linspace(x.min(), x.max(), 500)

fit1= asb.FittedModel(
    model=lambda x, p: p["m"] * x + p["b"],
    x_data=x,
    y_data=y,
    parameter_guesses={"m": 0, "b": 0},
)
plt.plot(
    x_plot, fit1(x_plot),
    "--",
    alpha=0.5,
    label="Naive Linear Fit"
)

fit3= asb.FittedModel(
    model=lambda x, p: p["a"] * x ** 3 + p["b"] * x ** 2 + p["c"] * x + p["d"],
    x_data=x,
    y_data=y,
    parameter_guesses={"a": 0, "b": 0, "c": 0, "d": 0},
)

plt.plot(
    x_plot, fit3(x_plot),
    "-.",
    alpha=0.5,
    label="Naive Cubic Fit"
)

# p.plot_with_bootstrapped_uncertainty(
#     x, y,
#     x_stdev=None,
#     y_stdev=tsuq.estimate_noise_standard_deviation(y[np.argsort(x)]),
#     ci=[0.75, 0.95],
#     color="coral",
#     n_bootstraps=100,
# )
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
    savefig="power_polar_naive.pdf"
)