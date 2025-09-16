# #############################################################################
# Earth's magnetic field model gufm1 1980 by Jackson et al. (2000)
# - North and south poles: maps with contour lines for inclindation and declination
# -----------------------------------------------------------------------------
# Grid calculated with pymagglobal
# https://sec23.git-pages.gfz-potsdam.de/korte/pymagglobal
# last access: 2024/02/20
# https://www.gfz-potsdam.de/magservice/faq
# -----------------------------------------------------------------------------
# History
# - Created: 2025/09/16
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

# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
status_quantity = "I"  # "I" for inclination | "D" for declination
status_pole = "north"  # "north" for north pole | "south" for south pole

# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

# Colors
color_land = "gray90"
color_sl = "gray50"  # shorelines

# Projection
match status_pole:
    case "north":
        lat_central = 90
    case "south":
        lat_central = -90
project = f"A0/{lat_central}/40/10c"

# Colormap and colorbar
match status_quantity:
    case "D":
        z_lim = 180  # degrees
        cb_x_afg = "a60f20"
        quantity_label = "declination"
    case "I":
        z_lim = 90  # degrees
        cb_x_afg = "a30f10"
        quantity_label = "inclination"

# Grid for gufm1
grid_gufm1 = f"{path_in}/gufm1_1980_2900km_{status_quantity}.grd"


# %%
# -----------------------------------------------------------------------------
# Make plots
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray50")

fig.basemap(region="g", projection=project, frame=0)
fig.coast(land=color_land)

# -----------------------------------------------------------------------------
# Plot gufm1 grid as contour lines with color-coding
contours_major_step = 10
contours_minor_step = 2
contours_major_file = f"{path_in}/contours_major.txt"
contours_minor_file = f"{path_in}/contours_minor.txt"

gmt.makecpt(cmap="vik", series=[-z_lim, z_lim, 1])

fig.grdcontour(grid=grid_gufm1, levels=contours_major_step, D=contours_major_file)
fig.grdcontour(grid=grid_gufm1, levels=contours_minor_step, D=contours_minor_file)
fig.plot(data=contours_major_file, pen="0.7p,+z", cmap=True)
fig.plot(data=contours_minor_file, pen="0.2p,+z", cmap=True)

with gmt.config(FONT="12p"):
    fig.colorbar(
        frame=f"x{cb_x_afg}+lgufm1: 1980 - 2900 km - {quantity_label}+u@.",
        position="JBC+o0c/1.3c+h+w9c+ml",
    )

# -----------------------------------------------------------------------------
# Add grid lines
fig.basemap(frame="a30f10g30")

# Add shorelines
fig.coast(shorelines=f"1/0.1p,{color_sl}")

# -----------------------------------------------------------------------------
fig.show()
fig_name = f"map_gufm1_1980_2900km_{status_quantity}_{status_pole}pole"
# for ext in ["png"]: # , "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)
