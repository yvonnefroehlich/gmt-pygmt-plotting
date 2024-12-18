# -*- coding: utf-8 -*-
# #############################################################################
# AGU24 | Washington, D.C. | December 9, 2024
#
# The impact of GMT in the Earth, Ocean and Space sciences: What's next? – U12B-05
# PyGMT – Accessing and Integrating GMT with Python and the Scientific Python Ecosystem
#
# Yvonne Fröhlich | Dongdong Tian | Wei Ji Leong | Max Jones | Michael Grund
#
# Python scripts to reproduce the examples shown in the presentation
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/12/01
#   PyGMT v0.13.0 -> https://www.pygmt.org/v0.13.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


# %%
# -----------------------------------------------------------------------------
# Background map on title slide
# -----------------------------------------------------------------------------

import pygmt

# Feel free to adjust for your needs
dataset = "earth_relief"  # Name of the remote dataset
res = "03m"  # Set resolution of grid, here 3 arc-minutes
reg = "p"  # Set registration of grid, here pixel

series = [-4000, 8000]  # Set minimum, maximum used for creating the colormap
cmap = "grayC"  # Set colormap used to plot the grid
alphas = [60]  # Set transparency

centers = [0]  # Set center longitude in degrees East

for center in centers:
    region = [center - 180, center + 180, -70.5, 71]

    for alpha in alphas:

        fig = pygmt.Figure()
        pygmt.config(MAP_FRAME_PEN="0.01p,white")
        fig.basemap(region=region, projection="M34.2c", frame=0)

        pygmt.makecpt(series=series, cmap=cmap)
        fig.grdimage(f"@{dataset}_{res}_{reg}", cmap=True)
        # fig.colorbar(frame=True)

        fig.coast(shorelines="1/0.3p,gray10", resolution="h")

        fig.plot(x=center, y=0, style="r34.2c/19.4c", fill=f"white@{alpha}")

        fig.show()


        fig_path = "02_out_figs"
        fig_name_basic = "FTLJG_agu24_u12b05_pygmt_"
        fig_name_add = f"titleslide_{dataset}_{res}_{reg}_{cmap}_center{center}_alpha{alpha}"
        dpi_png = 360  # Set resolution of the output image (PNG format) in dpi
        # fig.savefig(fname=f"{fig_path}/{fig_name_basic}{fig_name_add}.png", dpi=dpi_png)
