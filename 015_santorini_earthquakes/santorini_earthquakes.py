# #############################################################################
# Santorini earthquakes January - March 2025
# - 2-D maps for epicenters with different color-coding per day
# - 3-D plots for hypocenters with different color-coding per day
# - Histogram for earthquakes per day
# - Histograms for magnitude distribution per day
#
# Make GIF, e.g.,
# - https://ezgif.com/pdf-to-gif (last accessed 2025/09/25)
#
# Data taken from
# - Karakostas V, Lomax A, Anagnostou V, Papadimitriou E, Acoccela V, Hicks S
#   (2025). 2025 Santorini-Amorgos NLL-SSST-coherence high-precision relocated
#   earthquake catalog. Zenodo. https://doi.org/10.5281/zenodo.15111649 (v1).
#   https://doi.org/10.5281/zenodo.17668659 (v2).
#
# More information
# - Isken M P, Karstens J, Nomikou P, et al. (2025) Volcanic crisis reveals
#   coupled magma system at Santorini and Kolumbo. Nature, 645:939-945.
#   https://doi.org/10.1038/s41586-025-09525-7.
# - https://www.geomar.de/en/news/article/magmaverlagerung-loeste-zehntausende-erdbeben-aus
#   (last accessed 2025/09/26)
# -----------------------------------------------------------------------------
# History
# - Created: 2025/09/21
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.18.0 -> https://www.pygmt.org/v0.18.0 | https://www.pygmt.org
# - GMT 6.6.0 -> https://www.generic-mapping-tools.org
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import datetime

import numpy as np
import pandas as pd
import pygmt as gmt
from dateutil.rrule import DAILY, rrule

# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Path
path_in = "01_in_data"
path_out = "02_out_figs"

# Time window
start_date_data = datetime.datetime(2025, 1, 1, 0, 0)
start_date_plot = datetime.datetime(2025, 1, 15, 0, 0)
end_date_plot = datetime.datetime(2025, 3, 15, 0, 0)

add_one_day = datetime.timedelta(hours=23, minutes=59, seconds=59)
N_eqs_days = [-1] * (int(str(end_date_plot - start_date_plot).split(" ")[0]) + 1)
x_days = np.arange(1, len(N_eqs_days) + 1, 1)

# Colors
color_sl = "gray10"
color_hl = "255/90/0"  # -> orange
color_water = "gray"
color_land = "tan"

# Plotting region
lon_min = 25.34
lon_max = 25.93
lat_min = 36.35
lat_max = 36.80
region = [lon_min, lon_max, lat_min, lat_max]
region_ele = [21, 29.5, 34.5, 39]
region_surf = [25.251, 26.025, 36.275, 36.875]

# Santorini
args_santo = {"x": 25.43, "y": 36.42, "style": "x0.6c", "pen": f"5p,{color_hl}"}


# %%
# -----------------------------------------------------------------------------
# Prepare data
# -----------------------------------------------------------------------------
# Source:
# v1: https://doi.org/10.5281/zenodo.15111649  (last accessed 2025/09/24)
# v2: https://doi.org/10.5281/zenodo.17668659  (last accessed 2026/01/22)
doi = "17668659"
df_eq_raw = pd.read_csv(f"{path_in}/catalog_santorini_{doi}.csv", sep=",")

# Create column with datetime object
df_eq_raw["date_time"] = [0] * len(df_eq_raw)
for i_event in range(len(df_eq_raw)):
    df_eq_raw["date_time"][i_event] = datetime.datetime(
        df_eq_raw["year"][i_event],
        df_eq_raw["month"][i_event],
        df_eq_raw["day"][i_event],
        df_eq_raw["hour"][i_event],
        df_eq_raw["minute"][i_event],
        # int(np.floor(df_eq_raw["seconds"][i_event])),
    )

df_eq = df_eq_raw[df_eq_raw["date_time"] >= start_date_data]


# %%
# -----------------------------------------------------------------------------
# Create plots for elevation
# -----------------------------------------------------------------------------
# Download elevation grid
grd_ele = gmt.datasets.load_earth_relief(region=region_ele, resolution="15s")
grd_surf = gmt.datasets.load_earth_relief(region=region_surf, resolution="03s")

# -----------------------------------------------------------------------------
# 2-D map
fig_ele = gmt.Figure()
fig_ele.basemap(projection="M12c", region=region_ele, frame=["WSne", "a1f0.5"])

gmt.makecpt(cmap="oleron", series=[-1000, 2000])
fig_ele.grdimage(grid=grd_ele, cmap=True, shading=True)
fig_ele.colorbar(frame=["xa500f100+lelevation", "y+lm"], position="+e0.3c+o0c/1.3c+ml")

# Mark zoom area using in following maps
for data in [
    [[region_surf[0], region_surf[2], region_surf[1], region_surf[3]]],
    [[lon_min, lat_min, lon_max, lat_max]],
]:
    fig_ele.plot(data=data, style="r+s", pen=f"1p,{color_hl}", fill=f"{color_hl}@90")

fig_ele.show()
fig_name = "santorini_map_elevation"
# for ext in ["png"]:  # "pdf", "eps"
#     fig_ele.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)

# -----------------------------------------------------------------------------
# 3-D plot - takes some time
fig_surf = gmt.Figure()
fig_surf.basemap(
    projection="M12c",
    region=region_surf,
    frame=["wSnE", "af", "+e"],
    perspective=[150, 20],
)

gmt.makecpt(cmap="oleron", series=[-1000, 800])
fig_surf.grdview(
    grid=grd_surf,
    cmap=True,
    shading=True,
    perspective=True,
    zsize=1.5,
    surftype="s",
    plane="-1000+ggrey",
    facadepen="gray10",
)
fig_surf.colorbar(frame=["xa500f100+lelevation", "y+lm"], position="+e0.3c+o0c/0.4c+ml")

fig_surf.show()
fig_name = "santorini_surface_elevation"
# for ext in ["png"]:  # "pdf", "eps"
    # fig_surf.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Create plots over time (days)
# -----------------------------------------------------------------------------
# Histograms for magnitude distribution per day
fig_histo = gmt.Figure()
gmt.config(FONT="8p", MAP_TITLE_OFFSET="3p", MAP_GRID_PEN_PRIMARY="0.1p,gray70")
i_histo = 0

# -----------------------------------------------------------------------------
for i_day, day in enumerate(rrule(DAILY, dtstart=start_date_plot, until=end_date_plot)):
    df_eq_cum = df_eq[df_eq["date_time"] < (day + add_one_day)]
    df_eq_day = df_eq_cum[df_eq_cum["date_time"] > day]
    N_eqs_day = len(df_eq_day)
    N_eqs_days[i_day] = N_eqs_day

    print(day)
    # print(day + add_one_day)
    # print(len(df_eq_day))
    # print(len(df_eq_cum))

# -----------------------------------------------------------------------------
    # 2-D maps of epiceneters with different color-codings per day
    fig2d = gmt.Figure()
    gmt.config(MAP_TITLE_OFFSET="-5p")

    # 3-D plots of hypcenters with different color-codings per day
    fig3d = gmt.Figure()
    gmt.config(FONT="20p", MAP_GRID_PEN_PRIMARY="0.1p,gray30")

    for fill_quantity, frame, title, cmap, reverse, series, cb_label in zip(
        ["magnitude", "depth", "date_time"],
        ["WSne", "wSne", "wSne"],
        [
            "Santorini–Amorgos",
            f"@;{color_hl};{N_eqs_day}@;; / {len(df_eq_cum)} earthquakes",
            str(start_date_data).split(" ")[0]
            + f" — @;{color_hl};"
            + str(day).split(" ")[0]
            + "@;;",
        ],
        ["lipari", "lajolla", "hawaii"],
        [True, False, True],
        [[3, 5], [3, 15], [start_date_plot, end_date_plot]],
        ["magnitude", "hypocentral depth / km", "date"],
        strict=False,
    ):
        # Create colormap for epi- or hypocenters
        cmap_fill = f"{path_in}/{cmap}_fill.cpt"
        gmt.makecpt(cmap=cmap, series=series, reverse=reverse, output=cmap_fill)
        cb_x_afg = ""
        if fill_quantity == "date_time":
            cb_x_afg = "xa1O"

        # Vertical axis of 3-D plot
        z_label = " "
        if fill_quantity == "magnitude":
            z_label = "negative depth / km"

# -----------------------------------------------------------------------------
        fig2d.basemap(
            projection="M12c", region=region, frame=["af", f"{frame}+t{title}"]
        )
        fig2d.coast(land=color_land, water=color_water, shorelines=f"1/0.5p,{color_sl}")

        # Mark Santorini
        fig2d.plot(**args_santo)

        # Plot epicenters
        with gmt.config(FONT="15p"):
            fig2d.colorbar(
                frame=f"x{cb_x_afg}+l{cb_label}",
                position="+o0c/1.5c+e0.3c+ml",
                cmap=cmap_fill,
            )
        fig2d.plot(
            x=df_eq_cum.longitude,
            y=df_eq_cum.latitude,
            size=0.1 * df_eq_cum.magnitude,
            fill=df_eq_cum[fill_quantity],
            style="cc",  # 0.07c
            cmap=cmap_fill,
        )

        fig2d.shift_origin(xshift="w+0.5c")

# -----------------------------------------------------------------------------
        # Plot hypocenters
        fig3d.plot3d(
            projection="X15c",
            region=[lon_min, lon_max, lat_min, lat_max, -15, 0],
            frame=[
                f"wSnEZ1+g{color_water}+t{title}",
                "xafg+u° E",
                "yafg+u° N+e",
                f"za1f0.5g0.5+l{z_label}",
            ],
            perspective=[150, 20],
            zscale=2,
            x=df_eq_cum.longitude,
            y=df_eq_cum.latitude,
            z=-1 * df_eq_cum.depth,
            size=0.1 * df_eq_cum.magnitude,
            fill=df_eq_cum[fill_quantity],
            style="uc",
            cmap=cmap_fill,
        )
        fig3d.colorbar(
            frame=f"x{cb_x_afg}+l{cb_label}",
            position="+o0c/0.8c+e0.3c+ml",
            cmap=cmap_fill,
        )

        fig3d.shift_origin(yshift="28.2c")

        # Plot map at the top
        fig3d.coast(
            frame=["WSNE", "f"],
            perspective=True,
            land=color_land,
            water=f"{color_water}@80",
            shorelines=f"1/0.5p,{color_sl}",
        )
        # Mark Santorini
        fig3d.plot(perspective=True, **args_santo)

        fig3d.shift_origin(xshift="w+2c", yshift="-28.2c")

    fig_name = "santorini_2d_epicenters_" + str(day).split(" ")[0]
    fig2d.show()
    # for ext in ["png"]:  # "pdf", "eps"
    #     fig2d.savefig(fname=f"{path_out}/{fig_name}.{ext}")
    print(fig_name)
    fig3d.show()
    fig_name = "santorini_3d_hypocenters_" + str(day).split(" ")[0]
    # for ext in ["png"]:  # "pdf", "eps"
    #     fig3d.savefig(fname=f"{path_out}/{fig_name}.{ext}")
    print(fig_name)

# -----------------------------------------------------------------------------
    if day > datetime.datetime(2025, 1, 23, 0, 0) and \
       day < datetime.datetime(2025, 2, 17, 0, 0):
        x_afg_l = "xf0.5g1"
        y_afg_l = "yf5g5"
        if i_histo > 17:
            x_afg_l = "xa1f0.5g1+lmagnitude"
        if i_histo in [0, 6, 12, 18]:
            y_afg_l = "ya5g5+lnumber of earthquakes"

        fig_histo.basemap(
            region=[0, 6, 0, 40],
            projection="X6c/5c",
            frame=[
                f"WStr+t@;{color_hl};{N_eqs_day}@;; earthquakes on @;{color_hl};"
                + str(day).split(" ")[0]
                + "@;;",
                x_afg_l,
                y_afg_l,
            ],
        )
        if len(df_eq_day) > 0:
            fig_histo.histogram(
                data=df_eq_day["magnitude"],
                series=0.1,
                barwidth="0.08",
                fill=f"{color_hl}@40",
                histtype=0,  # counts
            )
        fig_histo.basemap(frame=0)

        fig_histo.shift_origin(xshift="+w+0.2c")
        if i_histo in [5, 11, 17, 23, 29]:
            fig_histo.shift_origin(yshift="-h-0.7c", xshift="-37.2c")

        i_histo = i_histo + 1

        fig_histo.show()
# fig_histo.show()
fig_name = "santorini_histo_magnitude_per_day"
# for ext in ["png"]:  # "pdf", "eps"
#     fig_histo.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)


# -----------------------------------------------------------------------------
# Bar plot for earthquakes per day
fig_bar = gmt.Figure()
fig_bar.basemap(
    region=[0, len(N_eqs_days) + 1, 0, 550],
    projection="X25c/15c",
    frame=[
        "x+ldays up on " + str(start_date_plot).split(" ")[0],
        "y+lnumber of earthquakes",
    ],
)

for i_day, x_day in enumerate(x_days):
    fill_bar = "gray50"
    if x_day > 9 and x_day < 34:
        fill_bar = f"{color_hl}@40"
    fig_bar.plot(x=[x_day, x_day], y=[0, N_eqs_days[i_day]], pen=f"5p,{fill_bar}")
    fig_bar.text(text=N_eqs_days[i_day], x=x_day, y=N_eqs_days[i_day] + 8)

fig_bar.basemap(frame=0)

fig_bar.show()
fig_name = "santorini_histo_earthquakes_per_day"
# for ext in ["png"]:  # "pdf", "eps"
#     fig_bar.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)
