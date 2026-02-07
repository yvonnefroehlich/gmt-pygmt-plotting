# #############################################################################
# Logo Olympics
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
import numpy as np

path_out = "02_out_figs"

# Diagonal length of the square
dgnl_sqr = 4
dgnl_sqr_h = dgnl_sqr / 2
# Size length of the square
size_sqr = np.sin(45 * 2 * np.pi / 360) * dgnl_sqr
# Outer circle with equal circumference as the square
r_out = 2 * size_sqr / np.pi
d_out = r_out * 2

# Vertical shift for lower row with the two circles
y_shift = (dgnl_sqr / 2 - r_out) * 2
# Inner circle
r_in = r_out - y_shift
d_in = r_in * 2

# Wedge with inner radius to create rings
style = f"w{d_out}/0/360+i{d_in}"

# Dimensions of plot
xlim = (dgnl_sqr * 3 / 2) + 0.5
ylim = dgnl_sqr
region = [-xlim, xlim, -ylim, ylim]
projection = f"X{xlim * 2}c/{2 * ylim}c"

# Colors taken from https://www.flagcolorcodes.com/olympic-rings-flag
# last accessed on 2026/02/06
blue = "0/129/200"
black = "black"
red = "238/51/78"
yellow = "252/177/49"
green = "0/166/81"

# Pen for the square
pen_sqr = "1p,darkbrown,4_2"


# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=region, projection=projection, frame="a1g0.5")

# Squares for construction
fig.plot(x=-dgnl_sqr, y=0, style=f"d{dgnl_sqr}c", pen=f"1p,{blue},4_2")
fig.plot(x=0, y=0, style=f"d{dgnl_sqr}c", pen=f"1p,{black},4_2")
fig.plot(x=dgnl_sqr, y=0, style=f"d{dgnl_sqr}c", pen=f"1p,{red},4_2")
fig.plot(x=-dgnl_sqr_h, y=-dgnl_sqr_h + y_shift, style=f"d{dgnl_sqr}c", pen=f"1p,{yellow},4_2")
fig.plot(x=dgnl_sqr_h, y=-dgnl_sqr_h + y_shift, style=f"d{dgnl_sqr}c", pen=f"1p,{green},4_2")

# Rings
fig.plot(x=-dgnl_sqr, y=0, style=style, pen=f"0.5p,{blue}")
fig.plot(x=0, y=0, style=style, pen=f"0.5p,{black}")
fig.plot(x=dgnl_sqr, y=0, style=style, pen=f"0.5p,{red}")
fig.plot(x=-dgnl_sqr_h, y=-dgnl_sqr_h + y_shift, style=style, pen=f"0.5p,{yellow}")
fig.plot(x=dgnl_sqr_h, y=-dgnl_sqr_h + y_shift, style=style, pen=f"0.5p,{green}")

fig.show()


# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=region, projection=projection, frame="+n")

# Rings
fig.plot(x=-dgnl_sqr, y=0, style=style, fill=blue)
fig.plot(x=0, y=0, style=style, fill=black)
fig.plot(x=dgnl_sqr, y=0, style=style, fill=red)
fig.plot(x=-dgnl_sqr_h, y=-dgnl_sqr_h + y_shift, style=style, fill=yellow)
fig.plot(x=dgnl_sqr_h, y=-dgnl_sqr_h + y_shift, style=style, fill=green)

# Ring sectors
fig.plot(x=-dgnl_sqr, y=0, style=f"w{d_out}/-30/10+i{d_in}", fill=blue)
fig.plot(x=0, y=0, style=f"w{d_out}/-20/10+i{d_in}", fill=black)
fig.plot(x=0, y=0, style=f"w{d_out}/240/270+i{d_in}", fill=black)
fig.plot(x=dgnl_sqr, y=0, style=f"w{d_out}/240/270+i{d_in}", fill=red)

fig.show()
fig.savefig(fname=f"{path_out}/01_logo_olympics.png")
