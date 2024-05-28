from common import *
from results_solver import get_results

b = get_results(bootstrap_resample=False)

bootstrap = []
N_runs = 3000
counter = tqdm(range(N_runs))
while len(bootstrap) < N_runs:
    run = get_results(bootstrap_resample=True)
    if run is not None:
        bootstrap.append(run)
        counter.update()
    else:
        print("Invalid run! Trying again...")

########## Plot Energy Polar
fig, ax = plt.subplots(figsize=(7, 4))


def jitter(data):
    iqr = np.percentile(data, 75) - np.percentile(data, 25)
    return data + np.random.uniform(-1, 1, len(data)) * iqr * 0.04


##### Plot data
airspeed_data = b["f"](b["airspeed"](b["t"]))
residuals = b["sol"](b["residuals"])

plt.plot(
    jitter(
        airspeed_data
    ),
    jitter(
        b["steady_state_required_electrical_power"](airspeed_data) + residuals
    ),
    ".",
    color="k",
    alpha=(1 - (1 - 0.5) ** (1 / (len(airspeed_data) / 250))),
    markersize=3,
)
plt.plot(
    [],
    [],
    ".k",
    markersize=3,
    label="Corrected Data",
)

# ##### Plot fit

color = "teal"

plot_speeds = np.linspace(6, 20, 1000)
plot_powers = np.array([
    r["steady_state_required_electrical_power"](plot_speeds)
    for r in bootstrap
])

def plot_with_bootstrapped_uncertainty(
        x_fit, y_bootstrap_fits,
        flip_xy=False,
):

    ### Plot the best-estimator line

    args = [x_fit, np.nanquantile(y_bootstrap_fits, q=0.5, axis=0)]

    line, = plt.plot(
        *(args if not flip_xy else args[::-1]),
        color=color,
        label="Best Estimate",
        zorder=2,
        alpha=0.9,
    )

    ci = np.array([0.75, 0.95])
    ci_to_alpha_mapping = lambda ci: 0.8 * (1 - ci) ** 0.4

    ### Using the method of equal-tails confidence intervals
    lower_quantiles = np.concatenate([[0.5], (1 - ci) / 2])
    upper_quantiles = np.concatenate([[0.5], 1 - (1 - ci) / 2])

    lower_ci = np.nanquantile(y_bootstrap_fits, q=lower_quantiles, axis=0)
    upper_ci = np.nanquantile(y_bootstrap_fits, q=upper_quantiles, axis=0)

    for i, ci_val in enumerate(ci):
        settings = dict(
            color=color,
            alpha=ci_to_alpha_mapping(ci_val),
            linewidth=0,
            zorder=1.5
        )
        fill_between = plt.fill_between if not flip_xy else plt.fill_betweenx
        fill_between(
            x_fit,
            lower_ci[i],
            lower_ci[i + 1],
            label=f"{ci_val:.0%} CI",
            **settings
        )
        fill_between(
            x_fit,
            upper_ci[i],
            upper_ci[i + 1],
            **settings
        )

plot_with_bootstrapped_uncertainty(plot_speeds, plot_powers)

plt.xlim(plot_speeds.min(), plot_speeds.max())
plt.ylim(-5, 500)
p.set_ticks(1, 0.25, 100, 25)
plt.legend(
    loc="lower right"
)
p.show_plot(
    xlabel="Airspeed [m/s]",
    ylabel="Electrical\nPower Consumed\n[Watts]",
    legend=False,
    savefig=["power_curve_with_physics.pdf", "power_curve_with_physics.png"]
)

########## Plot L/D Polar
fig, ax = plt.subplots(figsize=(7, 4))

##### Plot data
QS_plot = (0.5 * 1.225 * airspeed_data ** 2) * b["S"]

CL_plot = b["mass_total"] * 9.81 / QS_plot
CD_plot = b["steady_state_CD"](CL_plot) + residuals / QS_plot / airspeed_data

plt.plot(
    jitter(CD_plot),
    jitter(CL_plot),
    ".",
    color="k",
    alpha=(1 - (1 - 0.5) ** (1 / (len(airspeed_data) / 250))),
    markersize=3,
)
plt.plot(
    [],
    [],
    ".k",
    markersize=3,
    label="Corrected Data",
)

##### Plot fit
CL_plot = np.linspace(0, 1.8, 1000)
CD_plot = np.array([
    r["steady_state_CD"](CL_plot)
    for r in bootstrap
])

plot_with_bootstrapped_uncertainty(CL_plot, CD_plot, flip_xy=True)

LD_max = np.max(CL_plot / CD_plot)

plt.xlim(0, 0.2)
plt.ylim(CL_plot.min(), CL_plot.max())

p.set_ticks(0.02, 0.005, 0.2, 0.05)

plt.legend(
    loc="lower right",
)
p.show_plot(
    # "Solar Seaplane Aerodynamic Polar",
    "",
    "Drag Coefficient $C_D$",
    "Lift\nCoefficient\n$C_L$",
    legend=False,
    savefig=["aerodynamic_polar_with_physics.pdf", "aerodynamic_polar_with_physics.png"]
)

########## Plot Propeller Efficiency Polar
fig, ax = plt.subplots(figsize=(7, 4))

##### Plot data
mask = b["f"](b["current"](b["t"])) > 1

prop_efficiency_plot = (
                               b["propulsion_air_power"] - residuals
                       ) / (b["f"](b["voltage"](b["t"])) * b["f"](b["current"](b["t"])) - b["avionics_power"])

plt.plot(
    jitter(b["propto_J"][mask]),
    jitter(prop_efficiency_plot[mask]),
    ".",
    color="k",
    alpha=(1 - (1 - 0.5) ** (1 / (len(b["t"]) / 250))),
    markersize=3,
)
plt.plot(
    [],
    [],
    ".k",
    markersize=3,
    label="Corrected Data",
)

##### Plot fit
propto_J_plot = np.linspace(
    0, b["propto_J"][mask].max(), 1000
)

# prop_efficiency_plot = b["steady_state_prop_efficiency"](propto_J_plot)
prop_efficiency_plot = [
    r["steady_state_prop_efficiency"](propto_J_plot)
    for r in bootstrap
]

plot_with_bootstrapped_uncertainty(propto_J_plot, prop_efficiency_plot)

# _line, = plt.plot(
#     propto_J_plot,
#     prop_efficiency_plot,
#     linewidth=2.5,
#     color=p.adjust_lightness("red", 1.2),
#     alpha=0.75,
#     zorder=4,
#     label="Model Fit (physics-informed; $L_1$ norm)",
# )

# plt.xlim(0, b["propto_J"][mask].max())
plt.xlim(0, 2)
plt.ylim(bottom=0, top=1)
#
p.set_ticks(0.5, 0.1, 0.2, 0.05)

from matplotlib import ticker

ax.yaxis.set_major_formatter(ticker.PercentFormatter(1.0, decimals=0))

plt.legend(
    # loc="lower right",
)
p.show_plot(
    # "Solar Seaplane Propulsion Polar",
    "",
    r"$\frac{\rm Airspeed\ [m/s]}{(\rm Current\ [Amps])^{1/3}}$, proportional to advance ratio $J$",
    # "$V\\ /\\ (\\rm current)^{1/3}$, proportional to advance ratio $J$",
    "Propulsive\nEfficiency $\\eta_p$",
    legend=False,
    savefig=["propeller_polar_with_physics.pdf", "propeller_polar_with_physics.png"]
)
