# #############################################################################
# Earth magnetic field gufm1 1980
# Grid calculated with pymagglobal
# https://sec23.git-pages.gfz-potsdam.de/korte/pymagglobal
# last access: 2024/02/20
# https://www.gfz-potsdam.de/magservice/faq
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/04/29
#   PyGMT v0.11.0 / v0.12.0 -> https://www.pygmt.org/
#   GMT 6.4.0 / 6.5.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


import pygmt as gmt

# %%
# -----------------------------------------------------------------------------
# Set up for making the plots
# -----------------------------------------------------------------------------
# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

# Colors
color_land = "gray90"
color_shorelines = "gray30"
color_platebound = "216.750/82.875/24.990"
color_llpv = "gray40"
pattern_llpv = "p8+b+f"

z_lim = 850000
z_step = 100000


# %%
# -----------------------------------------------------------------------------
# Make plots
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray50")

gmt.makecpt(cmap="vik", series=[-z_lim, z_lim, z_step], reverse=True)

fig.basemap(region="d", projection="N10c", frame=["WsNE", "xa90f30", "ya30"])

# -----------------------------------------------------------------------------
# Plot gufm1 grid
fig.grdimage(grid=f"{path_in}/gufm1_1980_2900km_Z.grd", cmap=True)

with gmt.config(FONT="10p"):
    fig.colorbar(
        frame=["xaf+lgufm1: 1980 - 2900 km - Z component", "y+lnT"],
        position="JBC+o0c/0.8c+h+w7c+ml",
    )

# -----------------------------------------------------------------------------
# Add grid lines
fig.basemap(frame="g30")

# Add shorelines
fig.coast(shorelines=f"1/0.1p,{color_shorelines}")

# Plot plate boundaries, Bird 2003
fig.plot(
    data=f"{path_in}/plate_boundaries_Bird_2003.txt",
    pen=f"0.4p,{color_platebound}",
)

# -----------------------------------------------------------------------------
# Add LLPV, Wolf et al. 2023
for i_model in range(2, 9, 1):
    fig.plot(
        data=f"{path_in}/01_llvp/3model_2016_{i_model}.txt",
        pen=f"0.2p,{color_llpv}",
        fill=f"{pattern_llpv}{color_llpv}",
        close=True,
    )

# -----------------------------------------------------------------------------
fig.show()

fig_name = f"{path_out}/gufm1_1980_2900km_Z"
# for ext in ["png"]:  # , "pdf", "eps"]:
#     fig.savefig(fname=f"{fig_name}.{ext}")

print(fig_name)
