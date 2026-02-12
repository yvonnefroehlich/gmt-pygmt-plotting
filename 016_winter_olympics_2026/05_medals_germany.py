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
df_medals = pd.read_csv(f"{path_in}/medals_germany.txt", sep=";")

fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray60")
fig.basemap(
    region=[5.8, 22.2, 0.8, 3.2],
    projection="X15c/3c",
    frame=["xa1g1+lday in Febuary", "ya1g1+lcount of medals"],
)

for medal, color, xshift in zip(
    ["bronze", "silver", "gold"],
    ["tan", "gray", "gold"],
    [0.25, 0.5, 0.75]
):
    fig.plot(
        x=df_medals["day"] + xshift,
        y=df_medals[medal],
        style="c0.3c",
        fill=color,
    )

fig.show()
fig.savefig(fname=f"{path_out}/05_medals_germany.png")


# %%
df_medals = pd.read_csv(f"{path_in}/medals_germany_02.txt", sep=";")

fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray60")
fig.basemap(
    region=[5.8, 22.2, 0.8, 3.2],
    projection="X15c/3c",
    frame=["xa1g1+lday in Febuary", "ya1g1+lcount of medals"],
)

for medal, color, xshift in zip(
    ["bronze", "silver", "gold"],
    ["tan", "gray", "gold"],
    [0.25, 0.5, 0.75]
):

    df_medals_temp = df_medals[df_medals["medal"] == medal]

    for gender, pen in zip(["F", "M", "X"], ["tomato", "steelblue", "purple"]):

        df_medals_temp_temp = df_medals_temp[df_medals_temp["gender"] == gender]

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

fig.show()
fig.savefig(fname=f"{path_out}/05_medals_germany_02.png")

