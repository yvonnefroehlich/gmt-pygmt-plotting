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
# - GMT / PyGMT pre-workshop
#   https://www.generic-mapping-tools.org/agu24workshop/tut02_spec_pd_gpd.html
# - PyGMT gallery example
#   https://www.pygmt.org/v0.13.0/gallery/maps/choropleth_map.html
#   https://www.pygmt.org/v0.13.0/gallery/lines/roads.html


# %%
# -----------------------------------------------------------------------------
# Example for GeoPandas: spatial data (points, lines, polygons) -> geopandas.GeoDataFrame
# -----------------------------------------------------------------------------

import pygmt
import geopandas as gpd

# Download a dataset about Chicago into a geopandas.GeoDataFrame
gdf_airbnb = gpd.read_file("https://geodacenter.github.io/data-and-lab/data/airbnb.zip")

fig = pygmt.Figure()
fig.basemap(region=[-88, -87.5, 41.62, 42.05], projection="M10c", frame="rltb")

pygmt.makecpt(cmap="bilbao", series=[5000, 95000, 10])
fig.colorbar(frame="xa10000+lpopulation in Chicago", position="jLM+o2c/-1c+w6c+v")

# Plot the polygons with color-coding for the population
fig.plot(
    data=gdf_airbnb,
    fill="+z",
    aspatial="Z=population",
    cmap=True,
    pen="0.2p,gray10",
)

fig.show()


fig_path = "02_out_figs"
fig_name_basic = "FTLJG_agu24_u12b05_pygmt_"
dpi_png = 720
# fig.savefig(fname=f"{fig_path}/{fig_name_basic}geopandas.png", dpi=dpi_png)
