# #############################################################################
# Global seismicity
# - Create geographic map with coding for
#   - color (hypocentral depth)
#   - size (moment magitude)
# For making a gif: https://ezgif.com/maker
# -----------------------------------------------------------------------------
# History
# - Created: 2025/01/26
# - Updated: 2025/07/23
# -----------------------------------------------------------------------------
# Versions
#   PyGMT v0.16.0 -> https://www.pygmt.org/v0.16.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
import pygmt
import pandas as pd


# %%
# -----------------------------------------------------------------------------
# Set up
# -----------------------------------------------------------------------------
# >>> Choose for your needs <<<

# Set projection of map
status_projection = "epi"  ## "rob" | "epi" | "ortho"

# Use color- and size-coding for hypocentral depth and moment magnitude, respectively
status_color = "CMAP"  ## "MONO" | "CMAP"

# Mark specific epicentral distance rage for XKS phases
status_phase = "YES"  ## "YES", "NO"
if status_projection != "epi":
    status_phase = "NO"


#%%
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
color_highlight = "255/90/0"
color_sta = "gold"
color_land = "gray90"
color_water = "white"
color_pb = "216.750/82.875/24.990"
color_sl = "gray60"

box_standard = "+gwhite@30+p0.8p,gray50+r2p"
clearance_standard = "0.1c/0.1c+tO"

# File names
file_pb = "plate_boundaries_Bird_2003.txt"
file_legend = "legend_gmt_magitude.txt"

# -----------------------------------------------------------------------------
# Projections

# Recording stations -> Upper Rhine Graben area as center
sta_name = ["WLS", "ECH", "STU", "BFO", "TMO07", "TMO44"]
sta_lat = np.array([48.413, 48.216, 48.771, 48.331, 49.020, 48.989])
sta_lon = np.array([7.354, 7.159, 9.194, 8.330, 8.367, 8.492])
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

match status_projection:
    case "rob":
        proj_used = f"N{fig_size}c"
        frame_used = ["WSne", "xa60f30g", "ya30fg"]
    case "epi":
        proj_used = f"E{lon_center}/{lat_center}/{epi_dist}/{fig_size}c"
        frame_used = "af"
    case "ortho":
        proj_used = f"G{lon0}/{lat0}/{fig_size}c"
        frame_used = "afg"


# %%
# -----------------------------------------------------------------------------
# Load earthquake data
# -----------------------------------------------------------------------------
start_date = "1991-01-01"
end_date = "2019-12-31"
min_mag_w = 6
max_mag_w = 10

eq_catalog_name = f"global_seismicity_{start_date}to{end_date}_mw{min_mag_w}to{max_mag_w}"
data_eq_raw = pd.read_csv(f"{path_in}/data_{eq_catalog_name}.csv", sep="\t")

# Filter data
# mw, mwc, mwb, mwr, mww
data_eq_used = data_eq_raw[data_eq_raw["magType"].str.contains("mw")]

# Sort descending by magnitude to avoid overplotting
data_eq_used = data_eq_used.sort_values(by=["mag"], ascending=False)

# Scale hypocentral depth for size-coding
# >>> If you change the scaling you also have to update the legend file <<<
data_eq_used["mag_scaled"] = np.exp(data_eq_used["mag"] / 1.7) * 0.0035


# %%
# -----------------------------------------------------------------------------
# Create geographic map
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(projection=proj_used, region="d", frame=0)

# -----------------------------------------------------------------------------
# Plot shorelines, color land and water masses
fig.coast(shorelines=f"1/0.01p,{color_sl}", land=color_land, water=color_water)

# Plot plate boundaries
fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.8p,{color_pb}")

# -----------------------------------------------------------------------------
# Color epicentral distance range for XKS phases
if status_projection == "epi" and status_phase == "YES":
    fig.plot(
        style=f"w{dist_min * size2dist}/0/360+i{dist_max* size2dist}",
        fill=f"{color_highlight}@90",
        **center_coord,
    )

# -----------------------------------------------------------------------------
# Make colormap for hypocentral depth
pygmt.makecpt(cmap="lajolla", series=[0, 500, 1])

# Plot epicenters
epi_columns = ["longitude", "latitude", "depth", "mag_scaled"]

match status_color:
    case "MONO":
        fig.plot(
            data=data_eq_used[epi_columns],
            style="a0.15c",
            fill="darkred",
        )
    case "CMAP":
        fig.plot(
            data=data_eq_used[epi_columns],
            style="cc",
            cmap=True,
            pen="0.3p,gray30",
        )

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
if status_projection == "epi":
    # Plot recording stations
    fig.plot(style="i0.4c", fill=color_sta, pen="0.8p,black", **center_coord)
    fig.text(
        text=center_text,
        offset="0c/0.4c",
        fill="white@30",
        pen=f"0.8p,{color_highlight}",
        clearance=clearance_standard,
        font=f"8p,1,{color_highlight}",
        **center_coord,
    )
    if status_phase == "YES":
        # Mark epicentral distance range for XKS phases
        for epi_lim in [dist_min, dist_max]:
            fig.plot(
                style=f"E-{epi_lim*2}+d",
                pen=f"1p,{color_highlight},-",
                **center_coord,
            )

        # Label epicentral distance range for XKS phases
        for epi_lim in [dist_min, dist_max]:
            fig.text(
                text=f"{epi_lim}@.",
                offset=f"0c/-{epi_lim * size2dist / 2}c",
                fill="white@30",
                pen=f"0.3p,{color_highlight}",
                clearance=clearance_standard,
                no_clip=True,
                **center_coord,
            )

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = f"map_{status_projection}_{eq_catalog_name}_color{status_color}_rangemarked{status_phase}"
# for ext in ["png"]:  # "pdf", "eps"
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
