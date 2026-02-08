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

# Geometry taken from https://www.paralympic.org/sites/default/files/2022-08/2022_08%20Paralympic%20Symbol%20Guidelines.pdf
# last accessed on 2026/02/07
# Manually measured and used to calculate the ratios
# axis_minor = 2.2
# axis_major = 3.7
# x_shift = 0.35
# y_shift = 0.5
# x_rot = 0.6
# y_rot = 1.6

axis_minor = 1.5  # <<< change for desired size of the logo
axis_major = axis_minor * (3.7 / 2.2)
style = f"e90/{axis_major * 2}/{axis_minor * 2}"
x_shift = axis_minor * (0.35 / 2.2) * 2
y_shift = axis_major * (0.5 / 3.7) * 2
x_rot = axis_minor * (0.6 / 2.2) * 2
y_rot = axis_minor * (1.6 / 2.2) * 2
rot_center = f"{x_rot}/{y_rot}"

args_ell = {"x": 0, "y": 0, "style": style}
args_overlay = {"x": x_shift, "y": y_shift, "style": style, "perspective": True}

# Plot dimensions
xy_lim = axis_minor * 3.5
region = [-xy_lim, xy_lim, -xy_lim, xy_lim]
projection = f"X{xy_lim * 2}c/{xy_lim * 2}c"

# Colors taken from https://colorswall.com/palette/7932
# last accessed on 2026/02/07
red = "170/39/47"
blue = "0/83/159"
green = "0/133/66"


# %%
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=region, projection=projection, frame="a1g1")

fig.plot(pen=f"1p,{red}", perspective=f"-60+w{rot_center}", **args_ell)
fig.plot(fill="white@50", pen=f"1p,{red},4_2", **args_overlay)

fig.plot(pen=f"1p,{blue}", perspective=f"0+w{rot_center}", **args_ell)
fig.plot(fill="white@50", pen=f"1p,{blue},4_2", **args_overlay)

fig.plot(pen=f"1p,{green}", perspective=f"60+w{rot_center}", **args_ell)
fig.plot(fill="white@50", pen=f"1p,{green},4_2", **args_overlay)

fig.vlines(x=0, pen="1p,orange,4_2")
fig.hlines(y=0, pen="1p,orange,4_2")
fig.plot(x=x_rot, y=y_rot, style="x0.4c", pen="1p,orange")

fig.show()
fig.savefig(fname=f"{path_out}/02_logo_paralympics_constraction.png")


# %%
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=region, projection=projection, frame="+n")

fig.plot(fill=red, perspective=f"-60+w{rot_center}", **args_ell)
fig.plot(fill="white", **args_overlay)

fig.plot(fill=blue, perspective=f"0+w{rot_center}", **args_ell)
fig.plot(fill="white", **args_overlay)

fig.plot(fill=green, perspective=f"60+w{rot_center}", **args_ell)
fig.plot(fill="white", **args_overlay)

fig.show()
fig.savefig(fname=f"{path_out}/02_logo_paralympics.png")
