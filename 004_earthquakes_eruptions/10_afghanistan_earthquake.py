# #############################################################################
# Afghanistan earthquake on 2025/08/31
# See also: https://earthquake.usgs.gov/earthquakes/eventpage/us7000qsvj/region-info
#           last accessed: 2025/09/01
#           https://earthquakeinsights.substack.com/p/deadly-m6-earthquake-strikes-northeastern
#           last accessed: 2025/09/01
# -----------------------------------------------------------------------------
# History
# - Created: 2025/09/01
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.16.0 -> https://www.pygmt.org/v0.16.0 | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# >>> Adjust for your needs <<<
fig_name = "10_afghanistan_earthquake"  # Name of output figure
dpi_png = 360  # Resolution of output PNG
grid_res = "30s"  # Resolution of elevation grid
grid_reg = "g"  # Registration of elevation grid

# -----------------------------------------------------------------------------
# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

# -----------------------------------------------------------------------------
# Define region and projections
lon_min = 60  # degrees East
lon_max = 85
lat_min = 26  # degrees North
lat_max = 45

region = [lon_min, lon_max, lat_min, lat_max]
center_str = f"{(lon_max + lon_min) / 2}/{(lat_max + lat_min) / 2}"

fig_width = 12  # in centimeters
projection_main = f"M{fig_width}c"  # Mercator
projection_ortho = f"G{center_str}/?"

y_min = 0  # in meters
y_max = 5000

# -----------------------------------------------------------------------------
# File name for plate boundaries after Bird 2003
file_pb = "plate_boundaries_Bird_2003.txt"

# File name for elevation grid
grid = f"@earth_relief_{grid_res}_{grid_reg}"

# -----------------------------------------------------------------------------
# Coordinates of epicenter
lon_eq = 70.734  # degrees East
lat_eq = 34.519  # degrees North

# -----------------------------------------------------------------------------
# Colors
color_water = "steelblue"
color_river = "steelblue4"
color_land = "gray70"
color_sl = "gray30"  # shorelines
color_pb = "216.750/82.875/24.990"  # plate boundaries -> darkorange
color_nb = "black"  # national boundaries
color_hl = "255/90/0"  # highlight -> orange

# -----------------------------------------------------------------------------
# Stuff for scale, legends, colorbars, and insets
basemap_scale = f"JLB+jLB+w200+c{center_str}+f+lkm+at+o4.2c/0.55c"

pos_cb_grid = "JRB+jRB+w5c/0.25c+h+ml+o0.7c/0.55c+e0.2c"
frame_cb_grid = "xa1000f500+lelevation / m"

pos_study_inset = "jTL+w3.5c+o-0.6c"

box_standard = "+gwhite@30+p0.5p,gray30+r0.1c"


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray30")

fig.basemap(region=region, projection=projection_main, frame=0)

# -----------------------------------------------------------------------------
# Download and plot elevation grid
gmt.makecpt(cmap="oleron", series=[y_min, y_max])
fig.grdimage(grid=grid, region=region, cmap=True, shading=True)

# -----------------------------------------------------------------------------
# Plot plate boundaries after Bird 2003
fig.plot(data=f"{path_in}/{file_pb}", pen=f"1p,{color_pb}")

# Plot national boundaries and rivers
fig.coast(borders=f"1/1p,{color_nb}", rivers=f"1/1p,{color_river}")
fig.coast(dcw=f"AF+p1p,{color_hl},2_4")

# -----------------------------------------------------------------------------
# Add colorbar for elevation
fig.colorbar(position=pos_cb_grid, frame=frame_cb_grid, box=box_standard)

# Add frame and length scale
with gmt.config(FONT="8p"):
    fig.basemap(map_scale=basemap_scale, box=box_standard, frame=["af", "wSnE"])

# -----------------------------------------------------------------------------
# Plot earthquake

# Epicenter
fig.plot(
    x=lon_eq,
    y=lat_eq,
    style=f"k{path_in}/earthquake.def/1c",
    fill=color_hl,
    pen=color_hl,
)
# Beachball
pen_epi = "0.5p,black"
fig.meca(
    spec=f"{path_in}/meca_afghanistan.txt",
    convention="aki",
    scale="1c",
    compressionfill=color_hl,  # fill color of compressive quadrants
    offset=pen_epi,
    outline=pen_epi,
)
# Label
fig.text(
    x=lon_eq,
    y=lat_eq,
    text="Jalālābād",
    font="8p,Helvetica-Bold,black",
    offset="-1.2c/0c",
    fill="white@30",
    pen=f"0.8p,{color_hl}",
    clearance="0.1c/0.1c+tO",
)

# Info text
# Adjust position in txt file
fig.text(
    textfiles=f"{path_in}/info_afghanistan.txt",
    M=True,  # paragraph mode # read from file
    font="8p,black",
    fill="white@30",
    clearance="0.1c/0.1c+tO",
    pen="0.5p,gray30",
)

# Plate names
fig.text(
    x=[73, 80],
    y=[30, 39],
    text=["India Plate", "Eurasia Plate"],
    font="6p,Helvetica-Bold,black",
    fill="white@30",
    clearance="0.05c/0.05c+tO",
)

# -----------------------------------------------------------------------------
# Inset map of study region

# Use with statement and context manager
with fig.inset(position=pos_study_inset):
    # >>> use ? <<<

    # Azimuthal orthographic projection
    # glon0/lat0[/horizon]/scale or Glon0/lat0[/horizon]/width
    #  - lon0/lat0: set projection center
    #  - horizon: maximum distance from projection center (in degrees, <= 90, default 90)
    #  - scale or width: set figure size
    fig.basemap(region="g", projection=projection_ortho, frame=0)
    fig.coast(
        area_thresh="50000",
        resolution="c",
        shorelines=color_sl,
        land=color_land,
        water=color_water,
    )
    fig.basemap(frame="g")

    # Plot rectangle at study area
    fig.plot(
        data=[[lon_min, lat_min, lon_max, lat_max]], style="r+s", pen=f"1p,{color_hl}"
    )
    fig.plot(x=lon_eq, y=lat_eq, style="c0.1c", fill=color_hl)

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
# for ext in ["png"]:  # , "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
