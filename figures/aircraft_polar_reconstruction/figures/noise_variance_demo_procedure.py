from common import *

g = graphviz.Digraph(**gv_settings)
var_style = dict(fillcolor='#F1F7E9')

# g.attr(
#     label="Procedure for Numerical Demonstration\nof Estimator Performance",
#     labelloc="t",
#     fontname='Helvetica-Bold', fontsize='18', shape='plaintext'
# )

g.node("func", label="Underlying \"truth\" function\n(sinusoid with a known signal frequency)")
g.node("draw", label="Take discrete samples\nat sample frequency")
g.edge("func", "draw")

g.node("tvar", label="True variance", **var_style)
g.node("noise", label="Add noise\n(normally distributed, independent)")
g.edge("tvar", "noise")

g.edge("draw", "noise")

g.node("syn", label="Synthetic Dataset", fillcolor='#F7E9F1')
g.edge("noise", "syn")

g.node("est", label="Apply the noise estimator")
g.node("evar", label="Estimated variance", **var_style)

g.edge("syn", "est")
g.edge("est", "evar")

g.node("c", label="Compare to\nassess performance", shape='plaintext', fillcolor="white")

dashed_line = dict(
    style='dashed',
    color='gray',
    arrowhead='none',
    arrowtail='none',
    dir='both',
    penwidth='1',
)
g.edge("tvar", "c", **dashed_line)
g.edge("evar", "c", **dashed_line)

g.view(filename="noise_variance_demo_procedure")