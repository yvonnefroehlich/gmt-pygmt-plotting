# #############################################################################
# Overview earthquakes and eruptions
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/04/07
#   PyGMT v0.11.0 -> https://www.pygmt.org/v0.11.0/ | https://www.pygmt.org/
#   GMT 6.4.0 -> https://www.generic-mapping-tools.org/
# - Updated: 2024/04/23
#   Improve coding style
# #############################################################################

import pygmt as gmt

# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Colors
col_sta = "255/215/0"
col_eq = "255/90/0"  # -> orange
col_vol = "255/90/0"  # -> orange
col_pd = "216.750/82.875/24.990"
col_land = "gray90"
col_water = "steelblue"

# Standards
font = "7p"
pen_epi = "0.1p,black"
box_standard = "+gwhite@30+p0.5p,gray30+r1.5p"
clearance_standard = "0.1c/0.1c+tO"

# File name for plate boundaries after Bird 2003
data_pb = "plate_boundaries_Bird_2003.txt"

# Recording station
code_sta = "BFO"
lon_sta = 8.33
lat_sta = 48.33

# Epicenters
lon_epi = [121.562, 136.91, -79.611, 37.042, -8.391]  # , 46.443]
lat_epi = [23.819, 37.23, -0.904, 37.166, 31.064]  # , 35.277]

# Volcanos
lon_vol = [-17.84, -175.393]
lat_vol = [28.57, -20.545]


# -----------------------------------------------------------------------------
# Region and projections
# -----------------------------------------------------------------------------
map_size = "10c"

# Epicentral distance plot
epi_min = 80  # degrees
epi_max = 150
center_lon = lon_sta
center_lat = lat_sta
epi_plot = 160

proj_epi = f"E{center_lon}/{center_lat}/{epi_plot}/{map_size}"

proj_rob = f"N{map_size}c"

proj_used = proj_epi


# %%
# -----------------------------------------------------------------------------
# Create epicentral distance plot
# -----------------------------------------------------------------------------
fig = gmt.Figure()

fig.basemap(region="d", projection=proj_used, frame=True)

# Plot shorelines
fig.coast(land=col_land, shorelines="1/0.01p,darkgray", borders="1/0.01p,gray50")

# Plot plate boundaries
fig.plot(data=data_pb, pen="0.3p," + col_pd)

# Epicentral distance range used in this study
for epi_limit in [epi_min, epi_max]:
    if epi_limit == epi_min:
        offset_station_label = "0c/-2.5c"
    elif epi_limit == epi_max:
        offset_station_label = "0c/-4.7c"

    # Circles
    fig.plot(
        x=center_lon,
        y=center_lat,
        style=f"E-{epi_limit*2}+d",
        pen=f"1p,{col_sta},-",
    )
    # Annotations
    fig.text(
        x=center_lon,
        y=center_lat,
        offset=offset_station_label,
        text=f"{epi_limit}@.",
        font=font,
        fill="white@30",
        pen=f"0.5p,{col_sta}",
        clearance=clearance_standard,
    )

# Plot epicenter
fig.plot(x=lon_epi, y=lat_epi, style="kearthquake.def/0.7c", fill=col_eq, pen=col_eq)

# Plot volcanos
fig.plot(x=lon_vol, y=lat_vol, style="kvolcano/0.45c", fill=col_vol, pen="0.1p,black")

# Plot recording station
fig.plot(x=center_lon, y=center_lat, style="i0.4c", fill=col_sta, pen="0.3p,black")
fig.text(
    x=center_lon,
    y=center_lat,
    offset="0c/0.4c",
    text=code_sta,
    font=font,
    fill="white@30",
    pen=f"0.7p,{col_sta}",
    clearance=clearance_standard,
)

# Show and save
fig.show()  # method="external")

fig_name = "overview_earthquake_BFO"
# for ext in ["png"]: # , "pdf", "eps"]:
#     fig.savefig(fname=f"{fig_name}.{ext}")

print(fig_name)
