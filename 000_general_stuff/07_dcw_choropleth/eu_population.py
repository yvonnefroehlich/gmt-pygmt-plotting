# #############################################################################
# Population in Europe: change between July 1st 1990 and 2023
# Source of data: UN population prospect 2024
# See also:
#   https://www.visualcapitalist.com/mapped-how-europes-population-has-changed-1990-2023/
#   last accessed 2025/07/17
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/07/17
#   PyGMT v0.16.0 / dev -> https://www.pygmt.org/v0.16.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


import pandas as pd
import pygmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"

color_neg = "darkorange"
color_pos = "darkgreen"
color_null = "white"

lon_min = -26
lon_max = 52
lat_min = 33
lat_max = 72

region = [lon_min, lon_max, lat_min, lat_max]
projection="M10c"


# %%
# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
data_file = "eu_population.txt"
df_pop_raw = pd.read_csv(f"{path_in}/{data_file}", sep="\t")

sort_by = "change_percent"  # "land", "change_percent"
df_pop = df_pop_raw.sort_values(sort_by, ignore_index=True)

abs_max_change = abs(max(df_pop["change_percent"]))


# %%
# -----------------------------------------------------------------------------
# Create map
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=region, projection=projection, frame=True)

for i_land in range(len(df_pop)):

    land = df_pop["land"][i_land]
    change = df_pop["change_percent"][i_land]

    # Creat simple diverging colormap via semi-transparency
    color_sign = color_pos
    if change < 0: color_sign = color_neg
    elif change == 0: color_sing = color_null
    color_trans = f"{color_sign}@{abs_max_change - abs(change)}"

    # Make a choropleth map using dcw
    fig.coast(dcw=f"{land}+g{color_trans}")

    # Plot dummy data points outside of study area for legend
    leg_head = " "
    if i_land == 0:
        leg_head = "+N2+HPopulation change 1990 - 2023+f11p"
    fig.plot(
        x=0,
        y=0,
        style="s0.4c",
        fill=color_trans,
        pen="0.1p,gray30",
        label=f"{land}: {change} %{leg_head}",
    )

    print(land)
    # fig.show()

# Add shorelines and political boundaries
fig.coast(shorelines="1/0.1p,gray60", borders="1/0.3p,white")

# Add legend
with pygmt.config(FONT="9p"):
    fig.legend(position="JRM+jLM+o0.2c/0c+w7.5c")

# Show and save figure
fig.show()
fig_name = f"eu_population_sorted_by_{sort_by}"
for ext in ["png"]: #, "pdf", "eps"]:
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
