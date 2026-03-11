# #############################################################################
# Hemispherical maps for the reliefs of planetary bodies
# - Remote datasets provided by GMT: https://www.generic-mapping-tools.org/remote-datasets
# - Creatig a GIF: https://ezgif.com/maker
# -----------------------------------------------------------------------------
# History
# - Created: 2024/01/20
# - Updated: 2026/03/09 - Prepare for GitHub
# - Updated: 2026/03/10 - Improve colormap selection (default, batlow, oleron)
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


import os
import pygmt

status_plot = "single"  # "single" | "combined"
status_cmap = "default"  # "default" | "batlow" | "oleron"

color_hl = "255/90/0"  # highlight -> orange

bodies = ["mercury", "venus", "earth", "moon", "mars", "pluto"]


# %%
# -----------------------------------------------------------------------------
# Single plots
# -----------------------------------------------------------------------------
if status_plot == "single":

    lon_step = 5
    grd_res = "10m"

    for body in bodies:
        print(body)
        grid = f"@{body}_relief_{grd_res}"

        cmap = status_cmap
        if status_cmap == "default":
            cmap = f"@{body}_relief.cpt"
            if body == "earth":
                cmap = "geo"

        for lon0 in range(0, 360 + lon_step, lon_step):

            fig = pygmt.Figure()
            pygmt.config(MAP_GRID_PEN_PRIMARY="0.15p,gray70")

            fig.basemap(region="g", projection=f"G{lon0}/15/10c", frame="+n")
            fig.grdimage(grid=grid, shading=True, cmap=cmap)
            fig.basemap(frame="g10")

            fig.text(
                text=body.capitalize(),
                position="TL",
                font=f"15p,1,{color_hl}",
                offset="0.2c/-0.2c",
            )
            fig.text(
                text=f"{lon0}° E",
                position="TR",
                font=f"10p,1,{color_hl}",
                offset="-0.75c/-0.2",
            )

            fig.colorbar(
                frame=["x+lElevation", "y+lm"],
                position="JBC+jTC+o0c/0.75c+w9c+h+ml",
            )

            fig.show()
            name_basis = f"{body}_relief_{grd_res}_shading_{status_cmap}_lon"
            folder_name = f"{name_basis}{lon_step}deg"
            fig_name = f"{name_basis}{lon0}deg"
            try:
                os.mkdir(folder_name)
            except:
                pass
            # fig.savefig(fname=f"{folder_name}/{fig_name}.png")


# %%
# -----------------------------------------------------------------------------
# Combined plots
# -----------------------------------------------------------------------------
if status_plot == "combined":

    lon_step = 10
    grd_res = "20m"

    for lon0 in range(0, 360 + lon_step, lon_step):

        fig = pygmt.Figure()
        pygmt.config(MAP_GRID_PEN_PRIMARY="0.15p,gray70")

        for body in bodies:
            grid = f"@{body}_relief_{grd_res}"

            cmap = status_cmap
            if status_cmap == "default":
                cmap = f"@{body}_relief.cpt"
                if body == "earth":
                    cmap = "geo"

            fig.basemap(region="g", projection=f"G{lon0}/15/10c", frame="+n")
            fig.grdimage(grid=grid, shading=True, cmap=cmap)
            fig.basemap(frame="g10")

            fig.text(
                text=body.capitalize(),
                position="TL",
                font=f"15p,1,{color_hl}",
                offset="0.2c/-0.2c",
            )

            with pygmt.config(FONT="15p"):
                fig.colorbar(
                    frame=["xaf+lElevation", "y+lm"],
                    position="JBC+jTC+o0c/0.75c+w9c+h+ml",
                )

            fig.shift_origin(xshift="w+2.5c")

        fig.show()
        name_basis = f"combined_relief_{grd_res}_shading_{status_cmap}_lon"
        folder_name = f"{name_basis}{lon_step}deg"
        fig_name = f"{name_basis}{lon0}deg"
        try:
            os.mkdir(folder_name)
        except:
            pass
        # fig.savefig(fname=f"{folder_name}/{fig_name}.png", dpi=200)
