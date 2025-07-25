# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Script I
# Reproduction with modifications of GMT map "005_map_equidist_siberia"
# by Michael Grund in PyGMT
# source of original script, data, and manual (last access 2022/04/06):
# https://github.com/michaelgrund/GMT-plotting/tree/main/005_map_equidist_siberia
# a modified version is part of his PhD thesis (DOI: 10.5445/IR/1000091425)
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich
# -----------------------------------------------------------------------------
# created: 2022/04/04 - PyGMT v0.6.0 with GMT 6.3.0
# updated: 2023/08/08 - PyGMT v0.9.0 / dev with GMT 6.4.0
# updated: 2023/09/18 - PyGMT v0.10.0 / dev with GMT 6.4.0
# updated: 2024/05/15 - PyGMT v0.12.0 / dev with GMT 6.5.0
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


import pygmt as gmt

# -----------------------------------------------------------------------------
# Set up
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# What to plot - choose
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
status_area = "all"  ## "all", "zoom"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# -----------------------------------------------------------------------------
# Fixed values - do not change

fig_name = f"eqidist_SA_MG2pygmt_{status_area}"
myfont = "4p"

lon_cent = 74.305
lat_cent = 71.658
rad_zoom = "0.92i"
map_size = "1.8i"  # radius

match status_area:
   case "all":
        pro_area = 160
        rad_taget = "8.1p"
        key_choose = ["SA_2", "RUS"]
   case "zoom":
        pro_area = 80
        rad_taget = "17p"
        key_choose = ["SA", "AA_perm", "AA_temp", "USA_sub", "GL"]

# -----------------------------------------------------------------------------
# Colors - can be changed based on your personal preferences
col_patb = "216.750/82.875/24.990"  # plate boundaries
col_land = "lightgray"  # land masses
col_water = "white"  # waster masses
col_taget = "gold@30"  # target area
col_epi = "white"  # epicenter
col_outl = "gray50"  # outline of large circles

col_AA = "dodgerblue2"  # AlpArray
col_RUS = "darkblue"  # Russia
col_SA = "darkorange"  # ScanArray
col_GL = "springgreen3"  # Greenland
col_USA = "darkred"  # USArray

# -----------------------------------------------------------------------------
# Data
data_patb = "PB2002_boundaries_GMTready.txt"  # plate boundaries
data_epi = "EQall.dat"  # epicenters

# Coordinates of recording stations
sta_AA_perm = "coord_AlpArray_perm.dat"
sta_AA_temp = "coord_AlpArray_temp.dat"
sta_GL = "coord_Greenland.dat"
sta_RUS = "coord_Russia.dat"
sta_SA = "coord_ScanArray.dat"
sta_USA = "coord_USArray_Alaska.dat"
sta_USA_sub = "coord_USArray_Alaska_SUB.dat"

# Coordinates of ray paths (already in GMT-ready format)
path_AA_perm = "pathlist_AA_perm.dat"
path_AA_temp = "pathlist_AA_temp.dat"
path_GL = "pathlist_GREEN.dat"
path_RUS = "pathlist_RUSSIA.dat"
path_SA = "pathlist_SA.dat"
path_SA_2 = "pathlist_SA_2.dat"
path_USA = "pathlist_USA.dat"

# -----------------------------------------------------------------------------
# # Select sub datasets

# data_epi_zoom = gmt.select(
#     data=data_epi,
#     projection=f"E{lon_cent}/{lat_cent}/60/{map_size}",
#     region="g",
# )

# -----------------------------------------------------------------------------
# Dictionaries

# Fill color of station markers and line color of ray paths
dic_col = {
    "AA_perm": col_AA,
    "AA_temp": col_AA,
    "GL": col_GL,
    "RUS": col_RUS,
    "SA": col_SA,
    "SA_2": col_SA,
    "USA": col_USA,
    "USA_sub": col_USA,
}

# Semi-transparence of ray paths
dic_trans = {
    "AA_perm": "@97",
    "AA_temp": "@97",
    "GL": "@60",
    "RUS": "@80",
    "SA": "@97",
    "SA_2": "@97",
    "USA": "@95",
    "USA_sub": "@95",
}

# Coordinates of stations
dic_sta = {
    "AA_perm": sta_AA_perm,
    "AA_temp": sta_AA_temp,
    "GL": sta_GL,
    "RUS": sta_RUS,
    "SA": sta_SA,
    "SA_2": sta_SA,
    "USA": sta_USA,
    "USA_sub": sta_USA_sub,
}

# Coordinates of ray paths
dic_path = {
    "AA_perm": path_AA_perm,
    "AA_temp": path_AA_temp,
    "GL": path_GL,
    "RUS": path_RUS,
    "SA": path_SA,
    "SA_2": path_SA_2,
    "USA": path_USA,
    "USA_sub": path_USA,
}


# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------

# Create figure objection
fig = gmt.Figure()

# -----------------------------------------------------------------------------
# Global changes of default values of GMT
gmt.config(MAP_FRAME_WIDTH="1p")  # thickness of map frame

# -----------------------------------------------------------------------------
# Epidistance plot
fig.coast(
    region="g",
    projection=f"E{lon_cent}/{lat_cent}/{pro_area}/{map_size}",
    resolution="c",
    land=col_land,
    water=col_water,
)

# -----------------------------------------------------------------------------
# Plate boundaries after Bird 2003
fig.plot(
    data=data_patb,
    pen="0.25p," + col_patb,
)

# -----------------------------------------------------------------------------
# Ray paths
for key in key_choose:

    # Set input order of columns depending on file
    if key in ["AA_perm", "AA_temp"]:
        incols_first = 1
        incols_second = 0
    else:
        incols_first = 0
        incols_second = 1

    fig.plot(
        data=dic_path[key],
        pen=f"0.1p,{dic_col[key]}{dic_trans[key]}",
        incols=[incols_first, incols_second],
    )


# -----------------------------------------------------------------------------
# Epicenters
fig.plot(
    data=data_epi,
    style="a0.1c",  # star
    fill=col_epi,
    pen="0.1p,black",
    incols=[1, 0],
)

# -----------------------------------------------------------------------------
# Stations
for key in key_choose:

    # Set input order of columns depending on file
    if key in ["SA_2", "SA", "USA_sub"]:
        incols_first = 0
        incols_second = 1
    if key in ["RUS", "AA_perm", "AA_temp", "GL"]:
        incols_first = 1
        incols_second = 0

    fig.plot(
        data=dic_sta[key],
        style="i0.1c",
        fill=dic_col[key],
        pen="0.1p,black",
        incols=[incols_first, incols_second],
    )

# -----------------------------------------------------------------------------
# Zoom area
if status_area == "all":
    fig.plot(
        x=lon_cent,
        y=lat_cent,
        style=f"c{rad_zoom}",
        pen=f"0.7p,{col_outl},3_1:0p",  # dashed line
        # line segment length _ gap length : offset from origin; all in points
    )

# Target area
fig.plot(
    x=lon_cent,
    y=lat_cent,
    style=f"c{rad_taget}",
    fill=col_taget,
    pen=f"0.25p,{col_outl}",
)

# -----------------------------------------------------------------------------
# Annotation of continents
if status_area == "all":
    fig.text(
        x=[21.00, 74.305, -135.553, -140.553, 102.255, -54.665, 138.51, -13.708],
        y=[18.38, -75, 41.099, 48.099, 35.704, -17.154, -29.7, 47.388],
        text=[
            "Africa",
            "Antarctica",
            "North",
            "America",
            "Asia",
            "South America",
            "Australia",
            "Europe",
        ],
        font=myfont,
    )

if status_area == "zoom":
    fig.text(
        x=[21.00, -100.553, 102.255, -13.708],
        y=[18.38, 41.099, 37.704, 47.388],
        text=["Africa", "North America", "Asia", "Europe"],
        font=myfont,
    )

# -----------------------------------------------------------------------------
# Frame
fig.basemap(frame=True)

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
# for ext in ["eps"]:  #, "png", "pdf"]:
#     fig.savefig(fname=f"{fig_name}.{ext}")

