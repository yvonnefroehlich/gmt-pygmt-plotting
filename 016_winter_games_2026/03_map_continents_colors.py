# #############################################################################
# Global map with continents colored based on the colors of the Olympic rings
# -----------------------------------------------------------------------------
# History
# - Created: 2026/02/08
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

path_in = "01_in_data"
path_out = "02_out_figs"

# Cordinates of Cortina d'Ampezzo, Italia
lon_c = 12.1357  # deg East
lat_c = 46.5405  # deg North

color_hl = "255/90/0"  # -> orange
alpha = 60

# Colors taken from https://www.flagcolorcodes.com/olympic-rings-flag
# last accessed on 2026/02/06
blue = "0/129/200"
black = "black"
red = "238/51/78"
yellow = "252/177/49"
green = "0/166/81"


# %%
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
# fig.basemap(region="d", projection="N10c", frame=True)
fig.basemap(region="d", projection=f"E{lon_c}/{lat_c}/150/10c", frame=True)

fig.coast(shorelines="0.1p,gray")

# Fill countinents based on colors for the Olympic rings - takes very long
fig.coast(
    water="white",
    dcw=[
    # Europe
    f"=EU+g{blue}@{alpha}",
    # Africa
    f"=AF+g{black}@{alpha}",
    # North America
    f"=NA+g{red}@{alpha}",
    # South America
    f"=SA+g{red}@{alpha}",
    # Asia
    f"=AS+g{yellow}@{alpha}",
    # Oceania
    f"=OC+g{green}@{alpha}",
 ]
)

fig.plot(x=lon_c, y=lat_c, style=f"k{path_in}/marker_yf.def/0.3c", fill=color_hl)

fig.show()
fig.savefig(fname=f"{path_out}/03_map_continents_colors.png")
