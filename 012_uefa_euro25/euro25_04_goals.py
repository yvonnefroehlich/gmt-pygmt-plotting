# #############################################################################
# UEFA WOMEN'S EURO 2025 - group phase goals
# -----------------------------------------------------------------------------
# History
# - Created: 2025/07/07
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.16.0 - v0.18.0 -> https://www.pygmt.org
# - GMT 6.5.0 - 6.6.0 -> https://www.generic-mapping-tools.org
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
import pygmt


path_out = "02_out_figs"
fig_name = "euro25_04_goals"
dpi_png = 720

region = [0, 4, -16, 16]
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

goals_pos = np.array([
   [[1, 2, 0, 1],  # match day 1
    [5, 0, 0, 1],
    [2, 0, 0, 1],
    [2, 1, 0, 3]],
   [[3, 4, 0, 2],  # match day 2
    [11, 1, 2, 2],
    [4, 0, 1, 4],
    [6, 5, 1, 3]],
   [[4, 8, 3, 3],  # match day 3
    [14, 2, 4, 3],
    [5, 3, 3, 8],
    [11, 11, 2, 5]],
])

goals_neg = np.array([
   [[2, 1, 1, 0],  # match day 1
    [0, 5, 1, 0],
    [0, 2, 1, 0],
    [1, 2, 3, 0]],
   [[2, 2, 3, 2],  # match day 2
    [2, 6, 7, 1],
    [1, 5, 3, 0],
    [3, 2, 7, 4]],
   [[3, 4, 7, 3],  # match day 3
    [3, 8, 8, 4],
    [5, 7, 6, 1],
    [5, 3, 13, 9]],
])


fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray70")

for i_day in range(3):

    for i_group, group in enumerate(["A", "B", "C", "D"]):

        frame_title = "tbrW"
        if i_day == 0: frame_title = f"tbrW+tgroup {group}"
        frame_left = "yf1g1"
        if group == "A": frame_left = "ya2f1g1+lgoals+e"

        fig.basemap(region=region, projection=projection, frame=[frame_title, frame_left])

        for i_country in range(4):
            # vertical bars for goals
            for goals in [goals_pos, -goals_neg]:
                fig.plot(
                    x=x + i_country,
                    y=[0, goals[i_day][i_group][i_country]],
                    pen=f"20p,{colors[i_group]}",
                )
            fig.hlines(y=0, pen="1p,black")

            # labels for goals
            fig.text(
                text=goals_pos[i_day][i_group][i_country],
                x=x[0] + i_country,
                y=goals_pos[i_day][i_group][i_country] + 0.35,
                justify="CB",
                font="12p,1,black",
            )
            fig.text(
                text=-goals_neg[i_day][i_group][i_country],
                x=x[0] + i_country,
                y=-goals_neg[i_day][i_group][i_country] - 0.35,
                justify="CT",
                font="12p,1,black",
            )

            # labels for countries
            if i_day == 0:
                fig.text(
                    text=countries[i_group][i_country],
                    x=x[0] + i_country,
                    y=-15,
                    justify="LM",
                    font="14p",
                    angle=90,  # rotates also justify
                )

        frame_right = "yf1"
        if group == "D": frame_right = f"yf1+lmatch day {i_day + 1}"
        fig.basemap(region=region, projection=projection, frame=["wsnE", frame_right])

        fig.shift_origin(xshift="+w0.5c")

    fig.shift_origin(xshift="-22c", yshift="-h-0.25c")

fig.show()
# for ext in ["png"]: # "pdf", "eps"
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
