# #############################################################################
# North pole source configuration with global recording stations equally spaced
# - Variation with latitude -> epicentral distance / seismologcial phases
# - Variation with longitude -> backzimuth / seismogram components
# -----------------------------------------------------------------------------
# Related to
# - Fröhlich Y., Ritter J. R. R. (2024) http://dx.doi.org/10.5281/zenodo.14510993
#   Vertical and Small-scale Lateral Varying Seismic Anisotropy in the Upper
#   Mantle Underneath the Upper Rhine Graben, Central Europe. Annual Meeting of
#   the American Geophysical Union. http://dx.doi.org/10.5281/zenodo.14510993.
# -----------------------------------------------------------------------------
# History
# - Created: 2025/03/09
# -----------------------------------------------------------------------------
# Versions
#   PyGMT v0.14.2 -> https://www.pygmt.org/v0.14.2/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
import pandas as pd
import pygmt as gmt
import string


# %%
# -----------------------------------------------------------------------------
# Choose for your needs
# -----------------------------------------------------------------------------
# Quantity for color-coding: station, backazimuth, epicentral distance
cmap_quantity = "baz"  ## "sta", "dist", "baz"

# Projection: Robison, orthographic, epi-distance projections
status_proj = "epi"  ## "rob", "ortho", "epi"

# Add colorbar: True, False
status_cb = True


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"
dpi_png = 720  # resolution of saved PNG file

cmap_lat = "batlow"  # -> latitude or epicentral distance (dist)
cmap_lon = "romaO"  # -> longitude or backazimuth (baz)
color_station = "gold"  # -> recording station (sta)
color_source = "red"
color_land = "gray90"
color_water = "white"
color_sl = "gray50"  # shorelines

# Location of source at North pole
source_lon = 0  # degrees East
source_lat = 89.999  # degrees North

# Distance between recording stations
coord_step = 10  # degrees

cb_str = ""
if status_cb==True: cb_str = "_cb"

match cmap_quantity:
    case "dist": cmap_sta = cmap_lat
    case "baz": cmap_sta = cmap_lon
    case "sta": cmap_sta = "gold"

match status_proj:
    case "rob":
        proj_used = "N18c"
        no_clip_used = True
        sta_lat_min = 90
        sta_lat_max = -90
        y_text_add = 3.1
        sta_font = 4
    case "ortho":
        proj_used = "G0/2/10c"
        no_clip_used = False
        sta_lat_min = 80
        sta_lat_max = -70
        y_text_add = 2.5
        sta_font = 4.5
    case "epi":
        fig_width = 14
        proj_dist = 160
        dist2fig = fig_width / proj_dist
        proj_used = f"E{source_lon}/{source_lat}/{proj_dist}/{fig_width}c"
        no_clip_used = True
        sta_lat_min = 1
        sta_lat_max = -61
        y_text_add = 3.5
        sta_font = 4.5


# %%
# -----------------------------------------------------------------------------
# Load and prepare input data
# -----------------------------------------------------------------------------
data_sta = pd.read_csv(
    f"{path_in}/stations_global_Dlon{coord_step}_Dlat{coord_step}.txt",
    delimiter=" ",
    names=["station", "network", "lat", "lon", "value1", "value2"],
)

# Filter data based on latitude range
data_sta_plot_temp = data_sta[data_sta["lat"] < sta_lat_min]
data_sta_plot = data_sta_plot_temp[data_sta_plot_temp["lat"] > sta_lat_max]


# %%
# -----------------------------------------------------------------------------
# Make geographic map of source station collstalation
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray50", MAP_FRAME_PEN="1p")

fig.coast(
    region="d",
    projection=proj_used,
    shorelines=f"1/0.1p,{color_sl}",
    land=color_land,
    water=color_water,
    frame=["xafg10", "ya30fg10"],
    verbose="q",
)

# -----------------------------------------------------------------------------
# Set up colormap and colorbar

# for backazimuth (-> longitude) [the definition can be set freely]
if cmap_quantity == "baz":
    sta_color = data_sta_plot.lon
    sta_factor = 1
    bazs_left = np.arange(180, 0, -coord_step)
    bazs_right = np.arange(360, 180, -coord_step)
    bazs = list(bazs_left) + list(bazs_right)
    sta_nums = np.arange(0, len(bazs), 1)
    cb_annot_baz = ','.join(
        f"{str(sta_nums[i_baz] + 1).zfill(2)}: {bazs_left[i_baz]}° | " + \
        f"{str(sta_nums[i_baz] + 1 + 18).zfill(2)}: {bazs_right[i_baz]}°"
        for i_baz, baz in enumerate(bazs[0:18])
    )
    gmt.makecpt(
        cmap=cmap_sta,
        series=[-180 + coord_step, 0, coord_step],
        color_model=f"+c{cb_annot_baz}",
        cyclic=True,
    )
    if status_cb==True:
        with gmt.config(MAP_FRAME_PEN="0.2p", FONT="8p"):
            # +r reverse the sense of the positive direction
            fig.colorbar(cmap=True, position="JRM+jMC+w9c/0.2c+o0.5c/-0.2c+r", equalsize=0.2)

# for epicentral distance (-> latitude)
elif cmap_quantity == "dist":
    sta_color = data_sta_plot.lat
    sta_factor = -1  # Needed because lat and dist inverse
    dists = np.arange(coord_step, 180, coord_step)
    sta_chars = list(string.ascii_uppercase)
    cb_annot_dist = ','.join(
        f"{sta_chars[i_dist]}: {dist}°" for i_dist, dist in enumerate(dists)
    )
    gmt.makecpt(
        cmap=cmap_sta,
        series=[-90 + coord_step, 90 - coord_step, coord_step],
        color_model=f"+c{cb_annot_dist}",
        reverse=True,
    )
    if status_cb==True:
        with gmt.config(MAP_FRAME_PEN="0.2p", FONT="8p"):
            fig.colorbar(cmap=True, position="JRM+jMC+w9.3c/0.2c+o0.5c/0c+r", equalsize=0.2)

# -----------------------------------------------------------------------------
# Plot recording stations with color-coding
if status_proj in ["rob", "ortho"]:
    fill = color_station
    cmap = None
    if cmap_quantity in ["dist", "baz"]:
        fill = sta_color * sta_factor
        cmap = True
    fig.plot(
        x=data_sta_plot.lon,
        y=data_sta_plot.lat,
        style="i0.24c",
        fill=fill,
        cmap=cmap,
        pen="0.05p,black",
        no_clip=no_clip_used,
    )

elif status_proj in ["epi"]:
    for i_sta in np.array(data_sta_plot.index):
        fill = color_station
        zvalue = None
        cmap = None
        if cmap_quantity in ["dist", "baz"]:
            fill = "+z"
            zvalue = sta_color[i_sta] * sta_factor
            cmap = True
        perspective_receiver = \
            f"{data_sta_plot.lon[i_sta]}" + \
            f"+w{data_sta_plot.lon[i_sta]}/{data_sta_plot.lat[i_sta]}"
        fig.plot(
            x=data_sta_plot.lon[i_sta],
            y=data_sta_plot.lat[i_sta],
            style="i0.24c",
            fill=fill,
            zvalue=zvalue,
            cmap=cmap,
            pen="0.05p,black",
            no_clip=no_clip_used,
            perspective=perspective_receiver,
        )

# -----------------------------------------------------------------------------
# Add label for recording stations
angle_text = None
if status_proj == "epi": angle_text = data_sta_plot.lon

fig.text(
    x=data_sta_plot.lon,
    y=data_sta_plot.lat - y_text_add,
    text=data_sta_plot.station,
    justify="TC",
    font=f"{sta_font}p",
    angle=angle_text,
    fill="white@10",
    pen="0.2p,gray",
    clearance="0.035c/0.035c+tO",
    no_clip=no_clip_used,
)

# -----------------------------------------------------------------------------
# Plot source at North pole
fig.plot(
    x=source_lon, y=source_lat, style="a0.4c", fill=color_source, pen="0.2p", no_clip=True
)

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = f"setup_northpole_source_global_step{coord_step}deg_" + \
           f"{cmap_quantity}{cmap_sta}_{status_proj}{cb_str}"
for ext in ["png"]:  # "pdf", "png", "eps"
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
