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

max_points = 550
projection = "X17c/12c"
offset_y_land = 550 - 150  # manually adjusted

color_hl = "255/90/0"  # -> orange | URG paper
color_total = "orange"
color_public = "darkblue"
color_jury = "cyan3"


# %%
# -----------------------------------------------------------------------------
# Load and prepare data
# -----------------------------------------------------------------------------
df_esc = pd.read_csv(f"{path_in}/esc_{year}.txt", delimiter="\t")

# -----------------------------------------------------------------------------
# Add difference between public and jury points
diff_aud_jury = df_esc["public"] - df_esc["jury"]
df_esc["diff_public_jury"] = diff_aud_jury
df_esc_diff_neg = df_esc[df_esc["diff_public_jury"] < 0]
df_esc_diff_pos = df_esc[df_esc["diff_public_jury"] > 0]

# -----------------------------------------------------------------------------
# Add places based on public and jury points separatly
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

# Plot total points
fig.plot(
    data=df_esc[["place", "points"]],
    style="c0.2c",
    pen="0.5p,gray30",
    fill=color_total,
    label=f"total+HESC final {year}+f10p",
    no_clip=True,
)
# Add label for total points
fig.text(
    text=df_esc["points"],
    x=df_esc["place"],
    y=df_esc["points"],
    font="9p",
    justify="MC",
    offset="0c/0.3c",
    fill="white@50",
)

# Plot jury points
fig.plot(
    data=df_esc[["place", "jury"]],
    style="i0.25c",
    pen="0.5p,gray30",
    fill=color_jury,
    label="jury",
    no_clip=True,
)
# Plot public points
fig.plot(
    data=df_esc[["place", "public"]],
    style="t0.25c",
    pen="0.5p,gray30",
    fill=color_public,
    label="public",
    no_clip=True,
)

# Add label for lands
fig.text(
    text=df_esc["land"],
    x=df_esc["place"],
    y=np.ones(len(df_esc)) * offset_y_land,
    angle=90,
    font="9p",
    justify="LM",
    fill="white@30"
)

# Add legend
box_standard = "+gwhite+p0.1p,gray30+r2p"
fig.legend(position="jRM+o1c/0c+w2.7c", box=box_standard)

for ext in ["png"]:  # , "pdf", "eps"]
    fig.savefig(fname=f"{fig_name}_points.{ext}")
fig.show()


# %%
# -----------------------------------------------------------------------------
# Places based on public and jury points separatly
# -----------------------------------------------------------------------------
for points_sep in ["public", "jury"]:

    match points_sep:
        case "jury":
            color_sep = color_jury
            symbol = "i"
        case "public":
            color_sep = color_public
            symbol = "t"

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
    # Plot points
    fig.plot(
        data=df_esc[[f"place_{points_sep}", points_sep]],
        style=f"{symbol}0.25c",
        pen="0.5p,gray30",
        fill=color_sep,
        label=points_sep,
        no_clip=True,
    )
    # Add label for points
    fig.text(
        text=df_esc[points_sep],
        x=df_esc[f"place_{points_sep}"],
        y=df_esc[points_sep],
        font="9p",
        justify="MC",
        offset="0c/0.35c",
        fill="white@50"
    )
    # Add label for land
    fig.text(
        text=df_esc["land"],
        x=df_esc[f"place_{points_sep}"],
        y=np.ones(len(df_esc)) * offset_y_land,
        angle=90,
        font="9p",
        justify="LM",
        fill="white@30"
    )

    for ext in ["png"]:  # , "pdf", "eps"]
        fig.savefig(fname=f"{fig_name}_{points_sep}.{ext}")
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

# Plot differences
fig.plot(
    x=df_esc_diff_neg["place"],
    y=df_esc_diff_neg["diff_public_jury"],
    style="s0.25c",
    pen="0.5p,gray30",
    fill=color_jury,
)
fig.plot(
    x=df_esc_diff_pos["place"],
    y=df_esc_diff_pos["diff_public_jury"],
    style="s0.3c",
    pen="0.5p,gray30",
    fill=color_public,
)

# Add label for difference
fig.text(
    text=df_esc_diff_neg["diff_public_jury"],
    x=df_esc_diff_neg["place"],
    y=df_esc_diff_neg["diff_public_jury"],
    font="10p",
    justify="MC",
    offset="0c/-0.35c",
    fill="white@50"
)
fig.text(
    text=df_esc_diff_pos["diff_public_jury"],
    x=df_esc_diff_pos["place"],
    y=df_esc_diff_pos["diff_public_jury"],
    font="9p",
    justify="MC",
    offset="0c/0.35c",
    fill="white@50"
)

# Add label for lands
fig.text(
    text=df_esc["land"],
    x=df_esc["place"],
    y=np.ones(len(df_esc)) * (-max_points / 2 + 10),
    angle=90,
    font="9p",
    justify="LM",
    fill="white@30"
)

for ext in ["png"]:  # , "pdf", "eps"]
    fig.savefig(fname=f"{fig_name}_diff.{ext}")
fig.show()
