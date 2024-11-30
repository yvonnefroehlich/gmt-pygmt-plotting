# -*- coding: utf-8 -*-
# #############################################################################
# AGU24 | Washington, D.C. | December 9, 2024
#
# The impact of GMT in the Earth, Ocean and Space sciences: What's next? – U12B-05
# PyGMT – Accessing and Integrating GMT with Python and the Scientific Python Ecosystem
#
# Yvonne Fröhlich | Dongdong Tian | Wei Ji Leong | Max Jones | Michael Grund
#
# Python scripts to reproduce the examples shown in the presentation
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/11/25
#   PyGMT v0.13.0 -> https://www.pygmt.org/v0.13.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


# See also:
#  - Pre-workshop:
#  - PyGMT Gallery:


fig_name_basic = "FTLJG_agu24_u12b05_pygmt_"
dpi_png = 720


# %%
# -----------------------------------------------------------------------------
# Example for GeoPandas: aspatial data -> geopandas.GeoDataFrame
# -----------------------------------------------------------------------------

import pygmt
import geopandas as gpd

# Downlaod a dataset about Chicago into a geopandas.GeoDataFrame
gdf_airbnb = gpd.read_file("https://geodacenter.github.io/data-and-lab/data/airbnb.zip")

fig = pygmt.Figure()
fig.basemap(region=[-88, -87.5, 41.62, 42.05], projection="M10c", frame="rltb")

pygmt.makecpt(cmap="bilbao", series=[5000, 95000, 10])
fig.colorbar(frame="xa10000+lpopulation in Chicago", position="jLM+o2c/-1c+w6c+v")

# Plot the polygons with color-coding for the population
fig.plot(
    data=gdf_airbnb,
    pen="0.2p,gray10",
    fill="+z",
    cmap=True,
    aspatial="Z=population",
)

fig.show()


fig.savefig(fname=f"{fig_name_basic}geopandas.png", dpi=dpi_png)