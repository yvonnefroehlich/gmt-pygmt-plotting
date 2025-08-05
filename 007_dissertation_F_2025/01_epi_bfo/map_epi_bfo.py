# #############################################################################
# Earthquakes related to shear wave splitting measurements (SWSMs) at the
# recording station Black Forest Observatory (BFO)
#   - epicenters
#   - (projected) rays
#   - areas of SKS and SKKS piercing points (receiver side)
# -----------------------------------------------------------------------------
# Related to
#   - Figure 1 (a) of
#     Yvonne Fröhlich (2025). Shear wave splitting analysis of long-term data:
#     Anisotropy studies in the Upper Rhine Graben area, Central Europe.
#     Dissertation, Karlsruhe Institute of Technology, Geophysical Institute.
#     10.5445/IR/1000183786, https://publikationen.bibliothek.kit.edu/1000183786.
#  - SWSM dataset available at https://dx.doi.org/10.35097/685
#     published along with the publication https://doi.org/10.1093/gji/ggae245
# -----------------------------------------------------------------------------
# History
# - Created: 2025/07/31
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


import pygmt
import pandas as pd


# %%
# -----------------------------------------------------------------------------
# Set up
# -----------------------------------------------------------------------------
# >>> Set for your needs <<<

# Set projection of map
proj = "epi"  ## epi" | "rob" | "ortho"
fig_size = 11  # in centimeters

# Recording station
sta_name = "BFO"
sta_lat = 48.331
sta_lon = 8.330

# Epicentral distance
lon_center = sta_lon  # degrees East
lat_center = sta_lat  # degrees North
center_coord = {"x": lon_center, "y": lat_center}
epi_dist = 160  # degrees
size2dist = fig_size / epi_dist
dist_min = 90
dist_max = 150
dist_lmm_K_min = 5  # 5°-15°
dist_lmm_K_max = 13
dist_lmm_KK_min = 13  # 15°-20°
dist_lmm_KK_max = 20
# Orthographic
lon0 = sta_lon  # degrees East
lat0 = sta_lat  # degrees North

# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"
dpi_png = 360
file_pb = "plate_boundaries_Bird_2003.txt"

# Plotting
color_sta = "gold"  # station
color_land = "gray90"
color_water = "white"
color_pb = "216.750/82.875/24.990"  # plate boundaries -> darkorange
color_sl = "gray60"  # shorelines
color_hl = "255/90/0"  # highlight -> orange
color_epi = "steelblue"
color_SKS = "205/0/0"  # -> red
color_SKKS = "238/118/0"  # -> orange

box_standard = "+gwhite@30+p0.8p,gray50+r2p"
clearance_standard = "0.1c/0.1c+tO"

match proj:
    case "rob":
        proj_used = f"N{fig_size}c"
        frame_used = "af"
    case "epi":
        proj_used = f"E{lon_center}/{lat_center}/{epi_dist}/{fig_size}c"
        frame_used = "af"
    case "ortho":
        proj_used = f"G{lon0}/{lat0}/{fig_size}c"
        frame_used = "afg"


# %%
# Load SWSM data
df_null = pd.read_csv(f"{path_in}/splitresults_NULLS_goodfair_GR_BFO.csv", header=13, sep=";")
df_split = pd.read_csv(f"{path_in}/splitresults_SPLITS_goodfair_GR_BFO.csv", header=13, sep=";")


# %%
# -----------------------------------------------------------------------------
# Create geographic map
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(projection=proj_used, region="d", frame=0)

fig.coast(shorelines=f"1/0.01p,{color_sl}", land=color_land, water=color_water)

# Plot plate boundaries
fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.3p,{color_pb}")

# -----------------------------------------------------------------------------
# Color epicentral distance range for XKS phases
if proj == "epi":
    fig.plot(
        style=f"w{dist_min * size2dist}/0/360+i{dist_max * size2dist}",
        fill=f"{color_hl}@90",
        **center_coord,
    )

# -----------------------------------------------------------------------------
# Plot rays
pen_ray = "0.15p,black@80"
for i_eq in range(len(df_split)):
    fig.plot(
        x=[df_split["lon_in_degE"][i_eq], lon_center],
        y=[df_split["lat_in_degN"][i_eq], lat_center],
        pen=pen_ray,
    )
for i_eq in range(len(df_null)):
    fig.plot(
        x=[df_null["lon_in_degE"][i_eq], lon_center],
        y=[df_null["lat_in_degN"][i_eq], lat_center],
        pen=pen_ray,
    )

# -----------------------------------------------------------------------------
# Plot epicenters
epi_columns = ["lon_in_degE", "lat_in_degN"]
args_epi = {"style": "a0.25c", "fill": color_epi, "pen": "0.1p,gray20"}
fig.plot(data=df_null[epi_columns], **args_epi)
fig.plot(data=df_split[epi_columns], **args_epi)

# -----------------------------------------------------------------------------
if proj == "epi":

    for epi_lim in [dist_min, dist_max]:
        # Mark limits for epicentral distance range for XKS phases
        fig.plot(style=f"E-{epi_lim*2}+d", pen=f"0.6p,{color_hl},-", **center_coord)

        # Label epicentral distance range for XKS phases
        fig.text(
            text=f"{epi_lim}@.",
            offset=f"0c/-{epi_lim * size2dist / 2}c",
            fill="white@30",
            pen=f"0.3p,{color_hl}",
            font="7p",
            clearance=clearance_standard,
            **center_coord,
        )

    # Mark epicentral distance for LMM piercing points of SKS and SKKS phases
    fig.plot(
        style=f"w{dist_lmm_KK_max * size2dist}/0/360+i{dist_lmm_KK_min * size2dist}",
        fill=f"{color_SKKS}@50",
        **center_coord,
    )
    fig.plot(
        style=f"w{dist_lmm_K_max * size2dist}/0/360+i{dist_lmm_K_min * size2dist}",
        fill=f"{color_SKS}@50",
        **center_coord,
    )

# -----------------------------------------------------------------------------
# Plot recording stations
fig.plot(style="i0.4c", fill=color_sta, pen="0.8p,black", **center_coord)
fig.text(
    text=sta_name,
    offset="0c/0.4c",
    fill="white@30",
    pen=f"0.5p,{color_hl}",
    clearance=clearance_standard,
    font=f"7p,1,{color_hl}",
    **center_coord,
)

# -----------------------------------------------------------------------------
# Plot map frame on top
with pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray30"):
    fig.basemap(frame=frame_used)

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = f"map_{proj}_BFO"
# for ext in ["png"]:  # "pdf", "eps"
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
