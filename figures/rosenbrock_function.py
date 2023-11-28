### Don't worry about this code block; this is just here to visualize the Rosenbrock function.
from aerosandbox.tools.pretty_plots import plt, show_plot, contour, mpl, equal
import aerosandbox.numpy as np


def rosenbrock(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p

fig, ax = plt.subplots(figsize=(3, 2.5), dpi=200)
X, Y = np.meshgrid(np.linspace(-2, 2, 300), np.linspace(-1, 3, 300))
Z = rosenbrock(X, Y)
_, _, cbar = contour(X, Y, Z,
                     levels=np.geomspace(1e-2, Z.max(), 20),
                     # colorbar=False,
                     z_log_scale=True,
                     linelabels=False,
                     linelabels_fontsize=8,
                     cmap=plt.cm.get_cmap("viridis"),
                     zorder=3
                     )
plt.clim(vmin=1e-1)
equal()
p.set_ticks(1, 1, 1, 1)
show_plot("", "$x_i$", "$x_{i+1}$", set_ticks=False, savefig="rosenbrock_function.pdf")

