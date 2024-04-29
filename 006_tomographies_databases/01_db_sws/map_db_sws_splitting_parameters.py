# #############################################################################
# Shear wave splitting database
# Barruol, G., Wuestefeld, A., & Bokelmann, G. (2009). SKS-Splitting-database.
# Université de Montpellier, Laboratoire Géosciences.
# https://doi.org/10.18715/sks_splitting_database
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/04/29
#   PyGMT v0.11.0 -> https://www.pygmt.org/v0.11.0/ | https://www.pygmt.org/
#   GMT 6.4.0 -> https://www.generic-mapping-tools.org/
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
color_platebound = "216.750/82.875/24.990"
color_land = "gray90"
color_shorelines = "gray30"
color_borders = "gray10"
fill_null_max = "white"
pen_null = "0.4p,gray10"


# %%
# -----------------------------------------------------------------------------
# Load SWSM data
# -----------------------------------------------------------------------------
file_swsm = "sws_db_swsm_barruol_et_al_20231005_COR_GMT_phiGMT4j.txt"
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

# Make colormap for fast polarization direction
gmt.makecpt(cmap=f"{path_in}/phase.cpt", series=[-90, 90], cyclic=True)

# -----------------------------------------------------------------------------
# Set up basic map
fig.coast(
    region="d",
    projection="N11c",
    frame=["WSnE", "xa90f30", "ya30f15"],
    land=color_land,
    shorelines=f"1/0.05p,{color_shorelines}",
    borders=f"1/0.001p,{color_borders}",
)

# -----------------------------------------------------------------------------
# Plate boundaries
fig.plot(
    data=f"{path_in}/plate_boundaries_Bird_2003.txt",
    pen=f"0.4p,{color_platebound}",
)

# -----------------------------------------------------------------------------
# Plot splitting parameter as color-coded and orientated length-scaled bars
# according to phi and dt and nulls as white-filled black-outlined circles

# splits
fig.plot(
    data=df_bar_max_order,
    incols="0,1,2,3,4+s0.05,5+s0.006",
    style="j",
    cmap=True,
)

# nulls
fig.plot(
    data=df_null_max_order,
    style="c0.05c",
    fill=fill_null_max,
    pen=pen_null,
)

# -----------------------------------------------------------------------------
# Add colorbar for phi colormap
cb_label = "Complete Shear Wave Splitting Database - splits - @~f@~@-a@-"
fig.colorbar(cmap=True, frame=[f"xa30f10+l{cb_label}", "y+lN@.E"])

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()

fig_name = f"{path_out}/db_sws_splittingparameter"
# for ext in ["png"]:  # , "pdf", "eps"]:
#     fig.savefig(fname=f"{fig_name}.{ext}")

print(fig_name)
