# #############################################################################
# Collatz problem
# -----------------------------------------------------------------------------
# History
# - Created: 2023/12/11
# - Updated: 2025/07/22
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.16.0 -> https://www.pygmt.org/v0.16.0/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Path
path_in = "01_in_data"
path_out = "02_out_figs"



# %%
# -----------------------------------------------------------------------------
# Calculations
# -----------------------------------------------------------------------------
rand_int = 11

def cal_collatz(rand_int):
    sequenz_int = []

    while rand_int != 1:

        if rand_int%2 == 0: # modulo even
            rand_int = rand_int / 2
        else: # uneven
            rand_int = 3 * rand_int + 1

        sequenz_int.append(int(rand_int))

    return sequenz_int



# %%
# -----------------------------------------------------------------------------
# Create figure via PyGMT
# -----------------------------------------------------------------------------
max_number = 100

fig = gmt.Figure()

fig.basemap(
    region=[0, max_number, 0, max_number],
    projection="X10c",
    frame=["WStr", "xa10f1+linput integer", "ya10f1+lsequenz"]
)

for rand_int_start in range(2, max_number, 1):

    sequenz_int = cal_collatz(rand_int_start)

    fig.plot(
        x=rand_int_start * np.ones(len(sequenz_int)),
        y=sequenz_int,
        style="c0.05c",
        fill="blue",
    )

fig.show()
fig_name = "collatz_problem"
# for ext in ["png"]:  #, "pdf"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
