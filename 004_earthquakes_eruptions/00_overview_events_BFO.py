# #############################################################################
# Overview of earthquakes and eruptions
# -----------------------------------------------------------------------------
# History
# - Created: 2024/04/07
# - Updated: 2024/04/23 - Improve coding style
# - Updated: 2025/03/28 - Reorganize folder, rewrite code
# - Updated: 2025/03/29 - Introduce dictionary for events
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


import pandas as pd
import pygmt as gmt

# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# >>> Adjust for your needs <<<
fig_name = "00_overview_events_BFO"  # Name of output figure
dpi_png = 360  # Resolution of output PNG

# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

# File name for plate boundaries after Bird 2003
data_pb = "plate_boundaries_Bird_2003.txt"

# Recording station, here Black Forest Observatory BFO
lon_sta = 8.33
lat_sta = 48.33

# -----------------------------------------------------------------------------
# Set up dictionary of events
df_events = pd.DataFrame(
    {
        "event_type": [
            "eruption",
            "eruption",
            "earthquake",
            "earthquake",
            "earthquake",
            "earthquake",
            "earthquake",
            "earthquake",
        ],
        "location": [
            "La Palma",
            "Tonga",
            "Esmeraldas",
            "Turkey, Syria",
            "Marocco",
            "Japan",
            "Taiwan",
            "Myanmar",
        ],
        "date": [
            "2021/09/19-2021/12/13",
            "2022/01/14-15",
            "2022/03/27",
            "2023/02/06",
            "2023/09/08",
            "2024/01/01",
            "2024/04/02",
            "2025/03/28",
        ],
        "lon": [-17.84, -175.393, -79.611, 37.042, -8.391, 136.91, 121.562, 95.92],
        "lat": [28.57, -20.545, -0.904, 37.166, 31.064, 37.23, 23.819, 22.01],
        "event_id": ["01", "02", "03", "04", "05", "06", "07", "08"],
    }
)

# -----------------------------------------------------------------------------
# Colors
color_sta = "255/215/0"
color_event = "255/90/0"  # -> orange
color_pd = "216.750/82.875/24.990"  # plate boundaries  # -> dark orange
color_sl = "darkgray"  # shorelines
color_land = "gray90"
color_water = "steelblue"

# Standards
font = "7p"
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
fig.coast(land=color_land, shorelines=f"1/0.01p,{color_sl}", borders="1/0.01p,gray50")

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
        text=f"{epi_limit}@.",  # degree sign in GMT
        font=font,
        fill="white@30",
        pen=f"0.5p,{color_sta}",
        clearance=clearance_standard,
    )

# Plot epicenters
df_eqs = df_events[df_events["event_type"] == "earthquake"]
fig.plot(
    x=df_eqs.lon,
    y=df_eqs.lat,
    style=f"k{path_in}/earthquake.def/0.7c",
    fill=color_event,
    pen=color_event,
)

# Plot volcanos
df_erp = df_events[df_events["event_type"] == "eruption"]
fig.plot(
    x=df_erp.lon,
    y=df_erp.lat,
    style="kvolcano/0.4c",
    fill=color_event,
    pen="0.1p,black",
)

# Plot recording station
fig.plot(x=center_lon, y=center_lat, style="i0.4c", fill=color_sta, pen="0.3p,black")
# Add label for recording station
fig.text(
    text="BFO",
    x=center_lon,
    y=center_lat,
    justify="MC",
    offset="0c/0.4c",
    font=font,
    fill="white@30",
    pen=f"0.7p,{color_sta}",
    clearance=clearance_standard,
)

# Add labels for event ID
fig.text(
    text=df_events["event_id"],
    x=df_events["lon"],
    y=df_events["lat"],
    justify="MC",
    offset="0c/-0.35c",
    font="5p",
    fill="white@30",
    pen=f"0.1p,{color_event}",
    clearance="0.05c/0.05c+tO",
)

# Show and save
fig.show()  # method="external")

# for ext in ["png"]:  # , "pdf", "eps"]:
#     transparent = False
#     if ext == "png":
#         transparent = True
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png, transparent=transparent)

print(fig_name)
