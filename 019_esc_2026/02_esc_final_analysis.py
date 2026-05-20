# #############################################################################
# Final of the Eurovision Song Contest 2026 in Austria
# - Analyis comparing jury and public points
# Data
# - modified from https://eurovisionworld.com/eurovision/2026
# - last accessed: 2026/05/18
# -----------------------------------------------------------------------------
# History
# - Created: 2026/05/18
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

color_hl = "255/90/0"  # -> orange | URG paper
color_total = "orange"
color_jury = "cyan3"
color_public = "darkblue"

symbol_total = "c0.2c"
symbol_jury = "i0.25c"
symbol_public = "t0.25c"
symbol_diff = "s0.25c"

box_standard = "+gwhite+p0.1p,gray30+r2p"


# %%
# -----------------------------------------------------------------------------
# Load and prepare data
# -----------------------------------------------------------------------------
df_esc = pd.read_csv(f"{path_in}/esc_{year}.txt", delimiter="\t")

# -----------------------------------------------------------------------------
# Add column for difference between public and jury points
diff_public_jury = df_esc["public"] - df_esc["jury"]
df_esc["diff_public_jury"] = diff_public_jury
df_esc_diff_neg = df_esc[df_esc["diff_public_jury"] < 0]
df_esc_diff_pos = df_esc[df_esc["diff_public_jury"] > 0]

# -----------------------------------------------------------------------------
# Add column for places based on public and jury points separatly
df_esc = df_esc.sort_values(by=["jury"], ignore_index=True, ascending=False)
df_esc["place_jury"] = np.arange(1, len(df_esc)+1, 1)

df_esc = df_esc.sort_values(by=["public"], ignore_index=True, ascending=False)
df_esc["place_public"] = np.arange(1, len(df_esc)+1, 1)


# %%
# -----------------------------------------------------------------------------
# Points total, jury, public
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
):
    label = group
    if group == "total":
        label = f"{group}+HESC final {year}+f10p"

    fig.plot(
        data=df_esc[["place", group]],
        style=style,
        pen="0.5p,gray30",
        fill=color,
        label=label,
        no_clip=True,
    )

# Add text for total points
fig.text(
    text=df_esc["total"],
    x=df_esc["place"],
    y=df_esc["total"],
    justify="MC",
    offset="0c/0.3c",
    font="9p",
    fill="white@50",
)
# Add text for countries
fig.text(
    text=df_esc["country"],
    x=df_esc["place"],
    y=np.ones(len(df_esc)) * offset_y_country,
    justify="LM",
    angle=90,
    font="9p",
    fill="white@30"
)

# Add legend
fig.legend(position="jRM+o1c/0c+w2.7c", box=box_standard)

# for ext in ["png"]:  # , "pdf", "eps"]
#     fig.savefig(fname=f"{fig_name}_points.{ext}")
fig.show()


# %%
# -----------------------------------------------------------------------------
# Places based on public and jury points separatly
# -----------------------------------------------------------------------------
for points_sep in ["public", "jury"]:

    match points_sep:
        case "jury":
            color_sep = color_jury
            symbol_sep = symbol_jury
        case "public":
            color_sep = color_public
            symbol_sep = symbol_public

    fig = pygmt.Figure()
    pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray50")

    fig.basemap(
        region=[0.5, len(df_esc) + 0.5, 0, max_points],
        projection=projection,
        frame=[
            f"xa1g1+lplace based {points_sep} points",
            f"ya100f20+l{points_sep} points",
        ],
    )
    # Plot public / jury points
    fig.plot(
        data=df_esc[[f"place_{points_sep}", points_sep]],
        style=symbol_sep,
        pen="0.5p,gray30",
        fill=color_sep,
        label=points_sep,
        no_clip=True,
    )

    # Add text for public / jury points
    fig.text(
        text=df_esc[points_sep],
        x=df_esc[f"place_{points_sep}"],
        y=df_esc[points_sep],
        justify="MC",
        offset="0c/0.35c",
        font="9p",
        fill="white@50"
    )
    # Add text for countries
    fig.text(
        text=df_esc["country"],
        x=df_esc[f"place_{points_sep}"],
        y=np.ones(len(df_esc)) * offset_y_country,
        justify="LM",
        angle=90,
        font="9p",
        fill="white@30"
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
        "ya100f20+ldifference between public and jury points"
    ],
)

# Plot zero line
fig.plot(x=[0, 27], y=[0, 0], pen="1p,gray30")

# Difference
for df_diff, color, y_offset in zip(
    [df_esc_diff_neg, df_esc_diff_pos], [color_jury, color_public], [-0.35, 0.35]
):
    # Plot differences
    fig.plot(
        x=df_diff["place"],
        y=df_diff["diff_public_jury"],
        style=symbol_diff,
        pen="0.5p,gray30",
        fill=color,
    )
    # Add text for differences
    fig.text(
        text=df_diff["diff_public_jury"],
        x=df_diff["place"],
        y=df_diff["diff_public_jury"],
        justify="MC",
        offset=f"0c/{y_offset}c",
        font="9p",
        fill="white@50"
    )

# Add text for countries
fig.text(
    text=df_esc["country"],
    x=df_esc["place"],
    y=np.ones(len(df_esc)) * (-max_points / 2 + 10),
    justify="LM",
    angle=90,
    font="9p",
    fill="white@30"
)

# for ext in ["png"]:  # , "pdf", "eps"]
#     fig.savefig(fname=f"{fig_name}_diff.{ext}")
fig.show()
