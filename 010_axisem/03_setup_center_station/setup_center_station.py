# #############################################################################
# Station-centered configuration for XKS phases (epicentral distance 120 deg)
# -----------------------------------------------------------------------------
# Related to
# - Fr�hlich Y., Ritter J. R. R. (2024) http://dx.doi.org/10.5281/zenodo.14510993
#   Vertical and Small-scale Lateral Varying Seismic Anisotropy in the Upper
#   Mantle Underneath the Upper Rhine Graben, Central Europe. Annual Meeting of
#   the American Geophysical Union. http://dx.doi.org/10.5281/zenodo.14510993.
# -----------------------------------------------------------------------------
# History
# - Created: 2025/01/26
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.14.0 -> https://www.pygmt.org/v0.14.0/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fr�hlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_out = "02_out_figs"
dpi_png = 720  # resolution of saved PNG file

# Location of source at North pole
center_lon = 0
center_lat = 89.999

proj_dist = 160
fig_width = 10
dist2fig = fig_width / proj_dist
proj_used = f"E{center_lon}/{center_lat}/{proj_dist}/{fig_width}c"

dist_ani = 40
center_args = {"x": center_lon, "y": center_lat}  # North pole
clearance_text = "0.05c/0.05c+tO"

color_ani = "gray50"
color_source = "red"
color_station = "gold"
color_land = "gray90"
color_sl = "gray70"
color_pb = "216.750/82.875/24.990"
color_highlight = "255/90/0"
alpha_highlight = 98  # in percentage


# %%
# -----------------------------------------------------------------------------
# Make epidistant map
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray70")

fig.basemap(region="d", projection=proj_used, frame=0)
fig.coast(shorelines=f"1/0.1p,{color_sl}", land=color_land, frame="fg")

# -----------------------------------------------------------------------------
# Region for anisotropy in the upper mantle
fig.plot(
    style=f"c{dist_ani * dist2fig}c",
    fill=f"{color_ani}@80",
    pen=f"0.5p,{color_ani}",
    **center_args,
)

# -----------------------------------------------------------------------------
# Station at North pole
fig.plot(style="i0.45c", fill=color_station, pen="0.2p,black", **center_args)
fig.text(
    text="North pole",
    offset="0/0.4c",
    fill="white@30",
    pen=f"0.2p,{color_station}",
    font="7p",
    clearance=clearance_text,
    **center_args,
)

# -----------------------------------------------------------------------------
# Epicentral distance 120°, i.e. latitude -30° N
fig.plot(
    style=f"w{90 * dist2fig}c/-90/270+i{150 * dist2fig}c",
    fill=f"{color_highlight}@{alpha_highlight}",
    **center_args,
)
for dist in [90, 150]:
    fig.plot(
        style=f"E-{dist * 2}+d",
        pen=f"0.5p,{color_highlight},dashed",
        **center_args,
    )
fig.plot(style=f"E-{120 * 2}+d", pen=f"1p,{color_highlight}", **center_args)

# -----------------------------------------------------------------------------
# Sources in steps of 30° E longitude
fig.plot(
    x=np.arange(-180, 151, 30),  # [min, max[, step
    y=np.full(12, -30),  # amount, value
    style="a0.4c",
    fill=color_source,
    pen="0.2p,black",
)

# Source S01 should be at longitude 0° E
sta_step = 30
x_all = np.arange(0, 360, sta_step)  # [start, end[, step
for i_st in range(1, len(x_all) + 1):  # [start, end[

    station = f"S{i_st}"
    if i_st < 10: station = f"S0{i_st}"

    angle = sta_step * (i_st - 1)
    if i_st > 3 and i_st < 11: angle = sta_step * (i_st - 1) + 180

    fig.text(
        x=x_all[i_st - 1],
        y=-17,
        text=f"{station}",
        angle=angle,
        fill="white@30",
        pen=f"0.2p,{color_source}",
        font="8p",
        clearance=clearance_text,
    )
    fig.text(
        x=x_all[i_st - 1],
        y=-43,
        text=f"{x_all[i_st - 1]}@.",
        angle=angle,
        fill=f"{color_highlight}@80",
        pen=f"0.2p,{color_highlight}",
        font="8p",
        clearance=clearance_text,
    )

# -----------------------------------------------------------------------------
# Add epicentral distance values
epi_dists = [40, 90, 120, 150]
for epi_dist in epi_dists:
    fig.text(
        x=15,
        y=90 - epi_dist,
        text=f"{epi_dist}@.",
        angle=15,
        fill="white@30",
        font="7p",
        clearance=clearance_text,
    )

# -----------------------------------------------------------------------------
# Add arrow to show workflow of simulations
fig.plot(
    # center x,y, radius, cc-hor dir_start,dir_end
    # [[ ]] important
    data=[[0, 90, 5.3, -65, -25]],
    style="m0.5c+ea+h0c",
    pen=f"1p,{color_highlight}",
    fill=color_highlight,
    no_clip=True,
)
fig.text(
    x=45,
    y=-88,
    text="BAZ",
    fill=f"{color_highlight}@80",
    pen=f"0.2p,{color_highlight}",
    font="8p",
    angle=45,
    clearance=clearance_text,
    no_clip=True,
)

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = "setup_center_station_XKS"
# for ext in ["png"]:  # "pdf", "eps"
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
