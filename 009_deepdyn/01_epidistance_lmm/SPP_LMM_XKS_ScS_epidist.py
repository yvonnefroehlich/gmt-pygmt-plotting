# #############################################################################
# This maps show the epicenters of equarthakes usable to study shear wave
# splitting related to the lowermost mantle:
# - phases                |  XKS | ScS
# - moment magnitude Mw   |  > 6
# - hypocentral depth     |  > 50 km
# - time window           |  [2010,2020]
# - target zone           |  30 deg
# -----------------------------------------------------------------------------
# Highlighting concept
# - light green circle area            |  main target zone
# - light green dashed circle outline  |  additional target zone
# - dark green solid circle outlines   |  inner and outer limits for station regarding main target zone
# - dark green dashed circle outline   |  outer limit for stations regarding additional target zone
# - dark green dotted circle outline   |  section for ScS (only in XKS)
# - blue stars                         |  epicenters
# - colored inverse triangles          |  stations
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/05/15
#   PyGMT v0.12.0 -> https://www.pygmt.org/v0.12.0/ | https://www.pygmt.org/
#   GMT 6.4.0, 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Stations coordinates taken from GMT map "005_map_equidist_siberia" by Michael Grund
# Source of original script, data, and manual (last access 2022/04/06)
# https://github.com/michaelgrund/GMT-plotting/tree/main/005_map_equidist_siberia
# a modified version is part of his PhD thesis (DOI: 10.5445/IR/1000091425)
# #############################################################################


import pygmt as gmt


def sws_lmm_deepdyn(sws_type, target_center, fig_name_add="", folder_out=""):
    """

    :param sws_type: DESCRIPTION
    :type sws_type: TYPE
    :param target_center: DESCRIPTION
    :type target_center: TYPE
    :param fig_name_add: DESCRIPTION, defaults to ""
    :type fig_name_add: TYPE, optional
    :param folder_out: DESCRIPTION, defaults to ""
    :type folder_out: TYPE, optional
    :return: DESCRIPTION
    :rtype: TYPE

    """

# -----------------------------------------------------------------------------
    # Set up
# -----------------------------------------------------------------------------
    # general stuff
    path_in = "01_in_data"
    myfont = "4p"

# -----------------------------------------------------------------------------
    # coordinates of target area -> center, 2700 km piercing points
    target_center_split = target_center.split(",")
    lon_cent = target_center_split[0]
    lat_cent = target_center_split[1]

# -----------------------------------------------------------------------------
    # map set up
    map_size = 1.8  # inches, radius of whole figure
    pro_area_XKS = 150   # degrees
    pro_area_ScS = 100

    match sws_type:
        case "XKS": pro_area = pro_area_XKS
        case "ScS": pro_area = pro_area_ScS

    deg2inch = map_size / pro_area

# -----------------------------------------------------------------------------
    # circles related to target zone
    size_tag_main_deg = 15  # 15 deg radius main target zone
    size_tag_add_deg = 15  # 15 deg radius around main target zone
    size_tag_main = deg2inch * size_tag_main_deg
    size_tag_add = deg2inch * size_tag_add_deg

# -----------------------------------------------------------------------------
    # cricles related to epicenters
    match sws_type:
        case "XKS":
            size_epi_min_deg = 90
            size_epi_max_deg = 140
        case "ScS":
            size_epi_min_deg = 60
            size_epi_max_deg = 90
    size_epi_min = deg2inch * size_epi_min_deg
    size_epi_max = deg2inch * size_epi_max_deg

# -----------------------------------------------------------------------------
    # circles related to stations
    match sws_type:
        case "XKS":
            sta2tag_min = 22.5  # size_tag_main_deg + 2
            sta2tag_max = 35  # size_tag_main_deg + 20
        case "ScS":  # middel
            sta2tag_min = size_epi_min_deg / 2 - 1  # avoid overlap
            sta2tag_max = size_epi_max_deg / 2

    size_sta_main_min_deg = sta2tag_min
    size_sta_main_max_deg = sta2tag_max
    size_sta_main_min = deg2inch * size_sta_main_min_deg
    size_sta_main_max = deg2inch * size_sta_main_max_deg

    size_sta_add_max_deg = sta2tag_max + size_tag_add_deg
    size_sta_add_max = deg2inch * size_sta_add_max_deg

# -----------------------------------------------------------------------------
    # coordinates of example epicenters
    match sws_type:
        case "XKS":
            # lon_epi_exp_all = [-70, -70, 110, 130, 140, 120, 180, 170]  # degrees East
            # lat_epi_exp_all = [-10, -45, -10, 10, 15, 25, -20, -10]  # degrees North
            lon_epi_exp_all = [140]  # degrees East
            lat_epi_exp_all = [15]  # degrees North
        case "ScS":
            lon_epi_exp_all = [0]
            lat_epi_exp_all = [0]

# -----------------------------------------------------------------------------
    # legend
    box_standard = "+gwhite@20+p0.1p,gray30+r2p"  # box
    leg_net_pos = "JRB+jRB+w1.01c"  # position

# -----------------------------------------------------------------------------
    # colors - can be changed for personal preferences
    col_highlight = "255/90/0"
    col_patb = "216.750/82.875/24.990"
    col_land = "gray95"
    col_shorelines = "gray70"
    col_water = "white"

    col_AA = "goldenrod1"  # AlpArray
    col_SA = "tomato"  # ScanArray
    col_USA = "FIREBRICK3"  # USArray
    col_GL = "SALMON"  # Greenland
    col_RUS = "PALEVIOLETRED"  # Russia

    col_tag = "GREEN2"  # target area
    col_epi = "white"  # epicenter
    col_out_epi = "dodgerblue2"
    col_epi2tag = "DODGERBLUE3"
    col_sta2tag = "SEAGREEN"

# -----------------------------------------------------------------------------
    # data
    data_patb = "plate_boundaries_Bird_2003.txt"  # plate boundaries
    data_epi = "eq_CMT_lon_lat_LMM.txt"  # epicenters

    # coordinates of stations
    sta_AA_perm = "coord_AlpArray_perm.dat"
    sta_AA_temp = "coord_AlpArray_temp.dat"
    sta_GL = "coord_Greenland.dat"
    sta_RUS = "coord_Russia.dat"
    sta_SA = "coord_ScanArray.dat"
    sta_USA = "coord_USArray_Alaska.dat"
    sta_USA_sub = "coord_USArray_Alaska_SUB.dat"

    key_choose = ["SA_2", "RUS", "SA", "AA_perm", "AA_temp", "USA", "GL"]

# -----------------------------------------------------------------------------
    # dictionaries

    # fill color of station markers and line color of ray paths
    dic_col = {
        "AA_perm": col_AA,
        "AA_temp": col_AA,
        "GL": col_GL,
        "RUS": col_RUS,
        "SA": col_SA,
        "SA_2": col_SA,
        "USA": col_USA,
        "USA_sub": col_USA,
    }

    # coordinates of stations
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
# -----------------------------------------------------------------------------
    # Create geographic maps
# -----------------------------------------------------------------------------
    # Run loop over all example epicenters
    for i_epi in range(len(lon_epi_exp_all)):

        lon_epi_exp = lon_epi_exp_all[i_epi]
        lat_epi_exp = lat_epi_exp_all[i_epi]

# -----------------------------------------------------------------------------
        # Create new PyGMT Figure instance
        fig = gmt.Figure()

# -----------------------------------------------------------------------------
        # Change default values of GMT globally
        gmt.config(MAP_FRAME_PEN="0.5p,black", FONT_ANNOT_PRIMARY=myfont)

# -----------------------------------------------------------------------------
        # Create epidistance plot mit centre = target zone
        fig.coast(
            region="g",
            projection=f"E{lon_cent}/{lat_cent}/{pro_area}/{map_size}i",
            resolution="c",
            land=col_land,
            water=col_water,
            shorelines=f"1/0.1p,{col_shorelines}",
        )

# -----------------------------------------------------------------------------
        # Plot plate boundaries after Bird 2003
        fig.plot(data=f"{path_in}/{data_patb}", pen=f"0.25p,{col_patb}")

# -----------------------------------------------------------------------------
        # Plot epicenters
        fig.plot(
            data=f"{path_in}/{data_epi}",
            style="a0.1c",  # star
            fill=col_epi,
            pen=f"0.01p,{col_out_epi}",
        )

# -----------------------------------------------------------------------------
        # Stations around epicenters
        if sws_type == "XKS":
            # Plot example epicenters
            fig.plot(
                x=lon_epi_exp,
                y=lat_epi_exp,
                style="a0.15c",  # star
                fill=col_epi2tag,
                pen="0.01p,black",
            )
            # Mark area of appropriate stations
            fig.plot(
                x=lon_epi_exp,
                y=lat_epi_exp,
                style=f"c{(size_epi_max + size_epi_min) / 2}i",
                pen=f"{(size_epi_max - size_epi_min) / 2}i,{col_epi2tag}@80",
            )

# -----------------------------------------------------------------------------
        # Target area
        # additional
        fig.plot(
            x=lon_cent,
            y=lat_cent,
            style=f"c{size_tag_main + size_tag_add}i",
            pen=f"0.35p,{col_tag},-",
        )
        # main
        fig.plot(
            x=lon_cent,
            y=lat_cent,
            style=f"c{size_tag_main}i",
            fill=f"{col_tag}@60",
        )

# -----------------------------------------------------------------------------
        # Stations around target area
        # main
        fig.plot(
            x=lon_cent,
            y=lat_cent,
            style=f"c{size_sta_main_min}i",
            pen=f"0.35p,{col_sta2tag}",
        )
        fig.plot(
            x=lon_cent,
            y=lat_cent,
            style=f"c{size_sta_main_max}i",
            pen=f"0.35p,{col_sta2tag}",
        )
        # additional
        fig.plot(
            x=lon_cent,
            y=lat_cent,
            style=f"c{size_sta_add_max + size_tag_add}i",
            pen=f"0.35p,{col_sta2tag},-",
        )

# -----------------------------------------------------------------------------
        # Recording stations
        for key in key_choose:
            # set input order of columns depending on file
            if key in ["SA_2", "SA", "USA_sub"]:
                incols_first = 0
                incols_second = 1
            if key in ["RUS", "AA_perm", "AA_temp", "GL"]:
                incols_first = 1
                incols_second = 0

            fig.plot(
                data=f"{path_in}/{dic_sta[key]}",
                style="i0.1c",
                fill=dic_col[key],
                pen="0.01p,gray10",
                incols=[incols_first, incols_second],
            )

# -----------------------------------------------------------------------------
        # Circle zoom in for ScS
        if sws_type == "XKS":
            fig.plot(
                x=lon_cent,
                y=lat_cent,
                style=f"c{pro_area_ScS * deg2inch}i",
                pen="0.50p,gray30,.",
            )

# -----------------------------------------------------------------------------
        # Add map frame
        fig.basemap(frame="wsne")

# -----------------------------------------------------------------------------
        # Add labels of continents
        fig.text(
            x=[21.00, 74.305, -135.553, 102.255, -54.665, 138.51, -13.708],
            y=[18.38, -75, 41.099, 48.099, -17.154, -29.7, 47.388],
            text=[
                "Africa",
                "Antarctica",
                "North America",
                "Asia",
                "South America",
                "Australia",
                "Europe",
            ],
            font=myfont,
            fill="white@30",
            clearance="+tO",
        )

# -----------------------------------------------------------------------------
        # Add annotation circles
        match sws_type:
            case "XKS":
                text_circle = ["15@.", "22.5@.", "30@.", "35@.", "65@.", "100@."]
                offset_circle_x = [0, 0.13, 0.18, 0, 0, 0]
                offset_circle_y = [0.09, 0.05, -0.04, -0.20, -0.39, -0.60]
            case "ScS":
                text_circle = ["15@.", "29@.-30@.", "45@.", "75@."]
                offset_circle_x = [0, 0, 0, 0]
                offset_circle_y = [0.12, -0.26, -0.40, -0.67]

        for cl in range(len(text_circle)):
            fig.text(
                position="MC",
                offset=f"{offset_circle_x[cl]}i/{offset_circle_y[cl]}i",
                text=text_circle[cl],
                font=myfont,
                fill="white@30",
                clearance="+tO",
            )

# -----------------------------------------------------------------------------
        # Add label for phase
        fig.text(
            position="LT",
            offset="0.2c/-0.1c",
            text=sws_type,
            font=f"{myfont},{col_highlight}",
            pen=f"0.1p,{col_highlight}",
            clearance="0.05c/0.05c+tO",
        )

# -----------------------------------------------------------------------------
        # Add label for target region
        fig.text(
            position="RT",
            offset="-0.05c/-0.1c",
            text=f"{lon_cent}@.E {lat_cent}@.N",
            font=f"{myfont},{col_highlight}",
            pen=f"0.1p,{col_highlight}",
            clearance="0.05c/0.05c+tO",
        )

# -----------------------------------------------------------------------------
        # Add legend
        fig.legend(
            spec=f"{path_in}/legend_gmt_network.txt",
            position=leg_net_pos,
            box=box_standard,
        )

# -----------------------------------------------------------------------------
        # Show and save figure
        fig.show()
        fig_name = f"{folder_out}" + \
            f"DeepDyn_LMM_{sws_type}_{lon_cent}E{lat_cent}N_epi{i_epi}" + \
            f"{fig_name_add}"
        for ext in ["png"]: #, "pdf", "eps"]:
            fig.savefig(fname=f"{fig_name}.{ext}", dpi=720)
        print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Example
# -----------------------------------------------------------------------------
sws_lmm_deepdyn(
    sws_type="XKS",
    target_center="-105,60",  # lon_degE,lat_degN
    fig_name_add="",
    folder_out="02_out_figs/",
)
