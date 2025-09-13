# #############################################################################
# Harvard CMT catalog
# - Create epidistance map with
#   - beachballs for epicenters
#   - color-coding for different quantities
#   - size for moment magnitude
# - Single and combined figures are generated
# - Data are from the earthquake catalog provided along with the MATLAB package
#   SplitLab (Wüstefeld et al. 2008) exported as CSV file
#   See https://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/COMBO/combo.ndk
#   last accessed 2025/09/08
# >>> Just play around with the data <<<
# -----------------------------------------------------------------------------
# History
# - Created: 2025/09/08
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
# Adjust for your needs
# -----------------------------------------------------------------------------
# Use another quantity for color-coding as the hypocentral depth
# Figure.meca always uses the "depth" column for color-coding
# "depth" | "dis" | "magnitude" | "strike" | "dip" | "rake"
# "fault" | "xks"
status_color = "fault"

# Time window
year_min = 2020  # since 1976
year_max = 2025  # until 2025

# Moment magnitude
min_plot_mag = 6
max_plot_mag = 10
min_cmap_mag = min_plot_mag
max_cmap_mag = max_plot_mag
step_mag = 0.1

if status_color == "xks":
    min_plot_mag = 6  # Needed to observe a clear waveform
    max_plot_mag = 10

# Interval considered for the rake to classify the fault types; -/+ around the rake value
rake_intval = 10  # degrees

# Maximum epicentral distance of the map (i.e, radius)
epi_dist = 180  # degrees

# Resolution of output PNG
dpi_png = 360  #dpi

# Path
path_in = "01_in_data"
path_out = "02_out_figs"


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Colors
color_hl = "255/90/0"  # highlight -> orange
color_sta = "gold"  # recording station
color_land = "gray95"
color_water = "white"
color_pb = "216.750/82.875/24.990"  # plate boundaries after Bird 2003
color_sl = "gray60"  # shorelines

color_meca = "gray85"
color_ssl = "steelblue"  # strike-slip left
color_ssr = "purple"  # strike-slip right
color_dsn = "orange"  # dip-slip normal
color_dsr = "brown"  # dip-slip reverse

clearance_standard = "0.1c+tO"
x_shift = 0.5
y_shift = 1.3

# Center, here the Black Forest Observatory
lon_center = 8.330  # degrees East
lat_center = 48.331  # degrees North
center_coord = {"x": lon_center, "y": lat_center}
center_text = "BFO"

# Epidistance projection
fig_size = 12  # in centimeters
dist_step = 30  # in degrees
size2dist = fig_size / epi_dist
projection = f"E{lon_center}/{lat_center}/{epi_dist}/{fig_size}c"
dist_min = 90  # for XKS phases
dist_max = 150

# Input files
file_pb = "plate_boundaries_Bird_2003.txt"

# Colormaps
match status_color:
    case "depth":
        cmap = "lajolla"
        cmap_min = 0
        cmap_max = 100
        cmap_label = ["x+lhypocentral depth", "y+lkm"]
    case "dis":
        cmap = "lajolla"
        cmap_min = 0
        cmap_max = 180
        cmap_label = ["x+lepicentral distance", "y+ldeg"]
    case "magnitude":
        cmap = "hawaii"
        cmap_min = min_cmap_mag
        cmap_max = max_cmap_mag
        cmap_label = ["x+lmoment magnitude"]
    case "strike":
        cmap = "romaO"
        cmap_min = 0
        cmap_max = 360
        cmap_label = ["x+lstrike", "y+ldeg"]
    case "dip":
        cmap = "navia"
        cmap_min = 0
        cmap_max = 90
        cmap_label = ["x+ldip", "y+ldeg"]
    case "rake":
        cmap = "romaO"
        cmap_min = -180
        cmap_max = 180
        cmap_label = ["x+lrake", "y+ldeg"]


# %%
# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
df_eq_raw = pd.read_csv(f"{path_in}/harvardCMT.csv", sep=",")

# Keep only relevant columns without depth
columns = [
    "year", "month", "day", "hour", "minute", "second", "jday", "dstr",
    "latitude", "longitude", "azi", "bazi", "dis",
    "magnitude", "M0", "strike", "dip", "rake", "region",
]
df_eq_mod = df_eq_raw[columns]

# Quantity used for color-coding by Figure.meca has to be in the "depth" column
quantity_for_color = status_color
if status_color in ["fault", "xks"]:
    quantity_for_color = "depth"
df_eq_mod["depth"] = df_eq_raw[quantity_for_color]
df_eq_mod["depth_km"] = df_eq_raw["depth"]  # hypocentral depth

df_eq = df_eq_mod
# Sort descending by magnitude to avoid overplotting
df_eq = df_eq.sort_values(by=["magnitude"], ascending=False)

# Subset based on year
df_eq_temp00 = df_eq[df_eq["year"] >= year_min]
df_eq_temp01 = df_eq_temp00[df_eq_temp00["year"] <= year_max]

# Subset based on moment magnitude
df_eq_temp02 = df_eq_temp01[df_eq_temp01["magnitude"] >= min_plot_mag]
df_eq_temp03 = df_eq_temp02[df_eq_temp02["magnitude"] <= max_plot_mag]
# Scale moment magnitude for plotting
df_eq_temp03["magnitude"] = np.exp(df_eq_temp03["magnitude"] / 1.7) * 0.0035

fig_name_basic = f"map_harvardcmt_{year_min}to{year_max}_" + \
                    f"mw{min_plot_mag}to{max_plot_mag}_beachball_"


# %%
# -----------------------------------------------------------------------------
# Make epicentral distance map
# -----------------------------------------------------------------------------

fig_merge = gmt.Figure()

for depth_min, depth_max in zip([0, 10, 20, 30, 50, 100], [10, 20, 30, 50, 100, 600]):

    # Subset based on hypocentral depth
    df_eq_used = []
    df_eq_temp04 = df_eq_temp03[df_eq_temp03["depth_km"] >= depth_min]
    df_eq_used = df_eq_temp04[df_eq_temp04["depth_km"] < depth_max]

    # Subsets based on
    if len(df_eq_used) > 0:
        match status_color:
            # rake
            case "fault":
                # strike-slip left
                df_eq_ssl_temp = df_eq_used[df_eq_used["rake"] >= 0 - rake_intval]
                if len(df_eq_ssl_temp) > 0:
                    df_eq_ssl = df_eq_ssl_temp[df_eq_ssl_temp["rake"] <= 0 + rake_intval]
                # strike-slip right
                df_eq_ssr_01 = df_eq_used[df_eq_used["rake"] >= 180 - rake_intval]
                df_eq_ssr_02 = df_eq_used[df_eq_used["rake"] <= -180 + rake_intval]
                # dip-slip normal
                df_eq_dsn_temp = df_eq_used[df_eq_used["rake"] <= -90 + rake_intval]
                if len(df_eq_dsn_temp) > 0:
                    df_eq_dsn = df_eq_dsn_temp[df_eq_dsn_temp["rake"] >= -90 - rake_intval]
                # dip-slip reverse
                df_eq_dsr_temp = df_eq_used[df_eq_used["rake"] >= 90 - rake_intval]
                if len(df_eq_dsr_temp) > 0:
                    df_eq_dsr = df_eq_dsr_temp[df_eq_dsr_temp["rake"] <= 90 + rake_intval]
            # epicentral distance
            case "xks":
                df_eq_close = df_eq_used[df_eq_used["dis"] < dist_min]
                df_eq_far = df_eq_used[df_eq_used["dis"] > dist_max]
                df_eq_xks_temp = df_eq_used[df_eq_used["dis"] >= dist_min]
                if len(df_eq_xks_temp) > 0:
                    df_eq_xks = df_eq_xks_temp[df_eq_xks_temp["dis"] <= dist_max]

# -----------------------------------------------------------------------------
    fig_single = gmt.Figure()

    for fig in [fig_single, fig_merge]:

        # Set up basic map
        fig.basemap(region="g", projection=projection, frame=True)
        with gmt.config(FONT="10p", MAP_TITLE_OFFSET="-5p"):
            fig.basemap(
                frame=f"+t{year_min}-{year_max}   "
                f"Mw=[{min_plot_mag},{max_plot_mag}]   "
                f"hd=[{depth_min},{depth_max}[ km   "
                f"{len(df_eq_used)}/{len(df_eq_temp02)} events"
            )

        # Color land and water masses
        fig.coast(land=color_land, water=color_water)
        # Plot shorelines
        fig.coast(shorelines=f"1/0.01p,{color_sl}")
        # Plot plate boundaries
        fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.8p,{color_pb}")

        # Mark epicentral distance
        match status_color:
            case "xks":
                # range for XKS phases
                fig.plot(
                    style=f"w{dist_min * size2dist}/0/360+i{dist_max * size2dist}",
                    fill=f"{color_hl}@90",
                    **center_coord,
                )
                # limits for XKS phases
                for epi_lim in [dist_min, dist_max]:
                    fig.plot(
                        style=f"E-{epi_lim * 2}+d", pen=f"1p,{color_hl},-", **center_coord,
                    )
                    fig.text(
                        text=f"{epi_lim}@.",
                        offset=f"0c/-{epi_lim * size2dist / 2}c",
                        fill="white@30",
                        pen=f"0.3p,{color_hl}",
                        clearance=clearance_standard,
                        no_clip=True,
                        **center_coord,
                    )
            case _:
                # in steps of 30 degrees
                for epi_lim in np.arange(dist_step, epi_dist, dist_step):
                    fig.plot(
                        style=f"E-{epi_lim * 2}+d", pen="0.3p,black,-", **center_coord
                    )
                    fig.text(
                        text=f"{epi_lim}@.",
                        font="6p",
                        offset=f"0c/-{epi_lim * size2dist / 2}c",
                        fill="white@30",
                        pen="0.1p,black",
                        clearance=clearance_standard,
                        no_clip=True,
                        **center_coord,
                    )

        # Plot epicenters as beachballs
        match status_color:
            case "fault":
                for df_eq_fault, color_fault in zip(
                    [df_eq_used, df_eq_ssl, df_eq_ssr_01, df_eq_ssr_02, df_eq_dsn, df_eq_dsr],
                    [color_meca, color_ssl, color_ssr, color_ssr, color_dsn, color_dsr],
                ):
                    if len(df_eq_fault) > 0:
                        fig.meca(
                            spec=df_eq_fault,
                            scale="12c",
                            compressionfill=color_fault,
                            outline="0.3p,gray10",
                        )
            case "xks":
                for df_eq_dist, color_dist in zip(
                    [df_eq_close, df_eq_far, df_eq_xks], [color_meca, color_meca, color_hl]
                ):
                    if len(df_eq_dist) > 0:
                        fig.meca(
                            spec=df_eq_dist,
                            scale="12c",
                            compressionfill=color_dist,
                            outline="0.3p,gray10",
                        )
            case _:
                gmt.makecpt(cmap=cmap, series=[cmap_min, cmap_max])
                if len(df_eq_used) > 0:
                    fig.meca(
                        spec=df_eq_used, scale="12c", cmap=True, outline="0.3p,gray10"
                    )
                with gmt.config(FONT="15p"):
                    if fig == fig_single:
                        fig_single.colorbar(frame=cmap_label, position="+o0c/0.8c+e0.25c+ml")
                    # Add colorbar only once for merge figure
                    if fig == fig_merge and depth_min == 50:
                        fig_merge.colorbar(frame=cmap_label, position="+e0.25c+ml")

        # Mark center of the map as recording station
        fig.plot(style="i0.4c", fill=color_sta, pen="0.5p,black", **center_coord)
        fig.text(
            text=center_text,
            offset="0c/0.4c",
            fill="white@30",
            pen=f"0.8p,{color_hl}",
            clearance=clearance_standard,
            font=f"8p,1,{color_hl}",
            **center_coord,
        )

        # Frame on top
        fig.basemap(frame=True)

# -----------------------------------------------------------------------------
        # Show figure
        fig.show()

    # Shift plot origin for merge plot
    fig_merge.shift_origin(xshift=f"+w{x_shift}c")
    if depth_min == 20:
        fig_merge.shift_origin(
            yshift=f"-h{-y_shift}c", xshift=f"-{(fig_size + x_shift) * 3}c"
        )

    fig_name_add = status_color
    if status_color == "fault":
        fig_name_add = f"{status_color}_rakeD{rake_intval}deg"
    fig_name = f"{fig_name_basic}{fig_name_add}_depth"

    # Save single plot
    for ext in ["png"]:  # "pdf", "eps"
        fig_single.savefig(
            fname=f"{path_out}/{fig_name}{depth_min}to{depth_max}km.{ext}", dpi=dpi_png
        )

# Save merge plot
# for ext in ["png"]:  # "pdf", "eps"
#     fig_merge.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
