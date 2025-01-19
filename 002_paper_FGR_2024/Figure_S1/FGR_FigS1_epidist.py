# Fig. S1

import glob
import os

import numpy as np
import pandas as pd
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
orientation = "vertical"  ## "vertical", "horizontal"
dpi_png = 360
font_label = "9p,Helvetica-Bold"
rad_tot = 5.7  # radius

path_in = "01_in_data/"
path_out = "02_out_figs/"

# Epicenters
file_sta_in = f"{path_in}stations_info.txt"

# Plate boundaries; Bird 2003
file_plate_in = f"{path_in}plate_boundaries_Bird_2003.txt"

# Recording stations
sta_all = "BFO", "WLS", "STU", "ECH", "TMO44", "TMO07"

# -----------------------------------------------------------------------------
# Colors
color_land = "lightgray"
color_station_marker = "255/215/0"  # "gold"
color_station_lable = "255/90/0"  # -> orange | URG paper
color_platebound = "216.750/82.875/24.990"

# -----------------------------------------------------------------------------
# Box for
# legend
box_standard = "+gwhite@30+p0.8p,black+r1p"
# text
clearance_standard = "0.1c/0.1c+tO"

# -----------------------------------------------------------------------------
# Colormaps
# Hypocentral depth colored

hypodepth_max = 700  # hypocentral depth maximum, in km
pen_epi = "0.01,gray65"
cb_epi_e = ""

cmap_hypo_in = "lajolla"
cmap_hypo_out = f"{path_in}{cmap_hypo_in}_resampled_hypo.cpt"
gmt.makecpt(
    cmap=cmap_hypo_in,
    output=cmap_hypo_out,
    series=[0, hypodepth_max, 23], # 30 colors for [0,700] km see SplitLab
    # reverse=True,
)
cmap_hypo_in_cut = cmap_hypo_out
cmap_hypo_out_cut = f"{path_in}{cmap_hypo_in}_resampled_cut_hypo.cpt"
gmt.makecpt(
    cmap=cmap_hypo_in_cut,
    output=cmap_hypo_out_cut,
    truncate="92/598",
    # SplitLab (5:27) -> 4*23,26*23
    # this is done before any other operation therefore two-times makecpt
    series=[0, hypodepth_max],  # 10
)
cmap_hypo = cmap_hypo_out_cut
# ..............................................................................
hypodepth_max = 500
pen_epi = "0.01,gray20"
cb_epi_e = "+ef0.15c"

cmap_hypo_in = "lajolla"
gmt.makecpt(
    cmap=cmap_hypo_in,
    output=cmap_hypo_out,
    series=[0, hypodepth_max],
    reverse=True,
)
cmap_hypo = cmap_hypo_out

# -----------------------------------------------------------------------------
# Dictonaries for recording stations
dict_net = {}
dict_lat = {}
dict_lon = {}

station_file = open(file_sta_in,"r")
lines = station_file.readlines()
for line in lines[2:]:  # skip header line(s)
   (net, key, lat, lon, file, label, qstereo, sty, off01, off02, col, rand) = line.split()
   dict_net[key] = net
   dict_lat[key] = float(lat)
   dict_lon[key] = float(lon)
station_file.close()


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------

if orientation=="horizontal":
    nrows_use = 2
    ncols_use = 3
elif orientation=="vertical":
    nrows_use = 3
    ncols_use = 2

# -----------------------------------------------------------------------------
fig = gmt.Figure()

gmt.config(
    FONT_LABEL="10p",  # font size label colorbar
    FONT_ANNOT_PRIMARY="10p",  # font size annotation colorbar
    MAP_FRAME_PEN="0.8p",  # thickness of border around scale
)

# -----------------------------------------------------------------------------
with fig.subplot(
        nrows=nrows_use,
        ncols=ncols_use,
        subsize=(rad_tot,rad_tot),
        frame="lrtb",
        autolabel="(a)",
):

# -----------------------------------------------------------------------------
    for sta in range(6):
        with fig.set_panel(panel=sta):  # Set panel corresponding to station

# -----------------------------------------------------------------------------
            # Make azimuthal equistant plots / projection direct in GMT
            # azimuthal equidistant projection
            # - elon0/lat0[/horizon]/scale
            # - Elon0/lat0[/horizon]/width
            # - horizon max. distance to the projection center
            #   i.e. the visible portion of the rest of the world map
            #   in degrees <= 180° (default 180°)
            fig.coast(
                region="d",
                projection=f"E{dict_lon[sta_all[sta]]}/{dict_lat[sta_all[sta]]}/170/?",
                # projection="N?",
                area_thresh="50000",
                resolution="c",
                shorelines="1/0.1p,darkgray",
                land=color_land,
                water="white",
                frame="f",
            )

# -----------------------------------------------------------------------------
            # Plot plate boundaries
            fig.plot(data=file_plate_in, pen=f"0.5p,{color_platebound}")

# -----------------------------------------------------------------------------
            # Highlight Epicentral distance range used in this study
            epi_min = 90
            epi_max = 150

            # circles
            fig.plot(
                x=dict_lon[sta_all[sta]],
                y=dict_lat[sta_all[sta]],
                style=f"E-{epi_min*2}+d",  # 2 x 90 deg
                pen="1p,gray50,-",
            )
            fig.plot(
                x=dict_lon[sta_all[sta]],
                y=dict_lat[sta_all[sta]],
                style=f"E-{epi_max*2}+d",  # 2 x 150 deg
                pen="1p,gray50,-",
            )

            # Add label for annotations limits of epicentral distance range
            fig.text(
                x=dict_lon[sta_all[sta]],
                y=-28,
                text=f"{epi_min}@.",
                font="9p,black",
            )
            fig.text(
                x=dict_lon[sta_all[sta]],
                y=-88,
                text=f"{epi_max}@.",
                font="9p,black",
            )

# -----------------------------------------------------------------------------
            # Plot epicenters
            file_epi_in = f"{path_in}{sta_all[sta]}_epi_swsm_all.txt"
            df_epi_raw = pd.read_csv(
                file_epi_in,
                delimiter=" ",
                names=["longitude", "latitude", "magnitude", "hdepth"],
            )
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
            # Plot recording station
            # marker
            fig.plot(
                x=dict_lon[sta_all[sta]],
                y=dict_lat[sta_all[sta]],
                style="i0.4",
                fill=color_station_marker,
                pen="0.6p,black"
            )
            # lable
            fig.text(
                x=dict_lon[sta_all[sta]],
                y=dict_lat[sta_all[sta]],
                text=sta_all[sta],
                offset="0c/-0.55c",
                font=f"{font_label},{color_station_lable}",
                fill="white@30",
                pen=f"0.8p,{color_station_lable}",
                clearance=clearance_standard,
            )

# -----------------------------------------------------------------------------
# Add colorbar for hypocentral depth
fig.colorbar(
    cmap=cmap_hypo,
    position=f"JBR+jBR+w4.5c/0.3+o0.7c/-1c+h+ml{cb_epi_e}",
    frame="xa100f50+lhypocentral depth / km",
)

# -----------------------------------------------------------------------------
# Add legend for moment magnitude
leg_mag_file = "legend_gmt_magitude.txt"
fig.legend(
    spec=f"{path_in}{leg_mag_file}",
    position="JBL+jBL+w4.5c+o0.6c/-1.2c",
    box=box_standard,
)

# -----------------------------------------------------------------------------
# Show and save the figure
fig.show()

fig_name = f"{path_out}/paperURG_SWS_epi_ALL_{orientation}"
# for ext in ["png", "pdf", "eps"]:
#     fig.savefig(fname=f"{fig_name}.{ext}")

print(fig_name)