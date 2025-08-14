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


path_in = "01_in_data"
path_out = "02_out_fig"


# -----------------------------------------------------------------------------
# Files for
# -----------------------------------------------------------------------------
# Towns
file_twons_in = f"{path_in}/rhein_towns.dat"

# Recording stations
file_station_in = f"{path_in}/stations_info.txt"

# Faults
file_URGborder_in = f"{path_in}/faults_URGwesteast.geo"
file_URGnormal_in = f"{path_in}/faults_URGnormal.geo"
file_faults_in = f"{path_in}/faults_LLBB_TH_BLZ.geo"

# Plate boundaries; Bird 2003
file_plate_in = f"{path_in}/plate_boundaries_Bird_2003.txt"

# Epicenter distribution
file_epi_in = f"{path_in}/epicenters"

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
# Elevation
# Scientific Colour Maps by F. Crameri
cmap_bw_in = "grayC"
cmap_bw_out = f"{path_in}/{cmap_bw_in}_resampled_topo.cpt"
gmt.makecpt(cmap=cmap_bw_in, output=cmap_bw_out, series=[0, 2000, 10])

cmap_co_in = f"{path_in}/europe_3.cpt"
cmap_co_out = f"{path_in}/europe_3_resampled_insert.cpt"
gmt.makecpt(cmap=cmap_co_in, output=cmap_co_out, series=[0, 2000, 10])

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
cmap_hypo = cmap_hypo_out_cut
match status_color:
    case "bw": cmap_URG = cmap_bw_out
    case "co": cmap_URG = cmap_co_out


# -----------------------------------------------------------------------------
# Colors
# -----------------------------------------------------------------------------
color_land = "gray80"
color_water = "gray75"
if status_inset_study=="ortho": color_water = "steelblue"

color_pb = "216.750/82.875/24.990"  # plate boundaries

color_URG = "darkbrown"  # "sienna"
color_null_ano = "255/90/0"  # -> orange | URG paper

color_sta = "gold"  # -> GMT "gold"
color_hl = "255/90/0"  # -> orange | URG paper

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






# %%
# -----------------------------------------------------------------------------
# Special set up for URG manuscript


status_cb_ele_tomo = "yes"
status_scale = "no"
basemap_frame = ["WsNe", "a0.5f0.25", "x+e"]
status_inset_epi = ""
status_station_epi = ""
status_inset_pp = "yes"
status_depth_label = "yes"
status_inset_study = "merca"
status_null = ""


if status_size == "large":
    cb_hd_pos   = "JBR+jBR+o0.65c/3.45c+w3.7c/0.2c+h+ml"
    leg_mag_pos = "JBR+jBR+o0.1c/4.3c+w3.7c"
    leg_all_pos = "JBL+jBL+o0.135c/1.52c+w6.1c"

    if status_pp == "no":
        cb_ele_pos  = "JBL+jBL+o4.0c/0.65c+w4.5c/0.2c+h+ml"
    leg_sta_pos = "JBL+jBL+o3.5c/1.45c+w4.5c"


# -----------------------------------------------------------------------------
# main map: Mercator
proj_main = "M15c"

# inset study area: orthographic projection
match status_inset_study:
    case "merca": proj_study = "M?"
    case "ortho": proj_study = f"G{(lon_min+lon_max)/2}/{(lat_min+lat_max)/2}/?"



# %%
# -----------------------------------------------------------------------------
# Make geographic map
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
# Elevation
# -----------------------------------------------------------------------------
fig.grdimage(
    grid=f"{path_in}/{file_ele_in}",
    shading=f"{path_in}/{file_shading_in}",
    dpi=grid_dpi,
    cmap=cmap_URG,
)

fig.coast(
    resolution="f",  # (f)ull, (h)igh, (i)ntermediate, (l)ow, (c)rude
    borders=coast_borders,
    rivers=coast_rivers,
    water=coast_water,
)

# -----------------------------------------------------------------------------
# Faults
# -----------------------------------------------------------------------------
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
textfile_geology_in = "rhein_geology_large.dat"

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
# Recording stations
# -----------------------------------------------------------------------------
for key in key_choose:

    if status_stereo=="yes": offset_ind = 1
    else: offset_ind = 0

    myoffset_st = dict_off[key][offset_ind]
    mystyle_st = dict_sty[key]
    myfont_st = f"10p,Helvetica-Bold,{color_hl}"
    mycolor_st = color_sta

    if status_con=="geoarr" or status_con=="3D":
        mystyle_st = "i0.7c"
        myfont_st = f"17p,Helvetica-Bold,{color_hl}"

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
    pen=f"0.8p,{color_hl}",
    clearance=clearance_standard,
)

# -----------------------------------------------------------------------------
# Volcanic Complexes
# -----------------------------------------------------------------------------
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
# Map frame and map scale
# -----------------------------------------------------------------------------
with gmt.config(MAP_SCALE_HEIGHT="9p"):
    fig.basemap(frame=basemap_frame, map_scale=basemap_scale, box=box_standard)


# %%
# -----------------------------------------------------------------------------
# Inset map of Central Europe
# -----------------------------------------------------------------------------
inset_pos = "jTL+w3.5c+o-0.2c/0.1c"
if status_inset_study=="ortho": inset_pos = "jTL+w7.5c+o-1.5c/-1.2c"

# -----------------------------------------------------------------------------
with fig.inset(position=inset_pos):

    gmt.config(MAP_FRAME_TYPE="plain", MAP_TICK_LENGTH_PRIMARY="0p", MAP_FRAME_WIDTH="5p")

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
            fill=color_hl,
        )


        WDC = [-77.0364, 38.8951]
        URG = [8.0, 48.5]
        data = np.array([WDC + URG])
        # '=' means geographic vectors. With the modifier '+s', the input
        # data should contain coordinates of start and end points
        style = f"=0.7c+s+ea+g{color_hl}+h0.5+p0.3p,black"
        fig.plot(data=data, style=style, pen=f"3p,{color_hl}")

        fig.plot(
            x=-77.0364,
            y=38.8951,
            style="c0.25c",
            pen="0.5p,black",
            fill=color_hl,
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
            pen=f"1p,{color_hl}",
        )


# %%
# -----------------------------------------------------------------------------
# Inset of epicenter distribution
# -----------------------------------------------------------------------------
rad_tot = 6.3
inset_epi_pos = f"JMR+jMR+w{rad_tot}c+o-1.5c/-3.6"

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
    #   in degrees <= 180Â° (default 180Â°)
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

    # plate boundaries
    fig.plot(data=file_plate_in, pen=f"0.5p,{color_pb}")

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

fig.plot(
    x=df_epi.longitude,
    y=df_epi.latitude,
    style="c",
    size=df_epi.magnitude,
    fill=df_epi.hdepth,
    cmap=cmap_hypo,
    pen=pen_epi,
)

# -----------------------------------------------------------------------------
# Recording station
# Marker
fig.plot(
    x=dict_lon[status_station_epi],
    y=dict_lat[status_station_epi],
    style="i0.47c",
    fill=color_sta,
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
    pen=f"0.8p,{color_hl}",
    clearance=clearance_standard,
)

# -----------------------------------------------------------------------------
# Legends
# -----------------------------------------------------------------------------
fig.legend(
    spec=f"{path_in}/{leg_all_file}",
    position=leg_all_pos,
    box=box_standard,
)

# moment magnitude
# TODO check legend for size coding
fig.legend(
    spec=f"{path_in}/{leg_mag_file}",
    position=leg_mag_pos,
    box=box_standard,
)


# -----------------------------------------------------------------------------
# Colorbars
# -----------------------------------------------------------------------------
gmt.config(MAP_TICK_LENGTH_PRIMARY="2p")

# hypocentral depth
fig.colorbar(
    cmap=cmap_hypo,
    position=f"{cb_hd_pos}{cb_epi_e}",
    box=box_standard,
    frame="xa100f50+lhypocentral depth / km",
)

# elevation
fig.colorbar(
    cmap=cmap_URG,
    position=f"{cb_ele_pos}+ef0.15c",
    box=box_standard,
    frame="+lelevation / m",
)

# -----------------------------------------------------------------------------
# Show and save figure
# -----------------------------------------------------------------------------
fig.show()
fig_name = "FGR2024_GJI_FigS1"
for ext in ["png"]: #, "pdf", "eps"]:
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=720)
print(fig_name)
