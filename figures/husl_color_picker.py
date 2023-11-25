# picks a red, green, cyan, and blue from a husl color wheel

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colors

N = 10000

cmap = colors.LinearSegmentedColormap.from_list(
    name="huslmap",
    colors=sns.husl_palette(
        n_colors=N,
        s=1,
        l=0.5,
    ),
    N=N
)

fig, ax = plt.subplots(figsize=(6, 1))
fig.subplots_adjust(bottom=0.5)

plt.imshow(np.linspace(0, 100, 361)[None, :], aspect='auto', cmap=cmap)

plt.show()

# get the red, as defined by solving for the color where hue is 0
# Note that cmap does not start exactly at red, so cmap(0) does not work - needs to be solved for.
# Also, saturation and lightness are not 1, so you genuinely need to convert to HSL space and then solve for hue == 0.

from scipy import optimize


@np.vectorize
def get_hue(x):
    h, s, l = colors.rgb_to_hsv(cmap(x)[:3])
    return h


@np.vectorize
def get_cmap_input_from_hue(hue):
    def objective(x):
        hue_raw = get_hue(x)
        return np.linalg.norm(
            np.array([
                np.cos(2 * np.pi * hue_raw) - np.cos(2 * np.pi * hue),
                np.sin(2 * np.pi * hue_raw) - np.sin(2 * np.pi * hue),
            ])
        ) ** 2

    res = optimize.minimize_scalar(
        fun=objective,
        bounds=(0, 1),
    )
    return res.x


x_colors = get_cmap_input_from_hue([
    # 0.04,
    # 0.35,
    # 0.50,
    # 0.65,
    0,
    0.25,
    0.50,
    0.60,
])

cmap_colors = cmap(x_colors)

hex_colors = [colors.to_hex(c).upper() for c in cmap_colors]

for i, hc in enumerate(hex_colors):
    print(f"{i:2d}: {hc}")


fig, ax = plt.subplots(1, len(cmap_colors), figsize=(len(cmap_colors), 1.1))
for i, c in enumerate(cmap_colors):
    ax[i].imshow(np.ones((1, 1, 4)) * c)
    ax[i].axis('off')
    # ax[i].set_title(f"{i}")
    ax[i].set_title(f"{hex_colors[i]}")
plt.show()
