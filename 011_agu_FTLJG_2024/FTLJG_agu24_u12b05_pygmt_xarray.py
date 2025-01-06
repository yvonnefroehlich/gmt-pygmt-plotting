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
#   https://www.generic-mapping-tools.org/agu24workshop/tut03_spe_xarray.html
# - PyGMT gallery example
#   https://www.pygmt.org/v0.13.0/gallery/images/grdgradient.html


# %%
# -----------------------------------------------------------------------------
# Example for Xarray: gridded data -> xarray.DataArray
# -----------------------------------------------------------------------------

import pygmt
# import xarray as xr

# Download an elevation grid into a xarray.DataArray
da_ele = pygmt.datasets.load_earth_relief(resolution="01d")

fig = pygmt.Figure()
fig.basemap(region="g", projection="N10c", frame=True)

# Plot the grid with color-coding for the elevation
fig.grdimage(grid=da_ele, cmap="oleron")
fig.colorbar(frame=["xa2000+lelevation", "y+lm"])

fig.show()


fig_path = "02_out_figs"
fig_name_basic = "FTLJG_agu24_u12b05_pygmt_"
dpi_png = 720
# fig.savefig(fname=f"{fig_path}/{fig_name_basic}xarray.png", dpi=dpi_png)
