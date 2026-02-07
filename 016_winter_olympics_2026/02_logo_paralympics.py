# #############################################################################
# Logo Paralympics
# -----------------------------------------------------------------------------
# History
# - Created: 2026/02/06
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

path_out = "02_out_figs"

# source: https://www.paralympic.org/sites/default/files/2022-08/2022_08%20Paralympic%20Symbol%20Guidelines.pdf
axis_minor = 2.2
axis_major = 3.7
x_shift = 0.35
y_shift = 0.5
x_rot = 0.6
y_rot = 1.6
rot_center = f"{x_rot}/{y_rot}"
style = f"e90/{axis_major}/{axis_minor}"

args_ell = {"x": 0, "y": 0, "style": style}
args_overlay = {
    "x": x_shift,
    "y": y_shift,
    "style": style,
    "fill": "white", #"@50",
    "perspective": True,
    # "pen": True
}

# Plot dimensions
xy_lim = 4
region = [-xy_lim, xy_lim, -xy_lim, xy_lim]
projection = f"X{xy_lim * 2}c/{xy_lim * 2}c"

# Colors taken from https://colorswall.com/palette/7932
# last accessed on 2026/02/07
red = "170/39/47"
blue = "0/83/159"
green = "0/133/66"


# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=region, projection=projection, frame="+n")

fig.plot(fill=red, perspective=f"-60+w{rot_center}", **args_ell)
fig.plot(**args_overlay)

fig.plot(fill=blue, perspective=f"0+w{rot_center}", **args_ell)
fig.plot(**args_overlay)

fig.plot(fill=green, perspective=f"60+w{rot_center}", **args_ell)
fig.plot(**args_overlay)

# fig.vlines(x=0, pen="1p,orange,2_4")
# fig.hlines(y=0, pen="1p,orange,2_4")
# fig.plot(x=x_rot, y=y_rot, style="x0.2c", pen="1p,orange")

fig.show()
fig.savefig(fname=f"{path_out}/02_logo_paralympics.png")
