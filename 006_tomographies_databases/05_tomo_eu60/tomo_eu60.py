# #############################################################################
# Tomography EU60
#
# Azimuthal anisotropy - phi and strength
# Central Europe, upper mantle 198 km - 200 km - 202 km
#
# Hejun Zhu, Ebru Bozdağ, Jeroen Tromp, (2015).
# Seismic structure of the European upper mantle based on adjoint tomography.
# Geophysical Journal International, 201(1):18–52.
# https://doi.org/10.1093/gji/ggu492.
# -----------------------------------------------------------------------------
# History
# - Created: 2023/08/28
# - Updated: 2025/01/20
# - Updated: 2025/07/26
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.16.0 - v0.16.0 -> https://www.pygmt.org/
# - GMT 6.4.0 - 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
quantity = ["phi", "strength"]  # "phi", "strength"

depth_min = 200
depth_max = 200
depth_step = 2  # data is provided in steps of 2 km

path_in = "01_in_data"
path_out = "02_out_figs"

color_hl = "255/90/0"  # highlight -> orange | URG paper
color_pb = "216.750/82.875/24.990"  # plate boundaries
color_sl = "gray50"  # shorelines
color_land = "gray90"

file_pb = "plate_boundaries_Bird_2003.txt"

# -----------------------------------------------------------------------------
# Lambert projection
width_lamb = "15c"

# study region
lon_min_lamb = -40
lon_max_lamb = 70
lat_min_lamb = 30.0001
lat_max_lamb = 80

# projection center
lon0_lamb = np.mean([lon_min_lamb, lon_max_lamb])
lat0_lamb = np.mean([lat_min_lamb, lat_max_lamb])
# Calculate two standard parallels (only these two distortion-free)
lat1_lamb = lat_min_lamb + (lat_max_lamb - lat_min_lamb) / 3
lat2_lamb = lat_min_lamb + (lat_max_lamb - lat_min_lamb) / 3 * 2

projection = f"L{lon0_lamb}/{lat0_lamb}/{lat1_lamb}/{lat2_lamb}/{width_lamb}"
region = [lon_min_lamb, lon_max_lamb, lat_min_lamb, lat_max_lamb]


# %%
for quantity_str in quantity:

    for depth in range(depth_min, depth_max + depth_step, depth_step):  # in km

# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
        path_eu60 = f"{path_in}/{quantity_str}/"
        file_eu60 = f"tomoEU60_file_anisoazi_BAR_{depth}km.txt"

        file_aniso = open(f"{path_eu60}{file_eu60}", "r")
        data_aniso = np.loadtxt(file_aniso)
        file_aniso.close()


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------
        fig = gmt.Figure()
        gmt.config(FONT_LABEL="10p")

        fig.basemap(region=region, projection=projection, frame=["WSne", "a15f5"])

# -----------------------------------------------------------------------------
        # Plot shorelines
        fig.coast(shorelines=f"1/0.1p,{color_sl}", land=color_land)

        # Plot plate boundaries
        fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.5p,{color_pb}")

# -----------------------------------------------------------------------------
        # Set up colormap for
        match quantity_str:
            case "phi":
                gmt.makecpt(series=[-90, 90], cmap="phase", cyclic=True)
                cb_afg = "a30f10"
                cb_label = "@~f@~ / N°E"
                cb_pos = None
            case "strength":
                gmt.config(COLOR_BACKGROUND="cyan", COLOR_FOREGROUND="orange1")
                gmt.makecpt(series=[0, 4], cmap="navia", overrule_bg=True)
                cb_afg = "a0.5f0.1"
                cb_label = f"{quantity_str} / %"
                cb_pos = "+o-1c/0.87c+h+ef0.4c"

# -----------------------------------------------------------------------------
        # Plot anisotropy data with color-coding for phi or strength
        fig.plot(
            data=data_aniso,
            style="J",
            incols="0,1,2,3,4+s450,5+s700",
            cmap=True,
        )
        # Add colorbar
        with gmt.config(MAP_FRAME_PEN="0.5p,black"):
            fig.colorbar(frame=[f"x{cb_afg}", f"y+l{cb_label}"], position=cb_pos)

# -----------------------------------------------------------------------------
        # Add label for depth
        fig.text(position="TC", text=f"@@{depth} km", font=f"9p,{color_hl}")

        # Add label for tomography
        fig.text(position="BL", text="EU60", font=f"9p,{color_hl}")

# -----------------------------------------------------------------------------
        # Show and save figure
        fig.show()
        fig_name = f"map_eu60_azi_{quantity_str}_{depth}km"
        # for ext in ["png"]:  # , "pdf", "eps"]:
        #     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")

        print(fig_name)
