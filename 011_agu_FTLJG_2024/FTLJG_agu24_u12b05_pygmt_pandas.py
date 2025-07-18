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
# History
# - Created: 2024/11/30
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.13.0 -> https://www.pygmt.org/v0.13.0/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


# See also:
# - GMT / PyGMT pre-workshop
#   https://www.generic-mapping-tools.org/agu24workshop/tut02_spec_pd_gpd.html
#   https://zenodo.org/records/15809717
# - PyGMT basic tutorial
#   https://www.pygmt.org/v0.13.0/tutorials/basics/plot.html


# %%
# -----------------------------------------------------------------------------
# Example for pandas: tabular data -> pandas.DataFrame
# -----------------------------------------------------------------------------

import pygmt
# import pandas as pd  # Required dependency

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


fig_path = "02_out_figs"
fig_name_basic = "FTLJG_agu24_u12b05_pygmt_"
dpi_png = 720
# fig.savefig(fname=f"{fig_path}/{fig_name_basic}pandas.png", dpi=dpi_png)
