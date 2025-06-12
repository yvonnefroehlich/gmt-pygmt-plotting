# #############################################################################
# Earthquake map with lon-depth and depth-lat sections at the bottom and right sides
# -----------------------------------------------------------------------------
# History
# - Created: 2025/06/07
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.15.0 / dev -> https://www.pygmt.org/v0.15.0/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pandas as pd
import pygmt

# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
width_main = 15
width_depth = 6

box_standard = "+gwhite@30+p0.3p,gray30+r2p"

path_out = "02_out_figs"


# %%
# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
df_eqs = pygmt.datasets.load_sample_data(name="japan_quakes")
# Sort descending by magnitude to avoid overplotting
df_eqs = df_eqs.sort_values(by=["magnitude"], ascending=False)

depth_min = 0
depth_max = 600  # df_eqs.depth_km.max() + 10
mag_min = 4  # df_eqs.magnitude.min()
mag_max = 7  # df_eqs.magnitude.max()

lon_min = df_eqs.longitude.min() - 1
lon_max = df_eqs.longitude.max() + 1
lat_min = df_eqs.latitude.min() - 1
lat_max = df_eqs.latitude.max() + 1

region_main = f"{lon_min}/{lon_max}/{lat_min}/{lat_max}"  # Need string for GMT !!!
projection_main = f"M{width_main}c"


# %%
# -----------------------------------------------------------------------------
# Determine dimension of maps
# -> https://docs.generic-mapping-tools.org/dev/mapproject.html#w
# -> https://www.pygmt.org/dev/api/generated/pygmt.clib.Session.html
# -----------------------------------------------------------------------------
# Get hight of main map
file_dim_main = "map_dim_main"
with pygmt.clib.Session() as session:
    session.call_module(
        module="mapproject",
        args=[
            f"-J{projection_main}",
            f"-R{region_main}",
            "-W",
            f"->{file_dim_main}.txt",
        ],
    )
map_dim_main = pd.read_csv(f"{file_dim_main}.txt", sep="\t", names=["width", "hight"])
hight_depth = map_dim_main["hight"][0]

# -----------------------------------------------------------------------------
# Get width of depth-latitude map
factor_depth = 10  # To keep values within in value range expected for longitude
projection_lat = f"M{hight_depth}c+dh"  # Give hight instead of width
region_lat = (
    f"{depth_min / factor_depth}/{depth_max / factor_depth}/{lat_min}/{lat_max}"
)

file_dim_lat = "map_dim_lat"
with pygmt.clib.Session() as session:
    session.call_module(
        module="mapproject",
        args=[f"-J{projection_lat}", f"-R{region_lat}", "-W", f"->{file_dim_lat}.txt"],
    )
map_dim_lat = pd.read_csv(f"{file_dim_lat}.txt", sep="\t", names=["width", "hight"])
width_lat = map_dim_lat["width"][0]

# Scale depth relative to latitude
depth2lat = width_lat / width_depth * factor_depth


# %%
# -----------------------------------------------------------------------------
# Create map with depth sections on the bottom and right sides
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray50")

# -----------------------------------------------------------------------------
# Main map
fig.basemap(region=region_main, projection=projection_main, frame=0)

# Elevation
pygmt.makecpt(cmap="oleron", series=[-8000, 2500])
fig.grdimage("@earth_relief_30s_g", region=region_main, cmap=True)
with pygmt.config(FONT="16p"):
    fig.colorbar(
        position="jRB+w6c/0.3c+h+o-6.8c/-2c", frame="xa2000f500+lelevation / m"
    )

fig.coast(shorelines="1/0.1p,gray10", frame=["NsWe", "a2f0.5g1"])

# Hypocenteral depth
pygmt.makecpt(cmap="lajolla", series=[depth_min, depth_max])
fig.plot(
    x=df_eqs.longitude,
    y=df_eqs.latitude,
    size=0.02 * 2**df_eqs.magnitude,
    fill=df_eqs.depth_km,
    cmap=True,
    style="cc",
    pen="0.5,gray10",
)
with pygmt.config(FONT="16p"):
    fig.colorbar(
        position="jRB+w6c/0.3c+h+o-6.8c/-4c", frame="xa100f50+lhypocentral depth / km"
    )

# -----------------------------------------------------------------------------
# Depth sections
args_dethplot = {
    "fill": df_eqs.magnitude,
    "cmap": True,
    "style": "c0.25c",
    "pen": "0.3p,gray10",
    "no_clip": True,
}

pygmt.makecpt(cmap="acton", series=[mag_min, mag_max], reverse=True)
with pygmt.config(FONT="16p"):
    fig.colorbar(
        position="JRB+w6c/0.3c+h+o0.8c/5.5c", frame="a0.5f0.1+lmoment magnitude"
    )

# .............................................................................
# Longitude-depth plot
with fig.shift_origin(yshift=f"-{width_depth + 0.4}c"):
    with pygmt.config(MAP_FRAME_TYPE="plain"):
        fig.basemap(
            # Only needed for bottom longitude axis (South), random latitude range
            region=[lon_min, lon_max, -1, 1],
            projection=f"M{width_main}c",
            frame=["S", "xa2f0.5"],
        )
    fig.basemap(
        region=[lon_min, lon_max, depth_min, depth_max],
        # Invert axis direction by minus sign, here y for depth
        projection=f"X{width_main}c/-{width_depth}c",
        frame=["WeN", "xg1", "ya100f50g100+lhypocentral depth / km"],
    )
    fig.plot(x=df_eqs.longitude, y=df_eqs.depth_km, **args_dethplot)

# .............................................................................
# Depth-latitude plot
with fig.shift_origin(xshift="+w+0.4c"):
    fig.basemap(
        region=[depth_min, depth_max, lat_min, lat_max],
        projection=f"X{width_depth}c/{hight_depth}c",
        frame=["Sn", "xa100f50g100+lhypocentral depth / km"],
    )
    with pygmt.config(MAP_FRAME_TYPE="plain"):
        fig.basemap(
            region=[depth_min / depth2lat, depth_max / depth2lat, lat_min, lat_max],
            projection=f"M{width_depth}c",
            frame=["wE", "ya2f0.5g1"],
        )
    fig.plot(x=df_eqs.depth_km / depth2lat, y=df_eqs.latitude, **args_dethplot)

# -----------------------------------------------------------------------------
fig_name = "map_eqs_map_depthsection"
for ext in ["png"]:  # , "pdf"]:
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
fig.show()
print(fig_name)
