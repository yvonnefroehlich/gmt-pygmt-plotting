# #############################################################################
# Map in PyGMT for ScanArray network
# - showing good and fair SWSMs at NORSA by Michael Grund
# - stereoplots re-generated with phase colormap by Yvonne Fröhlich
# -----------------------------------------------------------------------------
# Usage of data provided along with
# - Grund 2019 doctoral thesis KIT-GPI (-> Stuff at GPI: SplitLab *txt output files)
# - Grund & Ritter 2020 GJI (-> GitHub: digitalized tectonic, recording stations)
# -----------------------------------------------------------------------------
# Related to
# - ScanArray / LITHOCAP project by Michael Grund 2014/08 - 2019/02
#   https://github.com/michaelgrund/GMT-plotting/tree/main/008_map_scan_tectonic
# - DeepDyn project by Yvonne Fröhlich 2023/08 - 2025/03
# -----------------------------------------------------------------------------
# History
# - Created: 2024/06/07
# - Updated: 2025/27/07 - reduced and adjusted for GitHub
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.16.0 -> https://www.pygmt.org/v0.16.0/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
import pandas as pd
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# Adjust for your needs
# -----------------------------------------------------------------------------
status_area = "norsa"  ## "scandinavia" | "norsa"

status_network = "ALL"  ## "NO" | "ALL" | "PERMANENT" | "TEMPORARY" | "SA"
status_color = "NETWORK"  ## "NO" | "NETWORK"
status_grid = "tectonic"  ## "land" | "elevation" | "tectonic"
grd_res = "30s"

status_phase = "XKS"  ## "XKS" | "SKS" | "SKKS" | "PKS"

size_station_symbol = 0.1  # in centimeters
stereo_size = 0.4  # in centimeters
thick_circle = "0.01p"
add_stereo_size = 0
fill_circle = "white@30"
font = "5p"
status_quality = "goodfair"  # stereoplots are only provided for good and fair qualities


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Path
path_in = "01_in_data"
path_out = "02_out_figs"

# -----------------------------------------------------------------------------
# Region and projection
match status_area:
    case "norsa":
        lon_min = 10.5
        lon_max = 12
        lat_min = 60.5001
        lat_max = 61.4
        size_station_symbol = 0.2
        stereo_size = 2.75
        status_label = "station"
        leg_pos = "jRB+o0.1c+w3.4c"
        add_stereo = f"_stereo_{status_quality}_SC_{status_phase}"
    case _:
        lon_min = 3.5  # in degrees East
        lon_max = 37
        lat_min = 54  # in degrees North
        lat_max = 71.5
        size_station_symbol = 0.15
        stereo_size = 0.4
        status_label = "no"
        leg_width = 3.25
        if status_grid == "elevation": leg_width = 1.5  # in centimeters
        leg_pos = f"jRB+o0.55c/0.58c+w{leg_width}c"
        add_stereo = ""

# Lambert projection
# Determine projection center
lon0 = np.mean([lon_min, lon_max])
lat0 = np.mean([lat_min, lat_max])
# Calculate two standard parallels (only these two distortion-free)
lat1 = lat_min + (lat_max - lat_min) / 3
lat2 = lat_min + (lat_max - lat_min) / 3 * 2
region = [lon_min, lon_max, lat_min, lat_max]
projection = f"L{lon0}/{lat0}/{lat1}/{lat2}/10c"

match status_area:
    case "norsa":
        MAP_ANNOT_OBLIQUE = "lat_parallel"
        FORMAT_GEO_MAP = "ddd.xxF"
        frame = ["WSne", "xa0.5f0.25g0.5", "ya0.25f0.05g0.25"]
    case "scandinavia":
        MAP_ANNOT_OBLIQUE = ""
        FORMAT_GEO_MAP = "dddF"
        frame = ["WSne", "xa10f1g5", "ya10f1g5"]
    case _:
        MAP_ANNOT_OBLIQUE = ""
        FORMAT_GEO_MAP = "ddd.xxF"
        frame = ["WSne", "xafg", "yafg"]

# -----------------------------------------------------------------------------
# Colors
color_water = "white"
if status_grid == "elevation": color_water = "white@100"
color_land = "gray95"
if status_grid != "land": color_land = "white@100"
color_sta = "gold"  # recording stations
color_sl = "gray70"  # shorelines
color_nb = "gray60"  # national boundaries
color_hl = "255/90/0"  # highlight -> orange | URG paper

style_station = f"i{size_station_symbol}c"
pen_station = "0.1p,gray10"

add_size_legend = "+S0.12c"
if status_network=="NO": add_size_legend = "+S0.15c"

box_standard = "+gwhite@30+p0.1p,gray30+r2p"
clearance_standard = "0.1c/0.1c+tO"


# %%
# -----------------------------------------------------------------------------
# Data - Recording stations
# -----------------------------------------------------------------------------
# >>> externally modified from Excel file provided along with GR2019 <<<
file_stations = f"{path_in}/sta_coordinates_whitespace.txt"
col_names = ["station", "longitude", "latitude"]
df_stations = pd.read_csv(file_stations, sep=" ", names=col_names)

sta_perm_ids = [
    "FINLAND", "NORWAY", "SWEDEN", "DENMARK",
    "LATVIA", "ESTONIA", "LITHUANIA", "RUSSIA",
]
sta_perm_ids = ["permanent"]
sta_temp_ids = ["SA", "NWG", "N1", "N2", "NBB"]

# Set up dictionary to asing colors to the different station networks
color_N2_NBB = "darkorange"
color_permanent = "dodgerblue"
color_no_network = color_sta

dict_net_col = {
    "SA":         "gold",
    "N2":         color_N2_NBB,
    "NBB":        color_N2_NBB,
    "N1":         "brown",
    "NWG":        "tomato",
    "permanent":  color_permanent,
    "FINLAND":    color_permanent,
    "NORWAY":     color_permanent,
    "SWEDEN":     color_permanent,
    "DENMARK":    color_permanent,
    "LATVIA":     color_permanent,
    "ESTONIA":    color_permanent,
    "LITHUANIA":  color_permanent,
    "RUSSIA":     color_permanent,
}


# %%
# -----------------------------------------------------------------------------
# Data - Tectonic units
# -----------------------------------------------------------------------------
# The tectonic/geological content shown in the following was partly
# digitised using Didger® (Golden Software, LLC) by Franz Lutz.
filein = f"{path_in}/scan_tectonic.dat"
namescol = ["lon", "lat", "name", "num"]
datatab = pd.read_table(filein, sep="\t", skiprows=5, names=namescol)

# Set up dictionary to assign colors to the tectonic unis
dict_prov_col = {
    "Phanerozoic2":     "115/195/128",
    "Svecofennian":     "248/188/203",
    "Rapaviki":         "darkgray",
    "Paleoproterozoic": "107/107/148",
    "Phanerozoic":      "115/195/128",
    "Sveconorwegian":   "238/106/80",
    "Archean":          "241/99/106",
    "Caledonides":      "249/190/75",
    "TIB":              "149/116/83",
}


# %%
# -----------------------------------------------------------------------------
# Self-defined functions
# -----------------------------------------------------------------------------
# Plot recording stations as inverse triangle
def plot_station_triangle(sta_id, sta_color, sta_label=None):

    x = df_stations.longitude[df_stations["station"].str.startswith(sta_id)]
    y = df_stations.latitude[df_stations["station"].str.startswith(sta_id)]
    if sta_id == "permanent":
        x = df_stations.longitude[0:136]
        y = df_stations.latitude[0:136]

    label = f"{sta_label}{add_size_legend}"
    if sta_label == None: label = None

    fig.plot(
        x=x,
        y=y,
        style=style_station,
        fill=sta_color,
        pen=pen_station,
        label=label,
    )

# -----------------------------------------------------------------------------
# Outline stereoplot
def plot_stereo_outline(sta_id, sta_col, sta_label=None):

    x = df_stations.longitude[df_stations["station"].str.startswith(sta_id)]
    y = df_stations.latitude[df_stations["station"].str.startswith(sta_id)]
    if sta_id == "permanent":
        x = df_stations.longitude[0:136]
        y = df_stations.latitude[0:136]

    label = f"{sta_label}{add_size_legend}"
    if sta_label == None: label = None

    fig.plot(
        x=x,
        y=y,
        style=f"c{stereo_size + add_stereo_size}c",
        fill=fill_circle,
        pen=f"{thick_circle},{sta_col}",
        label=label,
    )


# %%
# -----------------------------------------------------------------------------
# Create geographic map
# -----------------------------------------------------------------------------
# Create new Figure instance
fig = gmt.Figure()
gmt.config(
    FONT="8p",
    MAP_GRID_PEN_PRIMARY="0.01p,gray80",
    FORMAT_GEO_MAP=FORMAT_GEO_MAP,
    MAP_ANNOT_OBLIQUE=MAP_ANNOT_OBLIQUE,
)

# Make basic map
fig.basemap(region=region, projection=projection, frame=0)

# -----------------------------------------------------------------------------
# Plot tectonic units
if status_grid=="tectonic":
    # Fix small unclean edges for NORSA region
    # Manual adjusted for region and size
    fig.plot(x=11.95, y=61.27, style="s1.5c", fill=dict_prov_col["Caledonides"])
    fig.plot(x=11.60, y=61.15, style="s1c", fill=dict_prov_col["Caledonides"])
    fig.plot(x=11.38, y=60.975, style="s0.7c", fill=dict_prov_col["TIB"])
    fig.plot(x=11.33, y=60.95, style="s0.7c", fill=dict_prov_col["Phanerozoic"])
    fig.plot(x=10.70, y=60.65, style="s1c", fill=dict_prov_col["Phanerozoic"])
    fig.plot(x=[10.50, 10.80], y=[60.77, 60.77], pen="20p,249/190/75")
    fig.plot(x=[10.80, 11.25], y=[60.77, 60.90], pen="15p,249/190/75")
    fig.plot(x=[11.35, 11.35], y=[60.60, 60.93], pen="15p,241/99/106")
    fig.plot(x=[11.30, 11.30], y=[60.70, 60.40], pen="15p,241/99/106")
    fig.plot(x=[11.35, 11.78], y=[60.95, 60.55], pen="10p,149/116/83")

    for key in dict_prov_col:

        # For each data point get name of corresponding tectonic unit
        tabfilt11 = datatab[(datatab["name"] == key)].copy()
        vals = np.unique(tabfilt11["num"]) # remove doublets

        # Go through the unit names and plot the areas in the defined colors
        for val in vals:
            tabfilt12 = tabfilt11[(tabfilt11["num"] == val)].copy()

            tabfilt12["lon"] = tabfilt12["lon"].astype(float)

            lons = tabfilt12["lon"]
            lats = tabfilt12["lat"]

            # Consider each unit only once in the legend (label is set or not)
            label = None
            if val==1:
                label = key
                # Create a legend with two columns
                if key=="Svecofennian": label = f"{key}+N2"
            fig.plot(x=lons, y=lats, fill=dict_prov_col[key], label=label)

    # Overlay map with semi-transparent white rectangle to smooth colors
    fig.plot(
        x=[lon_min-5, lon_min-5, lon_max+5, lon_max+5, lon_min-5],
        y=[lat_min-5, lat_max+5, lat_max+5, lat_min-5, lat_min-5],
        fill="white@40",
        pen="1p,black",
    )

# Download and plot elevation grid
if status_grid == "elevation":
    fig.grdimage(grid=f"@earth_relief_{grd_res}", region=region, cmap="oleron", shading=True)
    with gmt.config(FONT="10p"):
        fig.colorbar(frame=["xa1000f100+lelevation", "y+lm"])

# Plot shorelines and borders, frame, and water (not the stacking approach)
fig.coast(
    resolution="i",
    area_thresh="20/0/1",
    shorelines=f"1/0.1p,{color_sl}",
    borders=f"1/0.1p,{color_nb}",
    land=color_land,
    water=color_water,
    frame=frame,
)

# -----------------------------------------------------------------------------
# Color based on network chosen for plotting stereoplots
sta_ids = [status_network]
net_outl_all = [status_network]
net_tria_all = ["permanent"] + sta_temp_ids

for a in net_tria_all:
  if a in [status_network]: net_tria_all.remove(a)

print(status_network)
match status_network:
    case "NO":
        sta_ids = []
        net_outl_all = []
        net_tria_all = ["permanent"] + sta_temp_ids
    case "ALL":
        sta_ids = sta_perm_ids + sta_temp_ids
        net_outl_all = ["permanent"] + sta_temp_ids
        net_tria_all = ["permanent"] + sta_temp_ids
    case "PERMANENT":
        sta_ids = sta_perm_ids
        net_outl_all = ["permanent"]
        net_tria_all = sta_temp_ids
    case "TEMPORARY":
        sta_ids = sta_temp_ids
        net_outl_all = sta_temp_ids
        net_tria_all = ["permanent"]

# Plot outline of stereoplots
if status_area == "norsa":
    for net_outl in net_outl_all:
        net_label = None
        # if status_color!="NO": net_label = net_outl
        net_col = dict_net_col[net_outl]
        if status_color=="NO": net_col = color_no_network
        plot_stereo_outline(net_outl, net_col, net_label)

# Plot recording stations as inverse triangles
for net_tria in net_tria_all:
    net_label = net_tria
    net_col = dict_net_col[net_tria]
    if status_color=="NO":
        net_label = None
        net_col = color_no_network
    plot_station_triangle(net_tria, net_col, net_label)

# Add legend for networks and tectonic units
if status_color!="NO" or status_grid=="tectonic":
    with gmt.config(FONT=font):
        fig.legend(position=leg_pos, box=box_standard)

# -----------------------------------------------------------------------------
# Add stereoplot eps files
if status_area == "norsa":
    for sta_id in sta_ids:
        print(sta_id)

        network = "permanent"
        match sta_id:
            case "SA": network = "SA"
            case "NWG": network = "MAGNUS"
            case "N2": network = "NEONOR2"
            case "NBB": network = "NEONOR2"
            case "N1": network = "SCANLIPS3D"

        # temporary stations
        df_net = df_stations[df_stations["station"].str.startswith(sta_id)]
        # permanent stations
        if sta_id in sta_perm_ids: df_net = df_stations[0:136]

        for sta_temp in df_net["station"]:

            stereo_name = f"Stereo_{sta_temp}_{status_quality}_" + \
                          f"SC_{status_phase}_swsms_" + \
                           "single_BAZ0to360_phase_noall_MG"
            df_sta_temp = df_net[df_net["station"] == sta_temp]
            lon_temp = float(df_sta_temp["longitude"].iloc[0])
            lat_temp = float(df_sta_temp["latitude"].iloc[0])

            if lon_temp > lon_min and lon_temp < lon_max and \
               lat_temp > lat_min and lat_temp < lat_max:
                try:
                    fig.image(
                        imagefile=f"{path_in}/stereos/{sta_temp}/{stereo_name}.eps",
                        position=f"g{lon_temp}/{lat_temp}+jMC+w{stereo_size}c",
                    )
                except:
                    print("No stereoplot EPS file found!")

            # Add station label
            if lon_temp > lon_min and lon_temp < lon_max and \
               lat_temp > lat_min and lat_temp < lat_max:
                if status_label=="station":
                    font_color = dict_net_col[sta_id]
                    if status_color=="NO": font_color = color_no_network
                    fig.text(
                        x=lon_temp,
                        y=lat_temp,
                        text=sta_temp,
                        offset="0c/-0.3c",
                        font=f"6p,{font_color}",
                    )

    # Add colorbar for fast polarization direction
    if status_network!="NO":
        with gmt.config(
            FONT="12p",
            MAP_FRAME_PEN="0.05p",
            MAP_TICK_LENGTH_PRIMARY="3p",
            COLOR_NAN="white",
        ):
            gmt.makecpt(cmap="phase", series=[-90, 90])
            fig.colorbar(
                cmap=True,
                frame=["xa30f10+lapp. fast pol. dir. @~f@~@-a@- / N@.E"],
                position="jBL+o0.35c/0.45c+h+w2.5c/0.14c+ml",
                box=box_standard,
            )

    # Add label for observation type and seismological phase
    if status_network!="NO":
        fig.text(
            position="TC",
            offset="0c/-0.4c",
            text=f"{status_phase} | SC | {status_quality}",
            font=f"6p,{color_hl}",
            fill="white@30",
            clearance=clearance_standard,
        )

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name= f"map_scanarray_{status_grid}_{status_area}" + \
          f"_network{status_network}_color{status_color}{add_stereo}"
# for ext in ["png"]:  # "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=360)
print(fig_name)
