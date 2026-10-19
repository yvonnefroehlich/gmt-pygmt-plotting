# #############################################################################
# Plate boundaries comparision of different studies
# - Bird 2003
# - Hasterok et al. 2022
#   https://zenodo.org/records/6586972
#   https://github.com/dhasterok/global_tectonics
#   https://doi.org/10.31223/X5TD1C
#   https://phys.org/news/2022-06-global-geological-provinces-tectonic-plates.html
#   https://www.researchgate.net/publication/360133385_New_maps_of_global_geologic_provinces_and_tectonic_plates
# - Spohn et al. 2026
#   https://doi.org/10.1007/s11214-026-01265-y
# -----------------------------------------------------------------------------
# History
# - Created: 2026/10/19
# -----------------------------------------------------------------------------
# Versions
# - PyGMT 0.19.0 -> https://www.pygmt.org
# - GMT 6.7.0 -> https://www.generic-mapping-tools.org
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
# Pahts
path_in = "01_in_data"
path_out = "02_out_figs"

# Colors
color_land = "gray97"
color_sl = "gray"
color_hl= "255/90/0"  # highlight -> orange

# Data files
pb_bird = f"{path_in}/pb_bird_2003/plate_boundaries_Bird_2003.txt"
pb_hasterok = f"{path_in}/pb_hasterok_2022/boundaries.gmt"

# Some variable definitions
args_bm = {"projection": "N12c", "frame": 0}
args_text = {
    "position": "TR",
    "offset": (0.4, -0.1),
    "font": f"10p,1,{color_hl}",
    "no_clip": True,
    "justify": "MC",
}


# %%
# -----------------------------------------------------------------------------
# Make map - overplot
# -----------------------------------------------------------------------------
fig = pygmt.Figure()

for region, frame in zip(["g", "d"], ["WSne", "Wsne"]):
    fig.basemap(**args_bm, region=region)
    fig.coast(land=color_land, shorelines=f"0.1p,{color_sl}")
    fig.plot(data=pb_bird, pen="0.8p,darkbrown", label="Bird 2003+N2+f5p")
    fig.plot(data=pb_hasterok, pen="0.2p,magenta", label="Hasterok et al. 2022")
    if region=="g":
        with pygmt.config(FONT=f"7p,1,{color_hl}"):
            fig.legend(position="jBC+o-0.5c/-0.1c+w3.5c")
    fig.basemap(frame=[frame, "af"])
    fig.shift_origin(yshift="h+0.5c")

fig.show()
fig_name = "map_plate_boundaries_overplot"
for ext in ["png"]:  # , "pdf", "eps"]:
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Make map - subplot
# -----------------------------------------------------------------------------
fig = pygmt.Figure()

for region, frame, data_pb, text_pb, color_pb in zip(
    ["d", "g", "d", "g"],
    ["Wsne", "wsne", "WSne", "wSne"],
    [pb_bird, pb_bird, pb_hasterok, pb_hasterok],
    ["Bird 2003", "", "Hasterok et al. 2022", ""],
    ["darkbrown", "darkbrown", "magenta", "magenta"]
):
    fig.basemap(**args_bm, region=region)
    fig.coast(land=color_land, shorelines=f"0.1p,{color_sl}")
    fig.plot(data=data_pb, pen=f"0.8p,{color_pb}")
    if region=="d":
        fig.text(**args_text, text=text_pb)
    fig.basemap(frame=[frame, "af"])

    if region=="d":
        fig.shift_origin(xshift="w+0.5")
    else:
        fig.shift_origin(xshift="-w-0.5", yshift="-h-0.5")
        
fig.show()
fig_name = "map_plate_boundaries_subplot"
for ext in ["png"]:  # , "pdf", "eps"]:
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)
