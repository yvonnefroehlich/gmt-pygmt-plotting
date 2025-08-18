# #############################################################################
# Fröhlich et al. (2024), GJI: Figure 10
# Topographic map of the Upper Rhine Graben area with stereoplots
# -----------------------------------------------------------------------------
# Fröhlich Y., Grund M., Ritter J. R. R. (2024)
# Lateral and vertical variations of seismic anisotropy in the lithosphere-asthenosphere
# system underneath Central Europe from long-term splitting measurements.
# Geophysical Journal International. 239(1), 112-135.
# https://doi.org/10.1093/gji/ggae245.
# -----------------------------------------------------------------------------
# History
# - Created: -
# - Updated: 2025/08/18 - adjusted for GitHub
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.16.0 -> https://www.pygmt.org/v0.16.0/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import glob
import os

import pandas as pd
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"
dpi_png = 360

# -----------------------------------------------------------------------------
# Towns
file_twons_in = f"{path_in}/rhein_towns.dat"

# Faults
file_URGnormal_in = f"{path_in}/faults_URGnormal.geo"
file_faults_in = f"{path_in}/faults_LLBB_TH_BLZ.geo"

# Tectonic
textfile_geology_in = f"{path_in}/rhein_geology_small.dat"

# Recording stations
file_station_in = f"{path_in}/stations_info.txt"
df_sta = pd.read_csv(file_station_in, sep="\t", header=2)
stations = ["BFO", "WLS", "STU", "ECH", "TMO44", "TMO07"]

# -----------------------------------------------------------------------------
# Kaiserstuhl Volcanic Complex (KVC)
lon_KVC = 7.690556
lat_KVC = 48.120833

# Vogelsberg Volcanic Complex (VVC)
lon_VVC = 9.242944
lat_VVC = 50.533528

# -----------------------------------------------------------------------------
# Region and Projection
lon_min = 6.9
lon_max = 9.6
lat_min = 47.8
lat_max = 49.2
region_main = [lon_min, lon_max, lat_min, lat_max]

# main map: Mercator
proj_main = "M15c"

# scale
scale_pos = f"{(lon_max + lon_min) / 2}/{(lat_max + lat_min) / 2}"
basemap_scale = f"JLB+jLB+w50+c{scale_pos}+f+lkm+at+o0.45c/0.55c"

# -----------------------------------------------------------------------------
# Create colormaps and colorbars
# elevation
cmap_ele_in = "grayC"
cmap_ele = f"{path_in}/{cmap_ele_in}_resampeled_ele.cpt"
gmt.makecpt(cmap=cmap_ele_in, series=[0, 2000, 10], output=cmap_ele)
cb_ele_label = "+lelevation / m"
cb_ele_pos = "JBC+jBC+o-0.4c/0.6c+w4.0c/0.2c+h+ml+ef0.15c"

# fast polarization direction
cmap_phi_in = "phase"
cmap_phi = f"{path_in}/{cmap_phi_in}_resampled_phi.cpt"
gmt.makecpt(cmap=cmap_phi_in, output=cmap_phi, series=[-90, 90], cyclic=True)
cb_phi_label = "a30f10+lsplit app. fast pol. dir. @~f@~@-a@- / N@.E"
cb_phi_pos = "JRB+jRB+o0.5c/0.6c+w4.3c/0.2c+h+ml"

# -----------------------------------------------------------------------------
# Colors
color_URG = "darkbrown"
color_sta = "gold"  # -> GMT "gold"
color_hl = "255/90/0"  # -> orange | URG paper
color_rivers = "dodgerblue2"
color_borders = "black"

# -----------------------------------------------------------------------------
# Legends
leg_pp_file = "legend_gmt_pp.txt"
leg_pp_pos = "JRB+jRB+w2.0c+o0.1c/1.5c"

# text
clearance_standard = "0.1c+tO"
font_sta = f"9.5p,Helvetica-Bold,{color_hl}"

box_standard = "+gwhite@30+p0.8p,black+r2p"

size_stereo = 3.2  # in centimeters


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------
fig = gmt.Figure()

# Global changes of default values of GMT
gmt.config(
    MAP_FRAME_TYPE="fancy+",
    # formatting template for geographical coordinates F adds NESW after degree sign
    FORMAT_GEO_MAP="ddd.xF",
    MAP_ANNOT_OBLIQUE="lat_parallel",
    MAP_FRAME_WIDTH="3p",
    FONT_LABEL="9p",
    FONT_ANNOT_PRIMARY="9p",
    MAP_FRAME_PEN="0.8p",  # thickness of border around scale
    MAP_ANNOT_OFFSET="0.05i",  # distance of scale ticks labels from scale
    MAP_LABEL_OFFSET="3.5p",  # distance of label from scale
    MAP_TICK_LENGTH_PRIMARY="5p",  # length of scale ticks
)

fig.basemap(region=region_main, projection=proj_main, frame=0)

# -----------------------------------------------------------------------------
# Elevation
fig.grdimage(grid="@earth_relief_15s", region=region_main, cmap=cmap_ele)

fig.coast(resolution="f", borders=f"1/1p,{color_borders}", rivers=f"r/1p,{color_rivers}")

# -----------------------------------------------------------------------------
# Faults
fig.plot(
    data=file_URGnormal_in,  # URG
    style="f0.25i/0.2c+l+f+o0.5c",  # normal fault
    fill=color_URG,
    pen=f"1.2p,{color_URG}",
)
fig.plot(
    data=file_faults_in,  # LLBB, HT, BLZ
    style="f0.25i/0.15c+r+t+o.5c",  # trust fault
    fill=color_URG,
    pen=f"1.2p,{color_URG}",
)

# -----------------------------------------------------------------------------
# Towns
# marker
fig.plot(data=file_twons_in, style="s0.3c", fill="white", pen="1p,black")
# labels
fig.text(
    textfiles=file_twons_in,
    font=True,  # read from file
    angle=True,  # read from file
    justify=True,  # read from file
    offset="0.2c",
    fill="white@30",
    clearance=clearance_standard,
)

# -----------------------------------------------------------------------------
# Tectonic
fig.text(
    textfiles=textfile_geology_in,
    font=True,  # fontsize,fonttyp,fontcolor
    angle=True,
    justify=True,
    offset="0.3/0.05",
    fill="white@30",
    pen=f"0.8p,{color_URG}",
    clearance=clearance_standard,
)

# -----------------------------------------------------------------------------
# Volcanic Complexes
# marker - self-defined symbol, read from file
for lon, lat, size in zip([lon_KVC, lon_VVC], [lat_KVC, lat_VVC], [0.7, 1]):
    fig.plot(
        x=lon,
        y=lat,
        style=f"k{path_in}/volcano_sleeping.def/{size}c",
        fill=color_URG,
        pen="0.8p,black",
    )

# label
fig.text(
    x=[lon_KVC, lon_VVC],
    y=[lat_KVC, lat_VVC],
    text=["Kaiserstuhl VC", "Vogelsberg VC"],
    font="8p,Helvetica-Bold,black",
    offset="-0.7c/-0.7c",
    justify="TC",
    fill="white@30",
    pen=f"0.8p,{color_URG}",
    clearance=clearance_standard,
)

# -----------------------------------------------------------------------------
# Map frame and map scale
with gmt.config(MAP_SCALE_HEIGHT="9p"):
    fig.basemap(frame=["WSne", "a0.5f0.25"], map_scale=basemap_scale, box=box_standard)


# %%
# -----------------------------------------------------------------------------
# Stereoplots
# -----------------------------------------------------------------------------
for station in stations:

    df_sta_temp = df_sta[df_sta["station"] == station]

    # Not very elegant but works
    lon_df = df_sta_temp["longitude"]
    lon_str = lon_df.to_string()
    lon_sta = lon_str[5:len(lon_str)]  # index + tab -> 4 signs

    lat_df = df_sta_temp["latitude"]
    lat_str = lat_df.to_string()
    lat_sta = lat_str[5:len(lat_str)]  # index + tab -> 4 signs

    # First plot semi-transparent white filled circle behind fully transparent
    # stereoplot to increase visibility
    fig.plot(x=lon_sta, y=lat_sta, fill="white@70", style=f"C{size_stereo}c")

    # Plot semi-transporent yellow sector (pie wedge) to highlight nulls at BFO in the
    # southwest [outer[/startdir/stopdir]][+i[inner]] in degrees counter-clockwise from
    # horizontal
    args_stereo = {"x": lon_sta, "y": lat_sta, "fill": "gold@70"}
    if station == "BFO":
        fig.plot(style=f"w{size_stereo}c/140/300", **args_stereo)
    if station == "WLS":
        fig.plot(style=f"w{size_stereo}c/10/30", **args_stereo)
    if station =="ECH":
        fig.plot(style=f"w{size_stereo}c/10/30", **args_stereo)
    if station == "TMO07":
        fig.plot(style=f"w{size_stereo}c/190/220", **args_stereo)

    # Stereoplots are perfect circles without any annotation, thus station coordinates
    # are used as mid point and the anchor point is set to MC
    stereo_in = f"Stereo_{station}_goodfair_SC_single_Baz0to360_phase_noall_trans.eps"
    fig.image(
        imagefile=f"{path_in}/stereos/{stereo_in}",
        position=f"g{lon_sta}/{lat_sta}+jMC+w{size_stereo}c",
    )

# -----------------------------------------------------------------------------
    # Recording stations
    size_sta = 0.5  # in centimeters
    label_sta = station
    if station in ["TMO44", "TMO07"]:
        size_sta = 0.4
        label_sta = station[3:5]

    offset_x_sta = 0  # in centimeters
    offset_y_sta = -1.4  # in centimeters
    if station in ["WLS", "ECH"]:
        offset_x_sta = 0.4
        offset_y_sta = -0.6

    # markers
    fig.plot(data=df_sta_temp, style=f"i{size_sta}c", fill=color_sta, pen="1p,black")
    # labels
    fig.text(
        text=label_sta,
        x=lon_sta,
        y=lat_sta,
        offset=f"{offset_x_sta}c/{offset_y_sta}c",
        fill="white@30",
        font=font_sta,
        pen=f"0.8p,{color_hl}",
        clearance=clearance_standard,
    )


# %%
# -----------------------------------------------------------------------------
# Highlight subregions by labels
# -----------------------------------------------------------------------------
style_vector = "v0.4c+ba+ea+a30+h0"

# Layer number change in South-North direction
fig.plot(
    x=8.82,
    y=48.15,
    # direction cc from horizontal, length in centimeters
    direction=[[90], [7.6]],
    style=style_vector,
    pen=f"2p,{color_hl}",
    fill=color_hl,
)
fig.text(
    x=8.88,
    y=48.5,
    text="change of layer number",
    font="8p,Helvetica-Bold,black",
    fill="white@30",
    pen=f"0.8p,{color_hl}",
    clearance=clearance_standard,
)

# Fast polarization direction change between the East West sides of the URG
fig.plot(
    x=7.6,
    y=48.39,
    direction=[[20], [8.1]],
    style=style_vector,
    pen=f"2p,{color_hl}",
    fill=color_hl,
)
fig.text(
    x=8.06,
    y=48.54,
    text="change of fast polarization direction",
    font="8p,Helvetica-Bold,black",
    fill="white@30",
    pen=f"0.8p,{color_hl}",
    clearance=clearance_standard,
)

# Null anomaly at BFO in the SW quadrant
fig.text(
    x=7.7,
    y=48.235,
    text="null anomaly",
    font="8p,Helvetica-Bold,black",
    fill="white@30",
    pen=f"0.8p,{color_hl}",
    clearance=clearance_standard,
)


# %%
# -----------------------------------------------------------------------------
# Legends
fig.legend(spec=f"{path_in}/{leg_pp_file}", position=leg_pp_pos, box=box_standard)

# -----------------------------------------------------------------------------
# Colorbars
with gmt.config(MAP_TICK_LENGTH_PRIMARY="2p", FONT="17p"):

    # elevation
    fig.colorbar(cmap=cmap_ele, frame=cb_ele_label, position=cb_ele_pos, box=box_standard)

    # piercing points
    fig.colorbar(cmap=cmap_phi, frame=cb_phi_label, position=cb_phi_pos, box=box_standard)

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = "FGR2024_GJI_Fig10"
# for ext in ["png"]:  #, "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)

# Remove colormap files
for cpt in glob.glob(f"{path_in}/*resampled*.cpt"):
    os.remove(cpt)
