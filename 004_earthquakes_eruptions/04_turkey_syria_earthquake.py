# #############################################################################
# Turkey Syria earthquakes on 2023/02/06 up on 01:17:35 (UTC)
# -----------------------------------------------------------------------------
# History
# - Created: 2024/04/07
# - Updated: 2024/04/23 - Improve coding style
# - Updated: 2025/03/28 - Reorganize folder, rewrite code
# - Updated: 2026/02/04 - Use parameter names of PyGMT v0.18.0
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.18.0 -> https://www.pygmt.org | https://www.pygmt.org
# - GMT 6.6.0 -> https://www.generic-mapping-tools.org
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
fig_name = "04_turkey_syria_earthquake"  # Name of output figure
dpi_png = 360  # Resolution of output PNG
grid_res = "01m"  # Resolution of elevation grid
grid_reg = "g"  # Registration of elevation grid

# -----------------------------------------------------------------------------
# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

# -----------------------------------------------------------------------------
# File name for plate boundaries after Bird 2003
file_pb = "plate_boundaries_Bird_2003.txt"

# -----------------------------------------------------------------------------
# Earthquakes
label_eq = ["1", "2", "3", "4"]

lon_eq = [37.042, 36.943, 37.203, 36.537]  # degrees East
lat_eq = [37.166, 37.127, 38.024, 38.061]  # degrees North

lon_eq_min = [37.0252, 36.5658, 37.121, 36.3222]  # degrees East
lat_eq_min = [37.0996, 37.0762, 38.0144, 38.0366]  # degrees North

# -----------------------------------------------------------------------------
# Define region and projections
lon_min = 35  # degrees East
lon_max = 40
lat_min = 36  # degrees North
lat_max = 40
region = [lon_min, lon_max, lat_min, lat_max]
center_str = f"{(lon_min + lon_max) / 2}/{(lat_min + lat_max) / 2}"

# Main map
project_main = "M15c"  # Mercator projection, 15 cm width
# Inset map - study region - Orthographic projection
project_ortho = f"G{center_str}/?"

# -----------------------------------------------------------------------------
# Colors
color_water = "steelblue"
color_land = "gray70"
color_sl = "gray30"  # shorelines
color_pb = "216.750/82.875/24.990"  # plate boundaries # -> darkorange
color_highlight = "255/90/0"  # -> orange
pen_epi = "0.5p,black"

# -----------------------------------------------------------------------------
# Stuff for scale, legends, colorbars, and insets
basemap_scale = f"JLB+jLB+w100+c{center_str}+f+lkm+at+o0.7c"

pos_study_inset = "jTL+w5c+o-1c"

pos_cb_grid = "JRB+jRB+w5c/0.25c+h+ml+o0.7c+e"
frame_cb_grid = "+lelevation / m"

box_standard = "+gwhite@30+p0.5p,gray30+r0.1c"


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------

# Create new Figure() instance
fig = gmt.Figure()
fig.basemap(region=region, projection="M15c", frame=["wSnE", "a1f0.5"])

# -----------------------------------------------------------------------------
# Download and plot elevation grid
fig.grdimage(grid=f"@earth_relief_{grid_res}_{grid_reg}", region=region, cmap="oleron")

# -----------------------------------------------------------------------------
# Plot plate boundaries after Bird 2003
fig.plot(data=f"{path_in}/{file_pb}", pen=f"1p,{color_pb}")

# -----------------------------------------------------------------------------
# Plot earthquakes

# Epicenter
fig.plot(
    x=lon_eq,
    y=lat_eq,
    style=f"k{path_in}/earthquake.def/1.3c",
    fill=color_highlight,
    pen=color_highlight,
)
# Beachball
fig.meca(
    spec=f"{path_in}/meca_turkeysyria.txt",
    convention="aki",
    scale="1c",
    outline=pen_epi,
    compression_fill=color_highlight,  # PyGMT v0.18.0
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
    textfiles=f"{path_in}/info_turkeysyria.txt",
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
        projection=project_ortho,
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

# for ext in ["png"]:  # , "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)

print(fig_name)
