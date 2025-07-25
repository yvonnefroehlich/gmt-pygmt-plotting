# -*- coding: utf-8 -*-
# #############################################################################
# Map in PyGMT for ScanArray network
# - Focus on SWSMst at recording station KEF - HE
# -----------------------------------------------------------------------------
# Usage of data provided along with
# - Grund & Ritter 2019 Geology (-> Data Repository: SKS-SKKS pairs)
# - Grund 2019 PhD (-> Stuff at GPI: SplitLab *txt output files)
# - Grund & Ritter 2020 GJI (-> GitHub: Stations)
# -----------------------------------------------------------------------------
# Related to
# - ScanArray / LITHOCAP project by Michael Grund 2014 - 2020
# - DeepDyn project by Yvonne Fröhlich 2023/08 - present
# - Master thesis by Fiona Dorn 2024
# - Master thesis by Muhammad Dillah 2024
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/01/25
#   PyGMT v0.12.0 -> https://www.pygmt.org/v0.12.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# - Updated: 2024/02/05 - Add recording stations
# - Updated: 2024/05/28 - Combine pairs and color highlighting
# - Updated: 2024/06/06 - Add stereoplots for ScanArray
# - Updated: 2024/06/07 - Move ScanArray to separat script
# #############################################################################


import numpy as np
import pandas as pd
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# Adjust for your needs
# -----------------------------------------------------------------------------
status_pc = "gpi"  # "private", "gpi"
status_cc = ""  ## "", "_CC"
status_slmsec = ""  ## "", "_slmsec""
status_stereo = "NO"  ## "NO", "KEF"
status_station = "pairs"  # "color", "pairs"


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Path
match status_pc:
    case "gpi":
        path_same = "/home/yfroe/Documents"
    case "private":
        path_same = "C:/Users/Admin/C2/EigeneDokumente/Studium/Promotion"

stereo_path = f"{path_same}/D_Matlab/stereoplots/"
path_in = "01_in_data/"
path_out = "02_out_fig/01_scandinavia/"

# -----------------------------------------------------------------------------
# Colors
color_land = "gray95"
color_shorelines = "gray70"
color_borders = "gray60"
color_highlight = "255/90/0"  # ->  orange | URG paper

color_disc = "lightmagenta"
color_same = "0/197/205"

color_SA = "gold"
color_N2_NBB = "orange"
color_N1 = "brown"
color_NWG = "tomato"
color_permanent = "dodgerblue"

style_station = "i0.17c"
match status_station:
    case "color":
        pen_station = "0.1p,gray10"
        color_station = f"{color_highlight}@50"
    case "pairs":
        pen_station = "0.1p,black"
        color_station = "tan"

box_standard = "+gwhite@30+p0.1p,gray30+r2p"
box_stereo = f"+c0.05c+p1p,{color_highlight}+gwhite"
font_stereo = f"7p,{color_highlight}"

# -----------------------------------------------------------------------------
# Region
lon_min = 3.5
lon_max = 36
lat_min = 54
lat_max = 72

# Mercator projection
region_used = [lon_min, lon_max, lat_min, lat_max]
projection_used = "M10c"

# Lambert projection
# Determine projection center
lon0 = np.mean([lon_min, lon_max])
lat0 = np.mean([lat_min, lat_max])
# Calculate two standard parallels (only these two distortion-free)
lat1 = lat_min + (lat_max - lat_min) / 3
lat2 = lat_min + (lat_max - lat_min) / 3 * 2
region_used = [lon_min, lon_max, lat_min, lat_max]
projection_used = f"L{lon0}/{lat0}/{lat1}/{lat2}/10c"

lon_KEF = 24.8706
lat_KEF = 62.1664


# %%
# -----------------------------------------------------------------------------
# Data - recording stations
# -----------------------------------------------------------------------------
# >>> tabes were replaced externally by four white spaces <<<
# >>> trailing white spaces were removed externally <<<
# Mixture of tabs, white spaces, tabs with with spaces

data_stations = f"{path_in}sta_coordinates"

col_names = ["station", "longitude", "latitude"]
tab_stations = pd.read_table(
    f"{path_in}/sta_coordinates_ORIGINAL.txt",
    sep="\s+",
    names=col_names,
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

df_stations = pd.read_csv(
    f"{data_stations}_whitespace.txt", sep=" ", names=col_names,
)


# %%
# -----------------------------------------------------------------------------
# Data - SKS-SKKS pairs
# -----------------------------------------------------------------------------
# >>> externally modified from Excel file provided along with GR2019 <<<

data_pairs = f"{path_in}2019049_TableDR1_mod.csv"
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

# Create new Figure instance
fig = gmt.Figure()
gmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray60")

# Make basic map with shorelines, borders, and land
fig.coast(
    region=region_used,
    projection=projection_used,
    frame=["WSnE", "a5f1g5"],
    land=color_land,
    shorelines=f"1/0.1p,{color_shorelines}",
    borders=f"1/0.1p,{color_borders}",
)

# -----------------------------------------------------------------------------
# Plot recording stations
fig.plot(
    data=f"{data_stations}_whitespace.txt",
    style=style_station,
    pen=pen_station,
    fill=color_station,
    incols=[1,2],
    label="none+HSKS-SKKS pairs"
)

# Mark stations with SKS-SKKS pairs
if status_station=="pairs":
    # No discrepant pairs
    fig.plot(
        data=df_pairs_same[["stalon","stalat"]],
        style=style_station,
        pen=pen_station,
        fill=color_same,
        label="only same",
    )
    # At least on discrepant pair
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

# -----------------------------------------------------------------------------
# Plot recording station KEF
fig.plot(
    x=lon_KEF,
    y=lat_KEF,
    style="i0.2c",
    pen="0.1p,black",
    fill=color_highlight,
)

# Label recording stations
if status_station=="color":
    fig.text(
        text="KEF",
        x=lon_KEF,
        y=lat_KEF,
        offset="0c/-0.25c",
        font=f"4.5p,{color_highlight}",
        fill="white@30",
        pen="0.01p,black",
        clearance="0.03c+tO",
    )
elif status_station=="pairs":
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
# Add stereoplot image
if status_stereo == "KEF":
    stereo_size = 2
    stereo_name = "Stereo_KEF_goodfair_SC_single_Baz0to360_phase_"
    stereo_stuff = "onlyNE_"
    args_stereo = {"justify": "CB", "font": font_stereo, "no_clip": True}

    fig.text(text="MG (2019, PhD)", position="BR", offset="-1.7c/2.72c", **args_stereo)
    fig.image(
        imagefile=f"{path_in}{stereo_name}{stereo_stuff}MG.eps",
        position=f"jBR+o0.7c/0.6c+w{stereo_size}c",
        box=box_stereo,
    )
    fig.text(text="FD (2024, MT)", position="TL", offset="0.3c/-0.95c", **args_stereo)
    fig.image(
        imagefile=f"{path_in}{stereo_name}{stereo_stuff}FD.eps",
        position=f"jTL+o-0.7c/1.05c+w{stereo_size}c",
        box=box_stereo,
    )
    fig.text(text="MD (2024, MT)", position="TR", offset="-0.3c/-0.95c", **args_stereo)
    fig.image(
        imagefile=f"{path_in}{stereo_name}{stereo_stuff}MD.eps",
        position=f"jTR+o-0.7c/1.05c+w{stereo_size}c",
        box=box_stereo,
    )

# -----------------------------------------------------------------------------
args_warn = {
    "position": "MC",
    "justify": "MC",
    "transparency": 50,
    "no_clip": True,
}
# Add warning regarding SLmsec error
if status_slmsec=="_SLmsec":
    fig.text(
        text="Affected by SLmsec error",
        font="15p",
        angle=-45,
        **args_warn,
    )
# Add warning reagarding copyright
if status_cc=="_CC":
    fig.text(
        text="Map created by Yvonne Fröhlich",
        font=f"15p,{color_highlight}",
        angle=45,
        **args_warn,
    )

# -----------------------------------------------------------------------------
# Show and save figure
fig.show(dpi=720) # method="external")
fig_name= f"map_scandinavia_{status_station}_stereo{status_stereo}{status_slmsec}{status_cc}"
for ext in ["png", "pdf", "eps"]:
    fig.savefig(fname=f"{path_out}{fig_name}.{ext}", dpi=720)
print(fig_name)
