# #############################################################################
# Fröhlich et al. (2024), GJI: Fig. 9
# Piercing points in the upper mantle
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
# color-coding used for the piercing points
status_pp = "phi"  ## "station" | "phi" | "dt" | "si" | "baz"
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
textfile_geology_in = f"{path_in}/rhein_geology_large.dat"

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
lon_min = 6
lon_max = 10.15
lat_min = 47.4
lat_max = 50
region_main = [lon_min, lon_max, lat_min, lat_max]

# main map: Mercator
proj_main = "M15c"

# inset study area: orthographic projection
proj_study = "M?"

# scale
scale_pos = f"{(lon_max + lon_min) / 2}/{(lat_max + lat_min) / 2}"
basemap_scale = f"JLB+jLB+w50+c{scale_pos}+f+lkm+at+o0.45c/0.55c"

# -----------------------------------------------------------------------------
# Create colormaps and colorbars
# elevation
cb_ele_pos  = "JBL+jBL+o4.0c/0.6c+w4.5c/0.2c+h+ml+ef0.15c"

# fast polarization direction
cmap_phi_in = "phase"
cmap_phi = f"{path_in}/{cmap_phi_in}_resampled_phi.cpt"
gmt.makecpt(cmap=cmap_phi_in, output=cmap_phi, series=[-90, 90], cyclic=True)
cb_phi_label = "a30f10+lsplit app. fast pol. dir. @~f@~@-a@- / N@.E"
cb_pp_pos = "JRB+jRB+o0.6c/0.6c+w4.3c/0.2c+h+ml"
cb_phi_pos = cb_pp_pos

# delay time
cmap_dt_in = "lapaz"
cmap_dt = f"{path_in}/{cmap_dt_in}_resampled_dt.cpt"
gmt.makecpt(cmap=cmap_dt_in, output=cmap_dt, series=[0, 3], reverse=True)
cb_dt_label = "a1f0.5+lsplit app. delay time @~d@~t@-a@- / s"
cb_dt_pos = f"{cb_pp_pos}+ef0.15c"

# splitting intenstiy
cmap_si_in = "vik"
cmap_si = f"{path_in}/{cmap_si_in}_resampled_si.cpt"
gmt.makecpt(cmap=cmap_si_in, output=cmap_si, series=[-2, 2])
cb_si_label = "a1f0.5+lsplitting intensity SI"
cb_si_pos = f"{cb_pp_pos}+e0.15c"

# backazimuth
cmap_baz_in = "romaO"
cmap_baz = f"{path_in}/{cmap_baz_in}_resampled_baz.cpt"
gmt.makecpt(cmap=cmap_baz_in, output=cmap_baz, series=[0, 360, 1], cyclic=True)
cb_baz_label = "a60f30+lbackazimuth @."
cb_baz_pos = cb_pp_pos

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
# Legends
leg_pp_file = "legend_gmt_pp.txt"
leg_dt_file = "legend_gmt_pp_dt.txt"
leg_pp_pos = "JRB+jRB+w2.0c+o0.2c/3.0c"
leg_dt_pos = "JRB+jRB+w2.8c+o0.2c/1.4c"

# text
clearance_standard = "0.1c+tO"
font_sta = f"9.5p,Helvetica-Bold,{color_hl}"

box_standard = "+gwhite@30+p0.8p,black+r2p"


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
    COLOR_NAN="white",  # color for NaN, default 127.5
)

fig.basemap(region=region_main, projection=proj_main, frame=0)

# -----------------------------------------------------------------------------
# Elevation
cmap_ele_in = "grayC"
cmap_ele = f"{path_in}/{cmap_ele_in}_resampeled_ele.cpt"
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
# Piercing points
# -----------------------------------------------------------------------------
for station in stations:

# -----------------------------------------------------------------------------
    # Recording stations
    df_sta_temp = df_sta[df_sta["station"] == station]

    style_sta = "i0.5c"
    label_sta = station
    if station in ["TMO44", "TMO07"]:
        style_sta = "i0.4c"
        label_sta = station[3:5]
        color_sta = color_sta
    if status_pp == "station":
        color_df = df_sta_temp["color"]
        color_str = color_df.to_string()
        color_sta = color_str[5:len(color_str)]  # index + tab -> 4 signs

    # markers
    fig.plot(data=df_sta_temp, style=style_sta, fill=color_sta, pen="1p,black")
    # labels
    fig.text(
        text=label_sta,
        x=df_sta_temp["longitude"],
        y=df_sta_temp["latitude"],
        offset="0c/-0.6c",
        fill="white@30",
        font=font_sta,
        pen=f"0.8p,{color_hl}",
        clearance=clearance_standard,
    )

# -----------------------------------------------------------------------------
    # lon | lat | phi_SL | phi_GMT | dt | si | baz | thick
    data_pp_end = "goodfair_hd0km.txt"
    data_path = f"{path_in}/pps/{station}_pp200km_"
    data_K_N_pp = f"{data_path}K_sp_N_{data_pp_end}"
    data_K_NN_pp = f"{data_path}K_sp_NN_{data_pp_end}"
    data_KK_N_pp = f"{data_path}KK_sp_N_{data_pp_end}"
    data_KK_NN_pp = f"{data_path}KK_sp_NN_{data_pp_end}"
    data_P_N_pp = f"{data_path}P_sp_N_{data_pp_end}"
    data_P_NN_pp = f"{data_path}P_sp_NN_{data_pp_end}"

# -----------------------------------------------------------------------------
    if status_pp == "station":  # color-coded by station

        args_pp_NN_sta = {
            "style": "j",
            "fill": color_sta,
            "pen": "0.2p,black",
            "incols": [0, 1, 3, 4, 7],
        }
        args_pp_N_sta = {
            "style": "C0.2",
            "fill": "white",
            "pen": f"1p,{color_sta}",
        }

        # non-null
        for data, phase in zip([data_K_NN_pp, data_KK_NN_pp, data_P_NN_pp], ["K", "KK", "P"]):
            try:
                fig.plot(data=data, **args_pp_NN_sta)
            except: print(f"{station} no pp {phase}_NN")
        # null
        for data, phase in zip([data_K_N_pp, data_KK_N_pp, data_P_N_pp], ["K", "KK", "P"]):
            try:
                fig.plot(data=data, **args_pp_N_sta)
            except: print(f"{station} no pp {phase}_N")

# -----------------------------------------------------------------------------
    elif status_pp!="station":  # color-coded by

        match status_pp:
            case "phi":  # fast polarization direction (phi)
                color_pp = cmap_phi
                incols_pp = [0, 1, 2, 3, 4, 7]
                incols_pp_N = [0, 1, 2]
            case "dt":  # delay time (dt)
                color_pp = cmap_dt
                incols_pp = [0, 1, 4, 3, 4, 7]
                incols_pp_N = [0, 1, 4]
            case "si":  # splitting intensity (si)
                color_pp = cmap_si
                incols_pp = [0, 1, 5, 3, 4, 7]
                incols_pp_N = [0, 1, 5]
            case "baz":  # backazimuth (baz)
                color_pp = cmap_baz
                incols_pp = [0, 1, 6, 3, 4, 7]
                incols_pp_N = [0, 1, 6]

        args_pp_NN_sp = {
            "style": "j",
            "cmap": color_pp,
            "pen": "0.2p,black",
            "incols": incols_pp,
        }
        args_pp_N_sp = {
            "style": "C0.2c",
            "cmap": color_pp,
            "pen": "1p,black",
            "incols": incols_pp_N,
        }

        # null
        for data, phase in zip([data_K_N_pp, data_KK_N_pp, data_P_N_pp], ["K", "KK", "P"]):
            try:
                fig.plot(data=data, **args_pp_N_sp)
            except: print(f"{station} no pp {phase}_N")
        # non-null
        for data, phase in zip([data_K_NN_pp, data_KK_NN_pp, data_P_NN_pp], ["K", "KK", "P"]):
            try:
                fig.plot(data=data, **args_pp_NN_sp)
            except: print(f"{station} no pp {phase}_NN")


# %%
# Sketch for piercing points
# -----------------------------------------------------------------------------
# Externaly created in Microsoft PowerPoint
pp_image = "percingpoints_sketch_orange.eps"
fig.image(imagefile=f"{path_in}/{pp_image}", position="jTR+w3c+o0.1c")

# -----------------------------------------------------------------------------
# Labels
args_label = {
    "pen": f"0.8p,{color_hl}",
    "font": f"9p,Helvetica-Bold,{color_hl}",
    "fill": "white@30",
    "clearance": clearance_standard,
}
# depth
fig.text(text="@@200 km", position="TR", offset="-3.4c/-0.25c", **args_label)

# -----------------------------------------------------------------------------
# Legends
fig.legend(spec=f"{path_in}/{leg_pp_file}", position=leg_pp_pos, box=box_standard)
fig.legend(spec=f"{path_in}/{leg_dt_file}", position=leg_dt_pos, box=box_standard)

# -----------------------------------------------------------------------------
# Colorbars
with gmt.config(MAP_TICK_LENGTH_PRIMARY="2p", FONT="17p"):

    # elevation
    fig.colorbar(
        cmap=cmap_ele,
        position=cb_ele_pos,
        box=box_standard,
        frame="+lelevation / m",
    )

    # piercing points
    match status_pp:
        case "phi":
            cmap_pp = cmap_phi
            frame_pp = cb_phi_label
            pos_pp = cb_phi_pos
        case "si":
            cmap_pp = cmap_si
            frame_pp = cb_si_label
            pos_pp = cb_si_pos
        case "dt":
            cmap_pp = cmap_dt
            frame_pp = cb_dt_label
            pos_pp = cb_dt_pos
        case "baz":
            cmap_pp = cmap_baz
            frame_pp = cb_baz_label
            pos_pp = cb_baz_pos
    if status_pp != "station":
        fig.colorbar(cmap=cmap_pp, frame=frame_pp, position=pos_pp, box=box_standard)


# %%
# -----------------------------------------------------------------------------
# Inset map of Central Europe
# -----------------------------------------------------------------------------
with fig.inset(position="jTL+jTL+w3.5c+o-0.24c/0.05c"):
    gmt.config(MAP_FRAME_TYPE="plain", MAP_TICK_LENGTH_PRIMARY="0p")
    # >>> use ? <<<
    # otherwise something goes wrong with the box around the study area

    fig.basemap(region=[2.8, 16, 46, 56], projection=proj_study, frame=0)
    fig.coast(
        land=color_land,
        water=color_water,
        area_thresh="20/0/1",
        resolution="h",
        shorelines="1/0.15p,black",
        borders="1/0.35p,black",
    )
    fig.basemap(frame="f")

    # label for countries
    fig.text(
        x=np.array([10.50,  4.50,  8.30]),
        y=np.array([51.10, 47.80, 46.70]),
        text=["DE", "FR", "CH"],
        font="8p,black",
        fill="white@30",
        clearance=clearance_standard,
    )

    # rectangle at study area
    fig.plot(
        x=[lon_min, lon_min, lon_max, lon_max, lon_min],
        y=[lat_min, lat_max, lat_max, lat_min, lat_min],
        pen=f"1p,{color_hl}",
    )

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = f"FGR2024_GJI_Fig9_{status_pp}"
# for ext in ["png"]:  #, "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
