# #############################################################################
# Global seismicity based on the USGS FDSN catalog
# - Create geographic map with
#   - color-coding for the hypocentral depth
#   - size-coding for the moment magnitude
# For making a GIF: https://ezgif.com/maker
# -----------------------------------------------------------------------------
# History
# - Created: 2025/01/26
# - Updated: 2025/07/23
# - Updated: 2025/09/07 - Improve code style and comments
# - Updated: 2026/02/20 - Improve Robinson projection, include elevation grid
# -----------------------------------------------------------------------------
# Versions
#   PyGMT v0.16.0 - v0.18.0 -> https://www.pygmt.org
#   GMT 6.5.0 - 6.6.0 -> https://www.generic-mapping-tools.org
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
import pandas as pd
import pygmt

# %%
# -----------------------------------------------------------------------------
# Set up
# -----------------------------------------------------------------------------
# >>> Choose for your needs <<<

# Set projection of map (Robinson, epicentral, orthographic)
status_projection = "epi"  ## "robg" | "robd" | "epi" | "ortho"

# Use color- and size-coding for hypocentral depth or moment magnitude, respectively
status_color = "MONO"  ## "MONO" | "CMAP"

# Color land and water or add elevation grid
status_bg = "plain"  ## "plain" | "elevation"

# Mark specific epicentral distance rage for XKS phases
status_phase = "YES"  ## "YES" | "NO"
if status_projection != "epi":
    status_phase = "NO"


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# >>> Adjust for your needs <<<
path_in = "01_in_data"
path_out = "02_out_figs"

fig_size = 11  # in centimeters
dpi_png = 360

# -----------------------------------------------------------------------------
# Plotting
color_hl = "255/90/0"  # highlight -> orange
color_sta = "gold"
color_land = "gray90"
color_water = "white"
color_pb = "216.750/82.875/24.990"  # plate boundaries after Bird 2003
color_sl = "gray60"  # shorelines

box_standard = "+gwhite@30+p0.8p,gray50+r2p"
clearance_standard = "0.1c+tO"

# File names
file_pb = "plate_boundaries_Bird_2003.txt"
file_legend = "legend_gmt_magitude.txt"

# -----------------------------------------------------------------------------
# Projections

# Recording stations -> Upper Rhine Graben area as center
sta_name = ["WLS", "ECH", "STU", "BFO", "TMO07", "TMO44"]
sta_lon = np.array([7.354, 7.159, 9.194, 8.330, 8.367, 8.492])
sta_lat = np.array([48.413, 48.216, 48.771, 48.331, 49.020, 48.989])
mean_lon = np.mean(sta_lon)
mean_lat = np.mean(sta_lat)

# Epicentral distance
epi_dist = 160  # degrees
dist_min = 90
dist_max = 150
size2dist = fig_size / epi_dist

lon_center = mean_lon  # degrees East
lat_center = mean_lat  # degrees North
center_coord = {"x": lon_center, "y": lat_center}
center_text = "URG"

# Orthographic
lon0 = 60  # degrees East
lat0 = 10  # degrees North

region = "d"
match status_projection:
    case "robg" | "robd":
        proj_used = f"N{fig_size}c"
        frame_used = ["WSne", "xa60f30g", "ya30fg"]
        if status_projection == "robd":
            region = "d"
    case "epi":
        proj_used = f"E{lon_center}/{lat_center}/{epi_dist}/{fig_size}c"
        frame_used = "af"
    case "ortho":
        proj_used = f"G{lon0}/{lat0}/{fig_size}c"
        frame_used = "afg10"


# %%
# -----------------------------------------------------------------------------
# Load earthquake data
# -----------------------------------------------------------------------------
start_date = "1991-01-01"
end_date = "2019-12-31"
min_mag_w = 6
max_mag_w = 10

eq_catalog_name = "usgsfdsn_" + "".join(str(start_date).split("-")) + "to" + \
    "".join(str(end_date).split("-")) + f"_mw{min_mag_w}to{max_mag_w}"

df_eq_raw = pd.read_csv(f"{path_in}/catalog_{eq_catalog_name}.csv", sep="\t")

# Filter data
# mw, mwc, mwb, mwr, mww
df_eq = df_eq_raw[df_eq_raw["magType"].str.contains("mw")]

# Sort descending by magnitude to avoid overplotting
df_eq = df_eq.sort_values(by=["mag"], ascending=False)

# Scale hypocentral depth for size-coding
# >>> If you change the scaling you also have to update the legend file <<<
df_eq["mag_scaled"] = np.exp(df_eq["mag"] / 1.7) * 0.0035

# Filter dataset to keep columns needed for color- and size-coding
epi_columns = ["longitude", "latitude", "depth", "mag_scaled"]
df_eq_used = df_eq[epi_columns]


# %%
# -----------------------------------------------------------------------------
# Loops for animations
# -----------------------------------------------------------------------------
# Uncomment and inset the rest of the code

# -----------------------------------------------------------------------------
# Over time

# Add separate year column
# years = []
# for i_eq in df_eq.index:
#     year_temp = int(df_eq["time"][i_eq][0:4])
#     years.append(year_temp)
# df_eq["year"] = years

# year_step = 1
# for year in range(1991, 2019 + year_step, year_step):

#     df_eq_years = df_eq[df_eq["year"] < year + year_step]
#     df_eq_used = df_eq_years[epi_columns]

# -----------------------------------------------------------------------------
# Over Longitude (only meaningful for orthographic projection)

# lon_step = 10
# for lon0 in range(0, 360 + lon_step, lon_step):

#     proj_used = f"G{lon0}/{lat0}/{fig_size}c"


# %%
# -----------------------------------------------------------------------------
# Create geographic map
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(projection=proj_used, region=region, frame=0)

# Plot shorelines, color land and water masses OR elevation grid
match status_bg:
    case "plain":
        fig.coast(shorelines=f"1/0.01p,{color_sl}", land=color_land, water=color_water)
    case "elevation":
        fig.grdimage("@earth_relief", cmap="oleron")

# Plot plate boundaries
fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.8p,{color_pb}")

# -----------------------------------------------------------------------------
# Color epicentral distance range for XKS phases
if status_projection == "epi" and status_phase == "YES":
    fig.plot(
        style=f"w{dist_min * size2dist}/0/360+i{dist_max * size2dist}",
        fill=f"{color_hl}@90",
        **center_coord,
    )

# -----------------------------------------------------------------------------
if status_projection == "epi":
    # Plot recording stations
    fig.plot(style="i0.4c", fill=color_sta, pen="0.8p,black", **center_coord)
    fig.text(
        text=center_text,
        offset="0c/0.4c",
        fill="white@30",
        pen=f"0.8p,{color_hl}",
        clearance=clearance_standard,
        font=f"8p,1,{color_hl}",
        **center_coord,
    )
    if status_phase == "YES":
        # Mark epicentral distance range for XKS phases
        for epi_lim in [dist_min, dist_max]:
            fig.plot(style=f"E-{epi_lim * 2}+d", pen=f"1p,{color_hl},-", **center_coord)

        # Label epicentral distance range for XKS phases
        for epi_lim in [dist_min, dist_max]:
            fig.text(
                text=f"{epi_lim}@.",
                offset=f"0c/-{epi_lim * size2dist / 2}c",
                fill="white@30",
                pen=f"0.3p,{color_hl}",
                clearance=clearance_standard,
                no_clip=True,
                **center_coord,
            )

# -----------------------------------------------------------------------------
# Make colormap for hypocentral depth
pygmt.makecpt(cmap="lajolla", series=[0, 500, 1])

# Plot epicenters
match status_color:
    case "MONO":
        fig.plot(data=df_eq_used, style="a0.15c", fill="darkred")
    case "CMAP":
        fig.plot(data=df_eq_used, style="cc", cmap=True, pen="0.3p,gray30")

        # Add colorbar for hypocentral depth color-coding
        with pygmt.config(FONT="14p"):
            fig.colorbar(
                frame=["xa100+lhypocentral depth", "y+lkm"],
                position="JBC+o-2.5c/1.1c+w5c/0.3c+h+ml+ef0.2c",
                box=box_standard,
            )

        # Add legend for magnitude size-coding
        fig.legend(
            spec=f"{path_in}/{file_legend}",
            position="JBC+o3c/1.2c+w4c",
            box=box_standard,
        )

        # Add label for time period
        fig.text(
            text=f"{start_date} to {end_date}",
            font="black",
            position="BR",
            offset="-0.6c/-1c",
            pen="0.8p,gray50",
            clearance=clearance_standard,
            no_clip=True,
        )

# -----------------------------------------------------------------------------
# Plot map frame on top
with pygmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray70"):
    fig.basemap(frame=frame_used)

# -----------------------------------------------------------------------------
# Time label for animation over time
# match status_color:
#     case "MONO":
#         offet = "0.3c"
#         if status_projection in ["robg", "robd"]:
#             offset = "-0.6c/-0.3c"
#         fig.text(
#             text=f"1991 - {year}",
#             font=f"10p,1,{color_hl}",
#             position="LB",
#             offset=offset,
#             no_clip=True,
#         )
#     case "CMAP":
#         fig.text(
#             text=f"1991 - {year}",
#             font=f"10p,1,{color_hl}",
#             position="BR",
#             offset="-1.6c/-0.95c",
#             pen="0.8p,gray50",
#             clearance=clearance_standard,
#             no_clip=True,
#         )

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = f"map_{eq_catalog_name}_{status_projection}_color{status_color}_" + \
            f"rangemarked{status_phase}"
# Names for single images of animations
# fig_name = f"map_{eq_catalog_name}_{status_projection}_color{status_color}_" + \
#             f"rangemarked{status_phase}_1991to{year}"
# fig_name = f"map_{eq_catalog_name}_{status_projection}_color{status_color}_" + \
#             f"rangemarked{status_phase}_lon{lon0}deg_elevation"

# for ext in ["png"]:  # "pdf", "eps"
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
