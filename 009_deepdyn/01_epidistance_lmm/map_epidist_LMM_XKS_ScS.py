# #############################################################################
# This maps show the epicenters of equarthakes usable to study shear wave
# splitting related to the lowermost mantle:
# - phases                |  XKS | ScS
# - moment magnitude Mw   |  > 6
# - hypocentral depth     |  > 50 km
# - time window           |  [2010,2020]
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# Related to:
# - Fröhlich Y., Dillah M. I. F., Dorn F., Ritter J. R. R. (2024).
#   Investigation of seismic anisotropy in the D'' layer and at the CMB
#   regarding intense magnetic flux regions. 18th Symposium of Study of the
#   Earth's Deep Interior, proceedings, session 2-04.
#   https://doi.org/10.5281/zenodo.12658821.
# -----------------------------------------------------------------------------
# History:
# - Created: 2022/07/11
# - Updated: 2022/08/16
# - Updated: 2022/09/01
# - Updated: 2023/07/25
# - Updated: 2023/11/13
# - Updated: 2024/05/15 - Convert to function
# - Updated: 2024/06/14 - Improve highlighting
# - Updated: 2024/10/02 - Improve input parameters
# - Updated: 2024/10/04 - Add option to plot ray paths
# -----------------------------------------------------------------------------
# Versions:
# - PyGMT v0.7.0  with GMT 6.4.0
# - PyGMT v0.9.0  with GMT 6.4.0
# - PyGMT v0.10.0 with GMT 6.4.0
# - PyGMT v0.12.0 with GMT 6.5.0 -> https://www.pygmt.org/v0.12.0/
# - PyGMT v0.13.0 with GMT 6.5.0 -> https://www.pygmt.org/v0.13.0/
# -----------------------------------------------------------------------------
# Station coordinates input files were modified from GMT map
# "005_map_equidist_siberia" by Michael Grund
# Source of original script, data, and manual (last access 2022/04/06)
# https://github.com/michaelgrund/GMT-plotting/tree/main/005_map_equidist_siberia
# a modified version is part of his PhD thesis (DOI: 10.5445/IR/1000091425)
# #############################################################################


import pandas as pd
import pygmt as gmt


def sws_lmm_deepdyn(
    sws_type,
    lon_center,
    lat_center,
    lon_epi,
    lat_epi,
    ray_path=False,
    fig_name_add="",
    folder_out="",
):
    # %%
    # -------------------------------------------------------------------------
    # Input
    # -------------------------------------------------------------------------
    # Required
    # - sws_type:   string | "XKS" or "ScS"
    # - lon_center: float  | longitude of center    | degrees East
    # - lat_center: float  | latitude of center     | degrees North
    # - lons_epi:   float  | longitude of epicenter | degrees East
    # - lats_epi:   float  | latitude of epicenter  | degrees North
    # Optional
    # - ray_path:   boolean  | plot the ray paths between the epicenter of the
    #                          example earthquake and the recording stations
    #                                                    | Default False
    # - fig_name_add: string | addition to file name     | Default ""
    # - folder_out:   string | folder to store images in | Default current working directory


    # %%
    # -------------------------------------------------------------------------
    # Set up
    # -------------------------------------------------------------------------
    # General stuff
    path_in = "01_in_data"
    font = "3.5p"
    ray_str = ""
    dpi_png = 720

    # -------------------------------------------------------------------------
    # Map set up
    map_size = 2  # inches, radius of whole figure
    pro_area_XKS = 150
    pro_area_ScS = 100

    match sws_type:
        case "XKS": pro_area = pro_area_XKS  # degrees
        case "ScS": pro_area = pro_area_ScS

    deg2inch = map_size / pro_area

    # -------------------------------------------------------------------------
    # Circles related to target zone
    size_tag_main_deg = 15  # 15 deg radius main target zone
    size_tag_add_deg = 15  # 15 deg radius around main target zone
    size_tag_main = deg2inch * size_tag_main_deg
    size_tag_add = deg2inch * size_tag_add_deg

    # -------------------------------------------------------------------------
    # Cricles related to epicenters
    match sws_type:
        case "XKS":
            size_epi_min_deg = 90  # 80
            size_epi_max_deg = 140  # 150
            size_epi_min_add_deg = 80  # 80
            size_epi_max_add_deg = 150  # 150
            size_epi_min_add = deg2inch * size_epi_min_add_deg
            size_epi_max_add = deg2inch * size_epi_max_add_deg
        case "ScS":
            size_epi_min_deg = 60
            size_epi_max_deg = 90
    size_epi_min = deg2inch * size_epi_min_deg
    size_epi_max = deg2inch * size_epi_max_deg

    # -------------------------------------------------------------------------
    # Circles related to stations
    match sws_type:
        case "XKS":
            sta2tag_min = 22.5  # size_tag_main_deg + 2  # rough eastimation
            sta2tag_max = 35  # size_tag_main_deg + 20
        case "ScS":  # middel
            sta2tag_min = size_epi_min_deg / 2
            sta2tag_max = size_epi_max_deg / 2

    size_sta_main_min_deg = sta2tag_min
    size_sta_main_max_deg = sta2tag_max
    size_sta_main_min = deg2inch * size_sta_main_min_deg
    size_sta_main_max = deg2inch * size_sta_main_max_deg

    size_sta_add_max_deg = sta2tag_max + size_tag_add_deg
    size_sta_add_max = deg2inch * size_sta_add_max_deg

    # -------------------------------------------------------------------------
    # Legend
    box_standard = "+gwhite@20+p0.1p,gray30+r2p"  # box
    leg_net_pos = "JRB+jRB+w1.01c"  # position

    # -------------------------------------------------------------------------
    # Colors - can be changed for personal preferences
    color_highlight = "255/90/0"
    color_patb = "216.750/82.875/24.990"
    color_land = "gray95"
    color_shorelines = "gray70"
    color_water = "white"

    color_AA = "goldenrod1"  # AlpArray
    color_SA = "tomato"  # ScanArray
    color_USA = "FIREBRICK3"  # USArray
    color_GL = "SALMON"  # Greenland
    color_RUS = "PALEVIOLETRED"  # Russia

    color_pen_epi = "dodgerblue2"
    color_epi2tag = "dodgerblue3"
    color_fill_epi = "white"  # epicenter

    color_frame = "black"
    color_tag = "magenta"
    color_sta2tag = "purple"

    clearance_standard = "0.03c/0.03c+tO"

    # -------------------------------------------------------------------------
    # Data
    data_patb = "plate_boundaries_Bird_2003.txt"  # plate boundaries
    data_epi = "eq_CMT_lon_lat_LMM.txt"  # epicenters

    # Coordinates of stations
    sta_AA_perm = "coord_AlpArray_perm.dat"
    sta_AA_temp = "coord_AlpArray_temp.dat"
    sta_GL = "coord_Greenland.dat"
    sta_RUS = "coord_Russia.dat"
    sta_SA = "coord_ScanArray.dat"
    sta_USA = "coord_USArray_Alaska.dat"
    sta_USA_sub = "coord_USArray_Alaska_SUB.dat"

    key_choose = ["SA_2", "RUS", "SA", "AA_perm", "AA_temp", "USA", "GL"]
    # key_choose = ["SA_2", "SA", "AA_perm", "AA_temp", "USA"]

    # -------------------------------------------------------------------------
    # Dictionaries

    # Fill color of station markers and line color of ray paths
    dic_col = {
        "AA_perm": color_AA,
        "AA_temp": color_AA,
        "GL": color_GL,
        "RUS": color_RUS,
        "SA": color_SA,
        "SA_2": color_SA,
        "USA": color_USA,
        "USA_sub": color_USA,
    }

    # Coordinates of stations
    dic_sta = {
        "AA_perm": sta_AA_perm,
        "AA_temp": sta_AA_temp,
        "GL": sta_GL,
        "RUS": sta_RUS,
        "SA": sta_SA,
        "SA_2": sta_SA,
        "USA": sta_USA,
        "USA_sub": sta_USA_sub,
    }


    # %%
    # -------------------------------------------------------------------------
    # Create geographic maps
    # -------------------------------------------------------------------------
    # Create new PyGMT Figure instance
    fig = gmt.Figure()

    # -------------------------------------------------------------------------
    # Change default values of GMT globally
    gmt.config(MAP_FRAME_PEN=f"1p,{color_frame}", FONT_ANNOT_PRIMARY=font)

    # -------------------------------------------------------------------------
    # Create epidistance plot mit centre = target zone
    fig.coast(
        region="g",
        projection=f"E{lon_center}/{lat_center}/{pro_area}/{map_size}i",
        resolution="c",
        land=color_land,
        water=color_water,
        shorelines=f"1/0.1p,{color_shorelines}",
    )

    # -------------------------------------------------------------------------
    # Plot plate boundaries after Bird 2003
    fig.plot(data=f"{path_in}/{data_patb}", pen=f"0.25p,{color_patb}")

    # -------------------------------------------------------------------------
    # Plot epicenters

    # Load epicenter coordinates into pandas DataFrame
    df_epi = pd.read_csv(f"{path_in}/{data_epi}", sep=" ")

    fig.plot(
        data=df_epi,
        style="a0.1c",  # star
        fill=color_fill_epi,
        pen=f"0.01p,{color_pen_epi}",
    )

    # -------------------------------------------------------------------------
    # Recording stations around example epicenter
    if sws_type == "XKS":
        # Mark area of appropriate stations
        fig.plot(
            x=lon_epi,
            y=lat_epi,
            style=f"c{(size_epi_max_add + size_epi_min_add) / 2}i",
            pen=f"{(size_epi_max_add - size_epi_min_add) / 2}i,{color_epi2tag}@80",
            # no_clip=True,
        )
        fig.plot(
            x=lon_epi,
            y=lat_epi,
            style=f"c{(size_epi_max + size_epi_min) / 2}i",
            pen=f"{(size_epi_max - size_epi_min) / 2}i,{color_epi2tag}@80",
            # no_clip=True,
        )

    # -------------------------------------------------------------------------
    # Target area
    # additional
    fig.plot(
        x=lon_center,
        y=lat_center,
        style=f"c{size_tag_main + size_tag_add}i",
        fill=f"{color_tag}@65",
    )
    # main
    fig.plot(
        x=lon_center,
        y=lat_center,
        style=f"c{size_tag_main}i",
        fill=f"{color_tag}@40",
    )

    # -------------------------------------------------------------------------
    # Stations around target area
    # main
    fig.plot(
        x=lon_center,
        y=lat_center,
        style=f"c{size_sta_main_min}i",
        pen=f"0.35p,{color_sta2tag}",
    )
    fig.plot(
        x=lon_center,
        y=lat_center,
        style=f"c{size_sta_main_max}i",
        pen=f"0.35p,{color_sta2tag}",
    )
    # additional
    fig.plot(
        x=lon_center,
        y=lat_center,
        style=f"c{size_sta_add_max + size_tag_add}i",
        pen=f"0.35p,{color_sta2tag},-",
    )

    # -------------------------------------------------------------------------
    # Plot ray paths (very slow at the moment due to the loop)
    if ray_path == True:
        ray_str = "_raypaths"

        for key in key_choose:
            # Load station coordinates into a pandas DataFrame
            df_sta = pd.read_csv(f"{path_in}/{dic_sta[key]}", sep=" ")

            for i_sta in range(len(df_sta)):
                fig.plot(
                    x=[lon_epi, df_sta["lon_degE"][i_sta]],
                    y=[lat_epi, df_sta["lat_degN"][i_sta]],
                    pen=f"0.01p,{dic_col[key]}@95",
                )

    # -------------------------------------------------------------------------
    # Plot example epicenter
    fig.plot(
        x=lon_epi,
        y=lat_epi,
        style="a0.15c",  # star
        fill=color_epi2tag,
        pen="0.01p,black",
    )

    # -------------------------------------------------------------------------
    # Plot recording stations
    for key in key_choose:

        # Set input order of columns depending on file
        match key:
            case "SA_2" | "SA" | "USA_sub":
                incols_first = 0
                incols_second = 1
            case "RUS" | "AA_perm" | "AA_temp" | "GL":
                incols_first = 1
                incols_second = 0

        # Load station coordinates into a pandas DataFrame
        df_sta = pd.read_csv(f"{path_in}/{dic_sta[key]}", sep=" ")

        fig.plot(
            data=df_sta,
            style="i0.1c",
            fill=dic_col[key],
            pen="0.01p,gray10",
            incols=[incols_first, incols_second],
        )

    # -------------------------------------------------------------------------
    # Circle zoom in for ScS
    # if sws_type == "XKS":
    #     fig.plot(
    #         x=lon_center,
    #         y=lat_center,
    #         style=f"c{pro_area_ScS * deg2inch}i",
    #         pen="0.50p,gray30,.",
    #     )

    # -------------------------------------------------------------------------
    # Add map frame
    fig.basemap(frame=0)

    # -------------------------------------------------------------------------
    # Add labels of continents
    text=[
        "Africa",
        "Antarctica",
        "North America",
        "Asia",
        "South America",
        "Australia",
        "Europe",
    ]

    fig.text(
        x=[21.00,  74.305, -135.553, 102.255, -54.665, 138.51, -13.708],
        y=[18.38, -75,       41.099,  48.099,  -2,     -29.7,   47.388],
        text=text,
        font=font,
        fill="white@30",
        clearance=clearance_standard,
    )

    # -------------------------------------------------------------------------
    # Add annotation circles
    match sws_type:
        case "XKS":
            text_circle = ["15@.", "22.5@.", "30@.", "35@.", "65@."]
            offset_circle_x = [0.00,  0.00, 0.18,  0.00,  0.00]
            offset_circle_y = [0.09, -0.14, 0.09, -0.23, -0.43]
        case "ScS":
            text_circle = ["15@.", "30@.", "30@.", "45@.", "75@."]
            offset_circle_x = [0.00,  0.00, 0.19,  0.00,  0.00]
            offset_circle_y = [0.10, -0.28, 0.12, -0.45, -0.75]

    for cl in range(len(text_circle)):
        color_pen = color_tag
        if cl in [1, 3, 4]: color_pen = color_sta2tag
        fig.text(
            position="MC",
            offset=f"{offset_circle_x[cl]}i/{offset_circle_y[cl]}i",
            text=text_circle[cl],
            font=font,
            fill="white@30",
            pen=f"0.1p,{color_pen}",
            clearance=clearance_standard,
        )

    # -------------------------------------------------------------------------
    # Add labels
    position_target = "LT"
    offset_cord = "0.05c/-0.1c"
    position_phase = "RT"
    offset_phase = "-0.2c/-0.1c"

    # for target region
    target_label = f"{lon_center}@.E {lat_center}@.N"
    fig.text(
        position=position_target,
        offset=offset_cord,
        text=target_label,
        font=f"{font},{color_frame}",
        pen=f"0.1p,{color_frame}",
        clearance="0.05c/0.05c+tO",
    )

    # for phase
    fig.text(
        position=position_phase,
        offset=offset_phase,
        text=sws_type,
        font=f"{font},{color_highlight}",
        pen=f"0.1p,{color_highlight}",
        clearance="0.05c/0.05c+tO",
    )

    # -------------------------------------------------------------------------
    # Add legend
    fig.legend(
        spec=f"{path_in}/legend_gmt_network.txt",
        position=leg_net_pos,
        box=box_standard,
    )

    # -------------------------------------------------------------------------
    # Show and save figure
    fig.show()
    fig_name = f"map_epidist_LMM_{sws_type}_" + \
               f"center{lon_center}E{lat_center}N_" + \
               f"epi{lon_epi}E{lat_epi}N{fig_name_add}{ray_str}"
    for ext in ["png"]: #, "pdf", "eps"]:
        fig.savefig(fname=f"{folder_out}{fig_name}.{ext}", dpi=dpi_png)
    print(fig_name)



# %%
# -----------------------------------------------------------------------------
# Example
# -----------------------------------------------------------------------------
sws_lmm_deepdyn(
    sws_type="XKS",
    lon_center=42,
    lat_center=35,
    lon_epi=140,
    lat_epi=15,
    # ray_path=True,
    folder_out="02_out_figs/",
)
