# #############################################################################
# Overview of earthquakes and eruptions
# -----------------------------------------------------------------------------
# History
# - Created: 2024/04/07
# - Updated: 2024/04/23 - Improve coding style
# - Updated: 2025/03/28 - Reorganize folder, rewrite code
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.14.2 -> https://www.pygmt.org/v0.14.2/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt as gmt

# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# >>> Set for your needs <<<
fig_name = "00_overview_events_BFO"  # Name of output figure
dpi_png = 360  # Resolution of output PNG

# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

# File name for plate boundaries after Bird 2003
data_pb = "plate_boundaries_Bird_2003.txt"

# -----------------------------------------------------------------------------
# Epicenters
lon_epi = [121.562, 136.91, -79.611, 37.042, -8.391, 95.92]
lat_epi = [23.819, 37.23, -0.904, 37.166, 31.064, 22.01]

# Volcanos
lon_vol = [-17.84, -175.393]
lat_vol = [28.57, -20.545]

# Recording station BFO
lon_sta = 8.33
lat_sta = 48.33

# -----------------------------------------------------------------------------
# Colors
color_sta = "255/215/0"
color_eq = "255/90/0"  # -> orange
color_vol = "255/90/0"  # -> orange
color_pd = "216.750/82.875/24.990"
color_land = "gray90"
color_water = "steelblue"

# Standards
font = "7p"
pen_epi = "0.1p,black"
box_standard = "+gwhite@30+p0.5p,gray30+r1.5p"
clearance_standard = "0.1c/0.1c+tO"

# -----------------------------------------------------------------------------
# Region and projections
map_size = 10  # in centimeters

# Epicentral distance plot
epi_min = 80  # degrees
epi_max = 150
center_lon = lon_sta
center_lat = lat_sta
epi_plot = 160

proj_epi = f"E{center_lon}/{center_lat}/{epi_plot}/{map_size}c"
proj_rob = f"N{map_size}c"
proj_used = proj_epi


# %%
# -----------------------------------------------------------------------------
# Create epicentral distance plot
# -----------------------------------------------------------------------------
fig = gmt.Figure()
fig.basemap(region="d", projection=proj_used, frame=True)

# Plot shorelines
fig.coast(land=color_land, shorelines="1/0.01p,darkgray", borders="1/0.01p,gray50")

# Plot plate boundaries
fig.plot(data=f"{path_in}/{data_pb}", pen=f"0.3p,{color_pd}")

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
        style=f"E-{epi_limit * 2}+d",
        pen=f"1p,{color_sta},-",
    )
    # Annotations
    fig.text(
        x=center_lon,
        y=center_lat,
        offset=offset_station_label,
        text=f"{epi_limit}@.",
        font=font,
        fill="white@30",
        pen=f"0.5p,{color_sta}",
        clearance=clearance_standard,
    )

# Plot epicenters
fig.plot(
    x=lon_epi,
    y=lat_epi,
    style=f"k{path_in}/earthquake.def/0.7c",
    fill=color_eq,
    pen=color_eq,
)

# Plot volcanos
fig.plot(x=lon_vol, y=lat_vol, style="kvolcano/0.45c", fill=color_vol, pen="0.1p,black")

# Plot recording station BFO
fig.plot(x=center_lon, y=center_lat, style="i0.4c", fill=color_sta, pen="0.3p,black")
fig.text(
    x=center_lon,
    y=center_lat,
    offset="0c/0.4c",
    text="BFO",
    font=font,
    fill="white@30",
    pen=f"0.7p,{color_sta}",
    clearance=clearance_standard,
)

# Show and save
fig.show()  # method="external")

for ext in ["png"]:  # , "pdf", "eps"]:
    transparent = False
    if ext == "png":
        transparent = True
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png, transparent=transparent)

print(fig_name)
