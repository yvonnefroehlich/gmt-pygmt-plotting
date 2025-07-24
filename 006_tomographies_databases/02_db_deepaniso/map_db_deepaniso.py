# #############################################################################
# Deep anisotropy database
#
#   Wolf, J., Long, M. D., Li, M., & Garnero, E. (2023). Global compilation of
#   deep mantle anisotropy observations and possible correlation with low velocity
#   provinces. Geochemistry, Geophysics, Geosystems, 24, e2023GC011070.
#   https://doi.org/10.1029/2023GC011070
#
#   Data are available at
#   https://github.com/wolfjonathan/Deep_Mantle_Anisotropy_Database
# -----------------------------------------------------------------------------
# History
# - Created: 2024/04/29
# - Updated: 2025/07/22 - Add color-coding and numeric labels with legend
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


import os

import numpy as np
import pandas as pd
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# Adjust for your needs
# -----------------------------------------------------------------------------
status_projection = "ROB"  # "ROB", "EPI"
status_color = "CMAP"  # "MONO", "CMAP"
status_labels = "YES"  # "NO", "YES"
status_legend = "BOTTOM"  # "NO", "RIGHT", "LEFT", "BOTTOM
status_title = "NO"  # "NO", "YES"

epi_lon = 7  # degrees East
epi_lat = 50  # degrees North
epi_max = 60  # degrees


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Paths
path_in = "01_in_data"
path_out = "02_out_figs"
file_pb = "plate_boundaries_Bird_2003.txt"

# Colors
color_pb = "216.750/82.875/24.990"  # plate boundaries after Bird 2003
color_sl = "gray50"  # shorelines (used data built-in in PyGMT / GMT)
color_sta = "gold"
color_hl = "255/90/0"  # highlight
color_land = "gray95"
color_llpv = "brown"
pattern_llpv = "p8+b+f"

# Projection
map_size = 11  # in centimeters
match status_projection:
    case "ROB": projection = f"N{map_size}c"
    case "EPI": projection = f"E{epi_lon}/{epi_lat}/{epi_max}/{map_size}c"


# %%
# -----------------------------------------------------------------------------
# Create global maps
# -----------------------------------------------------------------------------
folders_analysis = os.listdir(f"{path_in}/01_aniso/")

for analysis in folders_analysis:
    files_areas = os.listdir(f"{path_in}/01_aniso/{analysis}")

    match analysis:
        case "SKS-SKKS": color_aniso = "darkorange"
        case "S-ScS": color_aniso = "purple"
        case _: color_aniso = "tan"

    match status_title:
        case "YES": frame_title = f"+tLMM seismic anisotropy - {analysis}"
        case "NO": frame_title =  0

# -----------------------------------------------------------------------------
    fig = gmt.Figure()
    gmt.config(FONT_TITLE="12p", FONT_LABEL="10p")

    fig.basemap(
        region="g",
        projection=projection,
        frame=["WSnE", "xa90f30", "ya30f15", frame_title],
    )
    fig.coast(land=color_land, shorelines=f"1/0.05p,{color_sl}")

# -----------------------------------------------------------------------------
    # Plate boundaries
    fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.1p,{color_pb}")

# -----------------------------------------------------------------------------
    # LLVP
    for i_model in range(2, 9, 1):
        fig.plot(
            data=f"{path_in}/02_llvp/3model_2016_{i_model}.txt",
            pen=f"0.2p,{color_llpv}",
            fill=f"{pattern_llpv}{color_llpv}",
            close=True,
        )

# -----------------------------------------------------------------------------
    # Lowermost mantle (LMM) anisotropy
    gmt.makecpt(cmap="batlow", series=[0, len(files_areas), 1], transparency=40)

    for i_area, area in enumerate(files_areas):
        data_use = f"{path_in}/01_aniso/{analysis}/{area}"
        data_use_df = pd.read_csv(data_use, delimiter=",", names=["lon", "lat", "value"])

        # Use arithmetic mean as approximation for centers of the areas
        mean_lon = np.mean(data_use_df["lon"])
        mean_lat = np.mean(data_use_df["lat"])

        # Set up text for legend entries
        if i_area == 0:  # first legend entry with title for legend
            ana_leg_add = ""
            if analysis in ["SKS-SKKS", "S-ScS"]: ana_leg_add = " discrepancies"
            cb_columns = f"+N2+HLowermost mantle anisotropy studies using {analysis}" + \
                         f" {ana_leg_add}         @;white;.@;;+f8p"
        else:
            cb_columns = ""

        # Plot areas in color
        area_split = area.split("_")
        area_whitespace = " ".join(area_split)
        args_col = {
            "data": data_use,
            "pen": "0.1p,gray10",
            "close": True,
            "label": f"({i_area + 1}) {area_whitespace}{cb_columns}",  # start at 1
        }
        match status_color:
            case "MONO":
                fig.plot(fill=f"{color_aniso}@60", **args_col)
            case "CMAP":
                fig.plot(fill="+z", zvalue=i_area, cmap=True, **args_col)

        # Add numbers as labels for each area
        if status_labels == "YES":
            offset = 0
            if status_projection == "ROB": offset = "-0.25c/0.1c"
            fig.text(
                x=mean_lon,
                y=mean_lat,
                offset=offset,
                text=f"({i_area + 1})",
                font="6p,Helvetica-Bold,black",
                fill="white@50",
                clearance="0.05c/0.05c+tO",
            )

    # Add legend with studies related to the numbers
    if status_legend != "NO":
        match status_legend:
            case "LEFT": legend_pos = "JLM+jRM+o0c/1c+w9.3c"
            case "RIGHT": legend_pos = "JRM+jLM+o0.5c/1c+w9.3c"
            case "BOTTOM": legend_pos = "JCB+jCT+o0.5c/0.6c+w9.3c"
        with gmt.config(FONT="7p"):
            fig.legend(position=legend_pos)

    # Mark center of epidistance plot as inverse triangle for theoretical recording station
    if status_projection == "EPI":
        fig.plot(x=epi_lon, y=epi_lat, style="i0.3c", fill=color_sta, pen="0.5p,black")

# -----------------------------------------------------------------------------
    # Plot map frame on top
    fig.basemap(frame=0)

# -----------------------------------------------------------------------------
    fig.show()

    fig_name = f"deepaniso_{analysis}_projection{status_projection}_color{status_color}" + \
               f"_legend{status_legend}_labels{status_labels}_title{status_title}"
    # for ext in ["png"]:  # , "pdf", "eps"]:
    #     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")

    print(fig_name)
