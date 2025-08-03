# #############################################################################
# Plot custom symbols with PyGMT
# - General syntax of the argument passed to the "style" parameter (-S flag):
#   k<name_of_symbol_file>/<size_of_symbol>
# - Wind turbine symbol file: windturbine_yf.def (included in this folder)
# - Please note: Custom symbols cannot be used in a auto-legend yet
# -----------------------------------------------------------------------------
# Macro language to set up own custom symbols: GMT documentation at
#   https://docs.generic-mapping-tools.org/6.6/reference/custom-symbols.html#the-macro-language
# -----------------------------------------------------------------------------
# History
# - Created: 2024/05/16
# - Updated: 2025/08/02 - Add more symbols
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


import pygmt as gmt


fig = gmt.Figure()
fig.basemap(region=[-5, 5, -3.5, 5], projection="X10c/6c", frame=0)

fig.plot(x=-3, y=1, style="kwindturbine_yf.def/1c", fill="darkgray", pen="black")
fig.plot(x=-1, y=1, style="kwindturbine_yf.def/0.5c", fill="darkgray", pen="black")
fig.plot(x=1, y=1, style="kwindturbine_yf.def/0.5c", fill="black", pen="black")
fig.plot(x=3, y=1, style="kwindturbine_yf.def/1c", fill="lightgray", pen="gray30")

fig.plot(x=-4, y=-1, style="kearthquake_yf.def/1c", fill="darkred")
fig.plot(x=-2, y=-1, style="kmarker_yf.def/1c", fill="steelblue")
fig.plot(x=0, y=-1, style="kpinetree_yf.def/1c", fill="darkgreen")
fig.plot(x=2, y=-1, style="kpoplar_yf.def/1c", fill="seagreen")
fig.plot(x=4, y=-1, style="ktree_circle_yf.def/1c", fill="lightgreen")

fig.plot(x=2, y=-3, style="kflower_square_yf.def/1c", fill="purple")
fig.plot(x=4, y=-3, style="kflower_circle_yf.def/1c", fill="darkred")

# Mark plotting points
fig.plot(
    x=[-3, -1, 1, 3, -4, -2, 0, 2, 4, 2, 4],
    y=[1, 1, 1, 1, -1, -1, -1, -1, -1, -3, -3],
    style="x0.2c",
    fill="255/90/0",
)

fig.show()
# fig.savefig(fname="custom_symbols.png")
