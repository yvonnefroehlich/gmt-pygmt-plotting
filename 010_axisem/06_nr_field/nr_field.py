# #############################################################################
# AxiSEM3D - Nr field
# - complexity map
# - Cartesian histogram
# Note: This script is a general example on how to plot the Nr field based on the input
#       and output of a dummy simulation
# For details on wavefield scanning / learning see publications
# Leng et al. 2016, 2019 for details and background
# https://doi.org/10.1093/gji/ggw363 and https://doi.org/10.1093/gji/ggz092
# -----------------------------------------------------------------------------
# History
# - Created: 2023/05/15
# - Rewritten: 2024/09/20
# - Updated: 2025/08/02 - adjusted for GitHub
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


import netCDF4 as nc
import numpy as np
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
cmap_nr = "bamako"  # "lapaz"
color_hl = "255/90/0"  # highlight -> orange | URG paper
radius_earth = 6371  # in kilometers

path_in = "01_in_data"
path_out = "02_out_figs"

nr_const_set = 1200
nr_cmap_max = nr_const_set - 1
nr_cb_afg = "a200f100"

histo_nr_max = nr_const_set
histo_region_max = 300000
histo_bin_width = 50
histo_frame_xa = 100

file_basic = "isoPREM_3Dani_6p3s_Nr1200_2000s_100km"
file_wfs = f"scanning_output_{file_basic}.nc"


# %%
# -----------------------------------------------------------------------------
# Load data of wavefield scanning / learning
# -----------------------------------------------------------------------------
for nr_type in ["input", "output"]:  ## "input", "output"

    ds_wfs = nc.Dataset(f"{path_in}/{file_wfs}")

    sz_temp = ds_wfs["pointwise_sz"][:]
    sz = np.array(sz_temp)

    match nr_type:
        case "input": nr_str = "starting_Nr_for_scanning"
        case "output": nr_str = "pointwise_Nr"

    Nr_temp = ds_wfs[nr_str][:]
    Nr_used = np.array(Nr_temp)

    Nr_min = np.min(Nr_used)
    Nr_max = np.max(Nr_used)
    Nr_mean = np.round(np.mean(Nr_used), 1)
    Nr_median = np.round(np.median(Nr_used), 1)
    Nr_sum = np.sum(Nr_used)

    array_wfs = np.zeros((len(sz), 3))

    for i_gp in range(len(sz)):
        array_wfs[i_gp, 0] = sz[i_gp, 0] / 1000  # Earth radius km
        array_wfs[i_gp, 1] = sz[i_gp, 1] / 1000
        array_wfs[i_gp, 2] = Nr_used[i_gp]


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------
    fig = gmt.Figure()
    gmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray50", FONT="8p")

    overrule_bg = False
    if nr_type == "output":
        gmt.config(COLOR_BACKGROUND=color_hl, COLOR_FOREGROUND=color_hl)
        overrule_bg = True
    gmt.makecpt(
        series=[0, nr_cmap_max, 1], cmap=cmap_nr, reverse=True, overrule_bg=overrule_bg
    )

    fig.plot(
        projection="X6c/12c",
        # half circle in Cartesian coordinates
        region=[0, radius_earth, -radius_earth, radius_earth],
        frame=["WSne", "a1000f500g500", "x+lkm", "y+lkm"],
        data=array_wfs,
        style="p0.2p",
        cmap=True,
    )

    with gmt.config(FONT="12p"):
        fig.colorbar(
            frame=[f"x{nr_cb_afg}+l{nr_str}","y+lNr"],
            position="JBC+h+w5c/0.3c+o-0.5c/1.6c+ef0.3c+ml",
        )

    fig.show()
    fig_name = f"{file_basic}_{nr_type}_SECTION"
    # for ext in ["png"]:  # "eps", "pdf"]:
    #     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
    print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Make histogram
# -----------------------------------------------------------------------------
    fig = gmt.Figure()
    gmt.config(FONT="11p", MAP_FRAME_PEN="0.5p", MAP_TICK_LENGTH_PRIMARY="3p")

    fig.histogram(
        region=[0, histo_nr_max + histo_bin_width, 0, histo_region_max],
        data=Nr_used,
        frame=["WSne", f"xa{histo_frame_xa}+lNr", "y+lCounts"],  # +a90+e
        series=histo_bin_width,
        fill="gray80",
        pen="0.5p,gray60",
        histtype=0,
        annotate="+r",
    )

    for i_y, Nr_text in enumerate([
        f"{file_basic}",
        f"{nr_str}",
        f"  - Nr_min = {Nr_min}",
        f"  - Nr_max = {Nr_max}",
        f"  - Nr_mean = {Nr_mean}",
        f"  - Nr_median = {Nr_median}",
        f"  - Nr_sum = {Nr_sum}",
    ]):

        font_add = ""
        fill = "gray97"
        if i_y == 0:
            font_add = ",Helvetica-Bold"
            fill = f"{color_hl}@85"
        pen = None
        if i_y in [0, 1]:
            pen = f"0.2p,{color_hl}"

        fig.text(
            position="TC",
            justify="TL",
            font=f"10p{font_add}",
            offset=f"1c/{-0.5 - 0.6 * i_y}c",
            text=Nr_text,
            pen=pen,
            fill=fill,
            clearance="0.1c+tO"
        )

    fig.show()
    fig_name = f"{file_basic}_{nr_type}_HISTOGRAM"
    # for ext in ["png"]:  # "eps", "pdf"]:
    #     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
    print(fig_name)
