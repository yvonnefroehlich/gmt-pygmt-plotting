# #############################################################################
# Fröhlich et al. (2024), GJI: Fig. 1
# Topographic map of the Upper Rhine Graben area
# -----------------------------------------------------------------------------
# Fröhlich Y., Grund M., Ritter J. R. R. (2024)
# Lateral and vertical variations of seismic anisotropy in the lithosphere-asthenosphere
# system underneath Central Europe from long-term splitting measurements.
# Geophysical Journal International. 239(1), 112-135.
# https://doi.org/10.1093/gji/ggae245.
# -----------------------------------------------------------------------------
# History
# - Created: 2025/01/19
# - Updated: 2025/08/13 - adjusted for GitHub
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


import pandas as pd
import pygmt as gmt
import numpy as np


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"
png_dpi = 360

# -----------------------------------------------------------------------------
# Towns
file_twons_in = f"{path_in}/rhein_towns.dat"

# Recording stations
file_station_in = f"{path_in}/stations_info.txt"

# Faults
file_URGnormal_in = f"{path_in}/faults_URGnormal.geo"
file_faults_in = f"{path_in}/faults_LLBB_TH_BLZ.geo"

# Plate boundaries; Bird 2003
file_plate_in = f"{path_in}/plate_boundaries_Bird_2003.txt"

# Epicenter distribution
file_epi_in = f"{path_in}/epicenters"

# Tectonic
textfile_geology_in = f"{path_in}/rhein_geology_large.dat"

# Recording stations
df_sta = pd.read_csv(file_station_in, sep="\t", header=2)
stations = ["BFO", "WLS", "STU", "ECH", "44", "07"]

# -----------------------------------------------------------------------------
# Kaiserstuhl Volcanic Complex (KVC)
lon_KVC = 7.690556
lat_KVC = 48.120833

# Vogelsberg Volcanic Complex (VVC)
lon_VVC = 9.242944
lat_VVC = 50.533528

# Recording station Stuttgart (STU)
lon_STU = 9.194
lat_STU = 48.771
center_coord = {"x": lon_STU, "y": lat_STU}

# -----------------------------------------------------------------------------
# Colors
color_land = "gray80"
color_water = "steelblue"
color_pb = "216.750/82.875/24.990"  # plate boundaries
color_URG = "darkbrown"  # "sienna"
color_sta = "gold"  # -> GMT "gold"
color_hl = "255/90/0"  # -> orange | URG paper
color_rivers = "dodgerblue2"
color_borders = "black"
color_sl = "darkgray"

# -----------------------------------------------------------------------------
# Region and Projection
lon_min = 6
lon_max = 10
lat_min = 46.5
lat_max = 50.7
region_main = [lon_min, lon_max, lat_min, lat_max]

# main map: Mercator
proj_main = "M15c"

# inset study area: orthographic projection
proj_study = f"G{(lon_min + lon_max) / 2}/{(lat_min + lat_max) / 2}/?"

# inset epicenters: azimuthal epicentral distance projection
proj_epi = f"E{lon_STU}/{lat_STU}/170/?"

# -----------------------------------------------------------------------------
# Legends, colorbar, scale

# files for legends
leg_sta_file = "legend_gmt_stations.txt"
leg_mag_file = "legend_gmt_magitude.txt"
leg_fal_file = "legend_gmt_faults.txt"
leg_all_file = "legend_gmt_overall.txt"

# positions
leg_all_pos = "JBL+jBL+o0.135c/1.52c+w6.1c"
leg_fal_pos = "JLB+jLB+w3.15c+o0.17c/1.45c"
leg_mag_pos = "JBR+jBR+o0.1c/4.3c+w3.7c"
cb_hd_pos   = "JBR+jBR+o0.65c/3.45c+w3.7c/0.2c+h+ml"
cb_ele_pos  = "JBL+jBL+o4.0c/0.65c+w4.5c/0.2c+h+ml"

# scale
basemap_scale = f"JLB+jLB+w50+c{(lon_max + lon_min) / 2}/{(lat_max + lat_min) / 2}+f+lkm+at+o0.45c/0.55c"

box_standard = "+gwhite@30+p0.8p,black+r2p"

# text
clearance_standard = "0.1c+tO"
font_sta = f"10p,Helvetica-Bold,{color_hl}"


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
cmap_ele_in = f"{path_in}/europe_3.cpt"
cmap_ele = f"{path_in}/europe_3_resampeled_ele.cpt"
gmt.makecpt(cmap=cmap_ele_in, series=[0, 2000, 10], output=cmap_ele)
fig.grdimage(grid="@earth_relief_01m", region=region_main, cmap=cmap_ele)

fig.coast(
    resolution="f",  # (f)ull, (h)igh, (i)ntermediate, (l)ow, (c)rude
    borders=f"1/1p,{color_borders}",
    rivers=f"r/1p,{color_rivers}",
    water=color_water,
)

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
# Recording stations

# markers
for sta in stations:
    style_sta = "i0.5c"
    if sta in ["44", "07"]: style_sta = "i0.4c"
    print(sta)
    fig.plot(
        data=df_sta[df_sta["station"] == sta],
        style=style_sta, fill=color_sta,
        pen="1p,black",
    )
# labels
fig.text(
    textfiles=file_station_in,
    offset="0c/-0.65c",
    fill="white@30",
    font=font_sta,
    pen=f"0.8p,{color_hl}",
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
    fig.basemap(frame=["WSNE", "a0.5f0.25"], map_scale=basemap_scale, box=box_standard)


# %%
# -----------------------------------------------------------------------------
# Inset map of Central Europe
# -----------------------------------------------------------------------------
with fig.inset(position="jTL+w5.2c+o-1.5c/-1.2c"):
    # >>> use ? <<<
    # otherwise something goes wrong with the box around the study area

    # Orthographic projection
    # - glon0/lat0[/horizon]/scale  OR
    #   Glon0/lat0[/horizon]/width
    # - lon0 and lat0 projection center
    #   horizon maximum distance from projection center
    #   (in degrees, <= 90, default 90)
    #   scale and width figure size
    fig.basemap(region="g", projection=proj_study, frame=0)
    fig.coast(
        area_thresh="50000",
        resolution="c",
        shorelines="1/0.1p,black",
        land=color_land,
        water=color_water,
    )
    fig.basemap(frame="g")

    # rectangle at study area
    fig.plot(
        x=[lon_min, lon_min, lon_max, lon_max, lon_min],
        y=[lat_min, lat_max, lat_max, lat_min, lat_min],
        pen="0.5p,black",
        fill=color_hl,
    )

    # WDC = [-77.0364, 38.8951]
    # URG = [8.0, 48.5]
    # data = np.array([WDC + URG])
    # # '=' means geographic vectors. With the modifier '+s', the input
    # # data should contain coordinates of start and end points
    # style = f"=0.7c+s+ea+g{color_hl}+h0.5+p0.3p,black"
    # fig.plot(data=data, style=style, pen=f"3p,{color_hl}")
    # fig.plot(
    #     x=-77.0364,
    #     y=38.8951,
    #     style="c0.25c",
    #     pen="0.5p,black",
    #     fill=color_hl,
    # )


# %%
# -----------------------------------------------------------------------------
# Inset of epicenter distribution
# -----------------------------------------------------------------------------
with fig.inset(position="JMR+jMR+w6c+o-1.5c/-3.6"):
    # >>> use ? <<<
    # otherwise something goes wrong with the box around the study area

    # azimuthal equidistant projection
    # - elon0/lat0[/horizon]/scale  OR
    #   Elon0/lat0[/horizon]/width
    # - horizon max. distance to the projection center
    #   i.e. the visible portion of the rest of the world map
    #   in degrees <= 180Â° (default 180Â°)
    fig.basemap(region="g", projection=proj_epi, frame=0)
    fig.coast(
        area_thresh="50000",
        resolution="c",
        shorelines=f"1/0.1p,{color_sl}",
        land=color_land,
        water="white",
    )

    # plate boundaries
    fig.plot(data=file_plate_in, pen=f"0.5p,{color_pb}")

# -----------------------------------------------------------------------------
    # Mark epicentral distance range used in this study
    for epi_dist, y in zip([90, 150], [-28, -88]):
        # Plot circles
        fig.plot(style=f"E-{epi_dist * 2}+d", pen="1p,gray50,4_2", **center_coord)
        # Add label for annotations limits of epicentral distance range
        fig.text(x=center_coord["x"], y=y, text=f"{epi_dist}@.", font="9p,black")

# -----------------------------------------------------------------------------
    # Plot epicenters
    df_epi_raw = pd.read_csv(f"{path_in}/STU_epi_swsm_all.txt", sep="\t", header=1)
    df_epi = df_epi_raw
    df_epi.moment_magnitude = np.exp(df_epi_raw.moment_magnitude / 1.7) * 0.0035

# -----------------------------------------------------------------------------
    # Colormap hypocentral depth - Scientific Colour maps by F. Crameri
    cmap_hypo_in = "lajolla"
    cmap_hypo = f"{path_in}/{cmap_hypo_in}_resampeled_hypo.cpt"
    hypodepth_max = 500
    gmt.makecpt(cmap=cmap_hypo_in, series=[0, hypodepth_max], output=cmap_hypo)
    fig.plot(
        x=df_epi.longitude,
        y=df_epi.latitude,
        size=df_epi.moment_magnitude,
        fill=df_epi.hypocentral_depth_km,
        style="c",
        cmap=cmap_hypo,
        pen="0.01,gray20",
    )

# -----------------------------------------------------------------------------
    # Recording station
    # Marker
    fig.plot(style="i0.47c", fill=color_sta, pen="0.6p,black", **center_coord)
    # Label
    fig.text(
        text="STU",
        font=font_sta,
        offset="0c/-0.6c",
        fill="white@30",
        pen=f"0.8p,{color_hl}",
        clearance=clearance_standard,
        **center_coord,
    )


# %%
# -----------------------------------------------------------------------------
# Legends

# main map
fig.legend(spec=f"{path_in}/{leg_all_file}", position=leg_all_pos, box=box_standard)

# moment magnitude
fig.legend(spec=f"{path_in}/{leg_mag_file}", position=leg_mag_pos, box=box_standard)

# -----------------------------------------------------------------------------
# Colorbars
with gmt.config(MAP_TICK_LENGTH_PRIMARY="2p", FONT="17p"):

    # hypocentral depth
    fig.colorbar(
        cmap=cmap_hypo,
        position=f"{cb_hd_pos}+ef0.15c",
        box=box_standard,
        frame="xa100f50+lhypocentral depth / km",
    )

    # elevation
    fig.colorbar(
        cmap=cmap_ele,
        position=f"{cb_ele_pos}+ef0.15c",
        box=box_standard,
        frame="+lelevation / m",
    )

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = "FGR2024_GJI_FigS1"
for ext in ["png"]:  #, "pdf", "eps"]:
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=720)
print(fig_name)
