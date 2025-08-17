# #############################################################################
# Fröhlich et al. (2024), GJI: Fig. S1
# Earthquake distribution around the Upper Rhine Graben area as epicentral distance plot
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


import numpy as np
import pandas as pd
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
orientation = "vertical"  ## "vertical" | "horizontal"
dpi_png = 360
font_label = "9p,Helvetica-Bold"
rad_tot = 5.7  # radius

path_in = "01_in_data"
path_out = "02_out_figs"

# Recording stations
file_sta_in = "stations_info.txt"
# Plate boundaries; Bird 2003
file_plate_in = "plate_boundaries_Bird_2003.txt"
# Legend for moment magnitude
leg_mag_file = "legend_gmt_magitude.txt"

# Recording stations
sta_all = ["BFO", "WLS", "STU", "ECH", "TMO44", "TMO07"]

# -----------------------------------------------------------------------------
# Colors
color_land = "gray90"
color_water = "white"
color_sl = "gray70"
color_sta = "gold"
color_hl = "255/90/0"  # -> orange | URG paper
color_pb = "216.750/82.875/24.990"  # -> darkorange

# -----------------------------------------------------------------------------
cmap_hypo_in = "lajolla"
hd_max = 500  # hypocentral depth

box_standard = "+gwhite@30+p0.8p,black+r1p"
clearance_standard = "0.1c/0.1c+tO"

if orientation=="horizontal":
    nrows_use = 2
    ncols_use = 3
elif orientation=="vertical":
    nrows_use = 3
    ncols_use = 2

# -----------------------------------------------------------------------------
# Dictionaries for recording stations
dict_net = {}
dict_lat = {}
dict_lon = {}

station_file = open(f"{path_in}/{file_sta_in}", "r")
lines = station_file.readlines()
for line in lines[1:]:  # skip header line(s)
   (net, key, lon, lat) = line.split()
   dict_net[key] = net
   dict_lon[key] = float(lon)
   dict_lat[key] = float(lat)
station_file.close()



# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------
fig = gmt.Figure()

gmt.makecpt(cmap=cmap_hypo_in, series=[0, hd_max])

with fig.subplot(
        nrows=nrows_use,
        ncols=ncols_use,
        subsize=(rad_tot, rad_tot),
        frame="lrtb",
        autolabel="(a)",
):

# -----------------------------------------------------------------------------
    for i_sta, sta in enumerate(sta_all):
        center_coord = {"x": dict_lon[sta], "y": dict_lat[sta]}

        file_epi_in = f"{path_in}/{sta}_epi_swsm_all.txt"
        df_epi_raw = pd.read_csv(file_epi_in, delimiter="\t", header=1)
        df_epi = df_epi_raw
        df_epi.moment_magnitude = np.exp(df_epi_raw.moment_magnitude / 1.7) * 0.0035

# -----------------------------------------------------------------------------
        with fig.set_panel(i_sta):  # Set panel corresponding to station
            # Make azimuthal equistant plots / projection direct in GMT
            # azimuthal equidistant projection
            # - elon0/lat0[/horizon]/scale
            # - Elon0/lat0[/horizon]/width
            # - horizon max. distance to the projection center
            #   i.e. the visible portion of the rest of the world map
            #   in degrees <= 180 deg (default 180 deg)
            projection = f"E{dict_lon[sta]}/{dict_lat[sta]}/170/?"
            fig.basemap(region="d", projection=projection, frame=0)

            fig.coast(
                area_thresh="50000",
                resolution="c",
                shorelines="1/0.1p,{color_sl}",
                land=color_land,
                water=color_water,
            )

            # Plot plate boundaries
            fig.plot(data=f"{path_in}/{file_plate_in}", pen=f"0.5p,{color_pb}")

# -----------------------------------------------------------------------------
            # Highlighte epicentral distance range used in this study
            for epi_dist, y in zip([90, 150], [-28, -88]):
                # Plot circles
                fig.plot(style=f"E-{epi_dist * 2}+d", pen="1p,gray50,4_2", **center_coord)
                # Add label for annotations limits of epicentral distance range
                fig.text(x=center_coord["x"], y=y, text=f"{epi_dist}@.", font="9p,black")

# -----------------------------------------------------------------------------
            # Plot epicenters
            fig.plot(
                x=df_epi.longitude,
                y=df_epi.latitude,
                size=df_epi.moment_magnitude,
                fill=df_epi.hypocentral_depth_km,
                style="c",
                cmap=True,
                pen="0.01,gray20",
            )

# -----------------------------------------------------------------------------
            # Plot recording station
            # marker
            fig.plot(style="i0.4", fill=color_sta, pen="0.6p,black", **center_coord)
            # label
            fig.text(
                text=sta,
                offset="0c/-0.55c",
                font=f"{font_label},{color_hl}",
                fill="white@30",
                pen=f"0.8p,{color_hl}",
                clearance=clearance_standard,
                **center_coord,
            )

# -----------------------------------------------------------------------------
# Add colorbar for hypocentral depth
with gmt.config(FONT="15p"):
    fig.colorbar(
        position="JBR+jBR+w4.5c/0.3+o0.7c/-1c+h+ml+ef0.15c",
        frame="xa100f50+lhypocentral depth / km",
    )

# Add legend for moment magnitude
fig.legend(
    spec=f"{path_in}/{leg_mag_file}",
    position="JBL+jBL+w4.5c+o0.6c/-1.2c",
    box=box_standard,
)

# -----------------------------------------------------------------------------
# Show and save the figure
fig.show()
fig_name = f"FGR2024_GJI_FigS1_{orientation}"
# for ext in ["png"]:  #, "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
