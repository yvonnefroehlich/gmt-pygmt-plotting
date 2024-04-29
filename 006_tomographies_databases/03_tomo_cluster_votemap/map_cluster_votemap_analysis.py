# #############################################################################
# Cluster analysis; Lekic et al. 2012
# Votemap analysis; Shephard et al. 2017
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/04/29
#   PyGMT v0.11.0 -> https://www.pygmt.org/v0.11.0/ | https://www.pygmt.org/
#   GMT 6.4.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


import pygmt as gmt

# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

# Colors
color_land = "gray95"
color_shorelines = "gray50"
color_platebound = "216.750/82.875/24.990"


# %%
# -----------------------------------------------------------------------------
# Grids
# -----------------------------------------------------------------------------
analysis_all = ["cluster", "votemap"]
for analysis in analysis_all:
    # Cluster analysis; Lekic et al. 2012
    if analysis == "cluster":
        grid_in = f"{path_in}/cluster_analysis_Lekic2012.grd"
        cmap_grid = f"{path_in}/cmap_cluster.cpt"
        cb_trancate = [0, 6]
        cb_label = "low velocities - cluster analysis (Lekic et al. 2012)"

    # Votemap analysis; Shepard et al. 2017
    elif analysis == "votemap":
        grid_in = f"{path_in}/votemap_analysis_Shepard2017.grd"
        cmap_grid = f"{path_in}/cmap_votemap.cpt"
        cb_trancate = False
        cb_label = "high velocities - votemap analysis (Shephard et al. 2017)"

    # %%
    # -----------------------------------------------------------------------------
    # Make geographic map
    # -----------------------------------------------------------------------------
    fig = gmt.Figure()
    gmt.config(MAP_GRID_PEN_PRIMARY="0.1p,gray", FONT_LABEL="10p")

    fig.coast(region="d", projection="N11c", land=color_land)

    # -----------------------------------------------------------------------------
    # Plot grid with color-coding
    fig.grdimage(grid=grid_in, cmap=cmap_grid, nan_transparent=True)

    fig.colorbar(
        cmap=cmap_grid,
        frame=f"xa10+l{cb_label}",
        position="jBC+jBC+w0.001c/0.001c+o0c/-0.9c+h",
        truncate=[1, 2],
    )
    fig.colorbar(
        cmap=cmap_grid,
        frame="y+lmodels",
        position="jBC+jBC+o0c/-1c+h+mu",
        equalsize=0.15,
        truncate=cb_trancate,
    )

    # -----------------------------------------------------------------------------
    # Plot shorelines
    fig.coast(shorelines=f"1/0.1p,{color_shorelines}")

    # Plot plate boundaries
    fig.plot(
        data=f"{path_in}/plate_boundaries_Bird_2003.txt",
        pen=f"0.2p,{color_platebound}",
    )

    # Add map frame
    fig.basemap(frame=["WSnE", "xa90f30", "ya30f15"])

    # -----------------------------------------------------------------------------
    # Show and save figure
    fig.show()

    fig_name = f"{path_out}/{analysis}_analysis"
    # for ext in ["png"]:  # , "pdf", "eps"]:
    #     fig.savefig(fname=f"{fig_name}.{ext}")

    print(fig_name)
