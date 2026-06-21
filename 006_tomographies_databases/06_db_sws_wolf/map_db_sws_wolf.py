# #############################################################################
# Comprehensive global data set of uniformly processed shear-wave splitting
# measurements
# Wolf J, Becker T W, Garnero E, Liu K H, West J D (2025). GJI, 241(2):863–875.
# https://doi.org/10.1093/gji/ggaf076.
#
# Data available at
# Last accessed: 2026/06/02
#
# Skript II: Create maps showing shear wave splitting as orientated bars
#            Uses data files created via script prepare_db_sws_wolf
# -----------------------------------------------------------------------------
# History
# - Created: 2026/03/13
# - Updated: 2026/06/02
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.18.0 -> https://www.pygmt.org
# - GMT 6.6.0 -> https://www.generic-mapping-tools.org
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################

import pygmt
import numpy as np
import pandas as pd


# %%
# -----------------------------------------------------------------------------
# Adjust for your needs
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"

year_start = 2000
year_end = 2024
year_step = 1

bar_depth = 210  # depth of piercing points km  ## 2989, 660, 410, 210

scale_dt_bar = 0.8  # MUST be SAME for all plots in case of comparision

qualities = ["good", "average", "all"]  # for the criteria see the paper
qualities = ["good"]
obstypes = ["null", "split", "split"]
obstypes = ["split"]
color_quantities = ["phi", "dt", "SI"]  # used for color-coding the symbols
areas = [
    # "globalg", "globald",
    "europe",
    # "usa", #"africa", "samerica", "australia", "asia",
    # "northpole", "southpole",
    # "germany",
    # "mediterranean",
    # "urglarge",
    # "urgphd",
]


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
fig_width = 12

projection_rob = f"N{fig_width}c"

lon_de_min, lon_de_max, lat_de_min, lat_de_max = 5.5, 15.3, 47.1, 55.3
region_de = [lon_de_min, lon_de_max, lat_de_min, lat_de_max]
projection_de = f"M{fig_width}c"

lon_urg_min, lon_urg_max, lat_urg_min, lat_urg_max = 6, 10.15, 47.4, 50
lon_urg_mean = (lon_urg_min + lon_urg_max) / 2
lat_urg_mean = (lat_urg_min + lat_urg_max) / 2
center_coord = {"x": lon_urg_mean, "y": lat_urg_mean}

# -----------------------------------------------------------------------------
# Colors
color_sl = "gray80"  # shorelines
color_nb = "gray20"  # national borders
color_hl = "255/90/0"  # highlight
color_pb = "216.750/82.875/24.990"  # plate boundaries  # -> dark orange
color_urg = "darkbrown"  # "sienna"
color_land = "gray95"
color_station = "gold"
color_sks = "205/0/0"  # -> red
color_skks = "238/118/0"  # -> orange
color_pks = "yellow2"

box_standard = "+gwhite@30+p0.8p,gray50+r2p"
clearance_standard = "0.1c+tO"


# %%
# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
file_name = "measurements_NOwhitespaces_pierce"
df_sks = pd.read_csv(f"{path_in}/SKS_{file_name}.txt", sep=";")
df_skks = pd.read_csv(f"{path_in}/SKKS_{file_name}.txt", sep=";")
df_pks = pd.read_csv(f"{path_in}/PKS_{file_name}.txt", sep=";")


# %%
# -----------------------------------------------------------------------------
# Map stations - split, nulls | phi, dt, SI |
#                different areas | over time | different depths
# -----------------------------------------------------------------------------
for year in range(year_start, year_end + year_step, year_step):

    df_sks_temp = df_sks[
        (df_sks["event_year"] >= year_start) & (df_sks["event_year"] <= year)
    ]
    df_skks_temp = df_skks[
        (df_skks["event_year"] >= year_start) & (df_skks["event_year"] <= year)
    ]
    df_pks_temp = df_pks[
        (df_pks["event_year"] >= year_start) & (df_pks["event_year"] <= year)
    ]

    for area in areas:

        if area in ["globalepi", "globalg", "globald"]:
            circle_size = 0.03
        elif area in ["northpole", "southpole", "samerica", "asia"]:
            bar_width = 0.05
        elif area in ["germany", "urglarge"]:
            circle_size = 0.12
            bar_width = 0.01
        elif area in ["urgphd"]:
            circle_size = 0.12
            bar_width = 0.07
        else:
            circle_size = 0.065
            bar_width = 0.012

        match area:
            case "globalg":
                region = "g"
                projection = projection_rob
            case "globald":
                region = "d"
                projection = projection_rob
            case "europe":
                lon_min, lon_max, lat_min, lat_max = -27, 42, 34, 72
            case "usa":
                lon_min, lon_max, lat_min, lat_max = -130, -57, 25, 52
            case "africa":
                lon_min, lon_max, lat_min, lat_max = -20, 54.5, -37, 38
            case "samerica":
                lon_min, lon_max, lat_min, lat_max = -83, -33, -57, 14
            case "australia":
                lon_min, lon_max, lat_min, lat_max = 112, 155, -44, -10.01
            case "asia":
                lon_min, lon_max, lat_min, lat_max = 61, 149.99, -9, 57
            case "southpole":
                region = [-180, 180, -90, -60]
                projection = f"A0/-90/40/{fig_width}c"
            case "northpole":
                region = [-180, 180, 60, 90]
                projection = f"A0/90/40/{fig_width}c"
            case "germany":
                region = region_de
                projection = projection_de
            case "urgphd":
                region = [lon_urg_min, lon_urg_max, lat_urg_min, lat_urg_max]
                projection = projection_de
            case "urglarge":
                region = [4, 20, 42, 52]
                # region = [4, 12, 46, 51.5]
                projection = projection_de
            case "mediterranean":
                region = [-11, 45, 28, 53]
                projection = projection_de

        if area not in [
            "globalg", "globald",
            "africa", "northpole", "southpole",
            "germany", "urgphd", "urglarge", "mediterranean",
        ]:
            region = [lon_min, lon_max, lat_min, lat_max]
            # Calculate projection center
            lon0 = np.mean([lon_min, lon_max])
            lat0 = np.mean([lat_min, lat_max])
            # Calculate two standard parallels (only these two distortion-free)
            lat1 = lat_min + (lat_max - lat_min) / 3
            lat2 = lat_min + (lat_max - lat_min) / 3 * 2
            projection = f"L{lon0}/{lat0}/{lat1}/{lat2}/{fig_width}c"

            text_pos = "TC"
            text_just = "TC"
            text_offx = 0
            text_offy = 0
        elif area == "samerica":
            text_pos = "BC"
        else:
            text_pos = "RT"
            text_just = "RM"
            text_offx = -0.2
            text_offy = -0.3

# -----------------------------------------------------------------------------
        for phase, df_xks, color_xks in zip(
            ["SKS", "SKKS", "PKS"],
            [df_sks_temp, df_skks_temp, df_pks_temp],
            [color_sks, color_skks, color_pks],
        ):

            phi_gmt = []
            for i_swsm in df_xks.index.to_list(): #range(len(df_xks)):
                phi_temp = df_xks["phi"][i_swsm]
                if phi_temp >=0 :
                    phi_gmt_temp = 90 - phi_temp
                elif phi_temp < 0:
                    phi_gmt_temp = abs(phi_temp) + 90
                phi_gmt.append(phi_gmt_temp)

            df_xks["phi_gmt"] = phi_gmt
            df_xks["dt_scale"] = df_xks["dt"] * scale_dt_bar
            df_xks["bar_width"] = [bar_width] * len(df_xks)

# -----------------------------------------------------------------------------
            for obs_type, quality in zip(obstypes, qualities):

                if obs_type == "null":
                    df_xks_obs = df_xks[df_xks["quality"] == "null-measurement"]
                elif obs_type == "split":
                    if quality != "all":
                        df_xks_obs = df_xks[df_xks["quality"] == quality]
                    else:
                        df_xks_obs = df_xks[df_xks["quality"] != "null-measurement"]

# -----------------------------------------------------------------------------
                for color_quantity in color_quantities:

# -----------------------------------------------------------------------------
                    fig = pygmt.Figure()

                    with pygmt.config(MAP_FRAME_PEN=color_xks, MAP_GRID_PEN="0.01p,gray90"):
                        fig.basemap(region=region, projection=projection, frame="afg")
                    fig.coast(shorelines=f"1/0.2p,{color_sl}", land=color_land)

                    # Add Plate boundaries after Bird 2003
                    fig.plot(
                        data=f"{path_in}/plate_boundaries_Bird_2003.txt",
                        pen=f"0.3p,{color_pb}",
                    )

                    if color_quantity == "phi":
                        pygmt.makecpt(cmap="phase", series=[-90, 90])
                        cb_afg = "a30f10"
                        cb_label = "fast polarization direction @~f@~ / N°E"
                    elif color_quantity == "dt":
                        pygmt.makecpt(cmap="lapaz", series=[0, 3], reverse=True)
                        # pygmt.makecpt(cmap="roma", series=[0.5, 2], reverse=True)
                        cb_afg = "a0.5f0.1"
                        cb_label = "delay time @~d@~t / s"
                    elif color_quantity == "SI":
                        pygmt.makecpt(cmap="vik", series=[-2, 2])
                        cb_afg = "a0.5f0.1"
                        cb_label = "splitting intensity SI"

                    if bar_depth == 0:
                        bar_lon = "station_lon"
                        bar_lat = "station_lat"
                    elif bar_depth == 210:
                        bar_lon = "pierce210km_lon"
                        bar_lat = "pierce210km_lat"
                    elif bar_depth == 410:
                        bar_lon = "pierce410km_lon"
                        bar_lat = "pierce410km_lat"
                    columns_bar = [
                        bar_lon, bar_lat, color_quantity,
                        "phi_gmt", "dt_scale", "bar_width",
                    ]

                    # Plot piercing poinnts with color-coding
                    if obs_type == "null":
                        fig.plot(
                            data=df_xks_obs[columns_bar],
                            style=f"c{circle_size}c",
                            cmap=True,
                        )
                    elif obs_type == "split":
                        # orientated rectangels
                        style_bar = "j"
                        # GMT4 vector synthax tailwidth/headlength/halfheadwidth
                        # style_bar ="vB0.04c/0.02c/0.02c",
                        fig.plot(
                            data=df_xks_obs[columns_bar],
                            style=style_bar,
                            # fill="gray20",
                            # pen="0.01p,white",
                            cmap=True,
                            # pen="0.01p,black",
                        )

                    # Add label for year range and depth
                    for text, offx, offy in zip(
                        [f"2000 - {year}", f"@@ {bar_depth} km"],
                        [text_offx, text_offx],
                        [text_offy, text_offy - 0.35],
                    ):
                        fig.text(
                            text=text,
                            position=text_pos,
                            justify=text_just,
                            offset=f"{offx}c/{offy}c",
                            font=f"8p,1,{color_hl}",
                            fill="white@30",
                            clearance="0.1c+tO",
                        )

                    with pygmt.config(MAP_FRAME_PEN="0.1p"):
                        fig.colorbar(
                            frame=f"x{cb_afg}+l@%1%@;{color_xks};{phase}@;; " +\
                                f"@;{color_hl};{obs_type}s@;;@%% ({quality}): " + \
                                f"{cb_label}"
                        )

                    if obs_type == "null" and color_quantity in ["phi", "dt"]:
                        pass
                    else:
                        fig.show()
                        fig_name = f"map_stations_{obs_type}_{quality}_" +\
                            f"{color_quantity.lower()}_{area}_{bar_depth}km_" +\
                            f"{phase}_{year_start}to{year}"
                        fig.savefig(fname=f"{path_out}/{fig_name}.png")
                    print(fig_name)
