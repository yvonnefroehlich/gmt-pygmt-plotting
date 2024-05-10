# #############################################################################
# Shear wave splitting database
# Barruol, G., Wuestefeld, A., & Bokelmann, G. (2009). SKS-Splitting-database.
# Université de Montpellier, Laboratoire Géosciences.
# https://doi.org/10.18715/sks_splitting_database
#
# Spatial distribution of splits (i.e. nulls are not considered)
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/05/10
#   PyGMT v0.12.0 -> https://www.pygmt.org/
#   GMT 6.4.0 / 6.5.0 -> https://www.generic-mapping-tools.org/
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
color_shorelines = "darkred"
color_split = "white"

# Region and projection
region_used = "d"  # global with central longitude at 0° E, use "g" for 180° E
projection_used = "N11c"  # Robinson projection


# %%
# -----------------------------------------------------------------------------
# Load SWSM data
# -----------------------------------------------------------------------------
file_swsm = "sws_db_swsm_barruol_et_al_20231005_COR_GMT_phiGMT4j.txt"
df_swsm_raw = pd.read_csv(f"{path_in}/{file_swsm}", delimiter=",")
df_swsm_split = df_swsm_raw[df_swsm_raw.obs == "Split"]
df_swsm_null = df_swsm_raw[df_swsm_raw.obs == "Null"]


# %%
# -----------------------------------------------------------------------------
# Bin data
# -----------------------------------------------------------------------------
# Feel free to adjust the blocks size for your needs
for spacing_used in range(5, 21, 5):  # size of blocks degrees
    # Calculate counts of splits within blocks
    df_swsm_split_bin = gmt.blockmean(
        data=df_swsm_split[["Longitude", "Latitude", "phi_SL"]],
        region=region_used,
        spacing=spacing_used,
        summary="n",  # Counts within each block
    )

    # Convert to GMT-ready grid
    grd_swsm_split_bin = gmt.xyz2grd(
        data=df_swsm_split_bin,
        region=region_used,
        spacing=spacing_used,
    )


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------
    fig = gmt.Figure()
    gmt.config(FONT_LABEL="10p", MAP_GRID_PEN_PRIMARY="0.01p,gray50")

    fig.coast(
        region=region_used,
        projection=projection_used,
        land=color_land,
        frame=["WSnE", "xa90f30", "ya30f15"],
    )

# -----------------------------------------------------------------------------
    # Counts of splits with in blocks
    # Creat colormap
    gmt.makecpt(series=[0, 300, 10], cmap="nuuk", reverse=True)

    # Plot grid
    fig.grdimage(
        grid=grd_swsm_split_bin,
        region=region_used,
        cmap=True,
        nan_transparent=True,
    )

    # Add colorbar
    fig.colorbar(
        frame=f"x+lCount of splits within each block ({spacing_used}@. x {spacing_used}@.)",
        position="+ef0.3c",
    )

# -----------------------------------------------------------------------------
    # Data points for splits
    fig.plot(
        data=df_swsm_split[["Longitude", "Latitude"]],
        style="p0.1p",
        fill=color_split,
    )

# -----------------------------------------------------------------------------
    # Add Shorelines
    fig.coast(shorelines=f"1/0.15p,{color_shorelines}")

    # Plot plate boundaries
    fig.plot(
        data=f"{path_in}/plate_boundaries_Bird_2003.txt",
        pen=f"0.3p,{color_platebound}",
    )

    # Add frame
    fig.basemap(frame=0)

# -----------------------------------------------------------------------------
    # Show and save figure
    fig.show()

    fig_name = f"{path_out}/db_sws_spatial_distribution_splits_spacing{spacing_used}deg"
    # for ext in ["png"]:  # , "pdf", "eps"]:
    #     fig.savefig(fname=f"{fig_name}.{ext}")

    print(fig_name)
