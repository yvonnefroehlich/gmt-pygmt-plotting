# #############################################################################
# Map of Italy
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

region = [7, 15, 45.5, 48]


# %%
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=region, projection="M10c", frame="a1f0.25")

fig.grdimage(grid="@earth_relief_15s", region=region, cmap="oleron")

fig.plot(x=lon_c, y=lat_c, style="c0.25c", pen=f"1p,{color_hl}", fill="white")
fig.plot(x=lon_c, y=lat_c, style=f"k{path_in}/marker_yf.def/0.55c", fill=color_hl)

fig.show()
fig.savefig(fname=f"{path_out}/04_map_italy.png")
