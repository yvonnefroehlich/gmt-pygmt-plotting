# #############################################################################
# Final of the Eurovision Song Contest 2026 in Austria
# - Analysis comparing jury and public points
# Data
# - modified from https://eurovisionworld.com/eurovision/2026
# - last accessed: 2026/05/18
# -----------------------------------------------------------------------------
# History
# - Created: 2026/05/18
# - Updated: 2026/05/21 - Add analysis for start place, improve code
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


import numpy as np
import pandas as pd
import pygmt

# %%
# -----------------------------------------------------------------------------
# Choose for your needs
# -----------------------------------------------------------------------------
year = 2026


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"
fig_name = f"{path_out}/esc_final_{year}"

projection = "X17c/12c"

max_points = 550
offset_y_country = max_points - 150  # manually adjusted

color_total = "orange"
color_jury = "cyan3"
color_public = "darkblue"

symbol_total = "c0.22c"
symbol_jury = "i0.25c"
symbol_public = "t0.25c"
symbol_diff = "s0.25c"

box_standard = "+gwhite@30+p0.1p,gray30+r2p"


# %%
# -----------------------------------------------------------------------------
# Load and prepare data
# -----------------------------------------------------------------------------
df_esc = pd.read_csv(f"{path_in}/esc_{year}.txt", delimiter="\t")

# -----------------------------------------------------------------------------
# Add column for difference between public and jury points
diff_public_jury = df_esc["public_points"] - df_esc["jury_points"]
df_esc["diff_public_jury"] = diff_public_jury
df_esc_diff_neg = df_esc[df_esc["diff_public_jury"] < 0]
df_esc_diff_pos = df_esc[df_esc["diff_public_jury"] > 0]

# -----------------------------------------------------------------------------
# Add column for places based on public and jury points separately
df_esc = df_esc.sort_values(by=["jury_points"], ignore_index=True, ascending=False)
df_esc["jury_place"] = np.arange(1, len(df_esc) + 1, 1)

df_esc = df_esc.sort_values(by=["public_points"], ignore_index=True, ascending=False)
df_esc["public_place"] = np.arange(1, len(df_esc) + 1, 1)


# %%
# -----------------------------------------------------------------------------
# Total, jury, public points together
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray50")

fig.basemap(
    region=[0.5, len(df_esc) + 0.5, 0, max_points],
    projection=projection,
    frame=[
        "xa1g1+lplace based on total points",
        "ya100f20+ltotal / jury / public points",
    ],
)

# Plot total, jury and public points
for group, style, color in zip(
    ["total", "jury", "public"],
    [symbol_total, symbol_jury, symbol_public],
    [color_total, color_jury, color_public],
    strict=True,
):
    label = f"{group} points"
    if group == "total":
        label = f"{label}+HESC final {year}+f10p"

    fig.plot(
        data=df_esc[["total_place", f"{group}_points"]],
        style=style,
        pen="0.5p,gray30",
        fill=color,
        label=label,
        no_clip=True,
    )

# Add text for total points
fig.text(
    text=df_esc["total_points"],
    x=df_esc["total_place"],
    y=df_esc["total_points"],
    justify="MC",
    offset="0c/0.3c",
    font="9p",
    fill="white@50",
)
# Add text for countries
fig.text(
    text=df_esc["country"],
    x=df_esc["total_place"],
    y=np.ones(len(df_esc)) * offset_y_country,
    justify="LM",
    angle=90,
    font="9p",
    fill="white@30",
)

# Add legend
fig.legend(position="jRM+o1c/0c+w2.7c", box=box_standard)

# for ext in ["png"]:  # , "pdf", "eps"]
#     fig.savefig(fname=f"{fig_name}_points.{ext}")
fig.show()


# %%
# -----------------------------------------------------------------------------
# Places based on public and jury points separately
# -----------------------------------------------------------------------------
for group, style, color in zip(
    ["jury", "public"],
    [symbol_jury, symbol_public],
    [color_jury, color_public],
    strict=True,
):
    fig = pygmt.Figure()
    pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray50")

    fig.basemap(
        region=[0.5, len(df_esc) + 0.5, 0, max_points],
        projection=projection,
        frame=[
            f"xa1g1+lplace based on {group} points",
            f"ya100f20+l{group} points",
        ],
    )
    # Plot public / jury points
    fig.plot(
        data=df_esc[[f"{group}_place", f"{group}_points"]],
        style=style,
        pen="0.5p,gray30",
        fill=color,
        no_clip=True,
    )

    # Add text for public / jury points
    fig.text(
        text=df_esc[f"{group}_points"],
        x=df_esc[f"{group}_place"],
        y=df_esc[f"{group}_points"],
        justify="MC",
        offset="0c/0.35c",
        font="9p",
        fill="white@50",
    )
    # Add text for countries
    fig.text(
        text=df_esc["country"],
        x=df_esc[f"{group}_place"],
        y=np.ones(len(df_esc)) * offset_y_country,
        justify="LM",
        angle=90,
        font="9p",
        fill="white@30",
    )

    # for ext in ["png"]:  # , "pdf", "eps"]
    #     fig.savefig(fname=f"{fig_name}_{points_sep}.{ext}")
    fig.show()


# %%
# -----------------------------------------------------------------------------
# Difference between jury and public points
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray50")

fig.basemap(
    region=[0.5, len(df_esc) + 0.5, -max_points / 2, max_points / 2],
    projection=projection,
    frame=[
        "xa1g1+lplace based on total points",
        "ya100f20+ldifference between public and jury points",
    ],
)

# Plot zero line
fig.plot(x=[0, 27], y=[0, 0], pen="1p,gray30")

# Difference
for df_diff, color, y_offset in zip(
    [df_esc_diff_neg, df_esc_diff_pos],
    [color_jury, color_public],
    [-0.35, 0.35],
    strict=True,
):
    # Plot differences
    fig.plot(
        x=df_diff["total_place"],
        y=df_diff["diff_public_jury"],
        style=symbol_diff,
        pen="0.5p,gray30",
        fill=color,
    )
    # Add text for differences
    fig.text(
        text=df_diff["diff_public_jury"],
        x=df_diff["total_place"],
        y=df_diff["diff_public_jury"],
        justify="MC",
        offset=f"0c/{y_offset}c",
        font="9p",
        fill="white@50",
    )

# Add text for countries
fig.text(
    text=df_esc["country"],
    x=df_esc["total_place"],
    y=np.ones(len(df_esc)) * (-max_points / 2 + 10),
    justify="LM",
    angle=90,
    font="9p",
    fill="white@30",
)

# for ext in ["png"]:  # , "pdf", "eps"]
#     fig.savefig(fname=f"{fig_name}_diff.{ext}")
fig.show()


# %%
# -----------------------------------------------------------------------------
# Start vs. total, jury, public places
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray50")

fig.basemap(
    region=[0.5, len(df_esc) + 0.5, 0.5, len(df_esc) + 0.5],
    projection="X15c/-15c",
    frame=["xa1g1+lstart place", "ya1g1+ltotal / jury / public place"],
)

countries = df_esc["country"].tolist()
for country_temp in countries:
    df_esc_temp = df_esc[df_esc["country"] == country_temp]

    start_place_temp = df_esc_temp["start_place"].to_numpy().squeeze().tolist()
    place_public_temp = df_esc_temp["public_place"].to_numpy().squeeze().tolist()
    place_jury_temp = df_esc_temp["jury_place"].to_numpy().squeeze().tolist()

    if place_public_temp >= place_jury_temp:
        y = [place_public_temp, place_jury_temp]
    elif place_public_temp < place_jury_temp:
        y = [place_jury_temp, place_public_temp]

    fig.plot(x=[start_place_temp, start_place_temp], y=y, pen="1p,gray50")

for group, style, color in zip(
    ["total", "jury", "public"],
    [symbol_total, symbol_jury, symbol_public],
    [color_total, color_jury, color_public],
    strict=True,
):
    label = f"{group} place"
    if group == "total":
        label = f"{label}+HESC final {year}+f10p"

    # Plot jury / public / total places
    fig.plot(
        data=df_esc[["start_place", f"{group}_place"]],
        style=style,
        pen="0.5p,gray30",
        fill=color,
        label=label,
        no_clip=True,
    )

# Add text for countries
fig.text(
    text=df_esc["country"],
    x=df_esc["start_place"],
    y=np.ones(len(df_esc)) * 0.2,
    justify="LM",
    angle=90,
    font="9p",
    fill="white@30",
    no_clip=True,
)

# Add legend
fig.legend(position="jLB+o2.85c/0.15c+w2.7c", box=box_standard)

# for ext in ["png"]:  # , "pdf", "eps"]
#     fig.savefig(fname=f"{fig_name}_places.{ext}")
fig.show()
