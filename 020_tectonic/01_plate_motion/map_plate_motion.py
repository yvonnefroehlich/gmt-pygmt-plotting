# #############################################################################
# Maps of plate motion
# -----------------------------------------------------------------------------
# Usage of data calculated with
# - https://www.unavco.org/software/geodetic-utilities/plate-motion-calculator/plate-motion-calculator.html nehmen:
# - last access: 2024/06/08
#
# - GSRM v2.1 (2014) -> Kreemer, Blewitt, and Klein [2014]
# - MORVEL (2010) -> DeMets, Gordon, and Argus [2010]
#
# - DeMets, C., R.G. Gordon, and D.F. Argus, 2010. Geologically current plate motions,
#   Geophys. J. Int., 181, 1-80, https://doi.org/10.1111/j.1365-246X.2009.04491.x.
#   See also Erratum, 2011. Geophys. J. Int., 0, 1-1,
#   https://doi.org/10.1111/j.1365-246X.2011.05186.x.
# - Kreemer, C., G. Blewitt, and E.C. Klein, 2014. A geodetic plate motion and
#   Global Strain Rate Model, Geochemistry, Geophysics, Geosystems, 15, 3849-3889,
#   https://doi.org/10.1002/2014GC005407.
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
color_pb = "216.750/82.875/24.990"  # plate boundaries
color_sl = "gray40"  # shorelines

# Region and projection
args_basemap = {"region": "g", "projection": "N10c", "frame": 0}


# %%
# -----------------------------------------------------------------------------
# Data
# -----------------------------------------------------------------------------
# Plate velocity and direction
df_motion = pd.read_csv(f"{path_in}/plate_velocity_output.txt", sep=" ")

# Plate speed
speed = np.sqrt(
    df_motion["Evel_mmyr"] * df_motion["Evel_mmyr"] +
    df_motion["Nvel_mmyr"] * df_motion["Nvel_mmyr"]
)
df_motion["speed_mmyr"] = speed

# Plate boundaries
file_pb = "plate_boundaries_Bird_2003.txt"

# -----------------------------------------------------------------------------
# Colormaps
cmap_speed = "batlow"
cmap_speed_out = f"{path_in}/{cmap_speed}_speed.cpt"
pygmt.makecpt(cmap=cmap_speed, series=[0, 80], output=cmap_speed_out)

cmap_velocity = "vik"
cmap_velocity_out = f"{path_in}/{cmap_velocity}_velocity.cpt"
pygmt.makecpt(cmap=cmap_velocity, series=[-80, 80], output=cmap_velocity_out)


# %%
# -----------------------------------------------------------------------------
# Create maps of plate motion
# -----------------------------------------------------------------------------
fig = pygmt.Figure()

for motion, cb_label in zip(
    ["Evel_mmyr", "Nvel_mmyr", "speed_mmyr"],
    ["plate East velocity", "plate North velocity", "plate speed"]
):

    cmap = cmap_velocity_out
    if motion=="speed_mmyr":
        cmap = cmap_speed_out

    fig.basemap(**args_basemap)

    fig.plot(
        x=df_motion["longitude_degE"],
        y=df_motion["latitude_degN"],
        fill=df_motion[motion],
        style="c0.07c",
        cmap=cmap,
    )
    fig.colorbar(cmap=cmap, frame=[f"xa20f5+l{cb_label}", "y+lmm/yr"])

    fig.coast(shorelines=f"1/0.01p,{color_sl}")
    fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.3p,{color_pb}")

    fig.basemap(frame=["WnSe", "af"])

    fig.shift_origin(xshift="w+1c")
    if motion=="Nvel_mmyr":
        fig.shift_origin(xshift="-1.5w-1.5c", yshift="-h-3c")

# -----------------------------------------------------------------------------
fig.show()
fig_name = "map_plate_motion"
# for ext in ["png"]:  # , "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)
