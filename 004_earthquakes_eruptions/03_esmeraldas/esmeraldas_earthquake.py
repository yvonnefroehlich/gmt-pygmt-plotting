# #############################################################################
# Esmeraldas earthquake on 2022/03/27 at 04:28:12 (UTC)
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
# >>> Set for your needs <<<
fig_name = "esmeraldas_earthquake"  # Name of output figure
png_dpi = 360  # Resolution of output png
grid_res = "01m"  # Resolution of elevation grid
grid_reg = "g"  # Registration of elevation grid

# -----------------------------------------------------------------------------
# Coordinates for
# Esmeraldas earthquake
lon_eq = -79.611
lat_eq = 0.904
# Seismological recording station Black Forest Observatory (BFO)
lat_BFO = 48.331
lon_BFO = 8.330

# -----------------------------------------------------------------------------
# Define region and projection
lon_min = -85.00  # degrees East
lon_max = -75.00
lat_min = -5.00  # degrees North
lat_max = 5.00

project_main = "M15c"  # Mercator
project_study = f"G{(lon_min + lon_max) / 2}/{(lat_min + lat_max) / 2}/?"
project_epi = f"E{lon_BFO}/{lat_BFO}/160/?"

# -----------------------------------------------------------------------------
# File name for plate boundaries after Bird 2003
file_plate_in = "plate_boundaries_Bird_2003.txt"

# -----------------------------------------------------------------------------
# Colors
color_water = "steelblue"
color_land = "gray70"
color_shorelines = "gray50"
color_sta = "gold"
color_plate = "216.750/82.875/24.990"  # -> darkorange
color_highlight = "255/90/0"  # -> orange

# -----------------------------------------------------------------------------
# Stuff for scale, legends, colorbars, and insets
rad_tot = 6.0
fac_rad_epi90 = 3.0 / 5.5
fac_rad_epi140 = 4.7 / 5.5

pos_study_inset = "jTL+w5c+o-0.5c/-0.5c"
pos_epi_inset = f"JMR+jMR+w{rad_tot}c"

pos_cb_grid = "JRB+jRB+w5c/0.25c+h+ml+o1c/0.65c+e"
frame_cb_grid = "+lelevation / m"

box_standard = "+gwhite@30+p0.5p,gray30+r0.1c"
clearance_standard = "0.1c/0.1c+tO"


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------

# Create new Figure instance
fig = gmt.Figure()

# -----------------------------------------------------------------------------
# Change default values of GMT globally
gmt.config(
    PS_MEDIA="A4",
    PS_PAGE_ORIENTATION="portrait",
    MAP_FRAME_TYPE="fancy+",  # map frame style
    MAP_FRAME_WIDTH="3p",  # thickness of map frame
    FONT_LABEL="7p",
    FONT_ANNOT_PRIMARY="7p",
    MAP_FRAME_PEN="0.8p",  # thickness of border around scale
    MAP_ANNOT_OFFSET="0.05i",  # distance of scale ticks labels from scale
    MAP_LABEL_OFFSET="3.5p",  # distance of label from scale
    MAP_TICK_LENGTH_PRIMARY="5p",  # length of scale ticks
    COLOR_NAN="white",  # color for NaN; default 127.5
)

# -----------------------------------------------------------------------------
# Elevation grid
# Use grid provided by GMT and cut region
grid_topo = gmt.grdcut(
    grid=f"@earth_relief_{grid_res}_{grid_reg}",
    region=[lon_min, lon_max, lat_min, lat_max],
    projection=project_main,
)

fig.grdimage(grid=grid_topo, cmap="oleron", frame=["wSnE", "af"])

# -----------------------------------------------------------------------------
# Plot plate boundaries
fig.plot(data=file_plate_in, pen=f"1p,{color_plate}")

# -----------------------------------------------------------------------------
# Plot earthquake

# Epicenter
fig.plot(
    x=lon_eq,
    y=lat_eq,
    style="a1c",
    fill=color_highlight,
    pen="0.5p,gray30",
)
# Beachball
fig.meca(
    spec="meca_esmeraldas.txt",
    convention="aki",
    scale="1c",
    outline="0.5p,black",
    compressionfill=color_highlight,  # fill color of compressive quadrants
)
# Label
fig.text(
    x=lon_eq,
    y=lat_eq,
    text="Esmeraldas",
    font="12p,Helvetica-Bold,black",
    offset="-0.7c/-1.2c",
    fill="white@30",
    pen=f"0.8p,{color_highlight}",
    clearance="0.1c/0.1c+tO",
)
# Info text
# Adjust position in txt file
fig.text(
    textfiles="info_esmeraldas.txt",
    M=True,  # paragraph mode # read from file
    font="8p,black",
    fill="white@30",
    clearance="0.1c/0.1c+tO",
    pen="0.5p,gray30",
)

# -----------------------------------------------------------------------------
# Add colorbar for elevation
gmt.config(MAP_TICK_LENGTH_PRIMARY="2p")

fig.colorbar(
    position=pos_cb_grid,
    frame=frame_cb_grid,
    box=box_standard,
)

# -----------------------------------------------------------------------------
# Add length scale
gmt.config(MAP_SCALE_HEIGHT="7p")

basemap_scale = f"JLB+jLB+w200+c{(lon_max + lon_min) / 2}/{(lat_max + lat_min) / 2}" + \
                "+f+lkm+at+o0.45c/0.55c"

fig.basemap(
    map_scale=basemap_scale,
    box=box_standard,  # Box around map scale
)

# -----------------------------------------------------------------------------
# Inset map of study region
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
        resolution="c",
        area_thresh=50000,
        shorelines=f"1/0.01p,{color_shorelines}",
        land=color_land,
        water=color_water,
        frame="g",
    )

    fig.plot(
        data=[[lon_min, lat_min, lon_max, lat_max]],
        style="r+s",
        pen=f"2p,{color_highlight}",
    )

# -----------------------------------------------------------------------------
# Inset equal distance to show epicenter
with fig.inset(position=pos_epi_inset):

    # >>> use ? <<<

    # Azimuthal equidistant projection
    # - elon0/lat0[/horizon]/scale
    # - Elon0/lat0[/horizon]/width
    # - horizon max. distance to the projection center
    #   i.e. the visible portion of the rest of the world map
    #   in degrees <= 180° (default 180°)

    fig.coast(
        region="g",
        projection=project_epi,
        resolution="c",
        area_thresh=50000,
        shorelines=f"1/0.01p,{color_shorelines}",
        land=color_land,
        water="white",
        frame="f",
    )

    # Plate boundaries
    fig.plot(data=file_plate_in, pen=f"0.5p,{color_plate}")

# -----------------------------------------------------------------------------
    # Epicentral distance range for XKS phases
    epi_min = 90
    epi_max = 150

    for epi_limit in [epi_min, epi_max]:

        if epi_limit==epi_min: offset_station_label = "0c/-1.7c"
        elif epi_limit==epi_max: offset_station_label = "0c/-2.7c"

        # Circles
        fig.plot(
            x=lon_BFO,
            y=lat_BFO,
            style=f"E-{epi_limit*2}+d",
            pen=f"1p,{color_sta},-",
        )
        # Annotations
        fig.text(
            x=lon_BFO,
            y=lat_BFO,
            offset=offset_station_label,
            text=f"{epi_limit}@.",
            font="8p,black",
            fill="white@30",
            pen=f"0.5p,{color_sta}",
            clearance=clearance_standard,
        )

# -----------------------------------------------------------------------------
    # Epicenter
    fig.plot(
        x=lon_eq,
        y=lat_eq,
        style="kearthquake.def/1.3c",
        fill=color_highlight,
        pen=color_highlight,
    )

# -----------------------------------------------------------------------------
    # Recording station BFO

    # Marker
    fig.plot(x=lon_BFO, y=lat_BFO, style="i0.50c", fill=color_sta, pen="0.5p,black")

    # Label
    fig.text(
        x=lon_BFO,
        y=lat_BFO,
        offset="0c/-0.6c",
        text="BFO",
        font="9p,Helvetica,black",
        fill="white@30",
        pen=f"0.7p,{color_sta}",
        clearance=clearance_standard,
    )

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()

# for ext in ["png"]: # , "pdf", "eps"]:
#     fig.savefig(fname=f"{fig_name}.{ext}")

print(png_dpi)
