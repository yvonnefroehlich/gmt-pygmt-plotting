# #############################################################################
# Plot wind turbine symbol with PyGMT
# - Wind turbine symbol file: windturbine_YF.def (included in this folder)
# - General syntax of the argument passed to the "style" parameter (-S flag):
#   k<name_of_symbol_file>/<size_of_symbol>
# - Please note: Custom symbols cannot be used in a auto-legend yet
# -----------------------------------------------------------------------------
# History
# - Created: 2024/05/16
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.12.0 -> https://www.pygmt.org/v0.12.0/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt as gmt

fig = gmt.Figure()
fig.basemap(region=[-1, 1, -0.1, 1.5], projection="X8c/3c", frame=0)

fig.plot(x=-0.75, y=0, style="kwindturbine_YF.def/1c", fill="darkgray", pen="black")

fig.plot(x=-0.25, y=0, style="kwindturbine_YF.def/0.5c", fill="darkgray", pen="black")

fig.plot(x=0.25, y=0, style="kwindturbine_YF.def/0.5c", fill="black", pen="black")

fig.plot(x=0.75, y=0, style="kwindturbine_YF.def/1c", fill="lightgray", pen="gray30")

fig.show()
# fig.savefig(fname="windturbine.png")
