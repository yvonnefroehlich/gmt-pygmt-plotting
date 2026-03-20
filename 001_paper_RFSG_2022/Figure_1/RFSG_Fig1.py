# #############################################################################
# Ritter et al. (2022), Seismol: Figure 1
# Topographic map of the Upper Rhine Graben area with piercing points in the
# upper mantle at 410 km depth for shear wave splitting measurements at the
# Black Forest Observatory (BFO)
# -----------------------------------------------------------------------------
# Ritter J R R, Fröhlich Y, Sanz-Alonso Y, Grund M (2022).
# Short-scale laterally varying SK(K)S shear wave splitting at BFO, Germany –
# implications for the determination of anisotropic structures.
# Journal of Seismology, 26:1137-1156.
# https://doi.org/10.1007/s10950-022-10112-w,
# correction https://doi.org/10.1007/s10950-023-10136-w.
# -----------------------------------------------------------------------------
# History
# - Original Jupyter notebook by Michael Grund
#   https://github.com/michaelgrund/GMT-plotting/blob/main/010_paper_RFSG2022/RFSG_2022_Fig_01.ipynb
# - Converted to Python script: 2026/03/19
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


import pygmt

# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"

# Study area
region = [5, 12, 46, 50]

# BFO location
bfo_lat = 48.332  # latitude in degrees
bfo_lon = 8.331  # longitude in degrees
bfo_coords = {"x": bfo_lon, "y": bfo_lat}

# Colors
color_land = "217.6/217.6/217.6"
color_water = "white"
color_station = "24/116/205"  # -> blue
color_sks = "205/0/0"  # -> red
color_skks = "238/118/0"  # -> orange
color_pks = "yellow"
color_pb = "216.750/82.875/24.990"  # -> darkorange
color_epi = "gray40@20"

box_standard = "+r2p+gwhite@30+p0.5p"


# %%
# -----------------------------------------------------------------------------
# Create main map
# -----------------------------------------------------------------------------
fig = pygmt.Figure()

fig.basemap(projection="M16c", region=region, frame=["a1", "WNse"])

# Plot elevation grid
pygmt.makecpt(cmap=f"{path_in}/europe_3.cpt", series=[0, 3000, 10])
fig.grdimage(grid="@earth_relief_15s", shading=True)

# Add scalebar
with pygmt.config(FONT="10p"):
    fig.basemap(map_scale="f11/49.75/56/50+lkm+jt")

# Add colorbar
fig.colorbar(
    position="x2.5c/0.85c+w5c/0.25c/BL+h+ef0.2c+ml",
    frame="x1000+ltopography in m",
    box=box_standard,
)

fig.show()


# %%
# -----------------------------------------------------------------------------
# Mark BFO location
fig.plot(style="t19p", fill=color_station, pen="0.9p", **bfo_coords)
# Add station name
fig.text(text="BFO", font="10p", offset="0c/-0.5c", **bfo_coords)

# -----------------------------------------------------------------------------
# Plot important town locations as squares
lons = [
    8.40342, 7.84940, 8.46731, 11.0773, 7.58783,
    11.5754, 8.69472, 6.18341, 8.54104, 9.17507,
]
lats = [
    49.00687, 47.99609, 49.48929, 49.45387, 47.55811,
    48.13711, 49.40936, 48.69372, 47.37445, 47.65922,
]
for lon, lat in zip(lons, lats):
    fig.plot(x=lon, y=lat, style="s0.25c", fill="white", pen="0.6p")

# Add names of towns
lons = [
    8.32, 8.2, 8.19, 11.1296, 7.6,
    11.57601, 8.62, 6.18442, 8.53918, 9.17324,
]
lats = [
    49.11, 47.99, 49.57, 49.3741, 47.4667,
    48.0371, 49.33, 48.5921, 47.2687, 47.7580,
]
cities = [
    "Karlsruhe", "Freiburg", "Mannheim", "Nuremberg", "Basel",
    "Munich", "Heidelberg", "Nancy", "Zurich", "Konstanz",
]
for lon, lat, city in zip(lons, lats, cities):
    fig.text(x=lon, y=lat, text=city, font="8p")

# -----------------------------------------------------------------------------
# Label geological / tectonic features
for lon, lat, text, font, fill in zip(
    [8.6, 8.8, 6.8, 7.8, 10.2],
    [46.8, 48.2, 48.3, 48.61, 48],
    ["Alps", "Black Forest", "Vosges", "Upper Rhine Graben", "South German Block"],
    ["16p+a15", "9p+a50", "9p+a55", "9p+a55", "11p"],
    ["white@25", "white@40", "white@40", "white@40", "white@40"],
):
    fig.text(x=lon, y=lat, text=text, font=font, fill=fill)

fig.show()


# %%
# -----------------------------------------------------------------------------
# Plot piercing points
args_pp = {"incols": [2, 3], "style": "c0.25c", "pen": "0.8p,gray20"}

# Plot single event pierce points
fig.plot(
    data=f"{path_in}/BFO_SEA_pp410km_SKS_sp_hd0km.txt",
    fill=f"{color_sks}@20",
    label="SKS+S0.25c",
    **args_pp,
)
fig.plot(
    data=f"{path_in}/BFO_SEA_pp410km_SKKS_sp_hd0km.txt",
    fill=f"{color_skks}@20",
    label="SKKS+S0.25c",
    **args_pp,
)

# Plot pierce points of events used in the multi-event analysis (SIMW and WS)
fig.plot(
    data=f"{path_in}/BFO_MEAred_pp410km_SKS_sp_hd0km.txt",
    fill=f"{color_sks}@20",
    **args_pp,
)
fig.plot(
    data=f"{path_in}/BFO_MEAred_pp410km_SKKS_sp_hd0km.txt",
    fill=f"{color_skks}@20",
    **args_pp,
)
fig.plot(
    data=f"{path_in}/BFO_MEAred_pp410km_PKS_sp_hd0km.txt",
    fill=f"{color_pks}@20",
    label="PKS+S0.25c",
    **args_pp,
)

fig.legend(position="x0.25c/0.2c/1.6c/1.5c/BL", box=box_standard)

fig.show()


# %%
# -----------------------------------------------------------------------------
# Plot volcano symbol at Kaiserstuhl Volcanic Complex (VC)
fig.plot(
    x=7.690556,
    y=48.120833,
    style=f"k{path_in}/volcano_sleeping.def/25p",
    fill="magenta4@15",
    pen="thin",
)
# Add arrow
fig.plot(
    x=6.9,
    y=47.3,
    direction=[[35], [2.6]],
    style="V0.25c+e+n0.03c+a40",
    fill="magenta4",
    pen="2p,magenta4",
)
# Add label
fig.text(
    x=6.8,
    y=47.22,
    text="Kaiserstuhl VC",
    font="10p,white",
    fill="magenta4@30",
    clearance="0.025i",
)

fig.show()


# %%
# -----------------------------------------------------------------------------
# Add inset showing study area in Central Europe
# -----------------------------------------------------------------------------
with fig.inset(position="jTL+w2.8c/3.9c+o0.1c", box="+gwhite+p2p"):
    fig.basemap(region=[4, 15.5, 45, 55.3], projection="M?", frame="+n")
    fig.coast(
        land=color_land,
        water=color_water,
        shorelines="thinnest",
        borders="1/0.25p",
        area_thresh=10000,
    )

    # Outline study area
    rectangle = [[region[0], region[2], region[1], region[3]]]
    fig.plot(data=rectangle, style="r+s", pen="2p,gray20", straight_line=True)

    # Mark BFO location
    fig.plot(style="t6p", fill=color_station, pen="0.5p", **bfo_coords)

    # Label Germany
    fig.text(x=10.5, y=52, text="Germany", font="8p")

fig.show()


# %%
# -----------------------------------------------------------------------------
# Add inset for epicenters
# -----------------------------------------------------------------------------
with fig.inset(position="jBR+jBR+o-1.2c+w7.12c"):
    fig.basemap(region="g", projection=f"E{bfo_lon}/{bfo_lat}/160/?", frame=0)
    fig.coast(resolution="c", land=color_land, water=color_water)

    # Plot plate boundaries after Bird (2003)
    fig.plot(data=f"{path_in}/plate_boundaries_Bird_2003.txt", pen=f"0.5p,{color_pb}")

    # Plot circles at 90 and 130 degrees distance from the recording station
    distlims = [90, 130]  # GMT expects diameter
    for distlim in distlims:
        fig.plot(style=f"E-{distlim * 2}d", pen="0.7p,--", **bfo_coords)

    # Mark BFO location
    fig.plot(style="t0.25c", fill=color_station, pen="0.5p", **bfo_coords)

    # Plot epicenters
    for data in [
        "BFO_SEA_pp410km_SKS_sp_hd0km.txt",
        "BFO_SEA_pp410km_SKKS_sp_hd0km.txt",
        "BFO_MEAred_pp410km_SKS_sp_hd0km.txt",
        "BFO_MEAred_pp410km_SKKS_sp_hd0km.txt",
        "BFO_MEAred_pp410km_PKS_sp_hd0km.txt",
    ]:
        fig.plot(
            data=f"{path_in}/{data}", style="c0.2c", fill=color_epi, pen="0.8,gray10"
        )

    # Plot distance circles again on top in transparent white
    for distlim in distlims:
        fig.plot(
            style=f"E-{distlim * 2}d",
            pen="0.7p,white,--",
            transparency=70,
            **bfo_coords,
        )
    # Label circles
    fig.text(x=9, y=-33.5, text="90@.", font="10p")
    fig.text(x=9, y=-90, text="130@.", font="10p")

fig.show()


# %%
fig_name = "RFSG_Fig1"
# Uncomment to save the figure in PNG, PDF, or EPS format
# for ext in ["png"]:  # "pdf", "eps"]:
    # fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")

print(fig_name)
