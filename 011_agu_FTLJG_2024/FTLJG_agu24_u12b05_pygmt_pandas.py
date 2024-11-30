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
#  - PyGMT Tutorial:


fig_name_basic = "FTLJG_agu24_u12b05_pygmt_"
dpi_png = 720


# %%
# -----------------------------------------------------------------------------
# Example for pandas: tabular data -> pandas.DataFrame
# -----------------------------------------------------------------------------

import pygmt

# Load a GMT built-in dataset into a pandas.DataFrame
df_eqs = pygmt.datasets.load_sample_data(name="japan_quakes")

fig = pygmt.Figure()
fig.basemap(region=[131, 152, 33, 51], projection="M10c", frame=True)
fig.coast(land="gray95", shorelines="gray50")

pygmt.makecpt(cmap="navia", series=[0, 500], reverse=True)
fig.colorbar(frame=["xa100f50+lhypocentral depth", "y+lkm"], position="+ef0.2c")

# Plot the epicenters as color- and size-coded circels based on depth or magnitude
fig.plot(
    x=df_eqs.longitude,
    y=df_eqs.latitude,
    size=0.02 * 2**df_eqs.magnitude,
    fill=df_eqs.depth_km,
    cmap=True,
    style="cc",
    pen="gray10",
)

fig.show()


fig.savefig(fname=f"{fig_name_basic}pandas.png", dpi=dpi_png)
