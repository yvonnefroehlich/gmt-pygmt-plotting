# #############################################################################
# Colorwheel for cyclic colormaps created with PyGMT
# - Scientific colourmaps by Fabio Crameri: romaO, bamO, brocO, corkO, vikO
# - cmocean colormaps by Kristen M. Thyng: phase
# -----------------------------------------------------------------------------
# History
# - Created: 2024/05/15
# - Updated: 2025/01/14
# -----------------------------------------------------------------------------
# Versions
#   PyGMT v0.14.0 -> https://www.pygmt.org/v0.14.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
import pygmt


def colorwheel(cmap, perspective, rho_min=1, rho_max=2.5, fig_instance=None):
    """
    Parameters
    ----------
    Required
    - cmap : str | name of a cyclic colormap
    - perspective : list of two floats | azimuth, elevation
    Optional
    - rho_min : float | inner radius of colorwheel | Default 1
    - rho_max : float | outer radius of colorwheel | Default 2.5
    - fig_instance : Provide a PyGMT figure instance | Default a new one is set up
    """

# -----------------------------------------------------------------------------
# Set up rotated rectangle or bar data
# -----------------------------------------------------------------------------
    # [[lon, lat, direction, width, height]]
    # In polar coordinates lon refers to the angle and lat to the radius (rho)
    # Location applies to the center of the bar -> shift by length/2
    # Add quantity for fill color as second column (zero-based indexing)
    # Direction of bar (j) is from North but still counter-clockwise -> negative sign
    data_bars = np.zeros([360, 6])
    for i_ang in range(0, 360, 1):  # min, max], step
        data_bars_temp = np.array(
            [
                i_ang,
                rho_min + rho_max / 2,
                i_ang,
                -i_ang,
                0.05,
                rho_max - rho_min,
            ]
        )
        data_bars[i_ang, :] = data_bars_temp

# -----------------------------------------------------------------------------
# Create colorwheel plot
# -----------------------------------------------------------------------------
    if fig_instance != None:
        fig = fig_instance
    else:
        fig = pygmt.Figure()

    with pygmt.config(
        PS_PAGE_COLOR="white@1",  # Make area outside of plot transparent
        MAP_FRAME_PEN="white",  # Make frame outline white
    ):
        fig.basemap(
            region=[0, 360, 0, rho_max],
            # Use geographic azimuth instead of standard angle -> backazimuth
            # Go clockwise from North instead of counter-clockwise from East
            projection=f"P{rho_max * 2}c+a",
            frame="rltb",
        )

    # Create colormap for direction (backazimuth)
    pygmt.makecpt(cmap=cmap, cyclic=True, series=[0, 360, 1])

    # Plot rotated rectangles with color-coding
    # Set perspective as [azimuth, elevation]
    fig.plot(data=data_bars, style="j", cmap=True, perspective=perspective)

    # Show and save
    fig_name = f"colorwheel_N_cw_pygmt_bar_{cmap}"
    if fig_instance == None:
        fig.show()
        for ext in ["png"]:  # , "pdf", "eps"]:
            fig.savefig(fname=f"{fig_name}.{ext}", dpi=720)
    print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Examples
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -2, 2], projection="X10c/4c", frame=0)

fig.shift_origin(xshift="0.6c", yshift="2c")
for cmap in ["romaO", "bamO", "brocO", "corkO", "vikO", "phase"]:
    colorwheel(
        cmap=cmap,
        perspective=[90, -90],  # anti-clockwise from horizontal
        rho_min=0.2,
        rho_max=0.6,
        fig_instance=fig,
    )
    fig.shift_origin(yshift="-1.4c")
    colorwheel(
        cmap=cmap,
        perspective=[180, 90],  # clockwise from vertical (-> backazimuth)
        rho_min=0.2,
        rho_max=0.6,
        fig_instance=fig,
    )
    fig.text(x=1, y=2.4, text=cmap, no_clip=True)
    pygmt.makecpt(cmap=cmap, series=[0, 360], cyclic=True)
    fig.colorbar(cmap=True, position="jBC+o0c/-0.5c+w1.1c/0.25c+h", frame=0)
    fig.shift_origin(xshift="1.5c", yshift="1.4c")

fig.show()
fig.savefig(fname="colorwheel_all_cmaps.png", dpi=720)
