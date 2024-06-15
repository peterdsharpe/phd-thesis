import aerosandbox as asb
import aerosandbox.numpy as np


fuselage_diameter = 61.62e-3
fuselage_length = 460e-3
fuselage_TE_diameter = 0.020
nose_length = 70.76e-3
boattail_length = (84.92e-3 + 106.22e-3) / 2

x_nose = nose_length
x_boattail = fuselage_length - boattail_length

def fuselage_radius(x_g: float) -> float:
    return fuselage_diameter / 2 * np.where(
        x_g < nose_length,
        np.abs(1 - (1 - x_g / nose_length) ** 2 + 1e-16) ** 0.5,
        np.where(
            x_g < x_boattail,
            1,
            1 - (1 - (fuselage_TE_diameter / fuselage_diameter)) * (
                    (x_g - x_boattail) / (boattail_length))
        )
    )

fuse_x = np.concatenate((
    np.sinspace(0, x_nose, 15),
    np.linspace(x_nose, x_boattail, 15)[1:],
    np.linspace(x_boattail, fuselage_length, 15)[1:]
))
fuse_r = fuselage_radius(x_g=fuse_x)

fuse = asb.Fuselage(
    xsecs=[
        asb.FuselageXSec(
            xyz_c=[fuse_x[i], 0, 0],
            radius=fuse_r[i]
        )
        for i in range(np.length(fuse_x))
    ],
    analysis_specific_options={
        asb.AeroBuildup: dict(
            nose_fineness_ratio=nose_length / fuselage_diameter
        )
    }
)


wing_airfoil = asb.Airfoil("tasopt-c090")

wing_root_chord = 70e-3
wing_taper_ratio = 20e-3 / 70e-3
wing_tip_chord = wing_root_chord * wing_taper_ratio

wing_span = 480e-3
wing_x_le = 203.02e-3

wing_incidence = 0

wing = asb.Wing(
    symmetric=True,
    xsecs=[
        asb.WingXSec(
            chord=wing_root_chord,
            airfoil=wing_airfoil,
            twist=wing_incidence,
        ),
        asb.WingXSec(
            xyz_le=[0, 35.09e-3, 0],
            chord=wing_root_chord,
            airfoil=wing_airfoil,
            twist=wing_incidence,
        ),
        asb.WingXSec(
            xyz_le=[wing_root_chord - wing_tip_chord, wing_span / 2, 0],
            chord=wing_tip_chord,
            airfoil=wing_airfoil,
            twist=wing_incidence
        )
    ]
).translate([
    wing_x_le,
    0,
    30.82e-3
])

tail_airfoil = asb.Airfoil("naca0008")

tail_root_chord = 72.57e-3
tail_taper_ratio = 35e-3 / 72.57e-3
tail_tip_chord = tail_root_chord * tail_taper_ratio
tail_sweep = (87.89-58) / 2
tail_incidence = 0

tail_root_radial_position = (10.80e-3 + 26.26e-3) / 2
tail_tip_radial_position = (73.93e-3 + 81.21e-3 + 66.58e-3 + 71.65e-3) / 4
tail_dihedral = 45
tail_half_span = tail_tip_radial_position - tail_root_radial_position

tail_up = asb.Wing(
    symmetric=True,
    xsecs=[
        asb.WingXSec(
            xyz_le=[
                0,
                np.cosd(tail_dihedral) * tail_root_radial_position,
                np.sind(tail_dihedral) * tail_root_radial_position
            ],
            chord=tail_root_chord,
            airfoil=tail_airfoil,
        ),
        asb.WingXSec(
            xyz_le=[
                np.tand(tail_sweep) * tail_half_span + 0.5 * (tail_root_chord - tail_tip_chord),
                np.cosd(tail_dihedral) * tail_tip_radial_position,
                np.sind(tail_dihedral) * tail_tip_radial_position
            ],
            chord=tail_tip_chord,
            airfoil=tail_airfoil
        )
    ]
).translate([
    385.30e-3,
    0,
    0
])

import copy

tail_down = copy.deepcopy(tail_up)
for i, xsec in enumerate(tail_down.xsecs):
    x = xsec.xyz_le[0]
    y = xsec.xyz_le[1]
    z = xsec.xyz_le[2]
    tail_down.xsecs[i].xyz_le = np.array([x, y, -z])
    tail_down.xsecs[i].twist = tail_incidence

airplane = asb.Airplane(
    name="Firefly",
    wings=[
        wing.subdivide_sections(10),
        tail_up.subdivide_sections(10),
        tail_down.subdivide_sections(10)
    ],
    fuselages=[
        fuse.subdivide_sections(5)
    ],
    xyz_ref=[
        wing_x_le + 0.0 * wing_root_chord,
        0,
        0,
    ]
)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import aerosandbox.tools.pretty_plots as p

    airplane.draw_three_view(show=False)
    p.show_plot(savefig="firefly.png", dpi=600)



    # fig, ax = plt.subplots()
    # airplane.draw(
    #     backend="matplotlib",
    #     use_preset_view_angle="left_isometric",
    #     set_axis_visibility=False,
    #     show=False
    # )
    # p.show_plot(savefig="firefly.pdf")