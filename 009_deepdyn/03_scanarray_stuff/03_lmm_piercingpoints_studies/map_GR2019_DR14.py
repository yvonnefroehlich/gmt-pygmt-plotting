# -*- coding: utf-8 -*-
# #############################################################################
# Map of Grund & Ritter 2019 Data Repository DR14
# - Reproduced in PyGMT
# - Modified highlighting concept
# -----------------------------------------------------------------------------
# Usage of data provided along with
# - Grund & Ritter 2019 Geology (-> Data Repository: SKS-SKKS pairs)
# - Grund & Ritter 2020 GJI (-> GitHub: recording stations)
# - Wolf et al. 2023 (-> GitHub: LLSVPs)
# -----------------------------------------------------------------------------
# Related to
# - ScanArray / LITHOCAP project by Michael Grund 2014 - 2020
# - DeepDyn project by Yvonne Fröhlich 2023/08 - present
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/05/24
#   PyGMT v0.12.0 -> https://www.pygmt.org/v0.12.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


import numpy as np
import pandas as pd
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# Adjust for your needs
# -----------------------------------------------------------------------------
status_cc = ""  ## "", "_CC"
status_slmsec = ""  ##"", "_slmsec""
status_studies = "_GR2019"  ## "", "_GR2019", "_W2023"


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_fig/02_gr2019_dr14"

data_GR2019_same = "SKS_SKKS_GR2019_mod4pygmt_onlysame.dat"
data_GR2019_disc = "SKS_SKKS_GR2019_mod4pygmt_onlydisc.dat"
data_GR2019_stations = pd.read_csv(f"{path_in}/2019049_TableDR1_mod.csv", sep=";")

data_KEF = data_GR2019_stations[data_GR2019_stations["stacode"]=="KEF"]

# -----------------------------------------------------------------------------
lon_KEF = 24.8706
lat_KEF = 62.1664

siberia_lon = 105
siberia_lat = 60

atlantic_lon = -20
atlantic_lat = 60

# -----------------------------------------------------------------------------
lon_min = -30
lon_max = 110
lat_min = 40
lat_max = 80

lon_min = -35
lon_max = 120
lat_min = 40
lat_max = 85

# Lambert projection
# Determine projection center
lon0 = np.mean([lon_min, lon_max])
lat0 = np.mean([lat_min, lat_max])
# Calculate two standard parallels (only these two distortion-free)
lat1 = lat_min + (lat_max - lat_min) / 3
lat2 = lat_min + (lat_max - lat_min) / 3 * 2
region_used = [lon_min, lon_max, lat_min, lat_max]
projection_used = f"L{lon0}/{lat0}/{lat1}/{lat2}/10c"
# projection_used = "L40/60/16/80/10c"  # GR2019

# -----------------------------------------------------------------------------
font = "4p"
fill = "white@30"
justify = "MC"
pen = "0.5p"
trans = "70"

color_highlight = "255/90/0"  # ->  orange | URG paper

col_XKS = "lightred"
col_sScS = "goldenrod4"
col_SScS = "peru"
col_PSref = "darkbrown"
col_same = "white"

col_null = "white"
col_split = "gray50"
col_SKS = "216.75/82.875/24.990"  # -> red
col_SKKS = "236.895/176.97/31.875"  # -> orange
col_SKS = "red3"
col_SKKS = "darkorange"
col_PKS = "yellow2"

color_land = "tan@85"
color_shorelines = "gray70"

color_llvp = "gray50"
pattern_llvp = "p8+b+f"
color_HLFL = "green3"
color_missing = "gray30"

pen_KEF = "0.05p,gray30"
box_standard = "+gwhite@30+p0.1p,gray30+r2p"


# %%
# -----------------------------------------------------------------------------
# Generate geographic map
# -----------------------------------------------------------------------------

fig = gmt.Figure()
gmt.config(FONT="5.5p", MAP_GRID_PEN_PRIMARY="0.01p,gray80")

fig.coast(
    region=region_used,
    projection=projection_used,
    shorelines=f"1/0.01p,{color_shorelines}",
    resolution="h",  # high
    land=color_land,
    frame=["WSne", "a15f5g5"],
    # perspective=[130, 30],
)

# -----------------------------------------------------------------------------
# Region of other anisotropy studies in the lowermost mantle
if status_studies=="_GR2019":
    fig.plot(x=91, y=71, style="e145/1.4c/0.5c", fill=f"{col_PSref}@{trans}", pen=f"{pen},{col_PSref}")
    fig.plot(x=0, y=0, style="c0.1c", fill=f"{col_PSref}@{trans}", pen=f"{pen},{col_PSref}", label="P/S reflections+S0.1c")
    fig.text(x=95, y=71, text="W1993", angle=325, justify=justify, font=font, fill=fill)

    fig.plot(
        x=-13.5,
        y=65,
        style="c1.4c",
        fill=f"{col_sScS}@{trans}",
        pen=f"{pen},{col_sScS}",
        label="ScS-S sScS-sS+S0.1c",
    )
    fig.plot(x=0, y=0, style="c0.1c", fill="white", label="SKS/SPdKS/SKPdS+S0.1c")
    fig.text(x=-19, y=67, text="HELM1998", justify=justify, font=font, fill=fill)
    fig.text(x=-15, y=65.9, text="HE2015", justify=justify, font=font, fill=fill)
    fig.text(x=-15, y=62, text="-dvs", justify=justify, font=f"{font},red", fill=fill)

    fig.plot(
        x=75,
        y=74,
        style="c0.65c",
        fill=f"{col_SScS}@{trans}",
        pen=f"{pen},{col_SScS}",
        label="S-ScS+S0.1c",
    )
    fig.text(x=75, y=74, text="WK2008",  justify=justify, font=font, fill=fill)

    fig.plot(x=90, y=62, style="e5/2.8c/0.6c", fill=f"{col_SScS}@{trans}", pen=f"{pen},{col_SScS}")
    fig.text(x=90, y=61.5, text="TK2002", angle=5, justify=justify, font=font, fill=fill)

    fig.plot(
        x=92.5,
        y=55,
        style="c0.55c",
        fill=f"{col_XKS}@{trans}",
        pen=f"{pen},{col_XKS}",
        label="SKS-SKKS+S0.1c",
    )
    fig.text(x=92.5, y=55, text="LL2015", justify=justify, font=font, fill=fill)

    fig.plot(x=40.5, y=58, style="e5/1.8c/1.1c", fill=f"{col_XKS}@{trans}", pen=f"{pen},{col_XKS}")
    fig.text(x=38, y=60, text="LL2015", justify=justify, font=font, fill=fill)

    fig.plot(x=0, y=54, style="e0/1.1c/0.25c", fill=f"{col_XKS}@{trans}", pen=f"{pen},{col_XKS}")
    fig.text(x=0, y=54, text="LL2015", justify=justify, font=font, fill=fill)

    # fig.plot(x=5, y=37.5, style="e45/2c/1c", fill=f"{col_XKS}@{trans}", pen=f"{pen},{col_XKS}")
    # fig.text(x=5, y=37.5, text="LL2015", justify=justify, font=font, fill=fill)

    with gmt.config(FONT="4.5p"):
        fig.legend(box=box_standard, position="jTL+o-0.45c/-0.35c+w1.8c")

# -----------------------------------------------------------------------------
"""
# Plot and label recording station KEF
fig.plot(
    x=lon_KEF,
    y=lat_KEF,
    style="i0.15c",
    pen=pen_KEF,
    fill=color_highlight,
    label="recording station KEF"
)
fig.text(
    text="KEF",
    x=lon_KEF,
    y=lat_KEF,
    offset="0c/-0.18c",
    font=f"3.5p,{color_highlight}",
    fill="white@30",
    pen=pen_KEF,
    clearance="0.03c+tO",
)

# Mark piercing points related to recording station KEF
fig.plot(
    data=data_KEF[["ppCMBlon", "ppCMBlat"]],
    style="s0.2c",
    fill=f"{color_highlight}@80",
    pen=pen_KEF,
    label="pairs at KEF+S0.15c"
)
"""

# -----------------------------------------------------------------------------
# Plot LLVPs
# for i_model in range(1, 9, 1):
for i_model in range(2, 9, 1):
    label = None
    if i_model==2: label = "LLVPs"
    fig.plot(
        data=f"{path_in}/llvp/3model_2016_{i_model}.txt",
        pen=f"0.2p,{color_llvp}",
        fill=f"{pattern_llvp}{color_llvp}",
        close=True,
        #label=label,
    )

# with gmt.config(FONT="4.5p"):
#     fig.legend(box=box_standard, position="jBR+o-0.2c/-0.35c+w2c")

# -----------------------------------------------------------------------------
# Plot piercing point SKS-SKKS at CMB by Grund & Ritter (2019) Geology
# DISC
fig.plot(
    data=f"{path_in}/{data_GR2019_disc}",
    style="c0.07c",
    fill="white",
    pen=f"0.5p,{col_SKS}",
    incols=[1, 0],
    label="disc pairs - SKS null", #"+HGrund & Ritter (2019)",
    find="discSKSNull",
)
fig.plot(
    data=f"{path_in}/{data_GR2019_disc}",
    style="c0.08c",
    fill=col_SKS,
    pen="0.2p,gray10",
    incols=[1, 0],
    label="disc pairs - SKS split",
    find="discSKSSplit",
)
fig.plot(
    data=f"{path_in}/{data_GR2019_disc}",
    style="c0.07c",
    fill="white",
    pen=f"0.5p,{col_SKKS}",
    incols=[1, 0],
    label="disc pairs - SKKS null",
    find="discSKKSNull",
)
fig.plot(
    data=f"{path_in}/{data_GR2019_disc}",
    style="c0.08c",
    fill=col_SKKS,
    pen="0.2p,gray10",
    incols=[1, 0],
    label="disc pairs - SKKS split",
    find="discSKKSSplit",
)
# SAME
fig.plot(
    data=f"{path_in}/{data_GR2019_same}",
    style="c0.04c",
    fill=col_null,
    pen="0.2p,gray10",
    incols=[1, 0],
    label="same pairs - both null",
    find="sameSKSNull",
)
fig.plot(
    data=f"{path_in}/{data_GR2019_same}",
    style="c0.04c",
    fill=col_null,
    pen="0.2p,gray10",
    incols=[1, 0],
    find="sameSKKSNull",
)
fig.plot(
    data=f"{path_in}/{data_GR2019_same}",
    style="c0.04c",
    fill=col_split,
    pen="0.2p,gray10",
    incols=[1, 0],
    label="same pairs - both split",
    find="sameSKSSplit",
)
fig.plot(
    data=f"{path_in}/{data_GR2019_same}",
    style="c0.04c",
    fill=col_split,
    pen="0.2p,gray10",
    incols=[1, 0],
    find="sameSKKSSplit",
)

with gmt.config(FONT="4.5p"):
    fig.legend(box=box_standard, position="jTR+o-0.2c/-0.35c+w2c")

# -----------------------------------------------------------------------------
"""
# Plot DeepDyn target regions
fig.plot(
    x=siberia_lon,
    y=siberia_lat,
    style="d0.2c",
    fill=color_HLFL,
    pen="0.5,gray30",
    label="Siberia - stable HLFL+S0.14c+HDeepDyn target regions"
)
fig.plot(
    x=atlantic_lon,
    y=atlantic_lat,
    style="d0.2c",
    fill=color_missing,
    pen="0.5,gray30",
    label="North Atlantic - expected HLFL+S0.14c"
)

text_target = {
    "font": "4.5p", "fill": "white@30", "pen": pen_KEF, "clearance":"0.05c/0.05c+tO",
}
fig.text(
    text="Siberia",
    x=siberia_lon,
    y=siberia_lat,
    justify="TC",
    offset="0c/-0.25c",
    **text_target,
)
fig.text(
    text="Atlantic",
    x=atlantic_lon,
    y=atlantic_lat,
    justify="BC",
    offset="0c/0.25c",
    **text_target,
)

with gmt.config(FONT="4.5p"):
    fig.legend(box=box_standard, position="jBL+o-0.45c/-0.35c+w2.6c")
"""

# -----------------------------------------------------------------------------
args_warn = {"position": "MC", "justify": "MC", "transparency": 50, "no_clip": True}
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
fig.show() #method="external")
fig_name = f"map_GR2019_DR14_pygmt{status_studies}{status_slmsec}{status_cc}_TEST4phd"
# for ext in ["png", "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=720)
print(fig_name)
