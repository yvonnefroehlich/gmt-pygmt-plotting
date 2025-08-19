# #############################################################################
# Fröhlich et al. (2024), GJI: Figure S22
# Piercing points in the lowermost mantle
# -----------------------------------------------------------------------------
# Fröhlich Y., Grund M., Ritter J. R. R. (2024)
# Lateral and vertical variations of seismic anisotropy in the lithosphere-asthenosphere
# system underneath Central Europe from long-term splitting measurements.
# Geophysical Journal International. 239(1), 112-135.
# https://doi.org/10.1093/gji/ggae245.
#
# LLSVP data taken from Wolf et al. (2023). https://doi.org/10.1029/2023GC011070.
# Data are available at https://github.com/wolfjonathan/Deep_Mantle_Anisotropy_Database
# -----------------------------------------------------------------------------
# History
# - Created: -
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


import glob
import os

import numpy as np
import pygmt as gmt

# %%
# -----------------------------------------------------------------------------
# Choose
# -----------------------------------------------------------------------------
status_station = "URG"  ## "BFO" | "URG" | "URGwithBFO"
status_pp = "phi"  ## "phase" | "phi" | "dt" | "si" | "baz"


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"
png_dpi = 360
font_size = "9p"

# -----------------------------------------------------------------------------
# Projection and region

# Lambert Conic Conformal Projection
# llon0/lat0/lat1/lat2/scale  OR  Llon0/lat0/lat1/lat2/width
lon_min_lamb = -35
lon_max_lamb = 49
lat_min_lamb = 25
lat_max_lamb = 70

# Calculate projection center
lon0_lamb = np.mean([lon_min_lamb, lon_max_lamb])
lat0_lamb = np.mean([lat_min_lamb, lat_max_lamb])
# Calculate two standard parallels (only these two distortion-free)
lat1_lamb = lat_min_lamb + (lat_max_lamb - lat_min_lamb) / 3
lat2_lamb = lat_min_lamb + (lat_max_lamb - lat_min_lamb) / 3 * 2

width_lamb = "15c"
proj_lamb = f"L{lon0_lamb}/{lat0_lamb}/{lat1_lamb}/{lat2_lamb}/{width_lamb}"
region_lamb = f"{lon_min_lamb}/{lon_max_lamb}/{lat_min_lamb}/{lat_max_lamb}"

# -----------------------------------------------------------------------------
# Create colormaps and colorbars

# fast polarization direction
cmap_phi_in = "phase"
cmap_phi = f"{path_in}/{cmap_phi_in}_resampled_phi.cpt"
with gmt.config(COLOR_NAN="white"):
    gmt.makecpt(
        cmap=cmap_phi_in,
        output=cmap_phi,
        series=[-90, 90],
        cyclic=True,
        overrule_bg=True,
    )
cb_phi_label = "a30f10+lnull | split app. fast pol. dir. @~f@~@-a@- / N@.E"
cb_sp_pos = "JRT+jRT+w3.5/0.25+o0.34c/0c+h+ml"
cb_phi_pos = f"{cb_sp_pos}+n "

# delay time
cmap_dt_in = "lapaz"
cmap_dt = f"{path_in}/{cmap_dt_in}_resampled_dt.cpt"
gmt.makecpt(cmap=cmap_dt_in, output=cmap_dt, series=[0, 3], reverse=True)
cb_dt_label = "a1f0.5+lnull | split app. delay time @~d@~t@-a@- / s"
cb_dt_pos = f"{cb_sp_pos}+ef0.2c+n "

# splitting intenstiy
cmap_si_in = "vik"
cmap_si = f"{path_in}/{cmap_si_in}_resampled_si.cpt"
gmt.makecpt(cmap=cmap_si_in, output=cmap_si, series=[-2, 2])
cb_si_label = "a1f0.5+lsplitting intensity SI"
cb_si_pos = f"{cb_sp_pos}+e0.2c"

# backazimuth
cmap_baz_in = "romaO"
cmap_baz = f"{path_in}/{cmap_baz_in}_resampled_baz.cpt"
gmt.makecpt(cmap=cmap_baz_in, output=cmap_baz, series=[0, 360, 1], cyclic=True)
cb_baz_label = "a60f30+lbackazimuth / @."
cb_baz_pos = cb_sp_pos

# -----------------------------------------------------------------------------
# Colors
color_land = "gray95"
color_sl = "gray50"  # shorelines
color_sta = "255/215/0"  # recording station -> GMT "gold"
color_hl = "255/90/0"  # highlight -> orange | URG paper

# phases
color_null = "white"
color_SKS = "216.75/82.875/24.990"  # -> red
color_SKKS = "236.895/176.97/31.875"  # -> orange
color_PKS = "yellow2"

# piercing points
marker_size_pp = "0.18c"
outline_width_pp = "0.8p"
alpha_pp = "@30"
incols_pp = [7, 8]

# ray path
alpha_ray = "@97"
color_ray_K_N = "black"
color_ray_K_NN = "black"
color_ray_KK_N = "black"
color_ray_KK_NN = "black"
color_ray_P_N = "black"
color_ray_P_NN = "black"

# LLVPs
color_llvp = "gray50"
pattern_llvp = "p8+b+f"

# box around map scale, legends, colorbars
box_standard = "+gwhite@30+p0.1p,gray30+r2p"
# text
clearance_standard = "0.1c+tO"

# -----------------------------------------------------------------------------
# Set up dictionaries for recording stations
dict_net = {}
dict_lat = {}
dict_lon = {}
dict_file = {}

station_file = open(f"{path_in}/stations_info.txt")
lines = station_file.readlines()
for line in lines[4:]:  # skip header line(s)
    (lon, lat, key) = line.split()
    dict_lon[key] = float(lon)
    dict_lat[key] = float(lat)
    dict_file[key] = key
station_file.close()

match status_station:
    case "URG":
        stations = ["WLS", "STU", "ECH", "TMO44", "TMO07"]
        lon_sta = dict_lon["BFO"]
        lat_sta = dict_lat["TMO07"]
        text_sta = status_station
    case "URGwithBFO":
        stations = ["BFO", "WLS", "STU", "ECH", "TMO44", "TMO07"]
        lon_sta = dict_lon["BFO"]
        lat_sta = dict_lat["TMO07"]
        text_sta = "URG & BFO"
    case _:
        stations = [status_station]
        lon_sta = dict_lon[status_station]
        lat_sta = dict_lat[status_station]
        text_sta = status_station


# %%
# -----------------------------------------------------------------------------
# Create geographic maps
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(MAP_GRID_PEN_PRIMARY="0.2p,lightgray", FONT_LABEL=font_size)

fig.basemap(projection=proj_lamb, region=region_lamb, frame=["WSne", "a10g10f5"])
fig.coast(land=color_land, shorelines=f"1/0.01p,{color_sl}")

# -----------------------------------------------------------------------------
# Plot LLVPs
for i_model in range(2, 9, 1):
    label = None
    if i_model == 2:
        label = "LLPVs"
    fig.plot(
        data=f"{path_in}/llvp/3model_2016_{i_model}.txt",
        pen=f"0.2p,{color_llvp}",
        fill=f"{pattern_llvp}{color_llvp}",
        close=True,
        label=label,
    )

# -----------------------------------------------------------------------------
# Plot ray paths (epicenter to station)
for station in stations:
    file_ray_same = f"{path_in}/rays/{dict_file[station]}_rays_swsm_"
    file_ray_K_N = f"{file_ray_same}K_N_goodfair.txt"
    file_ray_K_NN = f"{file_ray_same}K_NN_goodfair.txt"
    file_ray_KK_N = f"{file_ray_same}KK_N_goodfair.txt"
    file_ray_KK_NN = f"{file_ray_same}KK_NN_goodfair.txt"
    file_ray_P_N = f"{file_ray_same}P_N_goodfair.txt"
    file_ray_P_NN = f"{file_ray_same}P_NN_goodfair.txt"

    # null
    try:
        fig.plot(data=file_ray_K_N, pen=f"1p,{color_ray_K_N}{alpha_ray}")
    except:
        print(f"{dict_file[station]} no ray K_N")
    try:
        fig.plot(data=file_ray_KK_N, pen=f"1p,{color_ray_KK_N}{alpha_ray}")
    except:
        print(f"{dict_file[station]} no ray KK_N")
    try:
        fig.plot(data=file_ray_P_N, pen=f"1p,{color_ray_P_N}{alpha_ray}")
    except:
        print(f"{dict_file[station]} no ray P_N")
    # non-null
    try:
        fig.plot(data=file_ray_K_NN, pen=f"1p,{color_ray_K_NN}{alpha_ray}")
    except:
        print(f"{dict_file[station]} no ray K_NN")
    try:
        fig.plot(data=file_ray_KK_NN, pen=f"1p,{color_ray_KK_NN}{alpha_ray}")
    except:
        print(f"{dict_file[station]} no ray KK_NN")
    try:
        fig.plot(data=file_ray_P_NN, pen=f"1p,{color_ray_P_NN}{alpha_ray}")
    except:
        print(f"{dict_file[station]} no ray P_NN")

# -----------------------------------------------------------------------------
# Plot piercing points (iasp91)
# >> separate loops for ray paths and piercing points
# being ALL rays below ALL piercing points <<<
for station in stations:
    data_pp_same = f"{path_in}/pps/{dict_file[station]}_pp2700km_"
    data_K_N_pp = f"{data_pp_same}K_sp_N_goodfair_hd0km.txt"
    data_K_NN_pp = f"{data_pp_same}K_sp_NN_goodfair_hd0km.txt"
    data_KK_N_pp = f"{data_pp_same}KK_sp_N_goodfair_hd0km.txt"
    data_KK_NN_pp = f"{data_pp_same}KK_sp_NN_goodfair_hd0km.txt"
    data_P_N_pp = f"{data_pp_same}P_sp_N_goodfair_hd0km.txt"
    data_P_NN_pp = f"{data_pp_same}P_sp_NN_goodfair_hd0km.txt"

    match status_pp:
        case "phase":
            color_station = color_sta
            color_pp_K = color_SKS
            color_pp_KK = color_SKKS
            color_pp_P = color_PKS
            color_pp_N = color_null
        case "phi":
            color_station = color_sta
            color_pp = cmap_phi
            color_pp_N = color_null
            incols_pp = [0, 1, 2]
        case "dt":
            color_station = color_sta
            color_pp = cmap_dt
            color_pp_N = color_null
            incols_pp = [0, 1, 4]
        case "si":
            color_station = color_sta
            color_pp = cmap_si
            incols_pp = [0, 1, 5]
        case "baz":
            color_station = color_sta
            color_pp = cmap_baz
            incols_pp = [0, 1, 6]

    # points and squares instead of bars
    # to be able to distinguish SKS and SKKS phases
    if status_pp in ["phase"]:
        # null
        try:
            fig.plot(
                data=data_K_N_pp,  # SKS
                style=f"C{marker_size_pp}",
                fill=f"{color_pp_N}{alpha_pp}",
                pen=f"{outline_width_pp},{color_pp_K}{alpha_pp}",
            )
        except:
            print(f"{dict_file[station]} no pp K_N")
        try:
            fig.plot(
                data=data_KK_N_pp,  # SKKS
                style=f"S{marker_size_pp}",
                fill=f"{color_pp_N}{alpha_pp}",
                pen=f"{outline_width_pp},{color_pp_KK}{alpha_pp}",
            )
        except:
            print(f"{dict_file[station]} no pp KK_N")
        try:
            fig.plot(
                data=data_P_N_pp,  # PKS
                style=f"D{marker_size_pp}",
                fill=f"{color_pp_N}{alpha_pp}",
                pen=f"{outline_width_pp},{color_pp_P}{alpha_pp}",
            )
        except:
            print(f"{dict_file[station]} no pp P_N")
        # non-null
        try:
            fig.plot(
                data=data_K_NN_pp,  # SKS
                style=f"C{marker_size_pp}",
                fill=f"{color_pp_K}{alpha_pp}",
                pen=f"{outline_width_pp},black{alpha_pp}",
            )
        except:
            print(f"{dict_file[station]} no pp K_NN")
        try:
            fig.plot(
                data=data_KK_NN_pp,  # SKKS
                style=f"S{marker_size_pp}",
                fill=f"{color_pp_KK}{alpha_pp}",
                pen=f"{outline_width_pp},black{alpha_pp}",
            )
        except:
            print(f"{dict_file[station]} no pp KK_NN")
        try:
            fig.plot(
                data=data_P_NN_pp,  # PKS
                style=f"D{marker_size_pp}",
                fill=f"{color_pp_P}{alpha_pp}",
                pen=f"{outline_width_pp},black{alpha_pp}",
            )
        except:
            print(f"{dict_file[station]} no pp P_NN")

    elif status_pp in ["phi", "dt", "si", "baz"]:
        # null
        try:
            fig.plot(
                data=data_K_N_pp,
                style=f"C{marker_size_pp}",
                cmap=color_pp,
                pen=f"{outline_width_pp},black",
                incols=incols_pp,
            )
        except:
            print(f"{dict_file[station]} no pp K_N")
        try:
            fig.plot(
                data=data_KK_N_pp,
                style=f"S{marker_size_pp}",
                cmap=color_pp,
                pen=f"{outline_width_pp},black",
                incols=incols_pp,
            )
        except:
            print(f"{dict_file[station]} no pp KK_N")
        try:
            fig.plot(
                data=data_P_N_pp,
                style=f"D{marker_size_pp}",
                cmap=color_pp,
                pen=f"{outline_width_pp},black",
                incols=incols_pp,
            )
        except:
            print(f"{dict_file[station]} no pp P_N")
        # non-null
        try:
            fig.plot(
                data=data_K_NN_pp,
                style=f"C{marker_size_pp}",  # "j"
                cmap=color_pp,
                pen=f"{outline_width_pp},black",
                incols=incols_pp,
            )
        except:
            print(f"{dict_file[station]} no pp K_NN")
        try:
            fig.plot(
                data=data_KK_NN_pp,
                style=f"S{marker_size_pp}",  # "j"
                cmap=color_pp,
                pen=f"{outline_width_pp},black",
                incols=incols_pp,
            )
        except:
            print(f"{dict_file[station]} no pp KK_NN")
        try:
            fig.plot(
                data=data_P_NN_pp,
                style=f"D{marker_size_pp}",  # "j"
                cmap=color_pp,
                pen=f"{outline_width_pp},black",
                incols=incols_pp,
            )
        except:
            print(f"{dict_file[station]} no pp P_NN")

# -----------------------------------------------------------------------------
# Plot station symbol
fig.plot(x=lon_sta, y=lat_sta, style="i0.4", fill=color_sta, pen="0.8p,black")

# -----------------------------------------------------------------------------
# Add labels
args_label = {
    "pen": f"0.8p,{color_hl}",
    "font": f"{font_size},Helvetica-Bold,{color_hl}",
    "fill": "white@30",
    "clearance": clearance_standard,
}
# recording stations
fig.text(text=text_sta, x=lon_sta, y=lat_sta, offset="0c/-0.6c", **args_label)
# depth
fig.text(text="@@2700 km", position="TC", no_clip=True, **args_label)

# -----------------------------------------------------------------------------
# Add colorbars
with gmt.config(FONT="15p", MAP_FRAME_PEN="0.5p", MAP_TICK_LENGTH_PRIMARY="3p"):
    match status_pp:
        case "phi":
            fig.colorbar(cmap=cmap_phi, position=cb_phi_pos, frame=cb_phi_label)
        case "si":
            fig.colorbar(cmap=cmap_si, position=cb_si_pos, frame=cb_si_label)
        case "dt":
            fig.colorbar(cmap=cmap_dt, position=cb_dt_pos, frame=cb_dt_label)
        case "baz":
            fig.colorbar(cmap=cmap_baz, position=cb_baz_pos, frame=cb_baz_label)

# -----------------------------------------------------------------------------
# Add legend for piercing point symbols
match status_pp:
    case "phase":
        leg_file = "phase"
        legend_pos = "JRT+jRT+w2.5c"
    case _:
        leg_file = "phisi"
        legend_pos = "JLT+jLT+w2.2c"

fig.legend(
    spec=f"{path_in}/legend_gmt_pp_{leg_file}_lmm.txt",
    position=legend_pos,
    box=box_standard,
)

# -----------------------------------------------------------------------------
fig.show()
fig_name = f"FGR2024_GJI_FigS22_{status_station}_{status_pp}"
# for ext in ["png"]: #, "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=png_dpi)
print(fig_name)

# Remove colormap files
for cpt in glob.glob(f"{path_in}/*resampled*.cpt"):
    os.remove(cpt)
