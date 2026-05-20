# #############################################################################
# Final of the Eurovision Song Contest 2026 in Austria
# - Points by countries plotted as scoreboards
# - Color-coding for jury, public, and total points
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


import pygmt
import pandas as pd
import numpy as np

# %%
# -----------------------------------------------------------------------------
# Choose for your needs
# -----------------------------------------------------------------------------
year = 2026
group = "public"  ## "jury" | "public" | "total"
add_numbers = False  ## False | True


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"

color_hl = "255/90/0"  # -> orange | URG paper

max_points = 12
cb_gap = 0.25
x_nan_offset = 0.9
if group == "total":
    max_points = 24
    cb_gap = 0.1
    x_nan_offset = 0.96


# %%
# -----------------------------------------------------------------------------
# Load and prepare data
# -----------------------------------------------------------------------------
df_sb = pd.read_csv(f"{path_in}/esc_{year}_scoreboard_{group}.txt", delimiter="\t")

country_recieve = df_sb["country"].values.tolist()
country_recieve.sort()

country_give = df_sb.columns.tolist()[3:len(df_sb.columns.tolist())-1]
country_give.sort()
country_give.append("Rest of world")

x = np.arange(0, len(country_give), 1)


# %%
# -----------------------------------------------------------------------------
# Make plot for scoreboards
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=[-0.6, len(country_give) - 1 + 0.6, -0.6, 24.6], projection="X15c/-10c", frame="wsne")

pygmt.makecpt(cmap="oslo", series=[0, max_points + 1, 1], reverse=True)

country_place = []
country_sum = []
for i_country_temp, country_temp in enumerate(country_recieve):

    df_sb_temp = df_sb[df_sb["country"]==country_temp]
    df_sb_temp[country_temp] = np.nan  # A country can not vote for itself

    array_sb_temp = df_sb_temp[country_give].values.squeeze()
    y = [i_country_temp] * len(array_sb_temp)

    # Plot squares with color-coding for points
    fig.plot(
        x=x,
        y=y,
        fill=array_sb_temp,
        style="s0.6c",
        pen="0.1p,gray90",
        cmap=True,
    )

# -----------------------------------------------------------------------------
    # NaN cannot be converted to int type directly
    # Int64 does not work as proposed by the docs ???
    if add_numbers == True:
        array_sb_temp_int = array_sb_temp.astype(int)
        list_sb_temp_int = array_sb_temp_int.tolist()
        for i_value, value in enumerate(list_sb_temp_int):
            if value == -9223372036854775808:
                list_sb_temp_int[i_value] = 'X'

        # Add number of points as text in the middle of the squares
        fig.text(
            text=list_sb_temp_int,
            x=x,
            y=y,
            font=f"5p,1,{color_hl}",
        )

# -----------------------------------------------------------------------------
    # Build list for y axis
    place_temp = df_sb_temp["place"].values.squeeze()
    country_place.append(place_temp)
    sum_temp = df_sb_temp["sum"].values.squeeze()
    country_sum.append(sum_temp)

# -----------------------------------------------------------------------------
# Text for x axis
fig.text(
    text=country_give,
    x=x,
    y=[-1] * len(country_give),
    angle=90,
    justify="LM",
    font="8p,black",
    no_clip=True,
)

# Text for y axis
for text_recieve, x_text in zip(
    [country_sum, country_place, country_recieve], [-1, -3, -4.5]
):
    fig.text(
        text=text_recieve,
        x=[x_text] * len(country_recieve),
        y=df_sb.index.tolist(),
        justify="RM",
        font="8p,black",
        no_clip=True,
    )

# Label for event, year and included voting group
for text_label, y_offset, font_size in zip(
    ["ESC", f"{year} | {group}"], [1.1, 0.65], [11, 11.5]
):
    fig.text(
        text=text_label,
        position="TL",
        justify="LM",
        offset=f"-2.6c/{y_offset}c",
        font=f"{font_size}p,1,{color_hl}",
        no_clip=True,
    )

# -----------------------------------------------------------------------------
# Add colorbar
with pygmt.config(MAP_FRAME_PEN="0.1p,gray50"):
    fig.colorbar(
        frame="y+lpoints", equalsize=cb_gap, position="+nno permission to vote"
    )

if add_numbers == True:
    fig.text(
        text="X",
        position="BL",
        offset=f"{x_nan_offset}c/-0.99c",
        justify="MC",
        font="8p,black",
        no_clip=True,
    )

# -----------------------------------------------------------------------------
fig.show()
fig_name = f"esc_final_{year}_scoreboard_{group}"
# for ext in ["png"]: #, "pdf"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
