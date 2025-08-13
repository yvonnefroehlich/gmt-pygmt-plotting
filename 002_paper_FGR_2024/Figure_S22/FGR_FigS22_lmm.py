# #############################################################################
# Fršhlich et al. (2024), GJI: Fig. S22
# Piercing points in the lowermost mantle
# -----------------------------------------------------------------------------
# Fršhlich Y., Grund M., Ritter J. R. R. (2024)
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
# - Author: Yvonne Fršhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt as gmt
import numpy as np


# %%
# -----------------------------------------------------------------------------
# Adjust for your needs
# -----------------------------------------------------------------------------
status_pc = "gpi"  ## "private", "gpi"
status_work = "URG"  ## "BFO", "URG"
status_grd = "land"  ## "land", "gypsum"
status_llvp = "yes"  ## "no", "yes"


#%%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
grd_dpi = 360
png_dpi = 360
font_size = "9p"

# color-coding of piercing points: "phase", "phi", "dt", "si", "baz", "station"
status_pp_all = ["phase", "phi", "dt", "si", "baz", "station"]

# depth of piecing points: lowermost mantle (D"" layer) im km
pp_depth_all = [2700]

# quality of shear wave splitting measurement: "goodfair", "all"
pp_quality_all = ["goodfair"]

# observation typ - shear wave splitting observed or not: "NNN", "NN", "N"
pp_NNN_all = ["NNN"]


# %%
# -----------------------------------------------------------------------------
# Projection and region
# -----------------------------------------------------------------------------
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

jj_lamb = f"L{lon0_lamb}/{lat0_lamb}/{lat1_lamb}/{lat2_lamb}/{width_lamb}"
RR_lamb = f"{lon_min_lamb}/{lon_max_lamb}/{lat_min_lamb}/{lat_max_lamb}"

jj_used = jj_lamb
RR_used = RR_lamb


# %%
# -----------------------------------------------------------------------------
# Set paths
# -----------------------------------------------------------------------------
match status_pc:
    case "private":
        path_grd = "C:/Users/Admin/C2/ColorGrid"
        path_same = "C:/Users/Admin/C2/EigeneDokumente/Studium/Promotion"
    case "gpi":
        path_grd = "/home/yfroe/ColorGrid"
        path_same = "/home/yfroe/Documents"

path_in = "01_in_data"
path_plot = f"{path_same}/E_GMT/map_lmm_ray/"
path_GR2019 = f"{path_same}/00_DATA_SWS/Grund_Ritter_2019_SuppMat/"

# plate boundaries; Bird 2003
file_platbound = f"{path_grd}/plate_boundaries_Bird_2003.txt"

# mantle tomography GyPSuM; Simmons et al. 2010
name_grid_gypsum = "tomographyGyPSuM_Simmons2010/dvs_self_grid/" + \
                    "tomo_gypsum_5m_grid_dvs_22_2650-2900km.grd"


# %%
# -----------------------------------------------------------------------------
# Create colormaps and colorbars
# -----------------------------------------------------------------------------
# tomography GyPSuM Simmons et al. 2010
cmap_tomo_in = "roma"
cmap_tomo_out = f"{path_grd}/{cmap_tomo_in}_resampled_gypsum.cpt"
gmt.makecpt(
    cmap=cmap_tomo_in,
    output=cmap_tomo_out,
    #series=[-2.5, 2.5, 0.01],
    series=[-2, 2, 0.01],
    # series=[-1.5, 1.5, 0.01], # GR2019
)
cmap_gypsum = cmap_tomo_out
# cmap_gypsum = f"{path_GR2019}cmap_gypsum.cpt" # GR2019

#tomo_cpt_str = "cptroma25_"
tomo_cpt_str = "cptroma15_"
#tomo_cpt_str = "cptGR15_"

cb_gypsum_label = "a1f0.5+ldv@-s@- / %" # subscript in gmt (here dv_s)
cb_gypsum_pos = "JLT+jLT+w3.5/0.25+o0.3c/0.0c+h+ml+e"
# J position
# +j justification
# +h horizontal
# +o offset
# +m move annotations and labels to opposite side
# for horizontal default below i. e. above
# for vertical default right i. e. left
# a annatation, l label, u unit

# -----------------------------------------------------------------------------
# fast polarization direction
cmap_phi_in = "phase"
cmap_phi_out = f"{path_in}/{cmap_phi_in}_resampled_phi.cpt"
match status_pc:
    case "gpi": cmap_phi_in = f"{path_in}/{cmap_phi_in}.cpt"

gmt.makecpt(
    cmap=cmap_phi_in,
    output=cmap_phi_out,
    series=[-90, 90],
    cyclic=True,
)
cmap_phi = cmap_phi_out

cb_phi_label = "a30f10+lnull | split app. fast pol. dir. @~f@~@-a@- / N@.E"
cb_sp_pos = "JRT+jRT+w3.5/0.25+o0.34c/0c+h+ml"
cb_phi_pos = f"{cb_sp_pos}+n "

# -----------------------------------------------------------------------------
# delay time
cmap_dt_in = "lapaz"
cmap_dt_out = f"{path_in}/{cmap_dt_in}_resampled_dt.cpt"
gmt.makecpt(
    cmap=cmap_dt_in,
    output=cmap_dt_out,
    series=[0, 3],
    reverse=True,
)
cmap_dt = cmap_dt_out

cb_dt_label = "a1f0.5+lnull | split app. delay time @~d@~t@-a@- / s"
cb_dt_pos = f"{cb_sp_pos}+ef+n "

# -----------------------------------------------------------------------------
# splitting intenstiy
cmap_si_in = "vik"
cmap_si_out = f"{path_in}/{cmap_si_in}resampled_si.cpt"
gmt.makecpt(
    cmap=cmap_si_in,
    output=cmap_si_out,
    series=[-2, 2],
)
cmap_si = cmap_si_out

cb_si_label = "a1f0.5+lsplitting intensity SI"
cb_si_pos = f"{cb_sp_pos}+e"

# -----------------------------------------------------------------------------
# backazimuth
cmap_baz_in = "romaO"
cmap_baz_out = f"{path_in}/{cmap_baz_in}_resampled_baz.cpt"
gmt.makecpt(
    cmap=cmap_baz_in,
    output=cmap_baz_out,
    series=[0, 360, 1],
    cyclic=True,
)
cmap_baz = cmap_baz_out

cb_baz_label = "a60f30+lbackazimuth @."
cb_baz_pos = cb_sp_pos


# %%
# -----------------------------------------------------------------------------
# Colors
# -----------------------------------------------------------------------------
color_land = "gray95"
color_shorelines = "gray50"
color_land = "tan@85"
color_shorelines = "gray70"
color_platbound = "216.750/82.875/24.990"
color_station_symbole = "255/215/0"  # GMT "gold"
# color_station_lable = "162/20/47"  # 0.6350 0.0780 0.1840 # -> darkred
color_highlight = "255/90/0"  # -> orange | URG paper

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
color_HLFL = "green3"
color_missing = "gray30"

# box around map scale, legends, colorbars
box_standard = "+gwhite@30+p0.1p,gray30+r2p"
# text
clearance_standard = "0.1c/0.1c+tO"


# %%
# -----------------------------------------------------------------------------
# Set up dictionaries for recording stations
# -----------------------------------------------------------------------------
dict_net = {}
dict_lat = {}
dict_lon = {}
dict_file = {}
dict_col = {}

station_file = open(f"{path_grd}/stations_info.txt", "r")
lines = station_file.readlines()
for line in lines[2:]:  # skip header line(s)
   (net, key, lat, lon, file, label, qstereo, sty, off01, off02, col, rand) = line.split()
   dict_net[key] = net
   dict_lat[key] = float(lat)
   dict_lon[key] = float(lon)
   dict_file[key] = file
   dict_col[key] = col
station_file.close()

# -----------------------------------------------------------------------------
match status_work:
    case "BFO":
        key_choose = ["BFO"]
    case "URG":
        key_choose = ["WLS", "STU", "ECH", "TMO44", "TMO07"]
    case "PhD":
        key_choose = [
            "BFO", "WLS", "STU", "ECH",
            "MILB", "TNS", "WLF",
            "TMO44", "TMO07",
            "TMO22", "TMO26", "TMO65", "A121A", "A129A",
            "BERGE", "METMA", "SLE", "EMING",
        ]
    case "all":
        key_choose = [
            "BFO", "WLS", "STU", "ECH",
            "MILB", "TNS", "WLF",
            "TMO44", "TMO07",
            "TMO20", "TMO22", "TMO26", "TMO65", "A129A",
            "BERGE", "METMA", "SLE", "EMING",
            "SFN01",
            "TMO08", "TMO09", "TMO10", "TMO11", "TMO12", "TMO13","TMO19",
        ]


#%%
# -----------------------------------------------------------------------------
# Create geographic maps
# -----------------------------------------------------------------------------
for status_pp in status_pp_all:

    for pp_NNN in pp_NNN_all:

        for pp_quality in pp_quality_all:

            for pp_depth in pp_depth_all:

# -----------------------------------------------------------------------------
                fig = gmt.Figure()

                # Set GMT default values globally
                gmt.config(
                    MAP_GRID_PEN_PRIMARY="0.2p,lightgray",
                    MAP_FRAME_TYPE="fancy+",
                    FONT_LABEL=font_size,
                    COLOR_NAN="white",
                )

# -----------------------------------------------------------------------------
                frame_used_agf = "a10g10f5"
                match status_work:
                    case "BFO": frame_used = ["WSne", frame_used_agf]
                    case "URG": frame_used = ["wSnE", frame_used_agf]

                coast_args = {
                    "frame": frame_used,
                    "resolution": "h",
                    "area_thresh": "30000",
                    "shorelines": "1/0.01p,gray70",
                }
                match status_grd:
                    case "gypsum":
                        fig.grdimage(
                            projection=jj_used,
                            region=RR_used,
                            grid=f"{path_grd}/{name_grid_gypsum}",
                            dpi=grd_dpi,
                            cmap=cmap_gypsum,
                        )
                        fig.coast(**coast_args)
                    case "land":
                        fig.coast(
                            projection=jj_used,
                            region=RR_used,
                            land=color_land,
                            **coast_args,
                        )

# -----------------------------------------------------------------------------
                # Plot LLVPs
                if status_llvp=="yes":
                # for i_model in range(1, 9, 1):
                    for i_model in range(2, 9, 1):
                        label = None
                        if i_model==2: label = "LLPVs"
                        fig.plot(
                            data=f"{path_in}/llvp/3model_2016_{i_model}.txt",
                            pen=f"0.2p,{color_llvp}",
                            fill=f"{pattern_llvp}{color_llvp}",
                            close=True,
                            label=label,
                        )

# -----------------------------------------------------------------------------
                # Plot plate boundaries
                # fig.plot(data=file_platbound, pen=f"0.5p,{color_platbound}")

# -----------------------------------------------------------------------------
                # Plot ray paths (epicenter to station)
                for key in key_choose:
                    file_ray_same = f"{path_grd}/raypaths/swsm_sep/" + \
                                        f"{dict_file[key]}_rays_swsm_"
                    file_ray_K_N = f"{file_ray_same}K_N_{pp_quality}.txt"
                    file_ray_K_NN = f"{file_ray_same}K_NN_{pp_quality}.txt"
                    file_ray_KK_N = f"{file_ray_same}KK_N_{pp_quality}.txt"
                    file_ray_KK_NN = f"{file_ray_same}KK_NN_{pp_quality}.txt"
                    file_ray_P_N = f"{file_ray_same}P_N_{pp_quality}.txt"
                    file_ray_P_NN = f"{file_ray_same}P_NN_{pp_quality}.txt"

                    if pp_NNN!="NN":  # -> N and NNN; null
                        try:
                            fig.plot(
                                data=file_ray_K_N,
                                pen=f"1p,{color_ray_K_N}{alpha_ray}",
                            )
                        except: print(f"{dict_file[key]} no ray K_N")
                        try:
                            fig.plot(
                                data=file_ray_KK_N,
                                pen=f"1p,{color_ray_KK_N}{alpha_ray}",
                            )
                        except: print(f"{dict_file[key]} no ray KK_N")
                        try:
                            fig.plot(
                                data=file_ray_P_N,
                                pen=f"1p,{color_ray_P_N}{alpha_ray}",
                            )
                        except: print(f"{dict_file[key]} no ray P_N")
                    if pp_NNN!="N":  # -> NN and NNN; non-null
                        try:
                            fig.plot(
                                data=file_ray_K_NN,
                                pen=f"1p,{color_ray_K_NN}{alpha_ray}",
                            )
                        except: print(f"{dict_file[key]} no ray K_NN")
                        try:
                            fig.plot(
                                data=file_ray_KK_NN,
                                pen=f"1p,{color_ray_KK_NN}{alpha_ray}",
                            )
                        except: print(f"{dict_file[key]} no ray KK_NN")
                        try:
                            fig.plot(
                                data=file_ray_P_NN,
                                pen=f"1p,{color_ray_P_NN}{alpha_ray}",
                            )
                        except: print(f"{dict_file[key]} no ray P_NN")

# -----------------------------------------------------------------------------
                # Plot piercing points (iasp91)
                # >> separate loops for ray paths and piercing points
                # being ALL rays below ALL piercing points <<<
                for key in key_choose:
                    data_pp_same = f"{path_grd}/piercingpoints/pp_sp/" + \
                                   f"{dict_file[key]}_pp{pp_depth}km_"
                    data_K_N_pp = f"{data_pp_same}K_sp_N_{pp_quality}_hd0km.txt"
                    data_K_NN_pp = f"{data_pp_same}K_sp_NN_{pp_quality}_hd0km.txt"
                    data_KK_N_pp = f"{data_pp_same}KK_sp_N_{pp_quality}_hd0km.txt"
                    data_KK_NN_pp = f"{data_pp_same}KK_sp_NN_{pp_quality}_hd0km.txt"
                    data_P_N_pp = f"{data_pp_same}P_sp_N_{pp_quality}_hd0km.txt"
                    data_P_NN_pp = f"{data_pp_same}P_sp_NN_{pp_quality}_hd0km.txt"

                    match status_pp:
                        case "phase":
                            color_station = color_station_symbole
                            color_pp_K = color_SKS
                            color_pp_KK = color_SKKS
                            color_pp_P = color_PKS
                            color_pp_N = color_null
                        case "station":
                            color_station = dict_col[key]
                            color_pp_K = dict_col[key]
                            color_pp_KK = dict_col[key]
                            color_pp_P = dict_col[key]
                            color_pp_N = color_null
                        case "phi":
                            color_station = color_station_symbole
                            color_pp = cmap_phi
                            color_pp_N = color_null
                            incols_pp = [0, 1, 2]
                        case "dt":
                            color_station = color_station_symbole
                            color_pp = cmap_dt
                            color_pp_N = color_null
                            incols_pp = [0, 1, 4]
                        case "si":
                            color_station = color_station_symbole
                            color_pp = cmap_si
                            incols_pp = [0, 1, 5]
                        case "baz":
                            color_station = color_station_symbole
                            color_pp = cmap_baz
                            incols_pp = [0, 1, 6]

                    # points and squares instead of bars
                    # to be able to distinguish SKS and SKKS phases

                    if status_pp in ["phase", "station"]:
                        if pp_NNN!="NN":  # -> N and NNN; null
                            try:
                                fig.plot(
                                    data=data_K_N_pp, # SKS
                                    style=f"C{marker_size_pp}",
                                    fill=f"{color_pp_N}{alpha_pp}",
                                    pen=f"{outline_width_pp},{color_pp_K}{alpha_pp}",
                                )
                            except: print(f"{dict_file[key]} no pp K_N")
                            try:
                                fig.plot(
                                    data=data_KK_N_pp,  # SKKS
                                    style=f"S{marker_size_pp}",
                                    fill=f"{color_pp_N}{alpha_pp}",
                                    pen=f"{outline_width_pp},{color_pp_KK}{alpha_pp}",
                                )
                            except: print(f"{dict_file[key]} no pp KK_N")
                            try:
                                fig.plot(
                                    data=data_P_N_pp,  # PKS
                                    style=f"D{marker_size_pp}",
                                    fill=f"{color_pp_N}{alpha_pp}",
                                    pen=f"{outline_width_pp},{color_pp_P}{alpha_pp}",
                                )
                            except: print(f"{dict_file[key]} no pp P_N")
                        if pp_NNN!="N":  # -> NN and NNN; non-null
                            try:
                                fig.plot(
                                    data=data_K_NN_pp,  # SKS
                                    style=f"C{marker_size_pp}",
                                    fill=f"{color_pp_K}{alpha_pp}",
                                    pen=f"{outline_width_pp},black{alpha_pp}",
                                )
                            except: print(f"{dict_file[key]} no pp K_NN")
                            try:
                                fig.plot(
                                    data=data_KK_NN_pp,  # SKKS
                                    style=f"S{marker_size_pp}",
                                    fill=f"{color_pp_KK}{alpha_pp}",
                                    pen=f"{outline_width_pp},black{alpha_pp}",
                                )
                            except: print(f"{dict_file[key]} no pp KK_NN")
                            try:
                                fig.plot(
                                    data=data_P_NN_pp,  # PKS
                                    style=f"D{marker_size_pp}",
                                    fill=f"{color_pp_P}{alpha_pp}",
                                    pen=f"{outline_width_pp},black{alpha_pp}",
                                )
                            except: print(f"{dict_file[key]} no pp P_NN")

                    elif status_pp in ["phi", "dt", "si", "baz"]:
                        if pp_NNN!="NN":  # -> N and NNN; null
                            try:
                                fig.plot(
                                    data=data_K_N_pp,
                                    style=f"C{marker_size_pp}",
                                    cmap=color_pp,
                                    pen=f"{outline_width_pp},black",
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp K_N")
                            try:
                                fig.plot(
                                    data=data_KK_N_pp,
                                    style=f"S{marker_size_pp}",
                                    cmap=color_pp,
                                    pen=f"{outline_width_pp},black",
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp KK_N")
                            try:
                                fig.plot(
                                    data=data_P_N_pp,
                                    style=f"D{marker_size_pp}",
                                    cmap=color_pp,
                                    pen=f"{outline_width_pp},black",
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp P_N")
                        if pp_NNN!="N":  # -> NN and NNN; non-null
                            try:
                                fig.plot(
                                    data=data_K_NN_pp,
                                    style=f"C{marker_size_pp}",  #"j"
                                    cmap=color_pp,
                                    pen=f"{outline_width_pp},black",
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp K_N")
                            try:
                                fig.plot(
                                    data=data_KK_NN_pp,
                                    style=f"S{marker_size_pp}",  #"j"
                                    cmap=color_pp,
                                    pen=f"{outline_width_pp},black",
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp KK_NN")
                            try:
                                fig.plot(
                                    data=data_P_NN_pp,
                                    style=f"D{marker_size_pp}",  #"j"
                                    cmap=color_pp,
                                    pen=f"{outline_width_pp},black",
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp P_NN")

# -----------------------------------------------------------------------------
                    # Plot station symbol
                    fig.plot(
                        x=dict_lon[key],
                        y=dict_lat[key],
                        style="i0.3",
                        fill=color_station,
                        pen="0.8p,black",
                    )

# -----------------------------------------------------------------------------
                # Add labels
                # recording stations
                fig.text(
                    text=status_work,
                    x=dict_lon["BFO"],
                    y=dict_lat["TMO07"],
                    offset="0c/-0.6c",
                    pen=f"0.8p,{color_highlight}",
                    font=f"{font_size},Helvetica-Bold,{color_highlight}",
                    fill="white@30",
                    clearance=clearance_standard,
                )
                # depth
                if status_work=="URG" and status_pp=="si":
                    fig.text(
                        text=f"@@{pp_depth} km",
                        position="TL",
                        offset="0.5c/-0.5c",
                        pen=f"0.5p,{color_highlight}",
                        font=f"{font_size},Helvetica-Bold,{color_highlight}",
                        fill="white@30",
                        clearance=clearance_standard,
                    )

# -----------------------------------------------------------------------------
                # Add colorbars
                with gmt.config(
                    FONT="8p",
                    MAP_FRAME_PEN="0.5p",
                    MAP_TICK_LENGTH_PRIMARY="3p",
                ):
                    # tomography
                    if status_work!="URG" and status_grd=="gypsum":
                        fig.colorbar(
                            cmap=cmap_gypsum,
                            position=cb_gypsum_pos,
                            frame=cb_gypsum_label,
                        )

                    # piercing points
                    if status_grd!="gypsum" and status_work=="BFO":
                        match status_pp:
                            case "phi":
                                fig.colorbar(
                                    cmap=cmap_phi,
                                    position=cb_phi_pos,
                                    frame=cb_phi_label,
                                )
                            case "si":
                                fig.colorbar(
                                    cmap=cmap_si,
                                    position=cb_si_pos,
                                    frame=cb_si_label,
                                )
                            case "dt":
                                fig.colorbar(
                                    cmap=cmap_dt,
                                    position=cb_dt_pos,
                                    frame=cb_dt_label,
                                )
                            case "baz":
                                fig.colorbar(
                                    cmap=cmap_baz,
                                    position=cb_baz_pos,
                                    frame=cb_baz_label,
                                )

# -----------------------------------------------------------------------------
                # Add legend for piercing point symbols
                match status_pp:
                    case "phase":
                        leg_file = "phase"
                        legend_pos = "JRT+jLT+w2.5c+o-3.4c/0.5c"
                        legend_pos = "JRT+jLT+w2.5c+o-2.8c/0.5c"
                    case "phi" | "si":
                        leg_file = "phisi"
                        legend_pos = "JRT+jLT+w2.1c+o-2.3c/1.2c"
                        legend_pos = "JLT+jLT+w2.1c+o0.5c"

                if status_work=="URG" and status_pp=="phi":
                    fig.legend(
                        spec=f"{path_in}/legend_gmt_pp_{leg_file}_lmm.txt",
                        position=legend_pos,
                        box=box_standard,
                    )

#  ----------------------------------------------------------------------------
                #"""
                # Add figure labels
                if status_work=="BFO" and status_pp=="phi": fig_lab_lmm = "(a)"
                elif status_work=="URG" and status_pp=="phi": fig_lab_lmm = "(b)"
                elif status_work=="BFO" and status_pp=="si": fig_lab_lmm = "(c)"
                elif status_work=="URG" and status_pp=="si": fig_lab_lmm = "(d)"
                elif status_pp=="baz": fig_lab_lmm = "(e)"
                else: fig_lab_lmm = ""

                if status_grd!="gypsum":
                    fig.text(
                        position="TC",
                        justify="TC",
                        text=fig_lab_lmm,
                        font="11p,Helvetica-Bold,black",
                    )
                #"""

# -----------------------------------------------------------------------------
               # Show and save figure
                pp_quality_str = pp_quality

                grd_str = "_land_"
                if status_grd=="gypsum": grd_str = "_dvs_"

                llvp_str = "_"
                if status_llvp=="yes": llvp_str = "_llvp"

                filename_ray_pp = f"{status_work}_pp{pp_depth}km_" + \
                                    f"{status_pp}_{pp_NNN}{pp_quality_str}" + \
                                    f"{llvp_str}{grd_str}lamb{status_cc}"
                filename_ray_pp_tot = f"03_out_maps_lamb/" + \
                                        f"{status_work}/{filename_ray_pp}"
                filename_ray_pp_tot = f"03_out_maps_lamb/00_TEST4phd/{filename_ray_pp}"

                fig.show() #method="external")
                for ext in ["png", "pdf", "eps"]:
                    fig.savefig(fname=f"{filename_ray_pp_tot}.{ext}", dpi=png_dpi)
                print(filename_ray_pp)
