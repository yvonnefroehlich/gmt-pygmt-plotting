# #############################################################################
# La Palma eruptions between 2021/09/19 and 2021/12/13
# -----------------------------------------------------------------------------
# History
# - Created 2024/04/07
# - Updated 2024/04/23: Improve coding style
# - Updated 2025/03/28: Reorganize folder, rewrite code
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
# >>> Set for your needs <<<
fig_name = "01_la_palma_eruption"  # Name of output figure
dpi_png = 360  # Resolution of output PNG
grid_res = "01m"  # Resolution of elevation grid
grid_reg = "g"  # Registration of elevation grid

# -----------------------------------------------------------------------------
# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

# -----------------------------------------------------------------------------
# Coordinates for La Palma volcano
lon_volc = -17.84
lat_volc = 28.57

# -----------------------------------------------------------------------------
# Define region and projectins
lon_min = -19  # degrees East
lon_max = -15
lat_min = 27  # degrees West
lat_max = 30
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

pos_study_inset = "jTL+w4.5c+o-1c/-0.5c"

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

fig.show()


# %%
# -----------------------------------------------------------------------------
# Plot plate boundaries after Bird 2003
fig.plot(data=f"{path_in}/plate_boundaries_Bird_2003.txt", pen=f"1p,{color_pb}")

fig.show()


# %%
# -----------------------------------------------------------------------------
# Add LaPalma eruption

# Volcano
fig.plot(
    x=lon_volc, y=lat_volc, style="kvolcano/1c", fill=color_highlight, pen="0.5p,gray30"
)
# Label
fig.text(
    x=lon_volc,
    y=lat_volc,
    text="Cumbre Vieja",
    font="8p,Helvetica-Bold,black",
    offset="0c/-1c",
    fill="white@30",
    pen=f"0.8p,{color_highlight}",
    clearance="0.1c/0.1c+tO",
)
# Info text
# Adjust position in txt file
fig.text(
    textfiles=f"{path_in}/info_lapalma.txt",
    M=True,  # paragraph mode # read from file
    font="8p,black",
    fill="white@30",
    clearance="0.1c/0.1c+tO",
    pen="0.5p,gray30",
)

fig.show()


# %%
# -----------------------------------------------------------------------------
# Add colorbar for the colormap of the elevation
fig.colorbar(position=pos_cb_grid, frame=frame_cb_grid, box=box_standard)

fig.show()


# %%
# -----------------------------------------------------------------------------
# Add length scale
fig.basemap(map_scale=basemap_scale, box=box_standard)

fig.show()


# %%
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
        projection=projection_ortho,
        area_thresh="50000",
        resolution="c",
        shorelines=color_sl,
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

fig.show()


# %%
# -----------------------------------------------------------------------------
# Finally you can let the figure be displayed inside your IDE or outside of
# it by setting the "method" parameter to "external" as well save it to a PDF
# or PNG file giving a filename via the "fname" parameter and a resolution
# passed to the "dpi" parameter
fig.show()

for ext in ["png"]:  # , "pdf", "eps"]:
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)

print(fig_name)
