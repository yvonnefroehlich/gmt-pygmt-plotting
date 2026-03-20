# #############################################################################
# Ritter et al. (2022), Seismol: Figure S4
# Piercing points in the lowermost mantle at 2700 km for shear wave splitting
# measurements at the Black Forest Observatory (BFO)
# -----------------------------------------------------------------------------
# Ritter J R R, Fröhlich Y, Sanz-Alonso Y, Grund M (2022).
# Short-scale laterally varying SK(K)S shear wave splitting at BFO, Germany –
# implications for the determination of anisotropic structures.
# Journal of Seismology, 26:1137-1156.
# https://doi.org/10.1007/s10950-022-10112-w,
# correction https://doi.org/10.1007/s10950-023-10136-w.
# -----------------------------------------------------------------------------
# History
# - Original Jupyter notebook
#   https://github.com/yvonnefroehlich/gmt-pygmt-plotting/blob/main/001_paper_RFSG_2022/Figure_S4/RFSG_FigS4_right_pairs.ipynb
# - Converted to Python script: 2026/03/20
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

# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
myfontsize = "9p"
dpi_png = 360  # resolution in dpi of output figure for PNG format
dpi_jn = 100  # resolution in dpi for display in this Jupyter notebook
fname_fig_out = "RFSG_FigS4_right_pairs"  # name of output figure

# -----------------------------------------------------------------------------
# Coordinates of recording station Black Forest Observatory BFO
lon_BFO = 8.330  # degrees East
lat_BFO = 48.331  # degrees North

# -----------------------------------------------------------------------------
# Plate boundaries after Bird 2003
file_pb = "plate_boundaries_Bird_2003.txt"

# -----------------------------------------------------------------------------
# Colors
color_land = "gray90"  # gray hue -> light gray
color_pb = "216.750/82.875/24.990"  # plate boundaries -> dark orange
color_station_symbol = "255/215/0"  # = "gold"
color_station_label = "162/20/47"  # -> dark red
color_null = "white"

color_SKS_nodisc = "gray50"
color_SKKS_nodisc = "gray50"
color_SKS_disc = "205/0/0"  # -> red
color_SKKS_disc = "238/118/0"  # -> orange

color_line = "gray50"
color_pp_K = color_SKS_nodisc
color_pp_KK = color_SKKS_nodisc
color_pp_N = color_null

# -----------------------------------------------------------------------------
# Piercing points
marker_size_pp_nodisc = "0.1c"  # centimeters
marker_size_pp_disc = "0.1c"
line_width_pp_nodisc = "0.2p"  # points
line_width_pp_disc = "0.2p"
outline_width_pp = "0.6p"
alpha_pp = "@30"  # transparency in percentage (0 equals opaque)
incols_pp = [7, 8]  # order of input columns, zero-based indexing

# -----------------------------------------------------------------------------
# Box around map scale, legends, colorbars
# +g fill color
# +p outline thickness and color
# +r rounded edges
box_standard = "+gwhite@30+p0.8p,black+r"

# -----------------------------------------------------------------------------
# Define projection center
lon0_lamb = 7  # degrees East
lat0_lamb = 48  # degrees North

# Define standard parallels (only these two are distortion-free)
lat1_lamb = 45  # degrees North
lat2_lamb = 55

# Define width of map
width_lamb = "15c"  # 15 centimeters

# Lambert Conic Conformal Projection
projection = f"L{lon0_lamb}/{lat0_lamb}/{lat1_lamb}/{lat2_lamb}/{width_lamb}"

# Region
lonmin_lamb = -35  # degrees East
lonmax_lamb = abs(lonmin_lamb) + 2 * lon0_lamb  # symmetric around lon0
latmin_lamb = 25  # degrees North
latmax_lamb = 70
region = [lonmin_lamb, lonmax_lamb, latmin_lamb, latmax_lamb]


# %%
# -----------------------------------------------------------------------------
# Create geographic map
# -----------------------------------------------------------------------------
# Create an instance or object of the pygmt.Figure class.
# In the following steps various plotting elements are added in a stacking fashion.
fig = gmt.Figure()
gmt.config(MAP_GRID_PEN="0.01p,gray50")

# Generate a basic map
# a annotations, here every 10 degrees
# g grid lines, here every 10 degrees
# f frame / ticks, here every 5 degrees
# wSnE annotations at South and East boundaries
frame = ["a10g10f5", "wSnE"]

fig.basemap(projection=projection, region=region, frame=0)
fig.coast(
    land=color_land,
    resolution="h",  # high
    area_thresh="30000",
    shorelines="black",
)
fig.basemap(frame=frame)

# Plot the plate boundaries by Bird 2003
fig.plot(data=file_pb, pen=f"0.8p,{color_pb}")

fig.show()


# %%
# -----------------------------------------------------------------------------
# Plot connection lines between related SKS and SKKS phases (SKS-SKKS pairs).
path_conect = "data_FigS4_right_pairs/"

# DISCREPANT
# SKKS split and SKS null
fig.plot(
    data=f"{path_conect}BFO_disc_pp2700km_KKNN2KN_all.txt",
    pen=f"{line_width_pp_disc},{color_line}",
)
# SKKS null and SKKS split
fig.plot(
    data=f"{path_conect}BFO_disc_pp2700km_KKN2KNN_all.txt",
    pen=f"{line_width_pp_disc},{color_line}",
)

# SAME
# SKKS null and SKS null
fig.plot(
    data=f"{path_conect}BFO_same_pp2700km_KKN2KN_all.txt",
    pen=f"{line_width_pp_nodisc},{color_line}",
)
# SKKS split and SKS split
fig.plot(
    data=f"{path_conect}BFO_same_pp2700km_KKNN2KNN_all.txt",
    pen=f"{line_width_pp_nodisc},{color_line}",
)

fig.show()


# %%
# -----------------------------------------------------------------------------
# Plot the piercing points in 2700 km depth.
# Externally and previously calculated after the iasp91 Earth model.
data_same_pp_same = "data_FigS4_right_pairs/BFO_same_pp2700km_"
data_same_K_N_pp = f"{data_same_pp_same}K_sp_N_all.txt"
data_same_K_NN_pp = f"{data_same_pp_same}K_sp_NN_all.txt"
data_same_KK_N_pp = f"{data_same_pp_same}KK_sp_N_all.txt"
data_same_KK_NN_pp = f"{data_same_pp_same}KK_sp_NN_all.txt"

data_disc_pp_same = "data_FigS4_right_pairs/BFO_disc_pp2700km_"
data_disc_K_N_pp = f"{data_disc_pp_same}K_sp_N_all.txt"
data_disc_K_NN_pp = f"{data_disc_pp_same}K_sp_NN_all.txt"
data_disc_KK_N_pp = f"{data_disc_pp_same}KK_sp_N_all.txt"
data_disc_KK_NN_pp = f"{data_disc_pp_same}KK_sp_NN_all.txt"

# SAME both null
# null, SKS
fig.plot(
    data=data_same_K_N_pp,
    style=f"C{marker_size_pp_nodisc}",  # circle
    fill=color_pp_N,  # before PyGMT v0.8.0 "color"
    pen=f"{outline_width_pp},{color_pp_K}",  # outline thickness and color
    incols=incols_pp,  # order of input columns, zero-based indexing
)
# null, SKKS
fig.plot(
    data=data_same_KK_N_pp,
    style=f"S{marker_size_pp_nodisc}",  # square
    fill=color_pp_N,  # before PyGMT v0.8.0 "color"
    pen=f"{outline_width_pp},{color_pp_KK}",
    incols=incols_pp,
)

# SAME both split
# split, SKS
fig.plot(
    data=data_same_K_NN_pp,
    style=f"C{marker_size_pp_nodisc}",
    fill=color_pp_K,  # before PyGMT v0.8.0 "color"
    pen=f"{outline_width_pp},black",
    incols=incols_pp,
)
# split, SKKS
fig.plot(
    data=data_same_KK_NN_pp,
    style=f"S{marker_size_pp_nodisc}",
    fill=color_pp_KK,  # before PyGMT v0.8.0 "color"
    pen=f"{outline_width_pp},black",
    incols=incols_pp,
)

# DISCREPANT null
# null, SKS
fig.plot(
    data=data_disc_K_N_pp,
    style=f"C{marker_size_pp_disc}",
    fill=color_pp_N,  # before PyGMT v0.8.0 "color"
    pen=f"{outline_width_pp},{color_SKS_disc}",
    incols=incols_pp,
)
# null, SKKS
fig.plot(
    data=data_disc_KK_N_pp,
    style=f"S{marker_size_pp_disc}",
    fill=color_pp_N,  # before PyGMT v0.8.0 "color"
    pen=f"{outline_width_pp},{color_SKKS_disc}",
    incols=incols_pp,
)

# DISCREPANT split
# split, SKS
fig.plot(
    data=data_disc_K_NN_pp,
    style="J",  # orientated rectangle
    fill="black",  # before PyGMT v0.8.0 "color"
    pen="0.05p,white",
    incols="7,8,9,10+s250,13+s150",
)
# split, SKKS
fig.plot(
    data=data_disc_KK_NN_pp,
    style="J",
    fill="black",  # before PyGMT v0.8.0 "color"
    pen="0.05p,white",
    incols="7,8,9,10+s250,13+s150",
)
# split, SKS
fig.plot(
    data=data_disc_K_NN_pp,
    style=f"C{marker_size_pp_disc}",  # circle
    fill=color_SKS_disc,  # before PyGMT v0.8.0 "color"
    pen=f"{outline_width_pp},black",
    incols=incols_pp,
)
# split, SKKS
fig.plot(
    data=data_disc_KK_NN_pp,
    style=f"S{marker_size_pp_disc}",
    fill=color_SKKS_disc,  # before PyGMT v0.8.0 "color"
    pen=f"{outline_width_pp},black",
    incols=incols_pp,
)

fig.show()


# %%
# -----------------------------------------------------------------------------
# Recording station BFO
# Add symbol
fig.plot(
    x=lon_BFO,
    y=lat_BFO,
    style="i0.3c",  # inverse triangle
    fill=color_station_symbol,  # before PyGMT v0.8.0 "color"
    pen="1p,black",
)
# Add station code
fig.text(
    x=lon_BFO,
    y=49.020,
    text="BFO",
    font=f"9p,Helvetica-Bold,{color_station_label}",
    offset="0c/0.3c",  # x/y
    fill="white@30",
    clearance="+tO",  # rounded edges of box
)

# -----------------------------------------------------------------------------
# Add legend for symbols of SKS-SKKS pairs
# J reference point, here outside of map bounding box Left Top
# +j anchor point, here Left Top
# +w width, here in centimeters
# +o offset x/y, here in centimeters
leg_pos_pp = "JLT+jLT+w2.4c+o0c/-0.5c"
leg_file_pp = "legend_gmt_pairs.txt"
fig.legend(spec=leg_file_pp, position=leg_pos_pp, box=box_standard)

# Add legend for length of delay time
leg_pos_dt = "JMT+jLT+o-1.4c/0c"
leg_file_dt = "legend_gmt_dt.txt"
fig.legend(spec=leg_file_dt, position=leg_pos_dt)

fig.show()


# %%
# -----------------------------------------------------------------------------
# Uncomment to save the figure in PNG, PDF, or EPS format
for ext in ["png"]: #, "pdf", "eps"]:
  fig.savefig(fname=f"{fname_fig_out}.{ext}", dpi=dpi_png)

print(fname_fig_out)
