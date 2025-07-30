# #############################################################################
# Kamtschatka earthquake on 2025/07/29-30
# See also: https://earthquake.usgs.gov/earthquakes/eventpage/pt25210002/executive
#           last accessed: 2025/07/30
# -----------------------------------------------------------------------------
# History
# - Created: 2025/07/30
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

# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# >>> Adjust for your needs <<<
fig_name = "09_kamtschatka_earthquake"  # Name of output figure
dpi_png = 360  # Resolution of output PNG
grid_res = "03m"  # Resolution of elevation grid
grid_reg = "g"  # Registration of elevation grid

# -----------------------------------------------------------------------------
# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

# -----------------------------------------------------------------------------
# File name for plate boundaries after Bird 2003
file_pb = "plate_boundaries_Bird_2003.txt"

# -----------------------------------------------------------------------------
# Define region and projections
# Zoom around Kamtschatka
lon_min = 150  # degrees East
lon_max = 180
lat_min = 45   # degrees North
lat_max = 60
# With east coast of US
lon_min = 115  # degrees East
lon_max = 250
lat_min = 15   # degrees North
lat_max = 70
region = [lon_min, lon_max, lat_min, lat_max]
center_str = f"{(lon_max + lon_min) / 2}/{(lat_max + lat_min) / 2}"

projection_main = "M12c"  # Mercator
projection_ortho = f"G{center_str}/?"

# -----------------------------------------------------------------------------
# Coordinates of epicenter
lon_eq = 160.165  # degrees East
lat_eq = 52.530  # degrees North

# -----------------------------------------------------------------------------
# Colors
color_water = "steelblue"
color_land = "gray70"
color_sl = "gray30"
color_pb = "216.750/82.875/24.990"  # plate boundaries # -> darkorange
color_nb = "gray70"  # national boundaries
color_hl = "255/90/0"  # higlight -> orange

# -----------------------------------------------------------------------------
# Stuff for scale, legends, colorbars, and insets
basemap_scale = f"JLB+jLB+w1000+c{center_str}+f+lkm+at+o4c/0.7c"

pos_study_inset = "jTL+w3c+o-0.7c"

pos_cb_grid = "JRB+jRB+w5c/0.25c+h+ml+o0.7c+e"
frame_cb_grid = "xa2500f500+lelevation / m"

box_standard = "+gwhite@30+p0.5p,gray30+r0.1c"


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------

# Create new Figure() instance
fig = gmt.Figure()
fig.basemap(region=region, projection=projection_main, frame=["wSnE", "af"])

# -----------------------------------------------------------------------------
# Download and plot elevation grid
fig.grdimage(grid=f"@earth_relief_{grid_res}_{grid_reg}", region=region, cmap="oleron")

# -----------------------------------------------------------------------------
# Plot plate boundaries after Bird 2003
fig.plot(data=f"{path_in}/{file_pb}", pen=f"1p,{color_pb}")

# -----------------------------------------------------------------------------
# Plot national boundaries
fig.coast(borders=f"1/0.1p,{color_nb}")

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

"""
# Beachball
pen_epi = "0.5p,black"
fig.meca(
    spec=f"{path_in}/meca_kamtschatka.txt",
    convention="aki",
    scale="1c",
    compressionfill=color_hl,  # fill color of compressive quadrants
    offset=pen_epi,
    outline=pen_epi,
)
"""
# Label
fig.text(
    x=lon_eq,
    y=lat_eq,
    text="Kamtschatka",
    font="8p,Helvetica-Bold,black",
    offset="0c/-0.7c",
    fill="white@30",
    pen=f"0.8p,{color_hl}",
    clearance="0.1c/0.1c+tO",
)
# Info text
# Adjust position in txt file
fig.text(
    textfiles=f"{path_in}/info_kamtschatka.txt",
    M=True,  # paragraph mode # read from file
    font="8p,black",
    fill="white@30",
    clearance="0.1c/0.1c+tO",
    pen="0.5p,gray30",
)


# -----------------------------------------------------------------------------
# Add colorbar for elevation
fig.colorbar(position=pos_cb_grid, frame=frame_cb_grid, box=box_standard)

# -----------------------------------------------------------------------------
# Add length scale
with gmt.config(FONT="8p"):
    fig.basemap(map_scale=basemap_scale, box=box_standard)

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

    fig.coast(
        region="g",  # global
        projection=projection_ortho,
        area_thresh="50000",
        resolution="c",
        shorelines=color_sl,
        land=color_land,
        water=color_water,
        frame="g",
    )

    # Plot rectangle at study area
    fig.plot(
        data=[[lon_min, lat_min, lon_max, lat_max]],
        style="r+s",
        pen=f"1p,{color_hl}",
    )

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
# for ext in ["png"]:  # , "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
