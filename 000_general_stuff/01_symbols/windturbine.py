# #############################################################################
# Plot wind turbine symbol with PyGMT
# - General syntax of the argument passed to the "style" parameter (-S flag)
#   k name_of_symbol_file / size_of_symbol
# - Please note: Custom symbols cannot be used in auto-legends yet
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/05/16
#   PyGMT v0.12.0 -> https://www.pygmt.org/v0.12.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


import pygmt as gmt


# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------

size = 5


# -----------------------------------------------------------------------------
# Make plot
# -----------------------------------------------------------------------------

fig = gmt.Figure()

fig.basemap(
    region=[-size, size, -size, size],
    projection=f"X{size * 2}c",
    frame=True,
)

fig.plot(
    x=-4,
    y=0,
    style="kwindturbine_YF.def/1c",
    fill="darkgray",
    pen="black",
)

fig.plot(
    x=-2,
    y=0,
    style="kwindturbine_YF.def/0.5c",
    fill="darkgray",
    pen="black",
)

fig.plot(
    x=0,
    y=0,
    style="kwindturbine_YF.def/.5c",
    fill="black",
    pen="black",
)

fig.plot(
    x=2,
    y=0,
    style="kwindturbine_YF.def/1c",
    fill="lightgray",
    pen="gray30",
)

fig.show()
# fig.savefig(fname="windturbine.png")
