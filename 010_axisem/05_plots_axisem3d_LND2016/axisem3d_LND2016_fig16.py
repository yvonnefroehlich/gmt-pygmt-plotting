# #############################################################################
# Reproduce Figure 16 of
# Leng K., Nissen-Meyer T., van Driel M. (2016). Efficient global wave propagation
# adapted to 3-D structural complexity: a pseudospectral/spectral-element approach.
# Geophysical Journal International, 207(3), 1700–1721.
# https://doi.org/10.1093/gji/ggw363.
# -----------------------------------------------------------------------------
# History
# - Created: 2025/05/07
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.16.0 - v0.18.0 -> https://www.pygmt.org
# - GMT 6.4.0 - 6.6.0 -> https://www.generic-mapping-tools.org
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

size_ratio = 4.4 / 7.8
width = 12

size = "0.225c"
pen = "0.3p,gray10"
color_highlight = "255/90/0"  # -> orange | URG paper
box_standard = "+ggray95@30+p0.1p,gray50+r1p"
args_leg = {"x":0 , "y":0, "pen":pen}

color_axisem = "steelblue"
color_specfem = "brown"
color_s362ani = "darkgreen"
color_s40rts = "green3"

symbol_axisem = "c"
symbol_specfem = "s"
symbol_s362ani = "t"
symbol_s40rts = "h"


# %%
# -----------------------------------------------------------------------------
# Read data values from plot
# -----------------------------------------------------------------------------
t_axisem = [2, 5, 11.3, 17]
t_specfem = [5, 11.3, 17, 34]
t_s362ani = [11.3, 17, 34]
t_s40rts = [11.3, 17, 34]

p_axisem = [98, 10.7, 2, 1]
p_specfem = [28000, 2000, 330, 73]
p_s362ani = [40, 11, 4.5]
p_s40rts = [25, 8, 3]


# %%
# -----------------------------------------------------------------------------
# Make plot
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray10,2_2")

with pygmt.config(
    FONT="10p",
    FONT_ANNOT_PRIMARY="8p",
    MAP_GRID_PEN_PRIMARY="0.1p,gray10,2_2",
    MAP_TICK_LENGTH_PRIMARY="6p",
):
    fig.basemap(
        region=[1.7, 40, 0.6, 50000],
        projection=f"X{width}cl/{width * size_ratio}cl",
        frame=["WrSt", "xa2f3g2+lseismic period / s", "ya1f3g+lnumber of processors"],
    )

# Plot decay lines and text
fig.plot(x=[2, 16], y=[98, 0.5], pen=f"0.5p,{color_highlight},4_2")
fig.plot(x=[5, 40], y=[28000, 10], pen=f"0.5p,{color_highlight},4_2")
fig.text(x=4.3, y=5.5, text="~@~w@~@+3@+", font=f"14p,Helvetica-Bold,{color_highlight}")
fig.text(x=8.2, y=1600, text="~@~w@~@+4@+", font=f"14p,Helvetica-Bold,{color_highlight}")

# Plot data points as lines
fig.plot(x=t_axisem, y=p_axisem, pen=f"0.6p,{color_axisem},")
fig.plot(x=t_specfem, y=p_specfem, pen=f"0.6p,{color_specfem}")
fig.plot(x=t_s362ani, y=p_s362ani, pen=f"0.6p,{color_s362ani}")
fig.plot(x=t_s40rts, y=p_s40rts, pen=f"0.6p,{color_s40rts}")

# Plot data points as symbols
fig.plot(x=t_axisem, y=p_axisem, fill=color_axisem, style=f"{symbol_axisem}{size}", pen=pen)
fig.plot(x=t_specfem, y=p_specfem, fill=color_specfem, style=f"{symbol_specfem}{size}", pen=pen)
fig.plot(x=t_s362ani, y=p_s362ani, fill=color_s362ani, style=f"{symbol_s362ani}{size}", pen=pen)
fig.plot(x=t_s40rts, y=p_s40rts, fill=color_s40rts, style=f"{symbol_s40rts}{size}", pen=pen)

# Create legend
fig.plot(fill=color_axisem, style=f"{symbol_axisem}{size}", label="AxiSEM", **args_leg)
fig.plot(fill=color_specfem, style=f"{symbol_specfem}{size}", label="SPECFEM", **args_leg)
fig.plot(fill=color_s362ani, style=f"{symbol_s362ani}{size}", label="AxiSEM3D s362ani", **args_leg)
fig.plot(fill=color_s40rts, style=f"{symbol_s40rts}{size}", label="AxiSEM3D s40rts", **args_leg)
fig.legend(position="jTL+w3.4c+o0.2c", box=box_standard)

# Save and show figure
fig.show()
fig_name = "axisem3d_LND2016_fig16"
# for ext in ["png"]: #, "pdf", "eps"]:
#     fig.savefig(fname = f"{path_out}/{fig_name}.{ext}")
print(fig_name)
