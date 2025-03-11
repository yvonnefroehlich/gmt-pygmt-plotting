# #############################################################################
# Virginia source with USArray, ScanArray, and AlpArray recording stations
# -----------------------------------------------------------------------------
# Related to
# - Fröhlich Y., Ritter J. R. R. (2024) http://dx.doi.org/10.5281/zenodo.14510993
#   Vertical and Small-scale Lateral Varying Seismic Anisotropy in the Upper
#   Mantle Underneath the Upper Rhine Graben, Central Europe. Annual Meeting of
#   the American Geophysical Union. http://dx.doi.org/10.5281/zenodo.14510993.
# -----------------------------------------------------------------------------
# History
# - Created: 2025/03/09
# -----------------------------------------------------------------------------
# Versions
#   PyGMT v0.14.2 -> https://www.pygmt.org/v0.14.2/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
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
# Adjust for your needs
# -----------------------------------------------------------------------------
proj_dist_max = 80  # degrees
epi_step = 10  # degrees
fig_width = 10  # centimeters


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"
dpi_png = 720  # resolution of saved PNG file

# Coordinates source in Virginia
source_lon = -77.93
source_lat = 37.91

proj_used = f"E{source_lon}/{source_lat}/{proj_dist_max}/{fig_width}c"

color_land = "gray90"
color_sl = "gray50"
color_source = "red"
color_station = "gold"

color_AA = "goldenrod1"  # AlpArray
color_SA = "tomato"  # ScanArray
color_USA = "FIREBRICK3"  # USArray
colors_net = [color_AA, color_SA, color_USA]

box_standard = "+gwhite@30+p0.1p,gray30+r2p"


# %%
# -----------------------------------------------------------------------------
# Virginia source
# -----------------------------------------------------------------------------
mt_virginia = {
    "mrr": 4.71,
    "mtt": 0.0381,
    "mff": -4.74,
    "mrt": 0.399,
    "mrf": -0.805,
    "mtf": -1.23,
    "exponent": 17,
    "event_name": "Virginia",
}

args_meca = {
    "scale": "0.4c+m+f5p",
    "compressionfill": color_source,
    "extensionfill": "cornsilk",
    "depth": 0,
}


# %%
# -----------------------------------------------------------------------------
# Create map
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray30")

fig.basemap(region="d", projection=proj_used, frame=0)
fig.coast(shorelines=f"1/0.01p,{color_sl}", land=color_land)
fig.basemap(frame=0)

# -----------------------------------------------------------------------------
# Plot networks
for i_net, station_file in enumerate(
    [
        "USTA_stations.txt",
        "AA_stations.txt",
        "SNSN_stations.txt",
    ]
):
    df_sta = pd.read_csv(f"{path_in}/{station_file}", sep="\t", header=0)
    label_sta = station_file.split("_")[0] + "+S0.2c"  # Adjust size in legend
    fill_sta = colors_net[i_net]

    fig.plot(
        data=df_sta[["lon", "lat"]], style="i0.05c", fill=fill_sta, label=label_sta
    )

with gmt.config(FONT="7p"):
    fig.legend(position="jRB+o0.1c+w1.3c", box=box_standard)

# -----------------------------------------------------------------------------
# Plot concentric circles for epicentral distance
for i_epi in range(epi_step, proj_dist_max, epi_step):
    fig.plot(x=source_lon, y=source_lat, style=f"E-{i_epi * 2}+d", pen="0.3p,gray50,-")
    fig.text(
        x=source_lon,
        y=-i_epi + source_lat,
        text=f"{i_epi}@.",
        font="7p",
        clearance="0.05c/0.05c+tO",
        fill="white@30",
    )

# -----------------------------------------------------------------------------
# Plot source in Virginia
fig.meca(spec=mt_virginia, longitude=source_lon, latitude=source_lat, **args_meca)

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = f"setup_virginia_arrays_dist{proj_dist_max}deg"
# for ext in ["png"]:  # "png", "pdf", "eps"
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
