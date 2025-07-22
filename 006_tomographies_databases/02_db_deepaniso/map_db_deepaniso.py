# #############################################################################
# Deep anisotropy database
#
# Wolf, J., Long, M. D., Li, M., & Garnero, E. (2023). Global compilation of
# deep mantle anisotropy observations and possible correlation with low velocity
# provinces. Geochemistry, Geophysics, Geosystems, 24, e2023GC011070.
# https://doi.org/10.1029/2023GC011070
#
# Data are available at https://github.com/wolfjonathan/Deep_Mantle_Anisotropy_Database
# -----------------------------------------------------------------------------
# History
# - Created: 2024/04/29
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.11.0 / v0.12.0 -> https://www.pygmt.org/
# - GMT 6.4.0 / 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import os

import pygmt as gmt


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
color_land = "gray95"
color_llpv = "brown"
pattern_llpv = "p8+b+f"


# %%
# -----------------------------------------------------------------------------
# Create global maps
# -----------------------------------------------------------------------------
folders_analysis = os.listdir(f"{path_in}/01_aniso/")

for analysis in folders_analysis:
    files_areas = os.listdir(f"{path_in}/01_aniso/{analysis}")

    color_aniso = "tan"
    if analysis == "SKS-SKKS":
        color_aniso = "darkorange"
    elif analysis == "S-ScS":
        color_aniso = "purple"

# -----------------------------------------------------------------------------
    fig = gmt.Figure()
    gmt.config(FONT_TITLE="12p", FONT_LABEL="10p")

    fig.coast(
        region="d",
        projection="N11c",
        land=color_land,
        shorelines=f"1/0.05p,{color_sl}",
        frame=f"+tLMM seismic anisotropy - {analysis}",
    )

# -----------------------------------------------------------------------------
    # Plate boundaries
    fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.1p,{color_pb}")

# -----------------------------------------------------------------------------
    # LLPV
    for i_model in range(2, 9, 1):
        fig.plot(
            data=f"{path_in}/02_llvp/3model_2016_{i_model}.txt",
            pen=f"0.2p,{color_llpv}",
            fill=f"{pattern_llpv}{color_llpv}",
            close=True,
        )

# -----------------------------------------------------------------------------
    # LMM Anisotropy
    for area in files_areas:
        fig.plot(
            data=f"{path_in}/01_aniso/{analysis}/{area}",
            pen="0.1p,gray10",
            fill=f"{color_aniso}@60",
            close=True,
        )

# -----------------------------------------------------------------------------
    # Map frame
    fig.basemap(frame=["WSnE", "xa90f30", "ya30f15"])

# -----------------------------------------------------------------------------
    fig.show()

    fig_name = f"{path_out}/deepaniso_{analysis}"
    # for ext in ["png"]:  # , "pdf", "eps"]:
    #     fig.savefig(fname=f"{fig_name}.{ext}")

    print(fig_name)
