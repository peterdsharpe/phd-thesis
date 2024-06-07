import aerosandbox as asb
import aerosandbox.numpy as np

wing_airfoil = asb.Airfoil("sd7037")
tail_airfoil = asb.Airfoil("naca0010")

### Define the 3D geometry you want to analyze/optimize.
# Here, all distances are in meters and all angles are in degrees.
airplane = asb.Airplane(
    name="Peter's Glider",
    xyz_ref=[0, 0, 0],  # CG location
    wings=[
        asb.Wing(
            name="Main Wing",
            symmetric=True,  # Should this wing be mirrored across the XZ plane?
            xsecs=[  # The wing's cross ("X") sections
                asb.WingXSec(  # Root
                    xyz_le=[0, 0, 0],  # Coordinates of the XSec's leading edge, relative to the wing's leading edge.
                    chord=0.18,
                    twist=2,  # degrees
                    airfoil=wing_airfoil,  # Airfoils are blended between a given XSec and the next one.
                ),
                asb.WingXSec(  # Mid
                    xyz_le=[0.01, 0.5, 0],
                    chord=0.16,
                    twist=0,
                    airfoil=wing_airfoil,
                ),
                asb.WingXSec(  # Tip
                    xyz_le=[0.08, 1, 0.1],
                    chord=0.08,
                    twist=-2,
                    airfoil=wing_airfoil,
                ),
            ]
        ),
        asb.Wing(
            name="Horizontal Stabilizer",
            symmetric=True,
            xsecs=[
                asb.WingXSec(  # root
                    xyz_le=[0, 0, 0],
                    chord=0.1,
                    twist=-10,
                    airfoil=tail_airfoil,
                ),
                asb.WingXSec(  # tip
                    xyz_le=[0.02, 0.17, 0],
                    chord=0.08,
                    twist=-10,
                    airfoil=tail_airfoil
                )
            ]
        ).translate([0.6, 0, 0.06]),
        asb.Wing(
            name="Vertical Stabilizer",
            symmetric=False,
            xsecs=[
                asb.WingXSec(
                    xyz_le=[0, 0, 0],
                    chord=0.1,
                    twist=0,
                    airfoil=tail_airfoil,
                ),
                asb.WingXSec(
                    xyz_le=[0.04, 0, 0.15],
                    chord=0.06,
                    twist=0,
                    airfoil=tail_airfoil
                )
            ]
        ).translate([0.6, 0, 0.07])
    ],
    fuselages=[
        asb.Fuselage(
            name="Fuselage",
            xsecs=[
                asb.FuselageXSec(
                    xyz_c=[0.8 * xi - 0.1, 0, 0.1 * xi - 0.03],
                    radius=0.6 * asb.Airfoil("dae51").local_thickness(x_over_c=xi)
                )
                for xi in np.sinspace(0, 1, 10)
            ]
        )
    ]
)

import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# fig, ax = p.figure3d(1, 3, figsize=(7, 4))
#
#
# airplane.draw_wireframe(
#     ax=ax[0],
#     show=False,
# )
# # shift zlim so the airplane is at the very top, but keep the aspect ratio
# points, faces = airplane.mesh_body()
# zmax = np.max(points, axis=0)[2]
# ax[0].set_zlim(zmax - np.diff(ax[0].get_zlim())[0], zmax)
#
#
# airplane.wings = [
#     w.subdivide_sections(12, spacing_function=np.cosspace)
#     for w in airplane.wings
# ]
# airplane.fuselages = [
#     f.subdivide_sections(4)
#     for f in airplane.fuselages
# ]
#
# points, faces = airplane.mesh_body(
#     method='quad',
#     thin_wings=True
# )
# mesh = Poly3DCollection([points[face] for face in faces], edgecolor='k', linewidths=0.1, facecolors='w', alpha=1)
# ax[1].add_collection3d(mesh)
#
# points, faces = airplane.mesh_body(
#     method='quad',
# )
# mesh = Poly3DCollection([points[face] for face in faces], edgecolor='k', linewidths=0.1, facecolors='w', alpha=0.8)
# ax[2].add_collection3d(mesh)
# # title
# ax[0].set_title("Original")
#
# for a in ax:
#     a.set_xlim(ax[0].get_xlim())
#     a.set_ylim(ax[0].get_ylim())
#     a.set_zlim(ax[0].get_zlim())
#     a.axis('off')
# plt.tight_layout(
#     rect=[-0.2, -0.5, 1.2, 0.95],
#     w_pad=-15,
#     h_pad=-15,
# )
#
# plt.show()

fig, ax0 = p.figure3d()
airplane.draw_wireframe(
    ax=ax0,
    show=False,
)
ax0.axis('off')
p.show_plot(savefig="geometry_concept.pdf")

airplane.wings = [
    w.subdivide_sections(12, spacing_function=np.cosspace)
    for w in airplane.wings
]
airplane.fuselages = [
    f.subdivide_sections(4)
    for f in airplane.fuselages
]


fig, ax = p.figure3d()
airplane_no_fuse = airplane.deepcopy()
airplane_no_fuse.fuselages = []
points, faces = airplane_no_fuse.mesh_body(
    method='quad',
    thin_wings=True
)
mesh = Poly3DCollection([points[face] for face in faces], edgecolor='k', linewidths=0.1, facecolors='w', alpha=1)
ax.add_collection3d(mesh)
ax.axis('off')
p.equal()
ax.set_xlim(ax0.get_xlim())
ax.set_ylim(ax0.get_ylim())
ax.set_zlim(ax0.get_zlim())
p.show_plot(savefig="geometry_mean_camber.pdf")


fig, ax = p.figure3d()
points, faces = airplane.mesh_body(
    method='quad',
)
mesh = Poly3DCollection([points[face] for face in faces], edgecolor='k', linewidths=0.1, facecolors='w', alpha=1)
ax.add_collection3d(mesh)
ax.axis('off')
p.equal()
ax.set_xlim(ax0.get_xlim())
ax.set_ylim(ax0.get_ylim())
ax.set_zlim(ax0.get_zlim())
p.show_plot(savefig="geometry_panel.pdf")

