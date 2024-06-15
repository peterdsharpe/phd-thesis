import aerosandbox as asb
import aerosandbox.numpy as np
from firefly import airplane
from aerosandbox.tools.code_benchmarking import time_function

atmo = asb.Atmosphere(altitude=0)

alpha = np.linspace(-20, 20, 300)

op_point = asb.OperatingPoint(
    velocity=0.15 * atmo.speed_of_sound(),
    alpha=alpha,
)

ab = asb.AeroBuildup(
    airplane=airplane,
    op_point=op_point,
)

aero = ab.run()

import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p

fig, ax = plt.subplots(2, 2, figsize=(6.5,4.5))
# fig, ax = plt.subplots(4, 1, figsize=(6,4), sharex=True)
ax_f = ax.flatten()


plt.sca(ax_f[0])
plt.plot(alpha, aero["CL"])
plt.xlabel(r"Angle of attack $\alpha$ [deg]")
plt.ylabel(r"$C_L$")
plt.title("Lift Coefficient")
p.set_ticks(5, 1, 0.5, 0.1)

plt.sca(ax_f[1])
plt.plot(alpha, aero["CD"])
plt.xlabel(r"Angle of attack $\alpha$ [deg]")
plt.ylabel(r"$C_D$")
plt.title("Drag Coefficient")
p.set_ticks(5, 1, 0.05, 0.01)
plt.ylim(bottom=0)

plt.sca(ax_f[2])
plt.plot(alpha, aero["Cm"])
plt.xlabel(r"Angle of attack $\alpha$ [deg]")
plt.ylabel(r"$C_m$")
plt.title("Pitching Moment Coeff.")
p.set_ticks(5, 1, 0.5, 0.1)

plt.sca(ax_f[3])
plt.plot(alpha, aero["CL"] / aero["CD"])
plt.xlabel(r"Angle of attack $\alpha$ [deg]")
plt.ylabel(r"$C_L/C_D$")
plt.title("Aerodynamic Efficiency")
p.set_ticks(5, 1, 10, 2)

p.show_plot(
    # "`asb.AeroBuildup` Aircraft Aerodynamics",
    savefig="polars.pdf"
)