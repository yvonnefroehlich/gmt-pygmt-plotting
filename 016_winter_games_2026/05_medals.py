# #############################################################################
# Winter games 2026 - medals plot for Olympics and Paralympics
# -----------------------------------------------------------------------------
# History
# - Created: 2026/02/11
# - Updated: 2026/02/22 - Complete medals plot for Olympics for Germany
# - Updated: 2026/02/22 - Update medals plot for Paralympics
# - Updated: 2026/03/07 - Complete medals plot for Paralympics for Ukraine
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
import pandas as pd

path_in = "01_in_data"
path_out = "02_out_figs"

color_g = "gold"
color_s = "gray"
color_b = "tan"
color_f = "tomato"
color_m = "steelblue"
color_x = "purple"
color_uk_blue = "0/91/187"
color_uk_yellow = "255/213/0"


# %%
fig = pygmt.Figure()

for event in ["olympics", "paralympics"]:

    match event:
        case "olympics":
            month = "Febuary"
            region = [5.8, 23.2, 0.001, 1]
            country = "germany"
        case "paralympics":
            month = "March"
            region = [3.8, 16.2, 0.001, 1]
            country = "ukraine"

    df_medals = pd.read_csv(f"{path_in}/medals_{country}_{event}.txt", sep=";")

    with pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray60", FONT="11p"):
        fig.basemap(
            region=region,
            projection="X15c/3c",
            frame=["WStr", f"xa1g1+lday in {month}", f"ya5+lmedals {country}"],
        )

    if event == "paralympics":
        uk_x = [3.8, 16.2, 16.2, 3.8, 3.8]
        fig.plot(x=uk_x, y=[0.5, 0.5, 1, 1, 0.5], fill=f"{color_uk_blue}@70")
        fig.plot(x=uk_x, y=[0, 0, 0.5, 0.5, 0], fill=f"{color_uk_yellow}@70")
        fig.text(
            x=10,
            y=0.85,
            text="Harmony does not mean ignoring the war!",
            font="12p,1",
            justify="MC",
        )
        fig.plot(
            x=[3.95, 5.2, 5.2, 3.85, 3.85],
            y=[0.1, 0.1, 0.9, 0.9, 0.1],
            fill="white@20",
        )

    for day in range(6, 22 + 1):
        df_medals_day = df_medals[df_medals["day"] == day]

        if len(df_medals_day) > 0:
            for medal, color, y_color in zip(
                ["bronze", "silver", "gold"],
                [color_b, color_s, color_g],
                [0.1, 0.3, 0.5]
            ):
                df_medals_color = df_medals_day[df_medals_day["medal"] == medal]
                N_color = len(df_medals_color)

                if N_color > 0:
                    for ic in range(N_color):

                        gender_temp = df_medals_color["gender"].tolist()[ic]
                        if gender_temp == "F":
                            pen = "tomato"
                        elif gender_temp == "M":
                            pen = "steelblue"
                        elif gender_temp == "X":
                            pen = "purple"

                        fig.plot(
                            x=0.17 * ic + day,
                            y=y_color,
                            style="c0.3c",
                            fill=color,
                            pen=f"1p,{pen}",
                        )

    N_tot = len(df_medals)
    N_g = len(df_medals[df_medals["medal"] == "gold"])
    N_s = len(df_medals[df_medals["medal"] == "silver"])
    N_b = len(df_medals[df_medals["medal"] == "bronze"])
    N_F = len(df_medals[df_medals["gender"] == "F"])
    N_M = len(df_medals[df_medals["gender"] == "M"])
    N_X = len(df_medals[df_medals["gender"] == "X"])

    y_text = 0.4
    for amount, color in zip(
        [f"gold: {N_g}", f"silver: {N_s}", f"bronze: {N_b}",
         f"total: {N_tot}", f"female: {N_F}", f"male: {N_M}",
         f"mixed: {N_X}"],
        [color_g, color_s, color_b, "black", color_f, color_m, color_x],
    ):
        fig.text(
            text=amount,
            offset=f"1.5c/{-y_text}c",
            font=f"8p,1,{color}",
            justify="TR",
            position="TL",
        )
        y_text = y_text + 0.33

    fig.shift_origin(yshift="-h-1.5c")

fig.show()
fig_name = "05_medals"
fig.savefig(fname=f"{path_out}/{fig_name}.png")
print(fig_name)
