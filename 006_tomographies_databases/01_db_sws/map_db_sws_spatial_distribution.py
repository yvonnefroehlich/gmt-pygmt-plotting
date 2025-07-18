# #############################################################################
# Shear wave splitting database
#
# Spatial distribution of splits (i.e. nulls are not considered)
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
# - PyGMT v0.11.0 - v0.14.2 -> https://www.pygmt.org/
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
color_sl = "darkred"  # shorelines
color_split = "white"

# Region and projection
region = "d"  # global with central longitude at 0° E, use "g" for 180° E
projection = "N11c"  # Robinson projection


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
for spacing in range(5, 21, 5):  # size of blocks in degrees
    # Calculate counts of splits within each block
    df_swsm_split_bin = gmt.blockmean(
        data=df_swsm_split[["Longitude", "Latitude", "phi_SL"]],
        region=region,
        spacing=spacing,
        summary="n",  # Counts within each block
    )

    # Convert to GMT-ready grid
    grd_swsm_split_bin = gmt.xyz2grd(data=df_swsm_split_bin, region=region, spacing=spacing)


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------
    fig = gmt.Figure()
    gmt.config(FONT_LABEL="10p", MAP_GRID_PEN_PRIMARY="0.01p,gray50")

    fig.basemap(region=region, projection=projection, frame=["WSnE", "xa90f30", "ya30f15"])
    fig.coast(land=color_land)

# -----------------------------------------------------------------------------
    # Counts of splits within in each block
    # Creat colormap
    gmt.makecpt(series=[0, 300, 10], cmap="nuuk", reverse=True)

    # Plot grid
    fig.grdimage(grid=grd_swsm_split_bin, region=region, cmap=True, nan_transparent=True)

    # Add colorbar
    cb_xlabel = f"Count of splits within each block ({spacing}@. x {spacing}@.)"
    fig.colorbar(frame=f"x+l{cb_xlabel}", position="+ef0.3c")

# -----------------------------------------------------------------------------
    # Plot data points for splits
    fig.plot(data=df_swsm_split[["Longitude", "Latitude"]], style="p0.1p", fill=color_split)

# -----------------------------------------------------------------------------
    # Add shorelines
    fig.coast(shorelines=f"1/0.15p,{color_sl}")

    # Plot plate boundaries
    fig.plot(data=f"{path_in}/plate_boundaries_Bird_2003.txt", pen=f"0.3p,{color_pb}")

    # Plot frame on top
    fig.basemap(frame=0)

# -----------------------------------------------------------------------------
    # Show and save figure
    fig.show()

    fig_name = f"{path_out}/db_sws_spatial_distribution_splits_spacing{spacing}deg"
    # for ext in ["png"]:  # , "pdf", "eps"]:
    #     fig.savefig(fname=f"{fig_name}.{ext}")

    print(fig_name)
