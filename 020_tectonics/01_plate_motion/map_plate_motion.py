# #############################################################################
# Maps of plate motion
# -> for creating the intput file see create_ngf_plate_motion_calculator_INPUT.py
# -----------------------------------------------------------------------------
# Data calculated with
# - https://www.unavco.org/software/geodetic-utilities/plate-motion-calculator/plate-motion-calculator.html
# - last access: 2024/06/08
# - model GSRM v2.1 (2014) -> Kreemer, Blewitt, Klein (2014)
#
# - DeMets C, Gordon R G, Argus D F (2010). Geologically current plate motions.
#   Geophysical Journal International, 181(1), 1-80.
#   https://doi.org/10.1111/j.1365-246X.2009.04491.x
#   See also Erratum (2011). Geophysical Journal International, 187(1), 538-538.
#   https://doi.org/10.1111/j.1365-246X.2011.05186.x.
# - Kreemer C, Blewitt G, Klein E C (2014). A geodetic plate motion and Global
#   Strain Rate Model. Geochemistry, Geophysics, Geosystems, 15, 3849-3889.
#   https://doi.org/10.1002/2014GC005407
# -----------------------------------------------------------------------------
# History
# - Created: 2024/06/08
# - Updated: 2026/08/25 - Adjusted for GitHub
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.19.0 -> https://www.pygmt.org
# - GMT 6.7.0 -> https://www.generic-mapping-tools.org
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################

import numpy as np
import pandas as pd
import pygmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"

# Colors
color_hl = "255/90/0"  # -> orange
color_pb = "216.750/82.875/24.990"  # plate boundaries
color_sl = "gray40"  # shorelines


# %%
# -----------------------------------------------------------------------------
# Data
# -----------------------------------------------------------------------------
# Plate velocity and direction
model = "GSRMv2.1"  # GSRMv2.1 | ITRF2020 | for other models create your own files
file_pm = f"ngf_plate_motion_calculator_OUTPUT_Dlon2deg_Dlat2deg_ele0m_{model}.txt"
df_motion = pd.read_csv(f"{path_in}/{file_pm}", sep=" ")

# Plate speed
speed = np.sqrt(
    df_motion["Evel_mmyr"] * df_motion["Evel_mmyr"] +
    df_motion["Nvel_mmyr"] * df_motion["Nvel_mmyr"]
)
df_motion["speed_mmyr"] = speed

# Plate boundaries
file_pb = "plate_boundaries_Bird_2003.txt"


# %%
# -----------------------------------------------------------------------------
# Create maps of plate motion
# -----------------------------------------------------------------------------
fig = pygmt.Figure()

for motion, cb_label, wsne in zip(
    ["Evel_mmyr", "Nvel_mmyr", "speed_mmyr"],
    ["plate East velocity", "plate North velocity", "plate speed"],
    ["WSne", "wSnE", "WSnE"]
):

    pygmt.makecpt(cmap="vik", series=[-80, 80])
    if motion=="speed_mmyr":
        pygmt.makecpt(cmap="acton", series=[0, 80], reverse=True)

    fig.basemap(region="g", projection="N10c", frame=0)

    fig.plot(
        x=df_motion["longitude_degE"],
        y=df_motion["latitude_degN"],
        fill=df_motion[motion],
        style="c0.07c",
        cmap=True,
    )
    fig.colorbar(frame=[f"xa20f5+l{cb_label}", "y+lmm/yr"])

    fig.coast(shorelines=f"1/0.01p,{color_sl}")
    fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.3p,{color_pb}")

    if motion == "Evel_mmyr":
        fig.text(
            text=model,
            position="BR",
            justify="TC",
            offset=(0.5, 0),
            font=f"12p,1,{color_hl}",
            no_clip=True,
        )

    fig.basemap(frame=[wsne, "af"])

    fig.shift_origin(xshift="w+1c")
    if motion=="Nvel_mmyr":
        fig.shift_origin(xshift="-1.5w-1.5c", yshift="-h-2.5c")

# -----------------------------------------------------------------------------
fig.show()
fig_name = f"map_plate_motion_{model}"
for ext in ["png"]:  # , "pdf", "eps"]:
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)
