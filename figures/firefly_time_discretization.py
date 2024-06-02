import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p

fig, ax = plt.subplots(
    figsize=(5,3)
)

### Time number line
ax.plot([0, 1.1], [0, 0], color='k', linewidth=3, zorder=4)
ax.plot([0, 0], [-0.1, 0.1], color='k', linewidth=3, zorder=4)
ax.arrow(0, 0, 1.1, 0, head_width=0.05, head_length=0.1, fc='k', ec='k', zorder=4)
ax.text(0.5, -0.1, "Time $t$", ha='center', va='center', fontsize=16)

switch = 0.3

phases = {
    "Dash" : [
        np.cosspace(0, switch, 15),
        "darkred"
    ],
    "Glide": [
        np.cosspace(switch, 1, 20),
        "darkblue"
    ]
}
y_vals = {
    k: 0.10 + 0.05 * (len(phases) - i)
    for i, k in enumerate(phases.keys())
}

for phase_name, (phase, color) in phases.items():
    y = y_vals[phase_name]

    ax.plot(phase, y * np.ones_like(phase), ".-", color=color, linewidth=2)
    ax.text(
        np.mean(phase),
        0.01 + y,
        f"{phase_name} phase",
        ha='center',
        va='bottom',
        color=color
    )

y_top = max(y_vals.values()) + 0.1

# Start
ax.plot([0, 0], [-0.05, y_top], "--", color='gray', linewidth=1)
ax.text(0, y_top + 0.01, "$t=0$\n(fixed)", ha='center', va='bottom', color='gray')

# Burnout
ax.plot([switch, switch], [-0.05, y_top], "--", color='gray', linewidth=1)
ax.text(switch, y_top + 0.01, "$t_\\mathrm{burnout}$", ha='center', va='bottom', color='gray')

# End
ax.plot([1, 1], [-0.05, y_top], "--", color='gray', linewidth=1)
ax.text(1, y_top + 0.01, "$t_\\mathrm{end}$", ha='center', va='bottom', color='gray')

ax.axis("off")
p.equal()
p.show_plot(
    savefig="firefly_time_discretization.svg"
)
