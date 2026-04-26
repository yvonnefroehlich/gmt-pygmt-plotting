# #############################################################################
# Climate stripes
# - Data available at https://data.giss.nasa.gov/gistemp/data_v4.html
#   last accessed 2026/04/24
# - Temperature anomalies: Deviations from the corresponding 1951-1980 means
# -----------------------------------------------------------------------------
# History
# - Created: 2026/04/24
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

import os

import pandas as pd
import pygmt


# %%
# -----------------------------------------------------------------------------
# General
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"

df_sst = pd.read_csv(f"{path_in}/GLB_Ts_plus_dSST.csv", sep=",", header=1)
year_min = df_sst["Year"].min() + 1
year_max = df_sst["Year"].max() - 1
dSST_lim = 1.5  # sea surface temperature anomaly
line_lim = 1.5  # y axis

color_hl = "255/90/0"  # -> orange
box_standard = "+ggray95+p0.1p,gray30+r2p"
clearance_standard = "0.1c+tO"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
file_name_basic = "SST"


# %%
# -----------------------------------------------------------------------------
# Curves for all month
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
with pygmt.config(FONT="10p"):
    fig.basemap(
        region=[year_min, year_max, -line_lim, line_lim],
        projection="X15c/5c",
        frame=["WSen", "xa20f5+lyear", "y+l@~D@~SST / K"],
    )

fig.plot(
    data=df_sst[["Year", "J-D"]],
    fill="lightred",
    fill_between="c+glightblue+y0",
)

pygmt.makecpt(cmap="acton", series=[0, 11, 1])
for i_month, month in enumerate(months):

    label = f"{month}+S0.5c"
    if month == "Jan":
        label = f"{month}+N6"

    fig.plot(
        data=df_sst[["Year", month]],
        cmap=True,
        zvalue=i_month,
        pen="0.3p,+z",
        label=label,
    )
    fig.plot(
        x=df_sst["Year"],
        y=df_sst[month],
        cmap=True,
        style="c0.05c",
        fill=[i_month] * len(df_sst),
    )

with pygmt.config(FONT="6p"):
    fig.legend(position="jBC+jBC+o0c/0.2c+w9c", box=box_standard)

fig.show()
fig.savefig(fname=f"{path_out}/{file_name_basic}_{year_min}to{year_max}_curves.png")


# %%
# -----------------------------------------------------------------------------
# Stripes for all months - subplot
# -----------------------------------------------------------------------------
hight = 5
shift = 0.5

fig = pygmt.Figure()
fig.basemap(
    region=[year_min, year_max, -line_lim, line_lim],
    projection=f"X20c/{hight}c",
    frame=0,
)

pygmt.makecpt(cmap="vik", series=[-dSST_lim, dSST_lim])

for month in months:

    for i_year, year in enumerate(range(year_min, year_max + 1)):
        diff_sst = df_sst[month][i_year]
        fig.plot(
            x=[year, year],
            y=[-line_lim, line_lim],
            pen="4p,+z",
            zvalue=diff_sst,
            cmap=True,
        )

    if month in ["Apr", "Aug", "Dec"]:
        fig.basemap(frame=["lStr", "xa10f5", "x+e"])
    else:
        fig.basemap(frame=["lStr", "xf5"])

    if month == "Aug":
        fig.colorbar(frame=[True, "y+l@~D@~SST / K"])

    fig.text(
        text=month,
        position="TL",
        offset="0.2c/-0.2c",
        fill="white@30",
        font=f"15p,1,{color_hl}",
        clearance=clearance_standard,
        no_clip=True,
    )

    fig.shift_origin(yshift=f"-h-{shift}c")
    if month in ["Apr", "Aug", "Dec"]:
        fig.shift_origin(xshift=f"+w+{shift}c", yshift=f"+{4 * (hight + shift)}c")

fig.show()
fig.savefig(fname=f"{path_out}/{file_name_basic}_{year_min}to{year_max}_stripes.png")


# %%
# -----------------------------------------------------------------------------
# Stripes for months - single plots
# -----------------------------------------------------------------------------
for month in [
    "J-D",
    # "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    # "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]:

    fig_name = f"{file_name_basic}_{year_min}to"

    fig = pygmt.Figure()
    fig.basemap(
        region=[year_min, year_max, -line_lim, line_lim],
        projection="X20c/5c",
        frame=0,
    )

    pygmt.makecpt(cmap="vik", series=[-dSST_lim, dSST_lim])
    fig.colorbar(frame=[True, "y+l@~D@~SST / K"])

    fig.text(
        position="BL",
        offset="0.1c/-1.3c",
        text=month,
        font=f"15p,1,{color_hl}",
        no_clip=True,
    )

    for i_year, year in enumerate(range(year_min, year_max + 1)):
        diff_sst = df_sst[month][i_year]
        fig.plot(
            x=[year, year],
            y=[-line_lim, line_lim],
            pen="4p,+z",
            zvalue=diff_sst,
            cmap=True,
        )
        fig.basemap(frame=["lStr", "xa10f5", "x+el"])

        # try:
        #     os.mkdir(f"{path_out}/{month}")
        # except:
        #     pass
        # fig.savefig(fname=f"{path_out}/{month}/{fig_name}{year}_NOframe.png")
        # fig.show()

    fig.show()
    fig.savefig(fname=f"{path_out}/{fig_name}{year_max}_strips_{month}.png")
