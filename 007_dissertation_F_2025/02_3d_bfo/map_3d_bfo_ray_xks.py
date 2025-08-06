# #############################################################################
# This script allows to reproduce
#   Fig. 1 (b) and Fig. C.3 of
#   Fröhlich Y. (2025). Shear wave splitting analysis of long-term data:
#   Anisotropy studies in the Upper Rhine Graben area, Central Europe.
#   Dissertation, Karlsruhe Institute of Technology, Geophysical Institute.
#   https://doi.org/10.5445/IR/1000183786.
# using the
#   SWSM dataset available at https://dx.doi.org/10.35097/685
#   published along with the publication https://doi.org/10.1093/gji/ggae245
# -----------------------------------------------------------------------------
# 3-D plot with different layers
# - Earth's magnetic field model gufm1 from 1981 at the core mantel boundary (CMB)
# - tomography GyPSum dvs for D'' layer by Simmons et al. 2010
#   on top areas of reduced shear wave velocity by Wolf et al. 2023
# - 410 km plane
# - elevation at surface
# with shear wave splitting measurements (SWSMs) at the recording station Black
# Forest Observatory (BFO)
# - piercing points at the CMB
# - rays from the CMB to the surface (receiver side)
# Note: No consideration of the spherical shape of the Earth
# -----------------------------------------------------------------------------
# History
# - Created: 2025/02/09
# - Updated: 2025/08/06 - adjust code for GitHub
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
import numpy as np
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# "KN", "KKN", "KNN", "KKNN"
# ray_groups = ["KN", "KKN"]
# ray_groups = ["KNN", "KKNN"]
ray_groups = ["KN", "KKN", "KNN", "KKNN"]
ray_groups_str = "_".join(ray_groups)
pierce_groups = ray_groups

status_cb = True
status_lgd = True

# "gufm1", "gypsum", "410 km", "elevation"
planes = ["gypsum", "410 km", "elevation"]

step = 1
cord_range = 40  # degrees

# Path
path_in = "01_in_data"
path_out = "02_out_figs"

# Data
file_gypsum = "tomo_gypsum_1d_grid_dvs_22_2650-2900km.grd"
file_gufm1 = "gufm1_1980_2900km_Z.grd"
file_pb = "plate_boundaries_Bird_2003.txt"

# -----------------------------------------------------------------------------
# Colors
color_hl = "255/90/0"  # -> orange | URG paper
color_station = "gold"
color_land = "gray80"
color_sl = "gray40"  # shorelines by GMT
color_pb = "216.750/82.875/24.990"  # plate boundaries by Bird 2023
color_nb = "gray10"  # national boundaries by GMT

color_SKS = "205/0/0"  # -> red
color_SKKS = "238/118/0"  # -> orange
color_PKS = "yellow2"
color_null = "white"
color_ray_KN = "lightred"
color_ray_KNN = color_SKS
color_ray_KKN = "lightorange"
color_ray_KKNN = color_SKKS

pen_pp = "0.3p,gray10"
color_llpv = "gray10"
color_llpv = "gray20"
pattern_llpv = "p8+b+f"
alpha_ele = 35
box_standard = "+gwhite@30+p0.1p,gray30+r2p"

if ray_groups_str == "KN_KKN_KNN_KKNN":
    pen_pp = "0.01p,gray10"
    color_ray_KN = f"{color_SKS}@40"
    color_ray_KNN = f"{color_SKS}@40"
    color_ray_KKN = f"{color_SKKS}@40"
    color_ray_KKNN = f"{color_SKKS}@40"

# color_SKS = "0/0/238"  # GMT blue2
# color_SKKS = "green2"  # GMT green2
# color_PKS =  "238/201/0"  # GMT gold2
# color_null = "white"
# color_ray_KN = "lightblue"
# color_ray_KNN = color_SKS
# color_ray_KKN = "lightgreen"
# color_ray_KKNN = color_SKKS

text_target = {
    "font": f"6p,1,{color_hl}",
    "fill": "white@30",
    "clearance": "0.09c/0.09c+tO",
    "perspective": [180, 80],
}

# -----------------------------------------------------------------------------
# Azimuth and elevation angle of the viewpoint [Default is [180, 90]]
perspective = [180, 12]

# Set y axis shift cummulativ up
y_gufm1 = 2  # centimeters
y_gypsum = 5.72
y_uppmantle = 1.18

# Recording station BFO
lon_BFO = 8.330
lat_BFO = 48.331



# %%
# -----------------------------------------------------------------------------
# Generate geographic map
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(FONT="8p", MAP_GRID_PEN_PRIMARY="0.01p,gray80", MAP_FRAME_WIDTH="2p")

for plane in planes:
    print(plane)

    # Study area
    lon_min = -60
    lon_max = 55
    lat_min = 20
    lat_max = 75
    region = [lon_min, lon_max, lat_min, lat_max]

    # Lambert projection
    # Determine projection center
    # lon0 = np.mean([lon_min, lon_max])
    lon0 = 60  # here manually adjusted
    lat0 = np.mean([lat_min, lat_max])
    # Calculate two standard parallels (only these two distortion-free)
    lat1 = lat_min + (lat_max - lat_min) / 3
    lat2 = lat_min + (lat_max - lat_min) / 3 * 2
    projection = f"L{lon0}/{lat0}/{lat1}/{lat2}/10c"

    frame = ["WSNE", "f5g5"]
    frame_a = ["wSnE", "a15f5g5"]
    if "gufm1" in planes:
        if plane == "gufm1": frame = frame_a
        fig_name_add = "gufm1_gypsum"
    else:
        if plane == "gypsum": frame = frame_a
        fig_name_add = "gypsum"
    fig.basemap(region=region, projection=projection, frame=frame, perspective=perspective)

# -----------------------------------------------------------------------------
    # Plot the different planes
    match plane:
        case "gufm1":  # CMB
            grd_gufm1_name = f"{path_in}/{file_gufm1}"
            gmt.makecpt(cmap="vik", series=[-850000, 850000], reverse=True)
            fig.grdimage(grid=grd_gufm1_name, cmap=True, perspective=True)
            # When plotting the colorbar here the shorelines are plotted wrongly
            # probably because due to the effect of the position parameter on the
            # anchor point in combination with the perspective not applied to the
            # colorbar
            fig.coast(shorelines=f"1/0.01p,{color_sl}", perspective=True)
            fig.show()
        case "gypsum":  # lower most mantle
            grd_gypsum_name = f"{path_in}/{file_gypsum}"
            gmt.makecpt(cmap="roma", series=[-2, 2])
            fig.grdimage(grid=grd_gypsum_name, cmap=True, perspective=True)
            # When plotting the colorbar here to code crashes
            # probably because due the effect of the position parameter on the
            # anchor point in combination changing to 3-D
            fig.coast(shorelines=f"1/0.01p,{color_sl}", perspective=True)
# .............................................................................
            # Plot LLSVPs by Wolf et al. 2023
            for i_model in range(2, 9, 1):
                fig.plot(
                    data=f"{path_in}/04_llvp/3model_2016_{i_model}.txt",
                    pen=f"0.2p,{color_llpv}",
                    fill=f"{pattern_llpv}{color_llpv}",
                    close=True,
                    perspective=True,
                )
            fig.show()
# .............................................................................
            # Plot piercing points in the lowermost mantle for BFO
            path_swsm = f"{path_in}/02_pp2700km/BFO_pp2700km_"
            if ray_groups_str == "KN_KKN_KNN_KKNN":
                fig.plot(
                    data=[f"{path_swsm}KN_goodfair.txt", f"{path_swsm}KNN_goodfair.txt"],
                    style="c0.12c",
                    fill=f"{color_SKS}",
                    pen=pen_pp,
                    perspective=True,
                )
                fig.plot(
                    data=[f"{path_swsm}KKN_goodfair.txt", f"{path_swsm}KKNN_goodfair.txt"],
                    style="c0.12c",
                    fill=f"{color_SKKS}",
                    pen=pen_pp,
                    perspective=True,
                )
            else:
                fig.plot(
                    data=f"{path_swsm}KNN_goodfair.txt",
                    style="c0.12c",
                    fill=color_SKS,
                    pen=pen_pp,
                    perspective=True,
                )
                fig.plot(
                    data=f"{path_swsm}KKNN_goodfair.txt",
                    style="c0.12c",
                    fill=color_SKKS,
                    pen=pen_pp,
                    perspective=True,
                )
                fig.plot(
                    data=f"{path_swsm}KN_goodfair.txt",
                    style="c0.12c",
                    fill=color_null,
                    pen=f"0.5p,{color_SKS}",
                    perspective=True,
                )
                fig.plot(
                    data=f"{path_swsm}KKN_goodfair.txt",
                    style="c0.12c",
                    fill=color_null,
                    pen=f"0.5p,{color_SKKS}",
                    perspective=True,
                )
            fig.show()
        case "410 km":
            fig.coast(
                shorelines=f"1/0.01p,{color_sl}",
                land=f"{color_land}@30",
                perspective=True,
            )
# .............................................................................
            # Plot plate boundaries
            fig.plot(
                data=f"{path_in}/{file_pb}", pen=f"0.01p,{color_pb}", perspective=True
            )
            fig.show()
# .............................................................................
            # Plot piercing points at 410 km for BFO
            for pierce_group in pierce_groups:
                match pierce_group:
                    case "KN": color_pp410 = color_ray_KN
                    case "KNN": color_pp410 = color_ray_KNN
                    case "KKN": color_pp410 = color_ray_KKN
                    case "KKNN": color_pp410 = color_ray_KKNN
                fig.plot(
                    data=f"{path_in}/03_pp410km/BFO_pp410km_{pierce_group}_goodfair.txt",
                    style="c0.07c",
                    fill=color_pp410,
                    perspective=True,
                )
            fig.show()
        case "elevation":
            gmt.makecpt(cmap="oleron", series=[-7100, 4500], transparency=alpha_ele)
            fig.grdimage(
                grid="@earth_relief",
                cmap=True,
                transparency=alpha_ele,
                perspective=True,
            )
            fig.coast(
                shorelines=f"1/0.01p,{color_sl}",
                borders=f"1/0.01p,{color_nb}",
                perspective=True,
            )
# .............................................................................
            # Add label for recording station
            # fig.plot(
            #     x=lon_BFO,
            #     y=lat_BFO,
            #     style="i0.35c",
            #     pen="0.1p,black",
            #     fill=color_station,
            #     perspective=True,
            # )
            fig.text(
                text="BFO",
                x=lon_BFO,
                y=lat_BFO,
                pen=f"0.8p,{color_hl}",
                justify="MC",
                offset="0c/-3.6c",
                **text_target,
            )
            fig.show()
# -----------------------------------------------------------------------------
    # 3-D plot
    # Cut the rays into two parts:
    # 2700-410 km (lower) and 410-0 km (upper) for correct layer order
    # Rays have to pierce through the piercing points, thus the piercing points have to
    # be plotted after the lower ray part but before the upper ray part
    if plane in ["gypsum", "410 km", "elevation"]:
        region3d = [lon_min, lon_max, lat_min, lat_max, 0, 2700]
        match plane:
            case "gypsum":
                min_depth = 410  # kilometers
                max_depth = 2700
            case "410 km":
                min_depth = -0.1
                max_depth = 410.1
                fig.shift_origin(yshift=f"-{y_gypsum}c")
            case "elevation":
                fig.shift_origin(yshift=f"-{y_gypsum + y_uppmantle}c")
        # Account for elevation angle and plot vertical frame only once
        if plane == "gypsum":
            with gmt.config(MAP_FRAME_PEN="0.8p,black"):
                fig.plot3d(
                    region=region3d,
                    frame=["wsneZ4", "za500f100+ldepth / km"],
                    zsize=f"-{y_gypsum + y_uppmantle}c",
                    x=[lon_BFO, lon_BFO],
                    y=[lat_BFO, lat_BFO],
                    z=[0, -50],  # Manually adjusted
                    pen=f"0.15p,{color_ray_KNN}",
                    perspective=True,
                )
        # Plot recording station
        if plane == "elevation":
            y_station = 2.95  # centimeters, manually adjusted
            fig.shift_origin(yshift=f"{y_station}c")
            fig.plot3d(
                region=region3d,
                x=lon_BFO,
                y=lat_BFO,
                z=0,
                style="i0.3c",  # 0.17c
                pen="0.3p,black",
                fill=color_station,
                no_clip=True,
                perspective=[180, 90],
            )
            fig.shift_origin(yshift=f"-{y_station}c")
        # Plot ray paths
        if plane in ["gypsum", "410 km"]:
            for ray_group in ray_groups:
                print(f"{plane} ray {ray_group}")
                match ray_group:
                    case "KN":
                        N_ray = 172
                        color_ray = color_ray_KN
                    case "KNN":
                        N_ray = 39
                        color_ray = color_ray_KNN
                    case "KKN":
                        N_ray = 54
                        color_ray = color_ray_KKN
                    case "KKNN":
                        N_ray = 12
                        color_ray = color_ray_KKNN
                for i_ray in range(step, N_ray + step, step):
                    ray_path = f"{path_in}/01_paths/{ray_group}"
                    ray_file = f"tt_PATH_{ray_group}_goodfair_path_{i_ray}.txt"
                    df_ray_temp = pd.read_csv(
                        f"{ray_path}/{ray_file}", sep=",", names=["lon", "lat", "depth"],
                    )
                    df_ray_temp0 = df_ray_temp.loc[df_ray_temp["depth"] < max_depth]
                    df_ray_temp1 = df_ray_temp0.loc[df_ray_temp0["depth"] > min_depth]
                    df_ray_temp2 = df_ray_temp1.loc[df_ray_temp1["lon"] > lon_BFO - cord_range]
                    df_ray_temp3 = df_ray_temp2.loc[df_ray_temp2["lon"] < lon_BFO + cord_range]
                    df_ray_temp4 = df_ray_temp3.loc[df_ray_temp3["lat"] > lat_BFO - cord_range]
                    df_ray_temp5 = df_ray_temp4.loc[df_ray_temp4["lat"] < lat_BFO + cord_range]
                    fig.plot3d(
                        region=region3d,
                        data=df_ray_temp5,
                        pen=f"0.3p,{color_ray}",
                        no_clip=True,
                        perspective=True,
                    )
        match plane:
            case "410 km": fig.shift_origin(yshift=f"{y_gypsum}c")
            case "elevation": fig.shift_origin(yshift=f"{y_gypsum + y_uppmantle}c")
        fig.show()

# -----------------------------------------------------------------------------
    # Add colorbars for grids
    if (ray_groups_str == "KN_KKN" and plane == "gypsum") or \
        (ray_groups_str == "KNN_KKNN" and plane == "elevation"):
        pass
    else:
        if plane in ["gufm1", "gypsum", "elevation"]:
            cb_pos = "jLB+h+w2.5c/0.2c"
            match plane:
                case "gufm1":
                   cb_frame = ["xaf+lmagnet field model gufm1", "y+lZ / nT"]
                   cb_offset = "+o-1c/0.5c"
                case "gypsum":
                    cb_frame = ["xaf+ltomography GyPSuM", "y+ldvs / %"]
                    # cb_offset = "+o-1c/0.5c"
                    cb_offset = "+o0.3c/2.5c"  # for PhD
                case "elevation":
                    cb_frame = ["xa4000f+lelevation", "y+lz / m"]
                    cb_offset = "+o0.8c/0.2c"
            if status_cb == True:
                with gmt.config(FONT="12p", MAP_FRAME_PEN="0.5p,black"):
                    fig.colorbar(frame=cb_frame, position=f"{cb_pos}{cb_offset}+ml")

# -----------------------------------------------------------------------------
    # Shift plotting origin
    match plane:
        case "gufm1": yshift_plane = f"{y_gufm1}c"
        case "gypsum": yshift_plane = f"{y_gypsum}c"
        case "410 km": yshift_plane = f"{y_uppmantle}c"
        case "elevation": yshift_plane = f"-{y_gypsum + y_uppmantle}c"
    fig.shift_origin(yshift=yshift_plane)

# -----------------------------------------------------------------------------
# Add legend for piercing points and rays
args_leg_pp = {"x": -1, "y": -1, "style": "c0.12c"}
args_leg_ray = {"x": [-1, -1], "y": [-1, -1]}

if ray_groups_str =="KN_KKN":
    fig.plot(fill=color_null, pen=f"1p,{color_SKS}", label="pierce @@2700 km SKS null", **args_leg_pp)
    fig.plot(fill=color_null, pen=f"1p,{color_SKKS}", label="pierce @@2700 km SKKS null", **args_leg_pp)
    fig.plot(pen=f"1p,{color_ray_KN}", label="ray SKS null", **args_leg_ray)
    fig.plot(pen=f"1p,{color_ray_KKN}", label="ray SKKS null", **args_leg_ray)

elif ray_groups_str =="KNN_KKNN":
    fig.plot(fill=color_SKS, pen=pen_pp, label="pierce @@2700 km SKS split", **args_leg_pp)
    fig.plot(fill=color_SKKS, pen=pen_pp, label="pierce @@2700 km SKKS split", **args_leg_pp)
    fig.plot(pen=f"1p,{color_ray_KNN}", label="ray SKS split", **args_leg_ray)
    fig.plot(pen=f"1p,{color_ray_KKNN}", label="ray SKKS split", **args_leg_ray)

elif ray_groups_str == "KN_KKN_KNN_KKNN":
    color_ray_KNN = color_SKS  # no semi-transparency in legend
    color_ray_KKNN = color_SKKS
    fig.plot(fill=color_SKS, pen=pen_pp, label="pierce @@2700 km SKS", **args_leg_pp)
    fig.plot(fill=color_SKKS, pen=pen_pp, label="pierce @@2700 km SKKS", **args_leg_pp)
    fig.plot(pen=f"1p,{color_ray_KNN}", label="ray SKS", **args_leg_ray)
    fig.plot(pen=f"1p,{color_ray_KKNN}", label="ray SKKS", **args_leg_ray)

if status_lgd == True:
    with gmt.config(FONT="5.5p"):
        if ray_groups_str == "KN_KKN_KNN_KKNN":
            leg_width = 2.8  # centimeters
        else:
            leg_width = 3.2
        fig.legend(box=box_standard, position=f"jCL+o0.2c/-1c+w{leg_width}c")

# %%
# -----------------------------------------------------------------------------
fig.show()
fig_name = f"maps_3d_lmm_bfo_{ray_groups_str}_{fig_name_add}"
# for ext in ["png"]:  # "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=360)
print(fig_name)
