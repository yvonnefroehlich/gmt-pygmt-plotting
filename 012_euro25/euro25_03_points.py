# -*- coding: utf-8 -*-
# #############################################################################
#
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created:
#   PyGMT v0.14.2 / dev -> https://www.pygmt.org/v0.14.2/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


import numpy as np
import pygmt


path_out = "02_out_figs"
fig_name = "euro25_03_points"
dpi_png = 720

region = [0, 4, 0, 10]
projection = "X5c/9c"

color_gra = "254/202/139"
color_grb = "242/111/111"
color_grc = "248/154/68"
color_grd = "127/210/232"
colors = [color_gra, color_grb, color_grc, color_grd]

countries_gra = ["Switzerland", "Norway", "Iceland", "Finland"]
countries_grb = ["Spain", "Portugal", "Belgium", "Italy"]
countries_grc = ["Germany", "Poland", "Denmark", "Sweden"]
countries_grd = ["France", "England", "Wales", "Netherlands"]
countries = [countries_gra, countries_grb, countries_grc, countries_grd]

x = np.array([0.5, 0.5])

points = np.array([
   [[0, 3, 0, 3],  # match day 1
    [3, 0, 0, 3],
    [3, 0, 0, 3],
    [3, 0, 0, 3]],
   [[3, 6, 0, 3],  # match day 2
    [6, 1, 0, 4],
    [6, 0, 0, 6],
    [6, 3, 0, 3]],
   [[4, 9, 0, 4],  # match day 3
    [9, 1, 3, 4],
    [6, 3, 0, 9],
    [6, 3, 0, 3]],
])


fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray70")

for i_day in range(3):

    for i_group, group in enumerate(["A", "B", "C", "D"]):

        frame_title = "tbrW"
        if i_day == 0: frame_title = f"tbrW+tgroup {group}"
        frame_left = "yf1g1"
        if group == "A": frame_left = "ya1f1g1+lpoints+e"

        fig.basemap(region=region, projection=projection, frame=[frame_title, frame_left])

        for i_country in range(4):
            # vertical bars for points
            fig.plot(
                x=x + i_country,
                y=[0, points[i_day][i_group][i_country]],
                pen=f"20p,{colors[i_group]}",
            )

            # label for points
            fig.text(
                text=points[i_day][i_group][i_country],
                x=x[0] + i_country,
                y=points[i_day][i_group][i_country] + 0.15,
                justify="CB",
                font="12p,1,black",
            )

            # label for countries
            if i_day == 0:
                fig.text(
                    text=countries[i_group][i_country],
                    x=x[0] + i_country,
                    y=6,
                    justify="LM",
                    font="14p",
                    angle=90,
                )

        frame_right = "yf1"
        if group == "D": frame_right = f"yf1+lmatch day {i_day + 1}"
        fig.basemap(region=region, projection=projection, frame=["wsnE", frame_right])

        fig.shift_origin(xshift="+w0.5c")
    fig.shift_origin(xshift="-22c", yshift="-h-0.25c")

fig.show()
for ext in ["png"]: # "pdf", "eps"
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)

