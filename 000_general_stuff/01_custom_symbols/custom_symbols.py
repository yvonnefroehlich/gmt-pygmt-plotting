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
# - Updated: 2025/08/02 - Add symbols for earthquake, marker, trees
# - Updated: 2025/08/03 - Add symbols for flowers
# - Updated: 2025/08/13 - Add symbol for lens
# - Updated: 2026/05/10 - Add symbol for olivine crystal, improve symbol for lens
# - Updated: 2026/08/29 - Re-organize example plot, improve some symbols
# - Updated: 2026/08/29 - Add landslide symbol
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


import pygmt as gmt

size = 8
color_hl = "255/90/0"  # highlight -> orange
x_mark = [-3, 0, 3, 6, -6, -3, 0, 3, 6, -6, -3, 0, 3, 6, -6, -3, 0, 3, 6]
y_mark = [6, 6, 6, 6, 2, 2, 2, 2, 2, -2, -2, -2, -2, -2, -6, -6, -6, -6, -6]


fig = gmt.Figure()
fig.basemap(region=[-size, size] * 2, projection=f"X{size}c/{size}c", frame=[0,"+gbisque"])

# Mark 1 by 1 boxes
fig.plot(x=x_mark, y=y_mark, style="s1.47c", pen="0.5p,steelblue,4_2")
fig.plot(x=x_mark, y=y_mark, style="+1c", pen="0.2p,steelblue,2_2")

# Plot symbols from top to bottom and left to right
fig.plot(x=0, y=6, style="kradioactivity_circle_yf.def/1c")
fig.plot(x=3, y=6, style="kradioactivity_triangle_yf.def/1c")
fig.plot(x=6, y=6, style="kcnd_yf.def/1c")

fig.plot(x=-6, y=2, style="kwindturbine_yf.def/1c", fill=color_hl, pen=True)
fig.plot(x=-0, y=2, style="kmarker_yf.def/1c", fill=color_hl)
fig.plot(x=3, y=2, style="klens_yf.def/1c", pen=f"2p,{color_hl}")

fig.plot(x=-6, y=-2, style="kvolcano/1c", fill=color_hl)  # not self-created
fig.plot(x=-3, y=-2, style="kvolcano_sleeping.def/1c", fill=color_hl)  # not self-created
fig.plot(x=-0, y=-2, style="kearthquake_yf.def/1c", fill=color_hl)
fig.plot(x=3, y=-2, style="klandslide_yf.def/1c", fill=color_hl)
fig.plot(x=6, y=-2, style="kolivine_crystal_yf.def/1c")

fig.plot(x=-6, y=-6, style="kflower_square_yf.def/1c", fill=color_hl)
fig.plot(x=-3, y=-6, style="kflower_circle_yf.def/1c", fill=color_hl)
fig.plot(x=0, y=-6, style="kpinetree_yf.def/1c", fill=color_hl)
fig.plot(x=3, y=-6, style="kpoplar_yf.def/1c", fill=color_hl)
fig.plot(x=6, y=-6, style="ktree_circle_yf.def/1c", fill=color_hl)

# Mark plotting points
fig.plot(x=x_mark, y=y_mark, style="x0.2c", fill="steelblue")

fig.show()
# fig.savefig(fname="custom_symbols.png")
