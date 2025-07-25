# #############################################################################
# Map in PyGMT for ScanArray network
# - Focus on SKS-SKKS pairs
# -----------------------------------------------------------------------------
# Usage of data provided along with
# - Grund & Ritter 2019 Geology (-> Data Repository: SKS-SKKS pairs)
# - Grund & Ritter 2020 GJI (-> GitHub: Stations)
# -----------------------------------------------------------------------------
# Related to
# - ScanArray / LITHOCAP project by Michael Grund, KIT, 2014/06 - 2019/02
# - DeepDyn project by Yvonne Fröhlich, KIT, 2023/08 - 2025/03
# -----------------------------------------------------------------------------
# History
# - Created: 2025/07/25
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
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"

# -----------------------------------------------------------------------------
# Colors
color_land = "gray95"
color_sl = "gray70"  # shorelines
color_nb = "gray60"  # national borders
color_hl = "255/90/0"  # highlight ->  orange | URG paper

color_disc = "lightmagenta"
color_same = "0/197/205"

style_station = "i0.17c"
pen_station = "0.1p,black"
color_station = "tan"

box_standard = "+gwhite@30+p0.1p,gray30+r2p"

# -----------------------------------------------------------------------------
# Lambert projection
lon_min = 3.5
lon_max = 36
lat_min = 54
lat_max = 72

# Determine projection center
lon0 = np.mean([lon_min, lon_max])
lat0 = np.mean([lat_min, lat_max])
# Calculate two standard parallels (only these two distortion-free)
lat1 = lat_min + (lat_max - lat_min) / 3
lat2 = lat_min + (lat_max - lat_min) / 3 * 2

region = [lon_min, lon_max, lat_min, lat_max]
projection = f"L{lon0}/{lat0}/{lat1}/{lat2}/10c"


# %%
# -----------------------------------------------------------------------------
# Data - recording stations
# -----------------------------------------------------------------------------
# >>> tabs were replaced externally by four white spaces <<<
# >>> trailing white spaces were removed externally <<<
# Mixture of tabs, white spaces, tabs with with spaces

data_stations = f"{path_in}/sta_coordinates"

col_names = ["station", "longitude", "latitude"]
tab_stations = pd.read_table(
    f"{data_stations}_ORIGINAL.txt", sep="\s+", names=col_names,
)

# -----------------------------------------------------------------------------
with open(f"{data_stations}_modified.txt") as f:
    lines = [line.rstrip('\n') for line in f]

stations = []
lons = []
lats = []

with open(f"{data_stations}_whitespace.txt", "a") as f_new:

    for i_line in range(len(lines)):
        line_temp_split = lines[i_line].split(" ")

        line_temp_red = []
        for i_ele in range(len(line_temp_split)):
            if line_temp_split[i_ele]=="":
                pass
            else:
                line_temp_red.append(line_temp_split[i_ele])

        line_temp_join = " ".join(line_temp_red)

        stations.append(line_temp_red[0])
        lons.append(float(line_temp_red[1]))
        lats.append(float(line_temp_red[2]))

        # f_new.write(line_temp_join + "\n")

df_stations = pd.read_csv(f"{data_stations}_whitespace.txt", sep=" ", names=col_names)


# %%
# -----------------------------------------------------------------------------
# Data - SKS-SKKS pairs
# -----------------------------------------------------------------------------
# >>> externally modified from Excel file provided along with GR2019 <<<

data_pairs = f"{path_in}/2019049_TableDR1_mod.csv"
df_pairs = pd.read_csv(data_pairs, sep=";")

df_pairs_same = df_pairs[df_pairs["pair"]=="same"]
df_pairs_same_reset = df_pairs_same.reset_index(drop=True)

df_pairs_disc = df_pairs[df_pairs["pair"]=="disc"]
df_pairs_disc_reset = df_pairs_disc.reset_index(drop=True)


stacods_pairs = []
lons_pairs = []
lats_pairs = []
for i_pair in range(len(df_pairs)):
    if df_pairs["stacode"][i_pair] in stacods_pairs:
        pass
    else:
        stacods_pairs.append(df_pairs["stacode"][i_pair])
        lons_pairs.append(df_pairs["stalon"][i_pair])
        lats_pairs.append(df_pairs["stalat"][i_pair])


# %%
# -----------------------------------------------------------------------------
# Create geographic map
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray60")

# Make basic map with shorelines, borders, and land
fig.basemap(region=region, projection=projection, frame=["WSnE", "a5f1g5"])
fig.coast(land=color_land, shorelines=f"1/0.1p,{color_sl}", borders=f"1/0.1p,{color_nb}")

# -----------------------------------------------------------------------------
# Plot recording stations
fig.plot(
    data=f"{path_in}/sta_coordinates_whitespace.txt",
    style=style_station,
    pen=pen_station,
    fill=color_station,
    incols=[1,2],
    label="none+HSKS-SKKS pairs"
)

# Mark stations with SKS-SKKS pairs
# NO discrepant pairs
fig.plot(
    data=df_pairs_same[["stalon","stalat"]],
    style=style_station,
    pen=pen_station,
    fill=color_same,
    label="only same",
)
# At least ONE discrepant pair
fig.plot(
    data=df_pairs_disc[["stalon","stalat"]],
    style=style_station,
    pen=pen_station,
    fill=color_disc,
    label="discrepant",
)

# Add legend
with gmt.config(FONT="6p"):
    fig.legend(position="jTL+o2.4c/0.4c+w1.8c", box=box_standard)

# Label recording stations
fig.text(
    text=df_pairs_disc["stacode"],
    x=df_pairs_disc["stalon"],
    y=df_pairs_disc["stalat"],
    offset="0c/-0.2c",
    font="5p",
    fill="white@30",
    pen=f"0.01p,{color_disc}",
    clearance="0.03c+tO",
)

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name= "map_network_xks_pairs"
# for ext in ["png"]:  #, "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)
