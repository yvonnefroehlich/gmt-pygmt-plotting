# #############################################################################
# PREM Earth model
#
# Data are available from
# https://github.com/AxiSEMunity/AxiSEM3D/tree/master/examples/05_anisotropy_global/PREM_anisotropy_w_and_wo_full_Cij_50s/processing/Cijkl_for_ani_PREM
# last accessed 2025/06/06
# -----------------------------------------------------------------------------
# History
# - Created: 2025/06/05
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.14.2 -> https://www.pygmt.org/v0.14.2/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt
import pandas as pd


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_fig"

depth_min = 0
depth_max = 3000

step_ag = (depth_max - depth_min) / 10
step_f = step_ag / 2
if depth_min == 0 and depth_max == 6371:
    step_ag = 500
    step_f = 100

region = [0, 14, depth_min, depth_max]  # xmin, xmax, ymin, ymax
projection = "X9c/-15c"  # Use minus sign to revert the direction of the axis, here y

color_highlight = "255/90/0"  # -> orange
color_vel = "brown"
color_density = "steelblue"

box_standard = "+ggray@90+p0.1p,gray30+r2p"


# %%
# -----------------------------------------------------------------------------
# Load data for PREM Earth model into in a pandas dataframe
# -----------------------------------------------------------------------------
df_prem = pd.read_csv(
    f"{path_in}/PREM_1s.csv",
    names=[
        "radius", "depth", "density",
        "v_pv", "v_ph", "v_sv", "v_sh",
        "eta", "Q_mu", "Q_kappa",
    ],
)

df_prem["v_p"] = (df_prem["v_pv"] + df_prem["v_ph"]) / 2
df_prem["v_s"] = (df_prem["v_sv"] + df_prem["v_sh"]) / 2


# %%
# -----------------------------------------------------------------------------
# Make plot
# -----------------------------------------------------------------------------
# Create new figure instance
fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray70")

# Set up frame for double-axes plot
# Left and right for depth
fig.basemap(
    region=region,
    projection=projection,
    frame=["We", f"ya{step_ag}g{step_ag}f{step_f}+ldepth / km"],
)
# Top for density
with pygmt.config(
    MAP_FRAME_PEN=color_vel,
    MAP_TICK_PEN=color_vel,
    FONT_ANNOT_PRIMARY=color_vel,
    FONT_LABEL=color_vel,
):
    fig.basemap(
        region=region,
        projection=projection,
        frame=["S", "xa1g1f0.5+lvelocity v / kms@+-1@+"],
    )
# Bottom for velocity
with pygmt.config(
    MAP_FRAME_PEN=color_density,
    MAP_TICK_PEN=color_density,
    FONT_ANNOT_PRIMARY=color_density,
    FONT_LABEL=color_density,
):
    fig.basemap(
        region=region,
        projection=projection,
        frame=["N", "xa1f0.5+ldensity @~r@~ / kgm@+-3@+"],
    )

# Mark important depths
pen_disc = f"1p,{color_highlight},2_2"
for y in [30, 120, 410, 660, 2700, 2890, 5150]:
    fig.plot(x=[0, 14], y=[y, y], pen=pen_disc)

# Plot velocity and density with depth
fig.plot(x=df_prem["v_p"], y=df_prem["depth"], pen=f"1.5p,light{color_vel}", label="v@-P@-")
fig.plot(x=df_prem["v_s"], y=df_prem["depth"], pen=f"1.5p,dark{color_vel}", label="v@-S@-")
fig.plot(x=df_prem["density"], y=df_prem["depth"], pen=f"1.5p,{color_density}", label="@~r@~")

# Add legend
fig.legend(box=box_standard, position="jBL+o0.1c+w1.5c")

# Save and show figure
fig_name = f"prem_1s_velocity_density_{depth_min}to{depth_max}km"
# for ext in ["png"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=360)
print(fig_name)
fig.show()
