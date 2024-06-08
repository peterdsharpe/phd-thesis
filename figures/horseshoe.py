from aerosandbox.aerodynamics.aero_3D.singularities.uniform_strength_horseshoe_singularities import \
    calculate_induced_velocity_horseshoe
# import aerosandbox as asb
import aerosandbox.numpy as np
import numpy as np

import pyvista as pv

##### Plot grid of single vortex
domain = [
    [-2, 2]
    for _ in range(3)
]

left = [0, -1, 0]
right = [0, 1, 0]

points = np.array([
    [domain[0][-1], left[1], left[2]],
    left,
    right,
    [domain[0][-1], right[1], right[2]]
])

pv.set_plot_theme('document')
plotter = pv.Plotter()
plotter.add_lines(
    lines=points,
    color='black',
    connected=True,
    width=15
)

# generate data and put it on a pyvista block
x = np.linspace(*domain[0])
y = np.linspace(*domain[1])
z = np.linspace(*domain[2])
X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

Xf = X.flatten(order="F")
Yf = Y.flatten(order="F")
Zf = Z.flatten(order="F")

Uf, Vf, Wf = calculate_induced_velocity_horseshoe(
    x_field=Xf,
    y_field=Yf,
    z_field=Zf,
    x_left=left[0],
    y_left=left[1],
    z_left=left[2],
    x_right=right[0],
    y_right=right[1],
    z_right=right[2],
    gamma=1,
)

# make imagedata from the vector field
dx, dy, dz = x[1] - x[0], y[1] - y[0], z[1] - z[0]

mesh = pv.ImageData(
    dimensions=[l + 1 for l in X.shape],
    spacing=(dx, dy, dz),
    origin=(x[0] - dx / 2, y[0] - dy / 2, z[0] - dz / 2),
)
vel = np.stack((Uf, Vf, Wf), axis=1)
velmag = np.linalg.norm(vel, axis=1)
mesh["velocity"] = vel

slices = [mesh.slice(normal="x")]

# plotter.add_mesh(
#     slices,
#     cmap="turbo",
#     opacity=1,
#     log_scale=True,
# )

# for slice in slices:
#     slice: pv.PolyData
#     plotter.add_arrows(
#         cent=slice.cell_centers().points,
#         direction=slice["velocity"] / np.linalg.norm(slice["velocity"], axis=1, keepdims=True),
#         mag=0.1,
#         opacity=0.5
#         # factor=1,
#         # color="black",
#         # log_scale=True
#     )

mask = np.logical_and(
    velmag > 0.5,
    velmag < 1.0,
)

plotter.add_arrows(
    cent=mesh.cell_centers().points[mask],
    direction=vel[mask],
    mag=0.2,
    cmap="turbo",
    log_scale=True,
    # opacity=0.5,
    # colorbar=True,
    scalar_bar_args=dict(
        title="Velocity magnitude",
        n_labels=5,
    )
)


# streamlines, src = mesh.to_tetrahedra().streamlines(
#     vectors='velocity',
#     return_source=True,
#     # max_time=100.0,
#     # initial_step_length=0.1,
#     # terminal_speed=0.01,
#     n_points=200,
#     # source_radius=1,
# )
# plotter.add_mesh(streamlines.tube(radius=0.15))


# planes_to_plot = [
#     ("x", 0),
#     ("y", 0),
#     ("z", 0),
# ]
#
# for axis, value in planes_to_plot:
#
#
#
#
# pos = np.stack((Xf, Yf, Zf)).T
# dir = np.stack((Uf, Vf, Wf)).T
#
# dir_norm = np.reshape(np.linalg.norm(dir, axis=1), (-1, 1))
#
# dir = dir / dir_norm * dir_norm ** 0.2
#
#
# plotter.add_arrows(
#     cent=pos,
#     direction=dir,
#     mag=0.15
# )
plotter.show_grid()
plotter.show()
