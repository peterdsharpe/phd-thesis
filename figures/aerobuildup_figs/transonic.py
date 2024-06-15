import aerosandbox as asb
import aerosandbox.numpy as np
from firefly import airplane
from aerosandbox.tools.code_benchmarking import time_function

atmo = asb.Atmosphere(altitude=10000)

Mach, Alpha = np.meshgrid(np.linspace(1e-3, 1.2, 300), np.linspace(-15, 15, 300))

op_point = asb.OperatingPoint(
    velocity=Mach.flatten() * atmo.speed_of_sound(),
    alpha=Alpha.flatten(),
)

ab = asb.AeroBuildup(
    airplane=airplane,
    op_point=op_point,
)

aero = ab.run()

import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p

fig, ax = plt.subplots(1, 2, figsize=(8, 5))
ax_f = ax.flatten()

colorbar_kwargs = dict(
    orientation="horizontal",
    pad=0.18,
)

plt.sca(ax_f[0])
p.contour(
    Mach, Alpha, aero["CL"].reshape(Alpha.shape),
    colorbar_label="Lift Coefficient $C_L$ [-]",
    linelabels_format=lambda x: f"{x:.2f}",
    linelabels_fontsize=7,
    cmap="RdBu",
    alpha=0.6,
    colorbar_kwargs=colorbar_kwargs
)
plt.clim(*np.array([-1, 1]) * np.max(np.abs(aero["CL"])))
plt.title("Lift Coefficient")

plt.sca(ax_f[1])
p.contour(
    Mach, Alpha, aero["CD"].reshape(Alpha.shape),
    colorbar_label="Drag Coefficient $C_D$ [-]",
    linelabels_format=lambda x: f"{x:.2f}",
    linelabels_fontsize=7,
    z_log_scale=True,
    cmap="YlOrRd",
    alpha=0.6,
    colorbar_kwargs=colorbar_kwargs
)
plt.title("Drag Coefficient")

# plt.sca(ax_f[2])
# downsample = 10
# l_w, m_w, n_w = op_point.convert_axes(
#     aero["l_b"], aero["m_b"], aero["n_b"],
#     from_axes="body",
#     to_axes="wind"
# )
# dBeta = -n_w.reshape(Alpha.shape)
# dAlpha = m_w.reshape(Alpha.shape)
#
# Beta_l = Beta[::downsample, ::downsample]
# Alpha_l = Alpha[::downsample, ::downsample]
# dBeta_l = dBeta[::downsample, ::downsample]
# dAlpha_l = dAlpha[::downsample, ::downsample]
#
# plt.quiver(
#     Beta_l, Alpha_l, dBeta_l, dAlpha_l,
#     np.arctan2(dBeta_l, dAlpha_l),
#     cmap=p.sns.color_palette("husl", as_cmap=True),
#     # scale=1,
#     zorder=4,
#     width=0.01,
# )
# plt.streamplot(
#     Beta, Alpha, dBeta, dAlpha,
#     density=2,
#     color=(0, 0, 0, 0.2),
#     arrowsize=0,
#     linewidth=1,
#     # alpha=0.5,
#     # arrowstyle="-"
# )
# plt.title("Quasi-Steady \"Moment Flow\" Diagram:\n$(C_n, C_m)$ as a function of $(\\beta, \\alpha)$")
#
#
# plt.sca(ax_f[3])
# p.contour(
#     Beta, Alpha, (aero["CL"] / aero["CD"]).reshape(Alpha.shape),
#     colorbar_label="Aerodynamic Efficiency $L/D$ [-]",
#     linelabels_format=lambda x: f"{x:.1f}",
#     linelabels_fontsize=7,
#     linelabels=False,
#     cmap="RdBu",
#     alpha=0.6,
#     colorbar_kwargs=colorbar_kwargs
# )
# plt.title("Lift-to-Drag Ratio")


for ax_i in ax_f:
    plt.sca(ax_i)
    plt.xlabel(r"Mach number $M_\infty$ [-]")
    plt.ylabel(r"Angle of Attack $\alpha$ [deg]")
    plt.xlim(left=0)
    # p.set_ticks(30, 5, 30, 5)
    # p.equal()

# p.show_plot(
#     set_ticks=False,
#     tight_layout=False
# )

plt.tight_layout(
    pad=0,
    w_pad=4,
    h_pad=2,
)

# plt.show()
p.show_plot(
    # set_ticks=False,
    tight_layout=False,
    rotate_axis_labels=False,
    savefig="transonic.pdf"
)

