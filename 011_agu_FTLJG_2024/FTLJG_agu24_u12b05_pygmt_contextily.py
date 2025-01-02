# -*- coding: utf-8 -*-
# #############################################################################
# AGU24 | Washington, D.C. | December 9, 2024
#
# The impact of GMT in the Earth, Ocean and Space sciences: What's next? – U12B-05
# PyGMT – Accessing and Integrating GMT with Python and the Scientific Python Ecosystem
#
# Yvonne Fröhlich | Dongdong Tian | Wei Ji Leong | Max Jones | Michael Grund
#
# Python scripts to reproduce the examples shown in the talk
#
# Slides of the talk are freely available at https://doi.org/10.6084/m9.figshare.28049495
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/11/30
#   PyGMT v0.13.0 -> https://www.pygmt.org/v0.13.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


# See also:
# - PyGMT gallery example
#   https://www.pygmt.org/v0.13.0/gallery/maps/tilemaps.html


# %%
# -----------------------------------------------------------------------------
# Example for background map: contextily -> tiled maps
# -----------------------------------------------------------------------------

import pygmt
import contextily

fig = pygmt.Figure()
fig.tilemap(
    region=[-77.2, -76.7, 38.7, 39],
    projection="M10c",
    zoom=10,
    source="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    frame=True,
)
fig.show()


fig_path = "02_out_figs"
fig_name_basic = "FTLJG_agu24_u12b05_pygmt_"
dpi_png = 720
# fig.savefig(fname=f"{fig_path}/{fig_name_basic}contextily.png", dpi=dpi_png)
