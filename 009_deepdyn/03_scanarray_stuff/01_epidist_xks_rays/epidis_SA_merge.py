# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Script II
# Reproduction with modifications of GMT map "005_map_equidist_siberia"
# by Michael Grund in PyGMT
# source of original script, data, and manual (last access 2022/04/06):
# https://github.com/michaelgrund/GMT-plotting/tree/main/005_map_equidist_siberia
# a modified version is part of his PhD thesis (DOI: 10.5445/IR/1000091425)
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich
# -----------------------------------------------------------------------------
# created: 2022/04/04 - PyGMT v0.6.0 with GMT 6.3.0
# updated: 2023/08/08 - PyGMT v0.9.0 / dev with GMT 6.4.0
# updated: 2023/09/18 - PyGMT v0.10.0 / dev with GMT 6.4.0
# updated: 2024/05/15 - PyGMT v0.12.0 / dev with GMT 6.5.0
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


import pygmt as gmt

# -----------------------------------------------------------------------------
# Set up
# -----------------------------------------------------------------------------

fig_all = "eqidist_SA_MG2pygmt_all.eps"
fig_zoom = "eqidist_SA_MG2pygmt_zoom.eps"
fig_out = "eqidist_SA_MG2pygmt_merge"

# Size
dia_single = 10  # diameter
x_total = dia_single * 2 + 2  # gap

# Zoom
col_zoom = "gray50"  # color
dashed_zoom = "5_2.5:0p"  # dashes
# line segment length _ gap length : offset from origin; all in point

# Legend
box_standard = "+gwhite@20+p0.8p,black+r0.1"  # box
leg_net_pos = "JCB+jCB+w2.75c"  # position


# -----------------------------------------------------------------------------
# Make geographical map
# -----------------------------------------------------------------------------

# Create figure object
fig_merge = gmt.Figure()

# -----------------------------------------------------------------------------
# Combine single maps
# all (left)
fig_merge.image(
    region=f"0/{x_total}/0/{dia_single}",
    projection=f"X{x_total}c/{dia_single}c",
    imagefile=fig_all,
    position=f"JLT+jLT+w{dia_single}c",
)
# zoom (right)
fig_merge.image(imagefile=fig_zoom, position=f"JRT+jRT+w{dia_single}c")

# -----------------------------------------------------------------------------
# Add zoom circle
fig_merge.plot(
    x=dia_single / 2 * 3 + 2,
    y=dia_single / 2,
    style=f"c{dia_single}c",
    pen="6p,white",  # Hide map frame of the single map
)
fig_merge.plot(
    x=dia_single / 2 * 3 + 2,
    y=dia_single / 2,
    style=f"c{dia_single - 0.2}c",
    pen=f"2p,{col_zoom},{dashed_zoom}",
)

# -----------------------------------------------------------------------------
# Add zoom lines
fig_merge.plot(
    x=[dia_single / 2, dia_single / 2 * 3 + 2 - 0.3],
    y=[dia_single / 4 * 3 + 0.05, dia_single - 0.085],
    pen=f"1.5p,{col_zoom},{dashed_zoom}",
)
fig_merge.plot(
    x=[dia_single / 2, dia_single / 2 * 3 + 2 - 0.3],
    y=[dia_single / 4 - 0.05, 0.08],
    pen=f"1.5p,{col_zoom},{dashed_zoom}",
)

# -----------------------------------------------------------------------------
# Add legend
fig_merge.legend(
    spec="legend_gmt_network.txt",
    position=leg_net_pos,
    box=box_standard,
)

# -----------------------------------------------------------------------------
# Show and save figure
fig_merge.show()
# for ext in ["png"]:  #, "pdf", "eps"]:
#     fig_merge.savefig(fname=f"{fig_out}.{ext}")
