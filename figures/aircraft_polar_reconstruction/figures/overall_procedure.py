from common import *

g = graphviz.Digraph(**gv_settings)

title_style = dict(fontname='Helvetica-Bold', fontsize='16', shape='plaintext')
hidden_style = dict(fillcolor='white')
model_style = dict(fillcolor='#F7F1E9')

# Create a node for the title
# g.attr(
#     label="Inference-Based Flight Data Reconstruction",
#     labelloc="t",
#     fontname='Helvetica-Bold', fontsize='18', shape='plaintext'
# )

g.node("true", label="True data", **hidden_style)
g.node("sensor", label="Sensor data")
g.node("noise", label="True noise", **hidden_style)
g.node("estimate", label="Estimate of\ntrue data")
g.node("noise_estimate", label="(Explicit) Estimate of noise,\ncomputed from sensor data")

g.edge("true", "sensor", style='dashed')
g.edge("noise", "sensor", style='dashed')

g.edge("sensor", "estimate")
g.edge("sensor", "noise_estimate")

g.node("model_unsolved", label="Aerodynamic / propulsive model\nwith unknown parameters", **model_style)
g.node("newton", label="Newtonian dynamics\nfor unsteady corrections", **model_style)

g.node("energy_balance", label="Energy-balance reconstruction\n(compute energy residuals)")

g.node("opti", label="Numerical optimization\n(minimize residuals)", **model_style)

g.node("model_solved", label="Aerodynamic / propulsive model\nwith known parameters", **model_style)

g.edge("newton", "energy_balance")
g.edge("estimate", "energy_balance")
g.edge("model_unsolved", "energy_balance")

g.edge("energy_balance", "opti")

g.edge("opti", "model_solved")

g.view(filename="overall_procedure")