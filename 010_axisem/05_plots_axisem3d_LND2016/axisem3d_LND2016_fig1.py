# #############################################################################
# Reproduce Figure 1 of
# Leng K., Nissen-Meyer T., van Driel M. (2016). Efficient global wave propagation
# adapted to 3-D structural complexity: a pseudospectral/spectral-element approach.
# Geophysical Journal International, 207(3), 1700–1721.
# https://doi.org/10.1093/gji/ggw363.
# -----------------------------------------------------------------------------
# History
# - Created: 2025/05/07
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.11.0 - v0.14.2 -> https://www.pygmt.org/v0.14.2/ | https://www.pygmt.org/
# - GMT 6.4.0 - 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_out = "02_out_figs"

color_highlight = "255/90/0"  # -> orange | URG
color_source = "red"
color_slice = "steelblue"
color_equ = "darkred"

width = 8


# %%
# -----------------------------------------------------------------------------
# Make plot
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray80")
fig.basemap(region="g", projection=f"G0/0/{width}c", frame=0)

fig.plot(x=0, y=0, style=f"e90/{width}/7.3", fill=f"{color_slice}@70", pen=f"1p,{color_slice},4_2")
fig.plot(x=0, y=0, style=f"w{width}/90/-90", fill="white")
fig.plot(x=[0, 0], y=[-89, 89], pen=f"1p,{color_highlight}")
fig.plot(x=0, y=0, style=f"e0/{width}/2.5", fill=f"{color_equ}@70", pen=f"1p,{color_equ},4_2")

fig.plot(x=0, y=65, style="a0.5c", fill="red", pen="0.3p,gray10")

fig.plot(data=[[0, 0, 1.05, 57.5, 90]], style="m0.2c+b+a40+h0+gblack", pen="1p,black")
fig.plot(x=0, y=0, style="v0.2c+e+a40+h0+gblack", pen="1p,black", direction=[57.5, 2.8])

fig.plot(x=[0, 65], y=[0, -7], pen="0.8p,black,1_1")
fig.plot(x=[0, 28], y=[40, 36], pen="0.8p,black,1_1", straight_line=True)
fig.plot(x=[28, 22.5], y=[36, -3], pen="0.8p,black,1_1", straight_line=True)

fig.text(x=-25, y=64, text="source", font=f"8p,Helvetica-Bold,{color_source}")
fig.text(x=25, y=-40, text="slice plane", font=f"10p,Helvetica-Bold,{color_slice}")
fig.text(x=-35, y=1, text="equatorial plane", font=f"10p,Helvetica-Bold,{color_equ}")
fig.text(x=-25.5, y=49, text="azimuth", font=f"8p,Helvetica-Bold,{color_highlight}")

fig.text(x=-2.3, y=0, text="o", font="12p,6")
fig.text(x=31.23, y=37.5, text="r", font="12p,6")
fig.text(x=2.35, y=8.5, text="@~q@~", font="12p,6")
fig.text(x=10, y=52, text="@~f@~", font=f"12p,6,{color_highlight}")

fig.basemap(frame=0)

fig.shift_origin(yshift="5.6c")
fig.plot(data=[[0, 0, 0.5, -295, -43]], style=f"m0.3c+e+a40+h0+g{color_highlight}", pen=f"1p,{color_highlight}", perspective=[180, 20], no_clip=True)

fig.show()
fig_name = "axisem3d_LND2016_fig1"
# for ext in ["png"]: #, "pdf"]:
#     fig.savefig(fname = f"{path_out}/{fig_name}.{ext}")
print(fig_name)
