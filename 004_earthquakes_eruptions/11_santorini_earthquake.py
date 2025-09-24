# #############################################################################
# Santorini earthquakes January - February 2025
#
# Data taken from
#   Karakostas V, Lomax A, Anagnostou V, Papadimitriou E, Acoccela V, & Hicks S (2025).
#   2025 Santorini–Amorgos NLL-SSST-coherence high-precision relocated earthquake catalog.
#   Zenodo. https://doi.org/10.5281/zenodo.15111649.
# -----------------------------------------------------------------------------
# History
# - Created: 2025/09/21
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


import pygmt as gmt
import pandas as pd
import datetime
from dateutil.rrule import rrule, DAILY
import numpy as np

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
min_lon = 25.34
max_lon = 25.91
min_lat = 36.35
max_lat = 36.82
region = [min_lon, max_lon, min_lat, max_lat]


# %%
# -----------------------------------------------------------------------------
# Prepare data
# -----------------------------------------------------------------------------
# Source: https://doi.org/10.5281/zenodo.15111649
# Last access: 2025/09/24
df_eq_raw = pd.read_csv(f"{path_in}/catalog_santorini.csv", sep=",")

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
# Make maps of epicenters with different color-codings over time
# -----------------------------------------------------------------------------
for i_day, day in enumerate(rrule(DAILY, dtstart=start_date_plot, until=end_date_plot)):

    df_eq_cum = df_eq[df_eq["date_time"] < (day + add_one_day)]
    df_eq_before = df_eq[df_eq["date_time"] < day]
    N_eqs_day = len(df_eq_cum) - len(df_eq_before)
    N_eqs_days[i_day] = N_eqs_day

    print(day)
    print(len(df_eq_cum))
    print(day + add_one_day)
    print(len(df_eq_before))

# -----------------------------------------------------------------------------
    fig = gmt.Figure()
    gmt.config(MAP_TITLE_OFFSET="-5p")

    for fill_quantity, title, cmap, reverse, series, cb_label in zip(
        ["magnitude", "depth", "date_time"],
        [
            "WSne+tSantorini–Amorgos",
            f"wSne+t@;{color_hl};{N_eqs_day}@;; / {len(df_eq_cum)} earthquakes",
            "wSne+t" + str(start_date_data).split(" ")[0] + \
               f" — @;{color_hl};" + str(day).split(" ")[0] + "@;;",
        ],
        ["lipari", "lajolla", "hawaii"],
        [True, False, True],
        [[3, 5], [3, 15], [start_date_plot, end_date_plot]],
        ["magnitude", "hypocentral depth / km", "date"],
    ):

        # Create basic map
        fig.basemap(projection="M12c", region=region, frame=["af", title])
        fig.coast(land=color_land, water=color_water, shorelines=f"1/0.5p,{color_sl}")

        # Mark Santorini
        fig.plot(x=25.43, y=36.42, style="x0.6c", pen=f"5p,{color_hl}")

        # Plot epicenters
        gmt.makecpt(cmap=cmap, series=series, reverse=reverse)
        with gmt.config(FONT="15p"):
            fig.colorbar(frame=f"x+l{cb_label}", position="+o0c/1.5c+e0.3c+ml")
        fig.plot(
            x=df_eq_cum.longitude,
            y=df_eq_cum.latitude,
            style="c0.07c",
            fill=df_eq_cum[fill_quantity],
            cmap=True,
        )

        fig.shift_origin(xshift="w+0.5c")

    fig.show()

    fig_name = "11_santorini_earthquake_" + str(day).split(" ")[0]
    for ext in ["png"]:  # "pdf", "eps"
        fig.savefig(fname=f"{path_out}/santorini/{fig_name}.{ext}")
    print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Make bar plot for earthquakes per day
# -----------------------------------------------------------------------------
fig = gmt.Figure()
fig.basemap(
    region=[0, len(N_eqs_days) + 1, 0, 550],
    projection="X25c/15c",
    frame=[
        "x+ldays up on " + str(start_date_plot).split(" ")[0],
        "y+lnumber of earthquakes",
    ]
)

for i_day, x_day in enumerate(x_days):
    fig.plot(x=[x_day, x_day], y=[0, N_eqs_days[i_day]], pen="5p,gray30")
    fig.text(text=N_eqs_days[i_day], x=x_day, y=N_eqs_days[i_day] + 8)

fig.show()
