# #############################################################################
# Turkey Syria earthquakes on 2023/02/06 up on 01:17:35 (UTC)
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/04/07
#   PyGMT v0.11.0 -> https://www.pygmt.org/v0.11.0/ | https://www.pygmt.org/
#   GMT 6.4.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


import pygmt as gmt


# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# >>> Adjust your needs <<<
fig_name = "turkey_syria_earthquake"  # Name of output figure
png_dpi = 360  # Resolution of output png
grid_res = "01m"  # Resolution of elevation grid
grid_reg = "g"  # Registration of elevation grid

# -----------------------------------------------------------------------------
# Earthquakes
label_eq = ["1", "2", "3", "4"]

lon_eq = [37.042, 36.943, 37.203, 36.537]  # degrees East
lat_eq = [37.166, 37.127, 38.024, 38.061]  # degrees North

lon_eq_min = [37.0252, 36.5658, 37.121, 36.3222]  # degrees East
lat_eq_min = [37.0996, 37.0762, 38.0144, 38.0366]  # degrees North

# -----------------------------------------------------------------------------
# Define region and projection
lon_min = 35  # degrees East
lon_max = 40
lat_min = 36  # degrees North
lat_max = 40

# Main map
project_main = "M15c"  # Mercator projection, 15 cm width
# Inset map - study region - rthographic projection
project_study = f"G{(lon_min + lon_max) / 2}/{(lat_min + lat_max) / 2}/?"

# -----------------------------------------------------------------------------
# Colors
color_water = "steelblue"
color_land = "gray70"
color_shorelines = "gray30"
color_plate = "216.750/82.875/24.990"  # -> darkorange
color_highlight = "255/90/0"  # -> orange
pen_epi = "0.5p,black"

# -----------------------------------------------------------------------------
# Stuff for scale, legends, colorbars, and insets
pos_study_inset = "jTL+w5.5c+o-1c/-1c"

pos_cb_grid = "JRB+jRB+w5c/0.25c+h+ml+o1c/0.65c+e"
frame_cb_grid = "+lelevation / m"

box_standard = "+gwhite@30+p0.5p,gray30+r0.1c"


#%%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------

# Create new Figure() instance
fig = gmt.Figure()

# -----------------------------------------------------------------------------
# Change default values of GMT globally
gmt.config(
    PS_MEDIA="A4",
    PS_PAGE_ORIENTATION="portrait",
    MAP_FRAME_TYPE="fancy+",  # map frame style
    MAP_FRAME_WIDTH="3p",  # thickness of map frame
    FONT_LABEL="9p",
    FONT_ANNOT_PRIMARY="9p",
    MAP_FRAME_PEN="0.8p",  # thickness of border around scale
    MAP_ANNOT_OFFSET="0.05i",  # distance of scale ticks labels from scale
    MAP_LABEL_OFFSET="3.5p",  # distance of label from scale
    MAP_TICK_LENGTH_PRIMARY="5p",  # length of scale ticks
)

# -----------------------------------------------------------------------------
# Plot elevation grid
# Use grid provided by gmt and cut region
grid_ele = gmt.grdcut(
    grid=f"@earth_relief_{grid_res}_{grid_reg}",
    region=[lon_min, lon_max, lat_min, lat_max],
    projection=project_main,
)

fig.grdimage(grid=grid_ele, cmap="oleron", frame=["wSnE", "a1f0.5"])

# -----------------------------------------------------------------------------
# Plot plate boundaries after Bird 2003
fig.plot(data="plate_boundaries_Bird_2003.txt", pen=f"1p,{color_plate}")

# -----------------------------------------------------------------------------
# Plot earthquakes

# Epicenter
fig.plot(
    x=lon_eq,
    y=lat_eq,
    style="kearthquake.def/1.3c",
    fill=color_highlight,
    pen=color_highlight,
)
# Beachball
fig.meca(
    spec="meca_turkeysyria.txt",
    convention="aki",
    scale="1c",
    outline=pen_epi,
    compressionfill=color_highlight,  # fill color of compressive quadrants
    offset=pen_epi,
)
# Label
fig.text(
    x=lon_eq,
    y=lat_eq,
    text=label_eq,
    font="12p,Helvetica-Bold,black",
    offset="0c/-0.8c",
    fill="white@30",
    pen="0.8p,black",
    clearance="0.1c/0.1c+tO",
)
# Info text
# Adjust position in txt file
fig.text(
    textfiles="info_turkeysyria.txt",
    M=True,  # paragraph mode # read from file
    font="8p,black",
    fill="white@30",
    clearance="0.1c/0.1c+tO",
    pen="0.5p,gray30",
)

# -----------------------------------------------------------------------------
# Add colorbar for elevation
gmt.config(MAP_TICK_LENGTH_PRIMARY="2p")

fig.colorbar(position=pos_cb_grid, frame=frame_cb_grid, box=box_standard)

# -----------------------------------------------------------------------------
# Add length scale
gmt.config(MAP_SCALE_HEIGHT="7p")

basemap_scale = f"JLB+jLB+w100+c{(lon_max + lon_min) / 2}/{(lat_max + lat_min) / 2}" + \
                "+f+lkm+at+o0.6c/0.6c"

fig.basemap(map_scale=basemap_scale, box=box_standard)

# -----------------------------------------------------------------------------
# Inset - study region
with fig.inset(position=pos_study_inset):

    # >>> use ? <<<

    # Orthographic projection
    # glon0/lat0[/horizon]/scale or Glon0/lat0[/horizon]/width
    #  - lon0 and lat0 projection center
    #  - horizon maximum distance from projection center (in degrees, <= 90, default 90)
    #  - scale and width figure size

    fig.coast(
        region="g",
        projection=project_study,
        area_thresh="50000",
        resolution="c",
        shorelines="black",
        land=color_land,
        water=color_water,
        frame="g",
    )

    fig.plot(
        data=[[lon_min, lat_min, lon_max, lat_max]],
        style="r+s",
        pen="0.5p,gray30",
        fill=color_highlight,
    )

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()

for ext in ["png"]: # , "pdf", "eps"]:
    fig.savefig(fname=f"{fig_name}.{ext}")

print(fig_name)
