# #############################################################################
# Winter Olympics 2026 - medals germany
# -----------------------------------------------------------------------------
# History
# - Created: 2026/02/11
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

    df_medals = pd.read_csv(f"{path_in}/medals_germany_{event}.txt", sep=";")
    N_tot = len(df_medals)

    match event:
        case "olympics":
            month = "Febuary"
            region = [5.8, 23.2, 0.8, 3.2]
        case "paralympics":
            month = "March"
            region = [3.8, 16.2, 0.8, 3.2]

    with pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray60", FONT="11p"):
        fig.basemap(
            region=region,
            projection="X15c/3c",
            frame=[f"xa1g1+lday in {month}", "ya1g1+lmedals Germany"],
        )

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
        fig.text(text=text, position="TL", justify="TR", offset=f"1.5c/{-xshift * 1.4}c")

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
                            # fill="white",
                            pen=f"1p,{pen}",
                        )

    fig.text(text=f"total: {N_tot}", justify="TR", position="TL", offset="1.5c/-1.38c")
    fig.text(text=f"female: {n_F}", justify="TR", position="TL", offset="1.5c/-1.7c")
    fig.text(text=f"male: {n_M}", justify="TR", position="TL", offset="1.5c/-2.05c")
    fig.text(text=f"mixed: {n_X}", justify="TR", position="TL", offset="1.5c/-2.4c")

    fig.shift_origin(yshift="-h-1.5c")

fig.show()
fig.savefig(fname=f"{path_out}/05_medals_germany.png")
