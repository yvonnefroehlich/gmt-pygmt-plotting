# #############################################################################
# Hunga Tonga eruption on 2022/01/14-15
# -----------------------------------------------------------------------------
# History
# - Created: 2024/04/07
# - Updated: 2024/04/23 - Improve coding style
# - Updated: 2025/03/28 - Reorganize folder, rewrite code
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.14.2 -> https://www.pygmt.org/v0.14.2/ | https://www.pygmt.org/
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
fig_name = "02_tonga_eruption"  # Name of output figure
dpi_png = 360  # Resolution of output PNG
grid_res = "01m"  # Resolution of elevation grid
grid_reg = "g"  # Registration of elevation grid

# -----------------------------------------------------------------------------
# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

# -----------------------------------------------------------------------------
# Coordinates for
# Hunga Tonga volcano
lon_vulc = -175.393
lat_vulc = -20.545
# Seismological recording station BFO
lat_BFO = 48.331
lon_BFO = 8.330

# -----------------------------------------------------------------------------
# Define region
lon_min = -176  # degrees East
lon_max = -173
lat_min = -21.7  # degrees North
lat_max = -18.4
region = [lon_min, lon_max, lat_min, lat_max]

projection_main = "M12c"
projection_ortho = f"G{(lon_min + lon_max) / 2}/{(lat_min + lat_max) / 2}/?"

# -----------------------------------------------------------------------------
# Colors
color_water = "steelblue"
color_land = "gray70"
color_sl = "gray30"
color_pb = "216.750/82.875/24.990"  # -> darkorange
color_highlight = "255/90/0"  # -> orange

# -----------------------------------------------------------------------------
# Stuff for scale, legends, colorbars, and insets
basemap_scale = f"JLB+jLB+w50+c{(lon_max + lon_min) / 2}/{(lat_max + lat_min) / 2}+f+lkm+at+o0.45c/0.55c"

pos_study_inset = "jTL+w5c+o-1.5c/-1.2c"

pos_cb_grid = "JRB+jRB+w5c/0.25c+h+ml+o1c/0.65c+e"
frame_cb_grid = "+lelevation / m"

box_standard = "+gwhite@30+p0.5p,gray30+r0.1c"


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------

# Create new Figure instance
fig = gmt.Figure()
fig.basemap(region=region, projection=projection_main, frame=["wSnE", "af"])

# -----------------------------------------------------------------------------
# Download and plot elevation grid
fig.grdimage(grid=f"@earth_relief_{grid_res}_{grid_reg}", region=region, cmap="oleron")

# -----------------------------------------------------------------------------
# Plot plate boundaries after Bird 2003
fig.plot(data=f"{path_in}/plate_boundaries_Bird_2003.txt", pen=f"1p,{color_pb}")

# -----------------------------------------------------------------------------
# Add Hunga Tonga eruption

# Volcano
fig.plot(
    x=lon_vulc,
    y=lat_vulc,
    style="kvolcano/1c",  # self-defined symbol, read from file
    fill=color_highlight,
    pen="0.5p,gray30",
)
# Label
fig.text(
    x=lon_vulc,
    y=lat_vulc,
    text="Hunga Tonga-Hunga-Haapi",
    font="10p,Helvetica-Bold,black",
    offset="0.2c/-1c",
    fill="white@30",
    pen=f"0.8p,{color_highlight}",
    clearance="0.1c/0.1c+tO",
)
# Info text
# Adjust position in txt file
fig.text(
    textfiles=f"{path_in}/info_tonga.txt",
    M=True,  # paragraph mode # read from file
    font="8p,black",
    fill="white@30",
    clearance="0.1c/0.1c+tO",
    pen="0.5p,gray30",
)

# -----------------------------------------------------------------------------
# Plot colorbar for elevation
fig.colorbar(position=pos_cb_grid, frame=frame_cb_grid, box=box_standard)

# -----------------------------------------------------------------------------
# Add length scale
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
        pen="0.5p,gray30",
        fill=color_highlight,
    )

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()

# for ext in ["png"]:  # , "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)

print(fig_name)
