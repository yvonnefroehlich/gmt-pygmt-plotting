# #############################################################################
# Shear wave splitting database
#
# Splitting parameters of splits as orientated and color-coded (fast
# polarization direction phi) length-scaled (delay time dt) bars
#
# Wüstefeld A., Bokelmann G., Barruol G., Montagner J.-P., (2009). Identifying
# global seismic anisotropy patterns by correlating shear-wave splitting and
# surface-wave data. Physics of the Earth and Planetary Interiors, 176(3–4),
# 198-212, https://doi.org/10.1016/j.pepi.2009.05.006, last access 2024/09/08.
#
# Shear wave splitting data is available at https://ds.iris.edu/ds/products/sws-dbs/
# - SWS-DB: The Géosciences Montpellier SplitLab Shear-Wave Splitting Database
#   https://ds.iris.edu/ds/products/sws-db/, last access 2024/09/08
#   https://doi.org/10.18715/sks_splitting_database
#   https://splitting.gm.univ-montp2.fr/
# - SWS-DB-MST: The Missouri S&T western and central United States shear-wave splitting database
#   https://ds.iris.edu/ds/products/sws-db-mst/, last access 2024/09/08
# -----------------------------------------------------------------------------
# History
# - Created: 2024/04/29
# - Updated: 2025/02/15
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.16.0 -> https://www.pygmt.org/
# - GMT 6.4.0 - 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pandas as pd
import pygmt as gmt

# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

# Colors
color_pb = "216.750/82.875/24.990"  # plate boundaries
color_land = "gray90"
color_water = "white"
color_sl = "gray30"  # shorelines
fill_null_max = "white"
pen_null = "0.4p,gray10"


# %%
# -----------------------------------------------------------------------------
# Load SWSM data
# -----------------------------------------------------------------------------
file_swsm = "sws_db_swsm_barruol_et_al_20251227_COR_GMT_phiGMT4j.txt"
df_swsm_raw = pd.read_csv(f"{path_in}/{file_swsm}", delimiter=",")
df_swsm_split = df_swsm_raw[df_swsm_raw.obs == "Split"]
df_swsm_null = df_swsm_raw[df_swsm_raw.obs == "Null"]

columns_used_bar_max = ["Longitude", "Latitude", "phi_SL", "phi_GMT", "dt", "thickness"]
df_bar_max_order = df_swsm_split[columns_used_bar_max]

df_null_max_order = df_swsm_null[["Longitude", "Latitude"]]


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(FONT_LABEL="10p", MAP_GRID_PEN_PRIMARY="0.01p,gray50")

# Set up basic map
fig.basemap(region="d", projection="N11c", frame=["WSnE", "xa90f30", "ya30f15"])

# Plot land masses, shorelines and political borders
fig.coast(land=color_land, shorelines=f"1/0.05p,{color_sl}")

# -----------------------------------------------------------------------------
# Plot plate boundaries
fig.plot(data=f"{path_in}/plate_boundaries_Bird_2003.txt", pen=f"0.4p,{color_pb}")

# -----------------------------------------------------------------------------
# Plot splitting parameter of splits as orientated and color-coded length-scaled
# bars according to phi and dt; nulls as white-filled black-outlined circles

# Make colormap for phi
gmt.makecpt(cmap="phase", series=[-90, 90], cyclic=True)

# Plot splits
fig.plot(data=df_bar_max_order, incols="0,1,2,3,4+s0.05,5+s0.006", style="j", cmap=True)

# Plot nulls
fig.plot(data=df_null_max_order, style="c0.05c", fill=fill_null_max, pen=pen_null)

# Add colorbar for phi colormap
cb_xlabel = "Complete Shear Wave Splitting Database - splits"
cb_ylabel = "@~f@~@-a@- / N@.E"
fig.colorbar(cmap=True, frame=[f"xa30f10+l{cb_xlabel}", f"y+l{cb_ylabel}"])

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()

fig_name = f"{path_out}/db_sws_splitting_parameters"
# for ext in ["png"]:  # , "pdf", "eps"]:
#    fig.savefig(fname=f"{fig_name}.{ext}")

print(fig_name)
