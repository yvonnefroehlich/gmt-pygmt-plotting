# #############################################################################
# Reproduction with modifications of GMT map "005_map_equidist_siberia"
# by Michael Grund in PyGMT
#
# Script II
#
# source of original script, data, and manual (last access 2022/04/06):
# https://github.com/michaelgrund/GMT-plotting/tree/main/005_map_equidist_siberia
# a modified version is part of his PhD thesis (DOI: 10.5445/IR/1000091425)
# -----------------------------------------------------------------------------
# History
# - Created: 2022/04/04 - PyGMT v0.6.0 with GMT 6.3.0
# - Updated: 2023/08/08 - PyGMT v0.9.0 / dev with GMT 6.4.0
# - Updated: 2023/09/18 - PyGMT v0.10.0 / dev with GMT 6.4.0
# - Updated: 2024/05/15 - PyGMT v0.12.0 / dev with GMT 6.5.0
# - Updated: 2025/07/25 - PyGMT v0.16.0 / dev with GMT 6.5.0
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


import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# Set up
# -----------------------------------------------------------------------------
# Path
path_in = "01_in_data"
path_out = "02_out_figs"

# Figure names
fig_all = "eqidist_SA_MG2pygmt_all.eps"
fig_zoom = "eqidist_SA_MG2pygmt_zoom.eps"
fig_out = "eqidist_SA_MG2pygmt_merge"

# Size
dia_single = 10  # diameter
x_total = dia_single * 2 + 2  # gap

# Zoom
color_zoom = "gray50"  # color
dashed_zoom = "5_2.5:0p"  # dashes
# line segment length _ gap length : offset from origin; all in point

# Legend
box_standard = "+gwhite@20+p0.8p,black+r0.1"  # box
leg_net_pos = "JCB+jCB+w2.75c"  # position


# %%
# -----------------------------------------------------------------------------
# Make geographical map
# -----------------------------------------------------------------------------
# Create figure object
fig = gmt.Figure()
with gmt.config(MAP_FRAME_PEN="white"):
    fig.basemap(
        region=f"0/{x_total}/0/{dia_single}",
        projection=f"X{x_total}c/{dia_single}c",
        frame=0,
    )

# -----------------------------------------------------------------------------
# Combine single maps
# all (left)
fig.image(imagefile=f"{path_out}/{fig_all}", position=f"JLT+jLT+w{dia_single}c")
# zoom (right)
fig.image(imagefile=f"{path_out}/{fig_zoom}", position=f"JRT+jRT+w{dia_single}c")

# -----------------------------------------------------------------------------
# Add zoom circle
fig.plot(
    x=dia_single / 2 * 3 + 2,
    y=dia_single / 2,
    style=f"c{dia_single}c",
    pen="6p,white",  # Hide map frame of the single map
)
fig.plot(
    x=dia_single / 2 * 3 + 2,
    y=dia_single / 2,
    style=f"c{dia_single - 0.2}c",
    pen=f"2p,{color_zoom},{dashed_zoom}",
)

# -----------------------------------------------------------------------------
# Add zoom lines
fig.plot(
    x=[dia_single / 2, dia_single / 2 * 3 + 2 - 0.3],
    y=[dia_single / 4 * 3 + 0.05, dia_single - 0.086],
    pen=f"1.5p,{color_zoom},{dashed_zoom}",
)
fig.plot(
    x=[dia_single / 2, dia_single / 2 * 3 + 2 - 0.3],
    y=[dia_single / 4 - 0.05, 0.08],
    pen=f"1.5p,{color_zoom},{dashed_zoom}",
)

# -----------------------------------------------------------------------------
# Add legend
fig.legend(spec=f"{path_in}/legend_gmt_network.txt", position=leg_net_pos, box=box_standard)

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
# for ext in ["png"]:  #, "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_out}.{ext}")
print(fig_out)