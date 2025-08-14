# #############################################################################
# Fr�hlich et al. (2024), GJI: Fig. 9
# Piercing points in the upper mantle
# -----------------------------------------------------------------------------
# Fr�hlich Y., Grund M., Ritter J. R. R. (2024)
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
# - Author: Yvonne Fr�hlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import glob
import os

import geopandas as gpd
import pandas
import pygmt as gmt
import numpy as np


# %%
# #############################################################################
# Adjust for your needs
# #############################################################################
status_pc = "private"  ## "private", "gpi"  # paths corresponding to computer
status_size = "large"  ## "small", "large"  # region
status_grid = "ele"  ## "ele"[vation], "tomo"[graphy], "geo"[olgy]"bw" / "all"
status_color = "co"  ## "", "bw", "co", "dvs", "dvp"  # colormap for elevation or velocity anomaly
status_cb_ele_tomo = ""  ## "", "yes"  # add colorbar for elevation or tomography
status_stereo = "no"  ## "no", "stereo"  # plot stereoplots for SWSMs
status_inset_epi = ""  ## "", "epi"  # inset for epicenter distribution of SWSMs
status_station_epi = ""  ## "STU", "BFO" which station also for colorwheel
status_pp = "no"  ## "no", "station", "phi", "dt", "si", "baz"  # color-coding of piercing points
status_inset_pp = ""  ## "", "yes"  # add sketch for piercining points concept
status_depth_label = ""  ## "", "yes"  # add depth label
status_scale = "yes"  ## "", "yes"  # add length scale
basemap_frame = ["WSNe", "a0.5f0.25", "x+e"]  # +e skip annotation at end of axis
MAP_ANNOT_OBLIQUE = "" #"lat_parallel"
label_frame = ""  ## "_1x2", "_2x2"  # for URG manuscript
status_inset_study = "ortho"  ## "", "merca", "ortho"  # projection of inset of study area
status_work = "MA"  ## "MA", "PhD", "all"  # which work especially stations
status_con = ""  ## "", "geoarr", "3D"  # which context
status_null = ""  ## "", "nullano"  # highlight nulls
status_var = ""  ## "", "latvar"  # highlight subregions

depth_step = 10
pierce_depth_all = np.arange(200, 200 + depth_step, depth_step)  # depth in km; [min,max[,step
pierce_obs_all = ["NNN"]  ## "N", "NN", "NNN" # observation type
pierce_qual_all = ["goodfair"]  ## "all", "goodfair" # quality category

grid_dpi = 360
png_dpi = 360
size_stereo = 3.2  # in centimeters



# %%
# #############################################################################
# Set up
# #############################################################################

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
match status_pc:
    case "private":
        path_grid = "C:/Users/Admin/C2/ColorGrid"
        path_plot = "C:/Users/Admin/C2/EigeneDokumente/Studium/Promotion"
    case "gpi":
        path_grid = "/home/yfroe/ColorGrid"
        path_plot = "/home/yfroe/Documents"

path_in = "01_in_data"
path_out = "02_out_fig"


# -----------------------------------------------------------------------------
# Files for
# -----------------------------------------------------------------------------
# Towns
file_twons_in = f"{path_in}/rhein_towns.dat"

# Recording stations
file_station_in = f"{path_grid}/stations_info.txt"

# Faults
file_URGborder_in = f"{path_grid}/faults_URGwesteast.geo"
file_URGnormal_in = f"{path_grid}/faults_URGnormal.geo"
file_faults_in = f"{path_grid}/faults_LLBB_TH_BLZ.geo"

# Plate boundaries; Bird 2003
file_plate_in = f"{path_grid}/plate_boundaries_Bird_2003.txt"

# Epicenter distribution
file_epi_in = f"{path_grid}/epicenters"

# Ray paths
file_ray_in = f"{path_grid}/raypaths"

# Elevation
file_ele_in = "srtm_FRBS.grd"
file_shading_in = "int_srtm_FRBS.grd"


# -----------------------------------------------------------------------------
# Coordinates for
# -----------------------------------------------------------------------------
# Kaiserstuhl Volcanic Complex (KVC)
lon_KVC = 7.690556
lat_KVC = 48.120833

# Vogelsberg Volcanic Complex (VVC)
lon_VVC = 9.242944
lat_VVC = 50.533528


# -----------------------------------------------------------------------------
# Colormaps
# -----------------------------------------------------------------------------
# Tomography EU60 dvs, dvp; Zhu et al. 2015
# Scientific Colour Maps by F. Crameri
cmap_EU60_in = "roma"
cmap_EU60_dvs_out = f"{path_in}/{cmap_EU60_in}_resampled_EU60_dvs.cpt"
cmap_EU60_dvp_out = f"{path_in}/{cmap_EU60_in}_resampled_EU60_dvp.cpt"
gmt.makecpt(cmap=cmap_EU60_in, output=cmap_EU60_dvs_out, series=[-4, 4, 0.1])
gmt.makecpt(cmap=cmap_EU60_in, output=cmap_EU60_dvp_out, series=[-3, 3, 0.1])

# -----------------------------------------------------------------------------
# Elevation
# Scientific Colour Maps by F. Crameri
cmap_bw_in = "grayC"
cmap_bw_out = f"{path_in}/{cmap_bw_in}_resampled_topo.cpt"
gmt.makecpt(cmap=cmap_bw_in, output=cmap_bw_out, series=[0, 2000, 10])

cmap_co_in = f"{path_in}/europe_3.cpt"
cmap_co_out = f"{path_in}/europe_3_resampled_insert.cpt"
gmt.makecpt(cmap=cmap_co_in, output=cmap_co_out, series=[0, 2000, 10])

# -----------------------------------------------------------------------------
# Fast polarization direction
# cmocean colormaps by Thyung et al. 2016
cmap_phi_in = "phase"
cmap_phi_out = f"{path_in}/{cmap_phi_in}_resampled_phi.cpt"
gmt.makecpt(
    cmap=f"{path_in}/{cmap_phi_in}.cpt",
    output=cmap_phi_out,
    series=[-90, 90],
    cyclic=True,
)

# -----------------------------------------------------------------------------
# Delay time
# Scientific Colour maps by F. Crameri
cmap_dt_in = "lapaz"
cmap_dt_out = f"{path_in}/{cmap_dt_in}_resampled_dt.cpt"
gmt.makecpt(
    cmap=cmap_dt_in, output=cmap_dt_out, series=[0, 3], reverse=True,
)

# -----------------------------------------------------------------------------
# Splitting intensity
# Scientific Colour maps by F. Crameri
cmap_si_in = "vik"
cmap_si_out = f"{path_in}/{cmap_si_in}_resampled_si.cpt"
gmt.makecpt(cmap=cmap_si_in, output=cmap_si_out, series=[-2, 2])  # "-3/3"

# -----------------------------------------------------------------------------
# Backazimuth
# Scientific Colour maps by F. Crameri
# phase, romaO, bamO, brocO, corkO, vikO
cmap_baz_in = "romaO"
cmap_baz_out = f"{path_in}/{cmap_baz_in}_resampled_baz.cpt"
gmt.makecpt(
    cmap=cmap_baz_in, output=cmap_baz_out, series=[0, 360, 1], cyclic=True,
)

# -----------------------------------------------------------------------------
# Hypocentral depth
# Scientific Colour maps by F. Crameri
# >>> Must be consistent with epicentral distance plot for Fig S <<<
cmap_hypo_in = "lajolla"
cmap_hypo_out_cut = f"{path_in}/{cmap_hypo_in}_resampled_hypo.cpt"
hypodepth_max = 500
pen_epi = "0.01,gray20"
cb_epi_e = "+ef0.15c"
gmt.makecpt(
    cmap=cmap_hypo_in, output=cmap_hypo_out_cut, series=[0, hypodepth_max],
)

# -----------------------------------------------------------------------------
cmap_insert = cmap_bw_out
cmap_phi = cmap_phi_out
cmap_si = cmap_si_out
cmap_dt = cmap_dt_out
cmap_baz = cmap_baz_out
cmap_hypo = cmap_hypo_out_cut
match status_color:
    case "bw": cmap_URG = cmap_bw_out
    case "co": cmap_URG = cmap_co_out
    case "dvs": cmap_URG = cmap_EU60_dvs_out
    case "dvp": cmap_URG = cmap_EU60_dvp_out


# -----------------------------------------------------------------------------
# Colors
# -----------------------------------------------------------------------------
color_land = "gray80"
color_water = "gray75"
if status_inset_study=="ortho": color_water = "steelblue"

# color_platebound = "255/128/128"  # -> light pink | stuff MG
color_platebound = "216.750/82.875/24.990"

color_URG = "darkbrown"  # "sienna"
color_null_ano = "255/90/0"  # -> orange | URG paper

# color_station_marker = "24/116/205" # blue | BFO paper
color_station_marker = "255/215/0"  # = GMT "gold"
# color_station_lable = "162/20/47"  # -> darkred | MA YF
color_station_lable = "255/90/0"  # -> orange | URG paper

coast_rivers = "r/1p,dodgerblue2"
coast_water = "steelblue"
coast_borders = "1/1p,black"


# -----------------------------------------------------------------------------
# Region and Projection
# -----------------------------------------------------------------------------
match status_size:

    case "small":
        lon_min = 6.9; lon_max = 9.6
        lat_min = 47.8; lat_max = 49.2

        if status_con == "3D":
            lon_min = 6.35; lon_max = 10.25
            lat_min = 47.7; lat_max = 49.7

    case "large":
        match status_work:
            case "MA":
                lon_min = 6; lon_max = 10.15
                lat_min = 47.4; lat_max = 50

                if status_pp == "no":
                    lon_min = 6; lon_max = 10
                    lat_min = 46.5; lat_max = 50.7

            case "PhD" | "all":
                lon_min = 6; lon_max = 10
                lat_min = 46.5; lat_max = 50.7

region_main = [lon_min, lon_max, lat_min, lat_max]


# -----------------------------------------------------------------------------
# Legends, colorbar, scale
# -----------------------------------------------------------------------------
# files for legends
leg_sta_file = "legend_gmt_stations.txt"
leg_stereo_file = "legend_gmt_stereoplot.txt"
leg_pp_sta_file = "legend_gmt_pp_station.txt"
leg_pp_phisi_file = "legend_gmt_pp_phisi.txt"
leg_pp_file = "legend_gmt_pp.txt"
leg_dt_file = "legend_gmt_delaytime.txt"
leg_mag_file = "legend_gmt_magitude.txt"
leg_fal_file = "legend_gmt_faults.txt"
leg_all_file = "legend_gmt_overall.txt"

# positions
leg_sta_pos = "JRB+jLB+w4.5c+o-4.65c/1.45c"
# leg_stereo_pos = "JRB+jLB+w2.2c+o-2.31c/1.45c"
leg_stereo_pos = "JRB+jLB+w2.2c+o-2.31c/0.09c"
leg_pp_pos = "JRB+jLB+w2.0c+o-2.10c/1.45c"
leg_dt_pos = "JRB+jLB+w2.8c+o-5.00c/1.45c"

leg_pp_pos = "JMB+jLB+w2.0c+o-1.95c/0.08c"
leg_dt_pos = "JMB+jLB+w2.8c+o0.15c/0.08c"

leg_mag_pos = "JBC+jBL+w5.4c+o-3.40c/1.45c"

leg_fal_pos = "JLB+jLB+w3.15c+o0.17c/1.45c"
if status_size=="small": leg_fal_pos = "JRB+jLB+w3.1c+o-4.65c/2.65c"

cb_ele_pos = "x10.80c/0.65c+w3.5c/0.2c+h+ml"  # +w width of [color]bar not of box
cb_tomo_pos = "x10.95c/0.65c+w3.5c/0.2c+h+ml"
cb_pp_pos = "x5.025c/0.65c+w4.8c/0.2c+h+ml"
cb_pp_pos = "x6.73c/0.65c+w4.8c/0.2c+h+ml"
if status_pp!="no" and status_size=="large":
    cb_pp_pos = "x4.82c/0.65c+w4.8c/0.2c+h+ml"  # more centered
cb_hd_pos = "x4.50c/0.65c+w4.5c/0.2c+h+ml"

# scale
basemap_scale = f"JLB+jLB+w50+c{(lon_max+lon_min)/2}/{(lat_max+lat_min)/2}+f+lkm+at+o0.45c/0.55c"
# Box around map scale, legends, colorbars
# Rounded edges only for set / fix width not for automatic width determination
box_standard = "+gwhite@30+p0.8p,black+r2p"
# box_standard = "+gwhite@30+p0.1p,gray30+r2p"

# text
clearance_standard = "0.1c/0.1c+tO"


# -----------------------------------------------------------------------------
# Dictionaries for recording stations
# -----------------------------------------------------------------------------
dict_net = {}
dict_lat = {}
dict_lon = {}
dict_file = {}
dict_label = {}
dict_qstereo = {}
dict_sty = {}
dict_off = {}
dict_col = {}
dict_rand = {}

station_file = open(file_station_in,"r")
lines = station_file.readlines()
for line in lines[2:]:  # skip header line(s)
   (net, key, lat, lon, file, label, qstereo, sty, off01, off02, col, rand) = line.split()
   dict_net[key] = net
   dict_lat[key] = float(lat)
   dict_lon[key] = float(lon)
   dict_file[key] = file
   dict_label[key] = label
   dict_qstereo[key] = qstereo
   dict_sty[key] = sty
   dict_off[key] = [off01,off02]
   dict_col[key] = col
   if status_work=="MA": dict_rand[key] = "black"
   else: dict_rand[key] = rand
station_file.close()

# -----------------------------------------------------------------------------
# Filtering of stations based on work
match status_work:
    case "MA":
        key_choose = [
            "BFO", "WLS", "STU", "ECH", "TMO44", "TMO07",
        ]
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
            "TMO08", "TMO09", "TMO10", "TMO11", "TMO12", "TMO13", "TMO19",
        ]


# -----------------------------------------------------------------------------
# Geological units
# -----------------------------------------------------------------------------
# Baden-Württemberg: https://maps.lgrb-bw.de
# Rheinland-Pfalz: https://mapclient.lgb-rlp.de
shp_geology = f"{path_in}/geology_BW_LGRB/gu300af_m"

# https://geopandas.org/en/stable/docs/user_guide/projections.html
gpd_btn = gpd.read_file(f"{shp_geology}.shp")
# gpd_btn.crs

gpd_btn_wgs84 = gpd_btn.to_crs('EPSG:4326')
# gpd_btn_wgs84.crs

gpd_btn_zeitalter = gpd_btn_wgs84["Zeitalter"]
gpd_btn_zeitalter_unique = list(dict.fromkeys(gpd_btn_zeitalter))

# -----------------------------------------------------------------------------
# Set up dictionary to asing colors to the geolgical units
dict_color_zeitalter = {
    "Quartär":                                            "skyblue",
    "Karbon":                                             "darkorange",
    "Jura":                                               "dodgerblue",
    "Tertiär im Oberrheingraben und Schichtstufenland":   "darkblue",
    "Tertiär im Molassebecken":                           "yellow3",
    "Perm":                                               "red",
    "Perm -Trias":                                        "brown",
    "Trias":                                              "greenyellow",
    "Metamorphe Gesteine":                                "mediumorchid",
    "Paläozoische Magmatite":                             "pink",
    "Jüngere Magmatite":                                  "purple4",
    "Impaktgesteine":                                     "tan",
    "Tektonitzone":                                       "darkbrown",
}

dict_color_tectonic = {
    "carboniferous":   "cadetblue3",
    "triassic":        "darkorchid2",
    "cretaceous":      "palegreen3",
    "devonian":        "orange3",
    "jurassic":        "deepskyblue1",
    "neogene":         "gold1",
    "ordovician":      "black",
    "paleogene":       "lightsalmon1",
    "permian":         "tomato1",
    "plut":            "darkgreen",
    "proterozoic":     "palevioletred2",
    "silurian":        "yellow",
    "paleozoic_volc":  "darkseagreen",
    "cenocoic_volc":   "yellow",
}


# -----------------------------------------------------------------------------
# Self defined-functions
# -----------------------------------------------------------------------------
# Select and plot different geological units (only Baden-Würtemberg)
def select_plot_zeitalter(zeitalter):
    gpd_btn_zeitalter = gpd_btn_wgs84[gpd_btn["Zeitalter"]==zeitalter]
    fig.plot(
        data=gpd_btn_zeitalter,
        fill=f"{dict_color_zeitalter[zeitalter]}@30",
        label=zeitalter,
    )

# Plot tectonic units
# BGR, Hannover
# https://www.bgr.bund.de/EN/Themen/Sammlungen-Grundlagen/GG_geol_Info/Karten/Europa/IGME5000/IGME_Project/IGME_Downloads.html?nn=1556388
# from Sarah Mader within the AlpArray Project
def plot_tectonic(tectonic):
    fig.plot(
        data=f"{path_in}/geology_urg_SMM/{tectonic}.txt",
        fill=dict_color_tectonic[tectonic],
        label=tectonic,
    )


# %%
# -----------------------------------------------------------------------------
# Special set up for URG manuscript

match status_pp:
    case "station":
        status_cb_ele_tomo = "yes"
        status_scale = "no"
        basemap_frame = ["WsNe", "a0.5f0.25", "x+e"]
        status_inset_epi = ""
        status_station_epi = ""
        status_inset_pp = "yes"
        status_depth_label = "yes"
        status_inset_study = "merca"
        status_null = ""
    case "phi":
        status_cb_ele_tomo = "yes"
        cb_ele_pos = "x10.75c/0.65c+w3.5c/0.2c+h+ml"
        status_scale = "yes"
        basemap_frame = ["wsNE", "a0.5f0.25", "x+e"]
        status_inset_epi = ""
        status_station_epi = ""
        status_inset_study = ""
        status_null = "yes"
        if status_con=="3D":
            status_cb_ele_tomo = ""
            status_scale = ""
            basemap_frame = ["WSNE", "a0.5f0.25", "x+e"]
    case "baz":
        status_cb_ele_tomo = "no"
        status_scale = "no"
        basemap_frame = ["WSne", "a0.5f0.25", "x+e"]
        status_inset_epi = "yes"
        status_station_epi = "BFO"
        status_inset_study = ""
        status_null = "yes"
    case "si" | "dt":
        status_cb_ele_tomo = "no"
        status_scale = "yno"
        basemap_frame = ["wSnE", "a0.5f0.25", "x+e"]
        status_inset_epi = ""
        status_station_epi = ""
        status_inset_study = ""
        status_null = "yes"

if status_size == "large":
    cb_hd_pos   = "JBR+jBR+o0.65c/3.45c+w3.7c/0.2c+h+ml"
    leg_mag_pos = "JBR+jBR+o0.1c/4.3c+w3.7c"
    leg_all_pos = "JBL+jBL+o0.135c/1.52c+w6.1c"

    if status_pp == "no":
        cb_ele_pos  = "JBL+jBL+o4.0c/0.65c+w4.5c/0.2c+h+ml"
    leg_sta_pos = "JBL+jBL+o3.5c/1.45c+w4.5c"


# # for point version of piercing points
# lon_min = 6.4; lon_max = 10
# lat_min = 47.4; lat_max = 49.5
# region_main = [lon_min, lon_max, lat_min, lat_max]
# cb_pp_pos = "x5.8c/0.65c+w4.8c/0.2c+h+ml"
# leg_pp_file = "legend_gmt_pp_points.txt"
# status_depth_label = "yes"
# status_size = "large"
# basemap_frame = ["wSNE", "a0.5f0.25", "x+e"]
# status_null = "yes"
# MAP_ANNOT_OBLIQUE = "lat_parallel"
# leg_pp_pos  = "JRB+jLB+w2.0c+o-2.10c/0.1c"

# # with geology
# status_null = ""


# -----------------------------------------------------------------------------
# main map: Mercator
proj_main = "M15c"

# inset study area: orthographic projection
match status_inset_study:
    case "merca": proj_study = "M?"
    case "ortho": proj_study = f"G{(lon_min+lon_max)/2}/{(lat_min+lat_max)/2}/?"



# %%
# #############################################################################
# Make geographic map
# #############################################################################

for pierce_obs in pierce_obs_all:

    for pierce_qual in pierce_qual_all:

        for pierce_depth in pierce_depth_all:

# -----------------------------------------------------------------------------
            # Create figure object
# -----------------------------------------------------------------------------
            fig = gmt.Figure()

            # Global changes of default values of GMT
            gmt.config(
                MAP_FRAME_TYPE="fancy+",
                # formatting template how geographical coordinate are plotted
                # F adds NESW after degree sign
                FORMAT_GEO_MAP="ddd.xF",
                MAP_FRAME_WIDTH="3p",
                FONT_LABEL="9p",
                FONT_ANNOT_PRIMARY="9p",
                MAP_FRAME_PEN="0.8p",  # thickness of border around scale
                MAP_ANNOT_OFFSET="0.05i",  # distance of scale ticks labels from scale
                MAP_LABEL_OFFSET="3.5p",  # distance of label from scale
                MAP_TICK_LENGTH_PRIMARY="5p",  # length of scale ticks
                COLOR_NAN="white",  # color for NaN, default 127.5
                MAP_ANNOT_OBLIQUE=MAP_ANNOT_OBLIQUE,
            )

            fig.basemap(region=region_main, projection=proj_main, frame=0)


# -----------------------------------------------------------------------------
            # Elevation OR tomography OR geology
# -----------------------------------------------------------------------------

            match status_grid:
# -----------------------------------------------------------------------------
                case "ele" | "tomo":
                    match status_grid:
                        case "ele":
                            grid_name = f"{path_grid}/{file_ele_in}"
                            # intensity, [-1,+1], const. or vari. via file
                            shading_name = f"{path_grid}/{file_shading_in}"
                        case "tomo":
                            grid_name = f"{path_grid}/tomographyEU60_Zhu2015/" + \
                                        f"tomoEU60_grids_{status_color}" + \
                                        "_10km_selfcalculated/tomoEU60_grid_" + \
                                        f"{status_color}_{pierce_depth}km.grd"
                            shading_name = 0

                    fig.grdimage(
                        grid=grid_name,
                        shading=shading_name,
                        dpi=grid_dpi,
                        cmap=cmap_URG,
                    )
# -----------------------------------------------------------------------------
                case "geobw" | "geoall":
                    match status_grid:
                        case "geobw":
                            for zeitalter in dict_color_zeitalter.keys():
                                select_plot_zeitalter(zeitalter)
                            cover_geo = "white@40"
                        case "geoall":
                            for tectonic in dict_color_tectonic.keys():
                                plot_tectonic(tectonic)
                            cover_geo = "white@40"

                    # Add white rectangle to reduce intensity of colors
                    fig.plot(
                        x=[lon_min-5, lon_max+5, lon_max+5, lon_min-5, lon_min-5],
                        y=[lat_min-5, lat_min-5, lat_max+5, lat_max+5, lat_min-5],
                        fill=cover_geo,
                    )

                    # Add legend
                    leg_geo_size = 2.7  # in centimeters
                    if status_grid == "geobw": leg_geo_size = 4

                    leg_geo_pos = "JTL+jTL+o0.1c/3c"
                    match status_size:
                        case "small": leg_geo_pos = "JTL+jTL+o0.1c"
                        case "large":
                            leg_geo_pos = "JLM+jTL+o0.1c/-4.3c"
                            if status_pp != "no":
                               leg_geo_pos = "JLM+jTL+o0.1c/-3.8c"
                    leg_geo_pos = "JTL+jTL+o0.1c"

                    with gmt.config(FONT="8p"):
                        fig.legend(
                            position=f"{leg_geo_pos}+w{leg_geo_size}c",
                            box=box_standard,
                        )

# -----------------------------------------------------------------------------
            if status_grid=="ele" and status_size=="large" and status_color=="co":
                fig.coast(
                    # (f)ull, (h)igh, (i)ntermediate, (l)ow, (c)rude
                    resolution="f",
                    borders=coast_borders,
                    rivers=coast_rivers,
                    water=coast_water,
                )


# -----------------------------------------------------------------------------
            # Highlight subregions by pattern (labels see below)
# -----------------------------------------------------------------------------
            # if status_var=="yes":
            #     # layer number change S-N direction
            #     fig.plot(
            #         x=[lon_min, lon_max, lon_max, lon_min],
            #         y=[lat_min, lat_min, 49, 48.4],
            #         close=True,
            #         fill=f"p8+f{color_2layerl}+b",
            #     )
            #     # fast polarization direction change E polar-W sides URG
            #     fig.plot(
            #         x=[lon_min, lon_max, lon_max, lon_min],
            #         y=[lat_min, lat_min, 49, 48.4],
            #         close=True,
            #         fill=f"p11+f{color_2layeru}+b",
            #     )
            #     # null anomaly at BFO SW quadrant
            #     fig.plot(
            #         x=[7.3, lon_max, lon_max, 8],
            #         y=[48.45, 49, lat_max, lat_max],
            #         close=True,
            #         fill=f"p8+f{color_1layer}+b",
            #     )


# -----------------------------------------------------------------------------
            # Faults
# -----------------------------------------------------------------------------
            # fig.plot(
            #     data=file_URGborder_in,  # west and east border
            #     pen="1.1p,black",
            # )
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
# -----------------------------------------------------------------------------
            if status_grid!="tomo" and status_size=="large" and status_color=="co":
                # marker
                fig.plot(
                    data=file_twons_in,
                    style="s0.3c",
                    fill="white",
                    pen="1p,black",
                )
                # labels
                fig.text(
                    textfiles=file_twons_in,
                    font=True,  # read from file
                    angle=True,  # read from file
                    justify=True,  # read from file
                    offset="0.2c/0.2c",
                    fill="white@30",
                    clearance=clearance_standard,
                )


# -----------------------------------------------------------------------------
            # Tectonic
# -----------------------------------------------------------------------------
            if status_size=="large" or (status_size=="small" and status_con=="3D"):
                textfile_geology_in = "rhein_geology_large.dat"
            elif status_size=="small":
                textfile_geology_in = "rhein_geology_small.dat"

            # labels
            fig.text(
                textfiles=f"{path_in}/{textfile_geology_in}",
                font=True,  # fontsize,fonttyp,fontcolor
                angle=True,
                justify=True,
                offset="0.3/0.05",
                fill="white@30",
                pen=f"0.8p,{color_URG}",
                clearance=clearance_standard,
            )


# -----------------------------------------------------------------------------
            # Plot semi-transparent ellipse
            # to highlight nulls for piercing points at 200 km depth
# -----------------------------------------------------------------------------
            # direction/major_axis/minor_axis
            # in degrees counter-clockwise from horizontal
            if status_null=="yes" and status_stereo=="no":

                style_ellipse = "e67/5c/2.9c"
                x_ellipse = 7.85
                y_ellipse = 48.40
                if status_con=="geoarr":
                    style_ellipse = "e67/6.1c/3.5c"
                    x_ellipse = 7.80
                    y_ellipse = 48.40

                fig.plot(
                    x=x_ellipse,
                    y=y_ellipse,
                    fill="255/215/0@70",
                    style=style_ellipse,
                )


# -----------------------------------------------------------------------------
            # Stereoplots
# -----------------------------------------------------------------------------
            if status_stereo=="yes":

                for key in key_choose:
                    stereo_in = f"{path_plot}/D_Matlab/stereoplots/" + \
                                f"{dict_file[key]}/Stereo_{dict_file[key]}" + \
                                "_goodfair_SC_single_Baz0to360_phase_noall_trans"
                    try:
                        # first plot semi-transparent white filled circle
                        # behind fully transparent stereoplot to increase
                        # visibility
                        fig.plot(
                            x=dict_lon[key],
                            y=dict_lat[key],
                            fill="white@70",
                            style=f"C{size_stereo}c",
                        )
                        # plot semi-transporent yellow sector (pie wedge)
                        # to highlight nulls at BFO in the southwest
                        # [outer[/startdir/stopdir]][+i[inner]]
                        # in degrees counter-clockwise from horizontal
                        if status_null=="yes" and dict_file[key]=="BFO":
                            fig.plot(
                                x=dict_lon[key],
                                y=dict_lat[key],
                                fill="gold@70",
                                style=f"w{size_stereo}c/140/300",  # 90
                            )
                        if status_null=="yes" and dict_file[key]=="WLS":
                            fig.plot(
                                x=dict_lon[key],
                                y=dict_lat[key],
                                fill="gold@70",
                                style=f"w{size_stereo}c/10/30",
                            )
                        if status_null=="yes" and dict_file[key]=="ECH":
                            fig.plot(
                                x=dict_lon[key],
                                y=dict_lat[key],
                                fill="gold@70",
                                style=f"w{size_stereo}c/10/30",
                            )
                        # if status_null=="yes" and dict_file[key]=="TMO07":
                        #     fig.plot(
                        #         x=dict_lon[key],
                        #         y=dict_lat[key],
                        #         fill="gold@70",
                        #         style=f"w{size_stereo}c/190/220",
                        #     )
                        # stereoplots are perfect circles without any
                        # annotation, thus station coordinates are used as
                        # mid point and the anchor point is set to MC
                        fig.image(
                            imagefile=f"{stereo_in}.eps",
                            position=[
                                f"g{dict_lon[key]}/{dict_lat[key]}" + \
                                f"+jMC+w{size_stereo}c"
                            ],
                        )
                    except: print(f"{dict_file[key]} no stereoplot found.")


# -----------------------------------------------------------------------------
            # Recording stations
# -----------------------------------------------------------------------------
            for key in key_choose:

                if status_stereo=="yes": offset_ind = 1
                else: offset_ind = 0

                myoffset_st = dict_off[key][offset_ind]
                mystyle_st = dict_sty[key]
                myfont_st = f"10p,Helvetica-Bold,{color_station_lable}"
                mycolor_st = color_station_marker

                if status_con=="geoarr" or status_con=="3D":
                    mystyle_st = "i0.7c"
                    myfont_st = f"17p,Helvetica-Bold,{color_station_lable}"

                if status_pp=="station":
                    mycolor_st = dict_col[key]

                if status_con!="3D" and status_con!="geoarr":
                    offset_sta_label = myoffset_st
                else:  # Avoid overlap
                    offset_x = 0
                    if key=="STU" and status_con=="3D": offset_x = 0.4
                    elif key=="TMO07": offset_x = -0.45
                    offset_sta_label = f"{offset_x}c/-0.8c"

# -----------------------------------------------------------------------------
                # markers
                fig.plot(
                    x=dict_lon[key],
                    y=dict_lat[key],
                    style=mystyle_st,
                    fill=mycolor_st,
                    pen=f"1p,{dict_rand[key]}",
                )

                # labels
                fig.text(
                    x=dict_lon[key],
                    y=dict_lat[key],
                    text=dict_label[key],
                    offset=offset_sta_label,
                    fill="white@30",
                    font=myfont_st,
                    pen=f"0.8p,{color_station_lable}",
                    clearance=clearance_standard,
                )


# -----------------------------------------------------------------------------
            # Piercing points
# -----------------------------------------------------------------------------
            if status_pp!="no":

                for key in key_choose:
                    # lon | lat | phi_SL | phi_GMT | dt | si | baz | thick
                    data_pp_path = f"{path_grid}/piercingpoints/pp_sp"
                    data_pp_mid = f"{dict_file[key]}_pp{pierce_depth}"
                    data_pp_end = f"{pierce_qual}_hd0km.txt"
                    data_path = f"{data_pp_path}/{data_pp_mid}km_"
                    data_K_N_pp = f"{data_path}K_sp_N_{data_pp_end}"
                    data_K_NN_pp = f"{data_path}K_sp_NN_{data_pp_end}"
                    data_KK_N_pp = f"{data_path}KK_sp_N_{data_pp_end}"
                    data_KK_NN_pp = f"{data_path}KK_sp_NN_{data_pp_end}"
                    data_P_N_pp = f"{data_path}P_sp_N_{data_pp_end}"
                    data_P_NN_pp = f"{data_path}P_sp_NN_{data_pp_end}"
# -----------------------------------------------------------------------------
                    if status_pp=="station":  # color-coded by station

                        fig_lab_pp = "(a)"
                        color_pp = dict_col[key]
                        incols_pp = [0, 1, 3, 4, 7]

                        color_NN_pen = "0.2p,black"  # 0.6  # 0.2 for block model

                        if pierce_obs!="N":  # -> NN and NNN; non-null
                            try:
                                fig.plot(
                                    data=data_K_NN_pp,  # SKS
                                    style="j", #"j",
                                    fill=color_pp,
                                    pen=color_NN_pen,
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp K_NN")
                            try:
                                fig.plot(
                                    data=data_KK_NN_pp,  # SKKS
                                    style="j", # "j",
                                    fill=color_pp,
                                    pen=color_NN_pen,
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp KK_NN")
                            try:
                                fig.plot(
                                    data=data_P_NN_pp,  # PKS
                                    style="j", #"j",
                                    fill=color_pp,
                                    pen=color_NN_pen,
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp P_NN")
                        if pierce_obs!="NN":  # -> N and NNN; null
                            try:
                                fig.plot(
                                    data=data_K_N_pp,  # SKS
                                    style="C0.2",
                                    fill="white",
                                    pen=f"1p,{color_pp}",
                                )
                            except: print(f"{dict_file[key]} no pp K_N")
                            try:
                                fig.plot(
                                    data=data_KK_N_pp,  # SKKS
                                    style="C0.2",
                                    fill="white",
                                    pen=f"1p,{color_pp}",
                                )
                            except: print(f"{dict_file[key]} no pp KK_N")
                            try:
                                fig.plot(
                                    data=data_P_N_pp,  # PKS
                                    style="C0.2",
                                    fill="white",
                                    pen=f"1p,{color_pp}",
                                )
                            except: print(f"{dict_file[key]} no pp P_N")

# -----------------------------------------------------------------------------
                    elif status_pp!="station":  # color-coded by
                        match status_pp:
                            case "phi":  # fast polarization direction (phi)
                                fig_lab_pp = "(b)"
                                color_pp = cmap_phi
                                incols_pp = [0, 1, 2, 3, 4, 7]
                                incols_pp_N = [0, 1, 2]
                            case "dt":  # delay time (dt)
                                fig_lab_pp = "(c)"
                                color_pp = cmap_dt
                                incols_pp = [0, 1, 4, 3, 4, 7]
                                incols_pp_N = [0, 1, 4]
                            case "si":  # splitting intensity (si)
                                fig_lab_pp = "(d)"
                                color_pp = cmap_si
                                incols_pp = [0, 1, 5, 3, 4, 7]
                                incols_pp_N = [0, 1, 5]
                            case "baz":  # backazimuth (baz)
                                fig_lab_pp = "(c)"
                                color_pp= cmap_baz
                                incols_pp = [0, 1, 6, 3, 4, 7]
                                incols_pp_N = [0, 1, 6]

                        color_N_pen = "1p,black"
                        color_NN_pen = "0.2p,black"  # 0.6  # 0.2 for block model

                        if pierce_obs!="NN":  # -> N and NNN; null
                            try:
                                fig.plot(
                                    data=data_K_N_pp,
                                    style="C0.2c",  # C
                                    cmap=color_pp,
                                    pen=color_N_pen,
                                    incols=incols_pp_N,
                                )
                            except: print(f"{dict_file[key]} no pp K_N")
                            try:
                                fig.plot(
                                    data=data_KK_N_pp,
                                    style="C0.2c",  # C
                                    cmap=color_pp,
                                    pen=color_N_pen,
                                    incols=incols_pp_N,
                                )
                            except: print(f"{dict_file[key]} no pp KK_N")
                            try:
                                fig.plot(
                                    data=data_P_N_pp,
                                    style="C0.2c",  # C
                                    cmap=color_pp,
                                    pen=color_N_pen,
                                    incols=incols_pp_N,
                                )
                            except: print(f"{dict_file[key]} no pp P_N")
                        if pierce_obs!="N":  # -> NN and NNN; non-null
                            try:
                                fig.plot(
                                    data=data_K_NN_pp,
                                    style="j",  # j
                                    cmap=color_pp,
                                    pen=color_NN_pen,
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp K_NN")
                            try:
                                fig.plot(
                                    data=data_KK_NN_pp,
                                    style="j",  # j
                                    cmap=color_pp,
                                    pen=color_NN_pen,
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp KK_NN")
                            try:
                                fig.plot(
                                    data=data_P_NN_pp,
                                    style="j",  # j
                                    cmap=color_pp,
                                    pen=color_NN_pen,
                                    incols=incols_pp,
                                )
                            except: print(f"{dict_file[key]} no pp P_NN")

# -----------------------------------------------------------------------------
            # null anomaly
            if (status_pp=="baz" and status_null=="yes") and \
                (pierce_depth==200 or pierce_depth==250):
                # STU splits
                fig.plot(
                    data=f"{path_in}/null_anomaly_{pierce_depth}km_STU.txt",
                    style="j",
                    cmap=color_pp,
                    pen=f"1p,{color_null_ano}",
                    incols=[7, 8, 5, 10, 11, 14],
                )
                # BFO nulls
                fig.plot(
                    data=f"{path_in}/null_anomaly_{pierce_depth}km_BFO.txt",
                    style="C0.2",
                    cmap=color_pp,
                    pen=f"1p,{color_null_ano}",
                    incols=[7, 8, 5],
                )
                # ECH splits
                fig.plot(
                    data=f"{path_in}/null_anomaly_{pierce_depth}km_ECH.txt",
                    style="j",
                    cmap=color_pp,
                    pen=f"1p,{color_null_ano}",
                    incols=[7, 8, 5, 10, 11, 14],
                )


# -----------------------------------------------------------------------------
            # Volcanic Complexes
# -----------------------------------------------------------------------------
            # after piercing points to have it above the piercing points

            # marker
            fig.plot(
                x=[lon_KVC],
                y=[lat_KVC],
                # self-defined symbol, read from file
                style=f"k{path_in}/volcano_sleeping.def/0.7",
                fill=color_URG,
                pen="0.8p,black",
            )
            fig.plot(
                x=[lon_VVC],
                y=[lat_VVC + 0.03],
                style=f"k{path_in}/volcano_sleeping.def/1",
                fill=color_URG,
                pen="0.8p,black",
            )

            # label
            fig.text(
                x=[lon_KVC, lon_VVC],
                y=[lat_KVC, lat_VVC],
                text=["Kaiserstuhl VC", "Vogelsberg VC"],
                font="8p,Helvetica-Bold,black",
                offset="-0.7/-0.6",
                fill="white@30",
                pen=f"0.8p,{color_URG}",
                clearance=clearance_standard,
            )


# -----------------------------------------------------------------------------
            # Highlight subregions by labels (patterns see above)
# -----------------------------------------------------------------------------
            if status_var=="yes":
                style_vector = "v0.4c+ba+ea+a30+h0"#+p0.5p,black"
                # layer number change S-N direction
                fig.plot(
                    x=8.82,
                    y=48.15,
                    # direction cc from horizontal, length in centimeters
                    direction=[[90], [7.6]],
                    style=style_vector,
                    pen=f"2p,{color_station_lable}",
                    fill=color_station_lable,
                )
                fig.text(
                    x=8.88,
                    y=48.5,
                    text="change of layer number",
                    font="8p,Helvetica-Bold,black",
                    fill="white@30",
                    pen=f"0.8p,{color_station_lable}",
                    clearance=clearance_standard,
                )

# -----------------------------------------------------------------------------
                # Fast polarization direction change East West sides of URG
                x_EW = 7.6
                y_EW = 48.39
                dir_EW = [[20], [8.1]]
                y_EW_text = 48.54
                if status_con=="geoarr":
                    x_EW = 7.1
                    y_EW = 48.3
                    dir_EW = [[20], [11.5]]
                    y_EW_text = 48.50


                fig.plot(
                    x=x_EW,
                    y=y_EW,
                    direction=dir_EW,
                    style=style_vector,
                    pen=f"2p,{color_station_lable}",
                    fill=color_station_lable,
                )
                fig.text(
                    x=8.06,
                    y=y_EW_text,
                    text="change of fast polarization direction",
                    font="8p,Helvetica-Bold,black",
                    fill="white@30",
                    pen=f"0.8p,{color_station_lable}",
                    clearance=clearance_standard,
                )

# -----------------------------------------------------------------------------
                # null anomaly at BFO SW quadrant
                fig.text(
                    x=7.7,
                    y=48.235,
                    text="null anomaly",
                    font="8p,Helvetica-Bold,black",
                    fill="white@30",
                    pen=f"0.8p,{color_station_lable}",
                    clearance=clearance_standard,
                )


# -----------------------------------------------------------------------------
            # Map frame and map scale
# -----------------------------------------------------------------------------
            if status_scale=="yes":
                with gmt.config(MAP_SCALE_HEIGHT="9p"):
                    fig.basemap(
                        frame=basemap_frame,
                        map_scale=basemap_scale,
                        box=box_standard,
                    )
            else:
                fig.basemap(frame=basemap_frame)


# -----------------------------------------------------------------------------
            # Inset map of Central Europe
# -----------------------------------------------------------------------------
            if status_inset_study!="":

                inset_pos = "jTL+w3.5c+o-0.2c/0.1c"
                if status_inset_study=="ortho":
                    # inset_pos = "jTL+w5.5c+o-1.5c/-1.2c"
                    inset_pos = "jTL+w7.5c+o-1.5c/-1.2c"

# -----------------------------------------------------------------------------
                with fig.inset(position=inset_pos):

                    gmt.config(
                        MAP_FRAME_TYPE="plain",
                        MAP_TICK_LENGTH_PRIMARY="0p",
                        MAP_FRAME_WIDTH="5p",
                    )

                    # >>> use ? <<<
                    # otherwise something goes wrong with the box
                    # around the study area

# -----------------------------------------------------------------------------
                    if status_inset_study=="ortho":

                        # Orthographic projection
                        # - glon0/lat0[/horizon]/scale  OR
                        #   Glon0/lat0[/horizon]/width
                        # - lon0 and lat0 projection center
                        #   horizon maximum distance from projection center
                        #   (in degrees, <= 90, default 90)
                        #   scale and width figure size
                        fig.coast(
                            region="g",
                            projection=proj_study,
                            area_thresh="50000",
                            resolution="c",
                            shorelines="1/0.1p,black",
                            land=color_land,
                            water=color_water,
                            frame="g",
                        )

                        # rectangle at study area
                        fig.plot(
                            x=[lon_min, lon_min, lon_max, lon_max, lon_min],
                            y=[lat_min, lat_max, lat_max, lat_min, lat_min],
                            pen="0.5p,black",
                            fill=color_station_lable,
                        )


                        WDC = [-77.0364, 38.8951]
                        URG = [8.0, 48.5]
                        data = np.array([WDC + URG])
                        # '=' means geographic vectors. With the modifier '+s', the input
                        # data should contain coordinates of start and end points
                        style = f"=0.7c+s+ea+g{color_station_lable}+h0.5+p0.3p,black"
                        fig.plot(data=data, style=style, pen=f"3p,{color_station_lable}")

                        fig.plot(
                            x=-77.0364,
                            y=38.8951,
                            style="c0.25c",
                            pen="0.5p,black",
                            fill=color_station_lable,
                        )

# -----------------------------------------------------------------------------
                    elif status_inset_study=="merca":

                        # Mercator projection
                        fig.coast(
                            region=[2.8, 16, 46, 56],
                            projection=proj_study,
                            land=color_land,
                            water=coast_water,
                            area_thresh="20/0/1",
                            resolution="h",
                            shorelines="1/0.15p,black",
                            borders="1/0.35p,black",
                            frame=["wsne", "f"],
                        )

                        # label for countries
                        fig.text(
                            x=np.array([10.50,  4.50,  8.30]),
                            y=np.array([51.10, 47.80, 46.70]),
                            text=["DE", "FR", "CH"],
                            font="8p,black",
                            fill="white@30",
                            clearance=clearance_standard,
                        )

                        # rectangle around study area
                        fig.plot(
                            x=[lon_min, lon_min, lon_max, lon_max, lon_min],
                            y=[lat_min, lat_max, lat_max, lat_min, lat_min],
                            pen=f"1p,{color_station_lable}",
                        )


# -----------------------------------------------------------------------------
            # Inset of epicenter distribution
# -----------------------------------------------------------------------------
            match status_work:
                case "MA":
                    rad_tot = 6.3
                    inset_epi_pos = f"JMR+jMR+w{rad_tot}c+o-1.5c/-3.6"
                    if status_pp=="baz":
                        inset_epi_pos = f"JLT+jLT+w{rad_tot}c"
                        width_cw = rad_tot * 0.888  # width of colorwheel eps file
                case "PhD":
                    rad_tot = 4.5
                    inset_epi_pos = f"JTR+jTR+w{rad_tot}c+o-1.2c/-1.2"

# -----------------------------------------------------------------------------
            if status_inset_epi=="yes":

                proj_epi = f"E{dict_lon[status_station_epi]}/" + \
                           f"{dict_lat[status_station_epi]}/170/?"

                epi_min = 90  # degrees
                epi_max = 150

                with fig.inset(position=inset_epi_pos):

                    # azimuthal equidistant projection
                    # - elon0/lat0[/horizon]/scale  OR
                    #   Elon0/lat0[/horizon]/width
                    # - horizon max. distance to the projection center
                    #   i.e. the visible portion of the rest of the world map
                    #   in degrees <= 180° (default 180°)
                    fig.coast(
                        region="g",
                        projection=proj_epi,
                        area_thresh="50000",
                        resolution="c",
                        shorelines="1/0.1p,darkgray",
                        land=color_land,
                        water="white",
                        frame=0,
                    )

# -----------------------------------------------------------------------------
                    # Add colorwheel for backazimuth as eps file
                    # instead of colorbar
                    if status_pp=="baz":
                        fig.image(
                            imagefile=f"{path_in}/colorwheel_N_cw_pygmt_{cmap_baz_in}.eps",
                            position=f"x{rad_tot/2}/{rad_tot/2}c+jMC+w{width_cw}c",
                        )

# -----------------------------------------------------------------------------
                    # plate boundaries
                    fig.plot(data=file_plate_in, pen=f"0.5p,{color_platebound}")

# -----------------------------------------------------------------------------
                    # epicentral distance range used in this study
                    # circles
                    fig.plot(
                        x=dict_lon[status_station_epi],
                        y=dict_lat[status_station_epi],
                        style=f"E-{epi_min*2}+d",  # 2 x 90 deg
                        pen="1p,gray50,-",  # dashed
                    )
                    fig.plot(
                        x=dict_lon[status_station_epi],
                        y=dict_lat[status_station_epi],
                        style=f"E-{epi_max*2}+d",  # 2 x 150 deg
                        pen="1p,gray50,-",
                    )
                    # annotations
                    fig.text(
                        x=dict_lon[status_station_epi],
                        y=-29,
                        text=f"{epi_min}@.",
                        font="10p,black",
                    )
                    fig.text(
                        x=dict_lon[status_station_epi],
                        y=-88,
                        text=f"{epi_max}@.",
                        font="10p,black",
                    )

# -----------------------------------------------------------------------------
                    # epicenters
                    file_epi = f"{file_epi_in}/swsm_all/{status_station_epi}_epi_swsm_all.txt"
                    df_epi_raw = pandas.read_csv(
                        file_epi,
                        delimiter=" ",
                        names=["longitude", "latitude", "magnitude", "hdepth"],
                    )
                    # TODO check size coding of moment magnitude
                    df_epi = df_epi_raw
                    df_epi.magnitude = np.exp(df_epi_raw.magnitude / 1.7) * 0.0035

                    if status_pp=="baz":
                        # raypaths
                        fig.plot(
                            data=f"{file_ray_in}/swsm_NNN/" + \
                                 f"{status_station_epi}_rays_swsm_NN_goodfair.txt",
                            pen="0.2p,gray25@70",
                        )
                        fig.plot(
                            data=f"{file_ray_in}/swsm_NNN/" + \
                                 f"{status_station_epi}_rays_swsm_N_goodfair.txt",
                            pen="0.2p,gray25@70",
                        )
                        # epicenters
                        fig.plot(
                            data=f"{file_epi_in}/swsm_NNN/" + \
                                 f"{status_station_epi}_epi_swsm_NN_goodfair.txt",
                            style="c0.17c",
                            fill="gray70",
                            pen="0.5p,gray25",
                        )
                        fig.plot(
                            data=f"{file_epi_in}/swsm_NNN/" + \
                                 f"{status_station_epi}_epi_swsm_N_goodfair.txt",
                            style="c0.12c",
                            fill="white",
                            pen="0.5p,gray25",
                        )
                        # null anomaly
                        if status_null=="yes":
                            fig.plot(
                                data=f"{path_in}/null_anomaly_200km_BFO.txt",
                                style="c0.15c",
                                fill=color_null_ano,
                                pen="0.5p,gray25",
                                incols=[1, 2],
                            )
                    else:
                        fig.plot(
                            x=df_epi.longitude,
                            y=df_epi.latitude,
                            style="c",
                            size=df_epi.magnitude,
                            fill=df_epi.hdepth,
                            cmap=cmap_hypo,
                            pen=pen_epi,
                        )
                        # fig.plot(
                        #     x=df_epi.longitude,
                        #     y=df_epi.latitude,
                        #     style="c0.17c",
                        #     # size=df_epi.magnitude,
                        #     fill="tan",
                        #     pen="0.01p,brown",
                        # )

# -----------------------------------------------------------------------------
                    # Recording station
                    # Marker
                    fig.plot(
                        x=dict_lon[status_station_epi],
                        y=dict_lat[status_station_epi],
                        style="i0.47c",
                        fill=color_station_marker,
                        pen="0.6p,black",
                    )
                    # Label
                    fig.text(
                        x=dict_lon[status_station_epi],
                        y=dict_lat[status_station_epi],
                        text=status_station_epi,
                        font=myfont_st,
                        offset="0c/-0.6c",
                        fill="white@30",
                        pen=f"0.8p,{color_station_lable}",
                        clearance=clearance_standard,
                    )


# -----------------------------------------------------------------------------
            # Inset of schema piercing points
# -----------------------------------------------------------------------------
            if status_inset_pp=="yes":
                fig.image(
                    imagefile=f"{path_plot}/G_Bilder/001_figures_general/" + \
                              "percingpoints_inset_orange_NOframe.eps",
                    position="JRT+jRT+o0.150c/0.7c+w2.5c",
                    box="+c0c+p0.5p,black",
                )


# -----------------------------------------------------------------------------
            # Legends
# -----------------------------------------------------------------------------
            if status_size=="large" and status_grid=="ele" and status_color=="co":
                fig.legend(
                    spec=f"{path_in}/{leg_all_file}",
                    position=leg_all_pos,
                    box=box_standard,
                )
            else:
                # running time of stations
                if status_pp=="no" and status_stereo=="no" and \
                   status_con!="geoarr" and status_con!="3D":
                    fig.legend(
                        spec=f"{path_in}/{leg_sta_file}",
                        position=leg_sta_pos,
                        box=box_standard,
                    )
                # faults
                if status_pp=="no" and status_stereo=="no" and \
                   status_inset_study=="ortho":
                    fig.legend(
                        spec=f"{path_in}/{leg_fal_file}",
                        position=leg_fal_pos,
                        box=box_standard,
                    )

            # stereoplots
            if status_stereo=="yes":
                fig.legend(
                    spec=f"{path_in}/{leg_stereo_file}",
                    position=leg_stereo_pos,
                    box=box_standard,
                )

            # piercing points general
            if status_pp=="station":
                fig.legend(
                    spec=f"{path_in}/{leg_pp_file}",
                    position=leg_pp_pos,
                    box=box_standard,
                )

            # piercing points delay time
            # TODO check legend for length coding
            if status_pp=="station" and status_con!="3D":
                fig.legend(
                    spec=f"{path_in}/{leg_dt_file}",
                    position=leg_dt_pos,
                    box=box_standard,
                )

            # moment magnitude
            # TODO check legend for size coding
            if status_inset_epi=="yes" and status_pp!="baz":
                fig.legend(
                    spec=f"{path_in}/{leg_mag_file}",
                    position=leg_mag_pos,
                    box=box_standard,
                )


# -----------------------------------------------------------------------------
            # Colorbars
# -----------------------------------------------------------------------------
            gmt.config(MAP_TICK_LENGTH_PRIMARY="2p")

            # fast polarization direction
            cb_pp_pos = "x6.37c/0.665c+w4.8c/0.2c+h+ml"  # with margin stereo
            cb_pp_pos = "x4.5c/0.65c+w4.8c/0.2c+h+ml"  # with margin pp phi
            if status_pp=="phi" and status_con!="3D" or status_stereo=="yes":
                fig.colorbar(
                    cmap=cmap_phi,
                    position=f"{cb_pp_pos}+n ", #"null",
                    box=box_standard + "+c-0.4c/0.3c/0.15c/0.15c",
                    # frame="xa30f10+lapp. fast pol. dir. @~f@~@-a@- / N@.E",
                    frame="xa30f10+lnull | split app. fast pol. dir. @~f@~@-a@- / N@.E        @;gray;.@;;",
                    # greek letter phi, degree sign, subscript in GMT here phi_a
                    # x step of labeled ticks of colorbar
                )

            # delay time
            if status_pp=="dt":
                fig.colorbar(
                    cmap=cmap_dt,
                    position=f"{cb_pp_pos}+ef+nnull",
                    box=box_standard,
                    frame="xa1f0.25+ldelay time @~d@~t / s",
                )

            # splitting intensity
            if status_pp=="si":
                fig.colorbar(
                    cmap=cmap_si,
                    position=f"{cb_pp_pos}+e",
                    box=box_standard,
                    frame="xa1f0.25+lsplitting intensity SI",
                )

            # hypocentral depth
            if status_inset_epi=="yes" and status_pp!="baz":
                fig.colorbar(
                    cmap=cmap_hypo,
                    position=f"{cb_hd_pos}{cb_epi_e}",
                    box=box_standard,
                    frame="xa100f50+lhypocentral depth / km",
                )

            # elevation OR tomography
            if status_grid=="ele":
                cb_frame_grid = "+lelevation / m"
                cb_pos_grid = f"{cb_ele_pos}+ef0.15c"
                # cb_pos_grid = f"{cb_pp_pos}+ef0.15c"  # for POINTS URG
            match status_color:
                case "dvp":
                    cb_frame_grid = "xa1f0.5+ldv@-p@- / %"  # subscript here dv_p
                    cb_pos_grid = f"{cb_tomo_pos}+e"
                case "dvs":
                    cb_frame_grid = "xa1f0.5+ldv@-s@- / %"
                    cb_pos_grid = f"{cb_tomo_pos}+e"

            if 1==1: # status_grid not in ["geobw", "geoall"] and status_cb_ele_tomo=="yes":
                fig.colorbar(
                    cmap=cmap_URG,
                    position=cb_pos_grid,
                    box=box_standard,
                    frame=cb_frame_grid
                )


# -----------------------------------------------------------------------------
            # Depth label
# -----------------------------------------------------------------------------
            text_depth = f"@@{pierce_depth} km"  # @ sign in GMT

            if status_depth_label=="yes":
                fig.text(
                    position="TR",
                    justify="TR",
                    offset="-0.2c/-0.2c",
                    text=text_depth,
                    font=f"11p,Helvetica-Bold,{color_station_lable}",
                    fill="white@30",
                    pen="0.8p,black",
                    clearance=clearance_standard,  # rounded rectangle text box
                )


# -----------------------------------------------------------------------------
            # Figure labels ((a), (b), (c), (d))
# -----------------------------------------------------------------------------
            if status_pp!="no" and status_con!="3D":
                fig.text(
                    position="TL",
                    justify="TL",
                    offset="0.2c/-0.2c",
                    text=fig_lab_pp,
                    font="11p,Helvetica-Bold,black",
                    fill="white@30",
                    pen="1p,black",
                    clearance=clearance_standard,
                )


# -----------------------------------------------------------------------------
            # Copyright label
# -----------------------------------------------------------------------------
            """
            text_copy="(c) Authors. All rights reserved."
            x_copy = 6.6
            y_copy = 47.44

            fig.text(
                x=x_copy,
                y=y_copy,
                text=text_copy,
                font="7p,Helvetica-Bold,black",
                clearance=clearance_standard,
                )
            """


# -----------------------------------------------------------------------------
            # Show and save figure
# -----------------------------------------------------------------------------
            pp_str = "sta"
            if status_pp!="no": pp_str = "pp"

            stereo_str = "stations"
            if status_stereo=="yes": stereo_str = "stereo"

            depth_str = ""
            if status_grid=="tomo": depth_str = f"{pierce_depth}km"

            con_str = ""
            if status_con=="geoarr": con_str = "_geoarr"
            elif status_con=="3D": con_str = "_3D"

            epi_str = ""
            if status_inset_epi=="yes": epi_str = f"_epi{status_station_epi}"

            null_str = ""
            if status_null=="yes": null_str = "_null"

            var_str = ""
            if status_var=="yes": var_str = "_var"


            fig_name_same = f"fig_{pp_str}_{status_grid}/mapURG_SWS_"

            fig_name_spec = f"{stereo_str}"
            if status_pp!="no":
                fig_name_spec = f"pp{pierce_depth}km_KKK_{status_pp}_" + \
                                f"{pierce_obs}_{pierce_qual}_dall"

            fig_name = f"{fig_name_same}{fig_name_spec}_{status_grid}{depth_str}_" + \
                       f"{status_color}_{status_size}_{status_work}_" + \
                       f"{status_inset_study}{con_str}" + \
                       f"{null_str}{epi_str}{var_str}" + \
                       f"{label_frame}_NOtowns_WITHticks" # + "_NOtowns_WITHticks" "_POINTS_

            fig.show() #method="external")
            # for ext in ["png", "pdf", "eps"]:
            #     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=720)

            print(fig_name)

# Remove colormap files
for cpt in glob.glob(f"{path_in}/*resampled*.cpt"):
    os.remove(cpt)