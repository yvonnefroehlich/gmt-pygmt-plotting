# #############################################################################
# UEFA WOMEN'S EURO 2025 - logo
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2025/07/07
#   PyGMT v0.16.0 / dev -> https://www.pygmt.org/v0.16.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


import pygmt


path_out = "02_out_figs"
fig_name = "euro25_01_logo"
dpi_png = 720

size = 5

dia_in = 1.4
dia_out = 2.3
dia_diff = dia_out - dia_in

col_letter = "0/160/201"
pen_letter = f"0.1p,{col_letter}"
args_letter = {"y": 0, "fill": col_letter, "pen": pen_letter}


fig = pygmt.Figure()
fig.basemap(region=[-size, size] * 2, projection=f"X{size * 2}/{size}", frame=0)

fig.plot(x=-3, style=f"w{dia_out}/60/160+i{dia_in}", **args_letter)
fig.plot(x=-3, style=f"w{dia_in}/160/200+i{dia_in - dia_diff}", **args_letter)
fig.plot(x=-3, style=f"w{dia_out}/200/310+i{dia_in}", **args_letter)

fig.plot(x=-1.2, style=f"w{dia_out}/140/400+i{dia_in}", **args_letter)

fig.plot(x=1.3, style=f"w{dia_out}/60/215+i{dia_in}", **args_letter)

fig.plot(x=3, style=f"w{dia_out}/45/385+i{dia_in}", **args_letter)

fig.show()
for ext in ["png"]: # "pdf", "eps"
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
