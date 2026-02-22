# #############################################################################
# Winter games 2026 - medals plot for Olympics and Paralympics
# -----------------------------------------------------------------------------
# History
# - Created: 2026/02/11
# - Updated: 2026/02/22 - Complete medals plot for Olympics for Germany
# - Updated: 2026/02/22 - Update medals plot for Paralympics
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


# %%
fig = pygmt.Figure()

for event in ["olympics", "paralympics"]:

    match event:
        case "olympics":
            month = "Febuary"
            region = [5.8, 23.2, 0.8, 3.2]
            country = "germany"
        case "paralympics":
            month = "March"
            region = [3.8, 16.2, 0.8, 3.2]
            country = "ukraine"

    df_medals = pd.read_csv(f"{path_in}/medals_{country}_{event}.txt", sep=";")
    N_tot = len(df_medals)

    with pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray60", FONT="11p"):
        fig.basemap(
            region=region,
            projection="X15c/3c",
            frame=[f"xa1g1+lday in {month}", f"ya1g1+lmedals {country}"],
        )

    uk_blue = "0/91/187"
    uk_yellow = "255/213/0"
    uk_x = [3.8, 16.2, 16.2, 3.8, 3.8]
    if event == "paralympics":
        fig.plot(x=uk_x, y=[2, 2, 3.2, 3.2, 2], fill=f"{uk_blue}@50")
        fig.plot(x=uk_x, y=[0.8, 0.8, 2, 2, 0.8], fill=f"{uk_yellow}@50")
        fig.text(
            x=10,
            y=2.6,
            text="Harmony does not mean ignoring the war!",
            font="12p,1",
            justify="MC",
        )

    fig.plot(x=[3.85, 5.2, 5.2, 3.85, 3.85], y=[1, 1, 3, 3, 1], fill="white@20")

    n_F = 0
    n_M = 0
    n_X = 0

    for medal, color, xshift in zip(
        ["bronze", "silver", "gold"],
        ["tan", "gray", "gold"],
        [0.75, 0.5, 0.25]
    ):

        df_medals_temp = df_medals[df_medals["medal"] == medal]

        text = f"{medal}: {len(df_medals_temp)}"
        fig.text(
            text=text,
            position="TL",
            justify="TR",
            offset=f"1.5c/{-xshift * 1.4}c",
            font=f"8p,1,{color}",
        )

        for gender, pen in zip(["F", "M", "X"], ["tomato", "steelblue", "purple"]):

            df_medals_temp_temp = df_medals_temp[df_medals_temp["gender"] == gender]

            match gender:
                case "F":
                    n_F = n_F + len(df_medals_temp_temp)
                case "M":
                    n_M = n_M + len(df_medals_temp_temp)
                case "X":
                    n_X = n_X + len(df_medals_temp_temp)


            if len(df_medals_temp_temp) > 0:

                for day in range(6, 22 + 1):

                    df_medals_day = df_medals_temp_temp[df_medals_temp_temp["day"] == day]

                    if len(df_medals_day) > 0:

                        fig.plot(
                            x=day + xshift,
                            y=len(df_medals_day),
                            style="c0.3c",
                            fill=color,
                            pen=f"1p,{pen}",
                        )

    args_text = {"justify": "TR", "position": "TL"}
    fig.text(text=f"total: {N_tot}", offset="1.5c/-1.38c", font="8p,1,black", **args_text)
    fig.text(text=f"female: {n_F}", offset="1.5c/-1.7c", font="8p,1,tomato", **args_text)
    fig.text(text=f"male: {n_M}", offset="1.5c/-2.05c", font="8p,1,steelblue", **args_text)
    fig.text(text=f"mixed: {n_X}", offset="1.5c/-2.4c", font="8p,1,purple", **args_text)

    fig.shift_origin(yshift="-h-1.5c")

fig.show()
fig.savefig(fname=f"{path_out}/05_medals.png")
