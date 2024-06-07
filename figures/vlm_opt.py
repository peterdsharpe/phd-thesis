import aerosandbox as asb
import aerosandbox.numpy as np

opti = asb.Opti()  # Initialize an optimization environment.

N = 16  # Spanwise resolution
y = np.sinspace(0, 1, N, reverse_spacing=True)  # Spanwise location of each cross section. Clustered near tip.
chords = opti.variable(init_guess=1 / 8, n_vars=N, lower_bound=0)  # Chord distribution
wing = asb.Wing(  # Defines the wing geometry.
    symmetric=True,
    xsecs=[
        asb.WingXSec(
            xyz_le=[
                -0.25 * chords[i],  # This keeps the quarter-chord-line straight.
                y[i],  # Our (known) span locations for each section.
                0
            ],
            chord=chords[i],
        )
        for i in range(N)
    ]
)

vlm = asb.VortexLatticeMethod(  # Compute aerodynamics using the VLM
    airplane=asb.Airplane(wings=[wing]),  # The geometry to analyze
    op_point=asb.OperatingPoint(  # Aerodynamic operating condition
        velocity=1,  # A fixed velocity; unimportant due to nondimensionalization.
        alpha=opti.variable(init_guess=5, lower_bound=0, upper_bound=30)  # Angle of attack
    ),
    spanwise_resolution=1,  # One panel per wing cross-section
)
aero = vlm.run()

opti.subject_to([
    aero["CL"] == 1,  # We want a fixed lift coefficient
    wing.area() == 0.25,  # We want a fixed wing area
])

opti.minimize(aero["CD"])
sol = opti.solve()



import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p

fig, ax = plt.subplots(figsize=(6, 3))
plt.plot(
    y,
    sol(chords),
    ".-",
    label="AeroSandbox VLM Result",
    zorder=4,
)
y_plot = np.linspace(0, 1, 500)
plt.plot(
    y_plot,
    (1 - y_plot ** 2) ** 0.5 * 4 / np.pi * 0.125,
    label="Elliptic Distribution",
)
p.vline(
    0,
    color="gray",
    text="Centerline (symmetric)",
)

p.show_plot(
    "AeroSandbox Drag Optimization using VortexLatticeMethod",
    "Spanwise location [m]",
    "Local chord [m]",
    savefig="vlm_opt_compare.pdf"
)