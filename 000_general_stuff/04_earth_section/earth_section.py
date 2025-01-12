# -*- coding: utf-8 -*-
# #############################################################################
# Earth section
# -----------------------------------------------------------------------------
# History
# - Created: 2025/01/12
# -----------------------------------------------------------------------------
# Versions
#   PyGMT v0.14.0 -> https://www.pygmt.org/v0.14.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"
fig_same_basic = "earth_section"

color_land = "bisque4"
color_water = "ivory"
color_shorelines = "navajowhite4"

color_land_kit = "76/181/167"
color_water_kit = "217/239/236"
color_shorelines_kit = "0/150/130"

pen_grid = "0.1p,gray80"
pen_map = "0.8p,gray30"
pen_sec = "0.01p,gray90"
pen_qua = "0.5p,gray30,dashed"



# %%
# -----------------------------------------------------------------------------
# Opened vertical
# -----------------------------------------------------------------------------
lon_min = -20
lon_max = 100
lat_lim = 89
x_sec = [lon_min, lon_max, lon_max, lon_min]
y_sec = [lat_lim, lat_lim, -lat_lim, -lat_lim]

fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY=pen_grid, MAP_FRAME_PEN=pen_map)

fig.coast(
    projection="G0/0/10c",
    region="g",
    frame="g10",
    land=color_land,
    water=color_water,
)

fig.plot(x=x_sec, y=y_sec, fill="gray55", pen=pen_map)

fig.plot(x=0.8, y=0, style="e90/8.0/2.7", pen=pen_sec, fill="gray65")
fig.plot(x=0.5, y=0, style="e90/5.0/1.9", pen=pen_sec, fill="gray75")
fig.plot(x=0.6, y=0, style="e90/2.5/1.2", pen=pen_sec, fill="gray85")

fig.plot(x=0, y=0, style="w10.0c/-90/90", pen=pen_sec, fill="gray60")
fig.plot(x=0, y=0, style="w8.0c/-90/90", pen=pen_sec, fill="gray70")
fig.plot(x=0, y=0, style="w5.0c/-90/90", pen=pen_sec, fill="gray80")
fig.plot(x=0, y=0, style="w2.5c/-90/90", pen=pen_sec, fill="gray90")

fig.basemap(frame=0)

fig.show()
fig_name = f"{fig_same_basic}_opened_vertical"
for ext in ["png"]:
    alpha_png = False
    if ext=="png": alpha_png = True
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=360, transparent=alpha_png)
print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Half vertical
# -----------------------------------------------------------------------------
lon_min = -20
lon_max = 100
lat_lim = 89
x_sec = [lon_min, lon_max, lon_max, lon_min]
y_sec = [lat_lim, lat_lim, -lat_lim, -lat_lim]

fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY=pen_grid, MAP_FRAME_PEN=pen_map)

fig.coast(
    projection="G0/0/10c",
    region="g",
    frame="g10",
    land=color_land,
    water=color_water,
)

fig.plot(x=x_sec, y=y_sec, fill="white")
fig.plot(x=0, y=0, style="w10c/-90/90", pen="1.5p,white", no_clip=True)

fig.plot(x=0, y=0, style="e90/10.0/3.6", pen=pen_map, fill="gray55", no_clip=True)
fig.plot(x=0, y=0, style="e90/8.0/2.7", pen=pen_sec, fill="gray65")
fig.plot(x=0, y=0, style="e90/5.0/1.9", pen=pen_sec, fill="gray75")
fig.plot(x=0, y=0, style="e90/2.5/1.2", pen=pen_sec, fill="gray85")

fig.show()
fig_name = f"{fig_same_basic}_half_vertical"
for ext in ["png"]:
    alpha_png = False
    if ext=="png": alpha_png = True
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=360, transparent=alpha_png)
print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Hafe horizontal
# -----------------------------------------------------------------------------
x_qua = [-10, -89, 90, 40]
y_qua = [90, 0, 0, 90]

fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY=pen_grid, MAP_FRAME_PEN="white")

fig.coast(
    projection="G0/20/10c",
    region="g",
    frame="g10",
    land=color_land,
    water=color_water,
)

fig.plot(x=x_qua, y=y_qua, fill="white", pen=None)

fig.plot(x=0, y=20, style="w10c/0/180", fill="white", pen="1.5p,white", no_clip=True)
fig.plot(x=0, y=20, style="w10c/-180/0", pen=pen_map, no_clip=True)

fig.plot(x=0, y=20, style="e0/10.0/3.6", pen=pen_map, fill="gray55", no_clip=True)
fig.plot(x=0, y=20, style="e0/8.0/2.7", pen=pen_sec, fill="gray65")
fig.plot(x=0, y=20, style="e0/5.0/1.9", pen=pen_sec, fill="gray75")
fig.plot(x=0, y=20, style="e0/2.5/1.2", pen=pen_sec, fill="gray85")

fig.show()
fig_name = f"{fig_same_basic}_half_horizontal"
for ext in ["png"]:
    alpha_png = False
    if ext=="png": alpha_png = True
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=360, transparent=alpha_png)
print(fig_name)
