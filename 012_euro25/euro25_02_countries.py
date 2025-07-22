# #############################################################################
# UEFA WOMEN'S EURO 2025 - group phase countries
# -----------------------------------------------------------------------------
# History
# - Created: 2025/07/07
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


import numpy as np
import pygmt


path_out = "02_out_figs"
fig_name = "euro25_02_countries"
dpi_png = 720

fig_width = "15c"

lon_min = -27
lon_max = 35
lat_min = 35
lat_max = 72
# Calcualte projection center
lon0_lamb = np.mean([lon_min, lon_max])
lat0_lamb = np.mean([lat_min, lat_max])
# Calculate two standard parallels (only these two distortion-free)
lat1_lamb = lat_min + (lat_max - lat_min) / 3
lat2_lamb = lat_min + (lat_max - lat_min) / 3 * 2

projection = f"L{lon0_lamb}/{lat0_lamb}/{lat1_lamb}/{lat2_lamb}/{fig_width}"
region = [lon_min, lon_max, lat_min, lat_max]

color_gra = "254/202/139"
color_grb = "242/111/111"
color_grc = "248/154/68"
color_grd = "127/210/232"

box_standard = "+gwhite@30+p0.1p,gray30+r2p"


fig = pygmt.Figure()
fig.basemap(projection=projection, region=region, frame=True)

fig.coast(
    dcw=[
        f"Switzerland,Norway,Iceland,Finland+g{color_gra}",
        f"Spain,Portugal,Belgium,Italy+g{color_grb}",
        f"Germany,Poland,Denmark,Sweden+g{color_grc}",
        f"France,GB,Netherlands+g{color_grd}",  # England, Wales in one group
    ]
)
fig.coast(shorelines="1/0.1p,gray30", borders="1/0.2p,gray20")

# Plot dummy data points for legend
args_leg = {"x": 0, "y": 0, "style": "s0.4c", "pen": "0.1p,gray30"}
fig.plot(fill=color_gra, **args_leg, label="group A")
fig.plot(fill=color_grb, **args_leg, label="group B")
fig.plot(fill=color_grc, **args_leg, label="group C")
fig.plot(fill=color_grd, **args_leg, label="group D")
with pygmt.config(FONT="8p"):
    fig.legend(box=box_standard, position="jLB+o1.3c+w2c")

fig.show()
for ext in ["png"]: # "pdf", "eps"
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
