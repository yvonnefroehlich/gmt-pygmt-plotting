# #############################################################################
# Kamtschatka earthquake on 2025/07/29-30
# See also: https://earthquake.usgs.gov/earthquakes/eventpage/pt25210002/executive
#           last accessed: 2025/07/31
# -----------------------------------------------------------------------------
# History
# - Created: 2025/07/30
# - Updated: 2025/08/03 - add profile for elevation
# - Updated: 2025/08/04 - fix profile for elevation, add plate names and motion direction
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


# %%
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
# Define region and projections
lon_min = 115  # degrees East
lon_max = 250
lat_min = 15  # degrees North
lat_max = 70

region = [lon_min, lon_max, lat_min, lat_max]
center_str = f"{(lon_max + lon_min) / 2}/{(lat_max + lat_min) / 2}"

fig_width = 12  # in centimeters
projection_main = f"M{fig_width}c"  # Mercator
projection_ortho = f"G{center_str}/?"

y_min = -8000  # in meters
y_max = 3000

# -----------------------------------------------------------------------------
# File name for plate boundaries after Bird 2003
file_pb = "plate_boundaries_Bird_2003.txt"

# File name for elevation grid
grid = f"@earth_relief_{grid_res}_{grid_reg}"

# -----------------------------------------------------------------------------
# Coordinates of epicenter
lon_eq = 160.324  # degrees East
lat_eq = 52.512  # degrees North

# -----------------------------------------------------------------------------
# Colors
color_water = "steelblue"
color_land = "gray70"
color_sl = "gray30"
color_pb = "216.750/82.875/24.990"  # plate boundaries -> darkorange
color_nb = "gray70"  # national boundaries
color_hl = "255/90/0"  # highlight -> orange
color_profile = "darkblue"

# -----------------------------------------------------------------------------
# Stuff for scale, legends, colorbars, and insets
basemap_scale = f"JLB+jLB+w1000+c{center_str}+f+lkm+at+o4c/0.7c"

pos_study_inset = "jBL+w3.5c+o-0.7c/-2c"

pos_cb_grid = "JRB+jRB+w5c/0.25c+h+ml+o0.7c+e0.2c"
frame_cb_grid = "xa2500f500+lelevation / m"

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
fig.grdimage(grid=grid, region=region, cmap=True)

# -----------------------------------------------------------------------------
# Plot plate boundaries after Bird 2003
fig.plot(data=f"{path_in}/{file_pb}", pen=f"1p,{color_pb}")

# Plot national boundaries
fig.coast(borders=f"1/0.1p,{color_nb}")

# Add frame
fig.basemap(frame=["wSnE", "xa20f5g10", "ya10f5g10"])

# Add lines
fig.hlines(y=lat_eq, pen=f"1p,{color_profile}")
fig.vlines(x=lon_eq, pen=f"1p,{color_hl},4_2")

# -----------------------------------------------------------------------------
# Add colorbar for elevation
fig.colorbar(position=pos_cb_grid, frame=frame_cb_grid, box=box_standard)

# Add length scale
with gmt.config(FONT="8p"):
    fig.basemap(map_scale=basemap_scale, box=box_standard)

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
    spec=f"{path_in}/meca_kamtschatka.txt",
    convention="aki",
    scale="1c",
    compression_fill=color_hl,  # PyGMT v0.18.0
    offset=pen_epi,
    outline=pen_epi,
)

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

# Plate names
fig.text(
    x=[152, 153, 182],
    y=[55.5, 33, 56],
    text=["Okhotsk Microplate", "Pazific Plate", "North American Plate"],
    angle=[55, 50, 0],
    font="6p,Helvetica-Bold,black",
    fill="white@30",
    clearance="0.05c/0.05c+tO",
)

# Plate motion direction
fig.plot(
    data=[[150.5, 35, 137, 0.6], [157.5, 40.5, 137, 0.6]],
    style="v0.3c+e+h0.1+a45",
    pen=f"3p,{color_hl}",
    fill=color_hl,
)

# -----------------------------------------------------------------------------
# profile plot elevation
fig.shift_origin(yshift="+h+0.4c")

lon0 = 180
total_lon = lon_max - lon_min
lon2width = fig_width / total_lon

for side in ["left", "right"]:

    match side:
        case "left":
            lon_start = lon_min
            lon_end = lon0
            delta_lon = lon0 - lon_min
        case "right":
            lon_start = -(lon0 - 0.001)
            lon_end = -(360 - lon_max)
            delta_lon = lon_max - lon0

    # Generate points along a great circle corresponding to the survey line
    track_df_points = gmt.project(
        center=[lon_start, lat_eq],  # Start point of survey line (longitude, latitude)
        endpoint=[lon_end, lat_eq],  # End point of survey line (longitude, latitude)
        generate=0.01,  # Output data in steps
        flat_earth=True,
    )
    gmt.config(MAP_FRAME_PEN="0.001p,white@100")
    fig.basemap(
        region=[lon_start, lon_end, y_min, y_max],
        projection=f"X{delta_lon * lon2width}c/6c",
        frame=0,
    )
    # Plot water
    fig.plot(data=[[lon_start, y_min, lon_end, 0]], style="r+s", fill="lightblue")
    fig.plot(x=[lon_start, lon_end], y=[0, 0], pen="0.5p,black")
    # Extract the elevation at the generated points from the downloaded grid
    track_df = gmt.grdtrack(grid=grid, points=track_df_points, newcolname="elevation")
    # Plot elevation
    fig.plot(
        x=track_df.r,
        y=track_df.elevation,
        fill="bisque",
        pen=f"0.5p,{color_profile},solid",
        close=f"+y{y_min}",
    )

    match side:
        case "left":
            fig.basemap(frame=["WNrs", "xa20f5g10", "yf500g1000+lelevation / meters"])
            fig.plot(x=[lon_eq, lon_eq], y=[y_min, y_max], pen=f"1p,{color_hl},4_2")
            fig.shift_origin(xshift="+w")
        case "right":
            fig.basemap(frame=["ENrs", "xa20f5g10", "ya1000f500g1000"])
            fig.shift_origin(xshift=f"-{(lon0 - lon_min) * lon2width}c")

gmt.config(MAP_FRAME_PEN="1p,black")
fig.basemap(projection=f"X{fig_width}c/6c", region=[-1, 1, -1, 1], frame=0)


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
