from common import *

t, a = simple_read("airspeed")

xlim = (60, 90)
mask = (t > xlim[0] - 10) & (t < xlim[1] + 10)

t=t[mask]
a=a[mask]

assumed_stdev = [
    0,
    0.8
]
names = [
    "Overfitted",
    "Underfitted"
]

estimators = [
    interpolate.UnivariateSpline(
        x=t,
        y=a,
        k=5,
        w=1 / s * np.ones_like(a) if s > 0 else None,
        s=len(a) if s > 0 else 0,
        check_finite=True,
        ext='raise'
    )
    for s in assumed_stdev
]

t_plot = np.linspace(t[0], t[-1], 5000)

fig, ax = plt.subplots(
    1, 3, figsize=(7, 6),
    sharey=True
)

for axi in ax:
    plt.sca(axi)
    plt.plot(
        t, a,
        ".k",
        label="Raw Data",
        alpha=0.5,
        markersize=6,
        markeredgewidth=0
    )
    plt.xlim(*xlim)
    plt.ylim(6, 13)
    plt.xlabel("Time after Takeoff [sec]")
    p.set_ticks(10, 2, 1, 0.2)

plt.sca(ax[0])
plt.plot(
    t_plot,
    estimators[0](t_plot),
    label="Estimated Truth",
    alpha=0.9,
    color="tomato"
)
plt.title("Overfitted")
plt.ylabel("Airspeed [m/s]")

plt.sca(ax[1])
p.plot_with_bootstrapped_uncertainty(
    t, a,
    n_bootstraps=10000,
    n_fit_points=500,
    draw_data=False,
    line_alpha=0.9,
    ci_to_alpha_mapping=lambda ci: 0.4,
    color="teal",
)
plt.title("Our Method")
plt.legend()

plt.sca(ax[2])
plt.plot(
    t_plot,
    estimators[1](t_plot),
    label="Estimated Truth",
    alpha=0.9,
    color="darkviolet"
)
plt.title("Underfitted")

plt.suptitle(f"One Dataset, Many Possible Interpretations")

p.show_plot(
    legend=False,
    # dpi=300,
    savefig="under_over_fitting.pdf"
)