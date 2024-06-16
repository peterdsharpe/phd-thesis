import aerosandbox as asb
import aerosandbox.numpy as np


def make_wing(
        span: float,
        ys_over_half_span: np.ndarray,
        chords: np.ndarray,
        twists: np.ndarray,
        offsets: np.ndarray = None,
        heave_displacements: np.ndarray = None,
        twist_displacements: np.ndarray = None,
        x_ref_over_chord: float = 0.33,
        airfoil: asb.Airfoil = asb.Airfoil("dae11"),
        color="black",
) -> asb.Wing:
    """
    Generates a wing based on a given set of per-cross-section characteristics.

    Args:

        span: Span of the wing [meters].

        ys_over_half_span: Array of the y-locations of each cross-section, normalized by half-span. Should be between 0 and 1.

        chords: Array of the chord lengths of each cross-section [meters].

        twists: Array of the twist angles of each cross-section [degrees].

        offsets: Array of the x-offsets of the leading edge of each cross-section [meters]. Defaults to -chords / 4, yielding an unswept quarter-chord.

        heave_displacements: Array of the vertical displacements of the shear center of each cross-section [meters]. Defaults to zero.

        twist_displacements: Array of the twist displacements of each cross-section [degrees], as measured about the shear center. Defaults to zero.

        x_ref_over_chord: The x-location of the shear center (i.e., torsion axis), normalized by the chord. Defaults to 0.33.

        airfoil: The airfoil to use for all cross-sections. Defaults to the DAE11.

    Returns:

        A Wing object.
    """
    if offsets is None:
        offsets = -chords / 4
    if heave_displacements is None:
        heave_displacements = np.zeros_like(ys_over_half_span)
    if twist_displacements is None:
        twist_displacements = np.zeros_like(ys_over_half_span)

    xsecs = []

    for i in range(len(ys_over_half_span)):
        xyz_le = np.array([
            -chords[i] * x_ref_over_chord,
            ys_over_half_span[i] * (span / 2),
            0
        ])
        xyz_le = np.rotation_matrix_3D(
            angle=np.radians(twists[i] + twist_displacements[i]),
            axis="y"
        ) @ xyz_le
        xyz_le += np.array([
            offsets[i] + chords[i] * x_ref_over_chord,
            0,
            heave_displacements[i]
        ])

        xsecs.append(
            asb.WingXSec(
                xyz_le=xyz_le,
                chord=chords[i],
                twist=twists[i] + twist_displacements[i],
                airfoil=airfoil,
            )
        )

    return asb.Wing(
        symmetric=True,
        xsecs=xsecs,
        color=color,
    )

import aerosandbox as asb
import aerosandbox.numpy as np

span = 10
ys_over_half_span = np.linspace(0, 1)
chords = np.linspace(2, 0.02) ** 0.5
twists = np.linspace(0, 0)
offsets = None

### Gather known-a-priori problem info
ys = ys_over_half_span * (span / 2)
EI = chords ** 3 * 20
GJ = chords ** 3 * 1

### Specify the unknowns in the context of an optimization problem
opti = asb.Opti()

u = opti.variable(init_guess=np.linspace(0, 1.5) ** 2)

theta = opti.variable(init_guess=np.linspace(0, -5))

### Make the geometry
wing = make_wing(
    span=span,
    ys_over_half_span=ys_over_half_span,
    chords=chords,
    twists=twists,
    offsets=offsets,
    heave_displacements=u,
    twist_displacements=theta,
)

### Do the aero analysis
vlm = asb.VortexLatticeMethod(
    airplane=asb.Airplane(
        name="Aerostructures Test",
        xyz_ref=[0, 0, 0],
        wings=[wing],
    ),
    op_point=asb.OperatingPoint(
        velocity=10,
        alpha=5,
    ),
    chordwise_resolution=1,
    spanwise_resolution=1,
)
aero = vlm.run()

### Do the heave structures analysis
du = opti.derivative_of(
    variable=u, with_respect_to=ys,
    derivative_init_guess=np.zeros_like(u),
)
ddu = opti.derivative_of(
    variable=du, with_respect_to=ys,
    derivative_init_guess=np.zeros_like(u),
)

opti.subject_to([  # Add the boundary conditions
    u[0] == 0,
    du[0] == 0,
    ddu[-1] == 0,
])

### Link the aerodynamic and heave analyses together
opti.constrain_derivative(
    variable=EI * ddu, with_respect_to=ys,
    derivative=np.concatenate([
        -vlm.forces_geometry[:len(ys) - 1, 2],
        0
    ]),
)

### Do the torsion structures analysis
dtheta = opti.derivative_of(
    variable=theta, with_respect_to=ys,
    derivative_init_guess=np.zeros_like(theta),
)

opti.subject_to([  # Add the boundary conditions
    theta[0] == 0,
    dtheta[-1] == 0,
])

opti.constrain_derivative(
    variable=GJ * dtheta, with_respect_to=ys,
    derivative=np.concatenate([
        -vlm.moments_geometry[:len(ys) - 1, 1],
        0
    ]),
)

### Solve the system
sol = opti.solve()

### Display output
import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p

fig, ax = plt.subplots(4, 1, sharex=True)
ax[0].plot(ys, sol(np.concatenate([
        vlm.forces_geometry[:len(ys) - 1, 2] / np.diff(ys),
        0
    ])))
ax[0].set_ylabel("Lift Force [N/m]")
ax[1].plot(ys, sol(np.concatenate([
        vlm.moments_geometry[:len(ys) - 1, 1] / np.diff(ys),
        0
    ])))
ax[1].set_ylabel("Pitching Moment [Nm/m]")

ax[2].plot(ys, sol(u))
ax[2].set_ylabel("Heave Displacement [m]")
ax[3].plot(ys, sol(theta))
ax[3].set_ylabel("Twist Displacement [deg]")

ax[3].set_xlabel("Spanwise Position $y$ [m]")

for a in ax:
    plt.sca(a)
    p.vline(
        0,
        text="Centerline\n(symmetric)" if a == ax[-1] else None,
        text_kwargs=dict(fontsize=8),
        color="gray",
        linestyle="--"
    )

p.show_plot(
    title="Spanwise Aerostructural Quantities\nat Static Aeroelastic Equilibrium",
    # xlabel="Spanwise Position [m]",
    legend=False,
    savefig="spanplot.pdf"
)

wing_deformed = make_wing(
    span=span,
    ys_over_half_span=ys_over_half_span,
    chords=chords,
    twists=twists,
    offsets=offsets,
    heave_displacements=sol(u),
    twist_displacements=sol(theta),
)
wing_deformed.color = "C0"
wing_jig = make_wing(
    span=span,
    ys_over_half_span=ys_over_half_span,
    chords=chords,
    twists=twists,
    offsets=offsets,
)
wing_jig.color="gray"
axs = wing_jig.draw_three_view(style="wireframe", show=False)
axs = wing_deformed.draw_three_view(axs = axs, style="wireframe", show=False)
plt.suptitle("Wing Displacement (Heave + Twist) at Static Aeroelastic Equilibrium")
p.show_plot(
    savefig="deformation.pdf"
)