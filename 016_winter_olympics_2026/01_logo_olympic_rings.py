# #############################################################################
# Olympic rings
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

y = 0.75
x_out = 3.25
x_in = 1.65

r_out = 3
r_in = 2.5
style = f"w{r_out}/0/360+i{r_in}"

# colors taken from: https://www.flagcolorcodes.com/olympic-rings-flag
# last accessed: 2026/02/06
blue = "0/129/200"
black = "black"
red = "238/51/78"
yellow = "252/177/49"
green = "0/166/81"

# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -2.5, 2.5], projection="X10c/5c", frame="+n")

fig.plot(x=-x_out, y=y, style=style, fill=blue)
fig.plot(x=0, y=y, style=style, fill=black)
fig.plot(x=x_out, y=y, style=style, fill=red)
fig.plot(x=-x_in, y=-y, style=style, fill=yellow)
fig.plot(x=x_in, y=-y, style=style, fill=green)

fig.plot(x=-x_out, y=y, style=f"w{r_out}/-30/5+i{r_in}", fill=blue)
fig.plot(x=0, y=y, style=f"w{r_out}/-20/10+i{r_in}", fill=black)
fig.plot(x=0, y=y, style=f"w{r_out}/250/270+i{r_in}", fill=black)
fig.plot(x=x_out, y=y, style=f"w{r_out}/250/270+i{r_in}", fill=red)

fig.show()
fig.savefig(fname=f"{path_out}/01_logo_olympic_rings.png")
