# #############################################################################
# Santorini earthquakes January - February 2025
# -----------------------------------------------------------------------------
# History
# - Created: 2025/09/21
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


import pygmt as gmt
import pandas as pd

# %%
# -----------------------------------------------------------------------------
# Request earthquake data
# -----------------------------------------------------------------------------
# Note the limitation to a search limit of 20000 events
# Exceeding this limit leads to Error 400: Bad Request

start_date = "2025-01-01"
end_date = "2025-03-14"
min_mag_w = "0"
max_mag_w = "10"
min_lon = 25.25
max_lon = 26
min_lat = 36.15
max_lat = 36.95
order_records = "time-asc"


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Path
path_in = "01_in_data"
path_out = "02_out_figs"

# Colors
color_sl = "gray10"
color_hl = "255/90/0"  # -> orange
color_water = "gray"

# Plotting region
coord_red = 0.1
region = [
    min_lon + coord_red / 2,
    max_lon - coord_red / 2,
    min_lat + coord_red,
    max_lat - coord_red / 2,
]


# %%
# -----------------------------------------------------------------------------
# Download USGS earthquake data
# -----------------------------------------------------------------------------
# Set up request using the webservice
# see https://earthquake.usgs.gov/fdsnws/event/1/
# last access: 2025/01/26
url_usgs = "https://earthquake.usgs.gov/fdsnws/event/1/query.csv"

url_usgs_request = url_usgs + "?" + \
    "&".join([
        "starttime=" + start_date + "%2000:00:00",
        "endtime=" + end_date + "%2000:00:00",
        "minmagnitude=" + min_mag_w,
        "maxmagnitude=" + max_mag_w,
        "minlongitude=" + str(min_lon),
        "maxlongitude=" + str(max_lon),
        "minlatitude=" + str(min_lat),
        "maxlatitude=" + str(max_lat),
    ])

eq_catalog_name = "usgsfdsn_" + "".join(str(start_date).split("-")) + "to" + \
    "".join(str(end_date).split("-")) + f"_mw{min_mag_w}to{max_mag_w}"

# Download data into a pandas DataFrame
data_eq_usgs = pd.read_csv(url_usgs_request)

# Save to a CSV file
data_eq_usgs.to_csv(f"{path_in}/{eq_catalog_name}.csv", sep="\t", index=False)

# Load data again into pandas DataFrame
df_eq_usgs = pd.read_csv(f"{path_in}/{eq_catalog_name}.csv", sep="\t")


# %%
# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
df_eq_cmt_raw = pd.read_csv(f"{path_in}/harvardCMT_santorini.csv", sep=",")

# Keep only relevant columns without depth
columns = [
    "year", "month", "day", "hour", "minute", "second", "jday", "dstr",
    "latitude", "longitude", "azi", "bazi", "dis",
    "magnitude", "M0", "strike", "dip", "rake", "region",
]
df_eq_cmt = df_eq_cmt_raw[columns]
df_eq_cmt_mod = df_eq_cmt
df_eq_cmt_mod["depth_km"] = df_eq_cmt_raw["depth"]

# https://doi.org/10.5281/zenodo.15111649
df_eq_external_raw = pd.read_csv(f"{path_in}/catalog_santorini.csv", sep=",")
df_eq_external = df_eq_external_raw[df_eq_external_raw["year"] > 2024]

# Download elevation grid
grid = gmt.datasets.load_earth_relief(resolution="03s", region=region)
grid = "@earth_relief_03s"


# %%
# -----------------------------------------------------------------------------
# Make map of epicenters with different color-codings
# -----------------------------------------------------------------------------

fig = gmt.Figure()

for cmap, reverse, series, fill_usgs, fill_cmt, fill_external, frame, label in zip(
    ["lipari", "lajolla"],
    [True, False],
    [[3, 5], [3, 15]],
    [df_eq_usgs.mag, df_eq_usgs.depth],
    [df_eq_cmt.magnitude, df_eq_cmt.depth_km],
    [df_eq_external.magnitude, df_eq_external.depth],
    [["af", "WSne"], ["af", "wSne"]],
    ["magnitude", "hypocentral depth / km"],
):

    fig.basemap(projection="M12c", region=region, frame=frame)

    # Elevation
    gmt.makecpt(cmap="oleron", series=[0, 1500])
    fig.grdimage(grid=grid, region=region, cmap=True, shading=True)
    fig.coast(water=color_water, shorelines=f"1/0.5p,{color_sl}")
    if cmap == "navia" and coord_red == 0:  # Plot elevation colorbar only once
        fig.colorbar(frame="x+lelevation / m", position="+o0c/-0.85c+ef0.3c+ml")

    # Mark Santorini
    fig.plot(x=25.43, y=36.42, style="x0.6c", pen=f"5p,{color_hl}")

    # Epicenters
    gmt.makecpt(cmap=cmap, series=series, reverse=reverse)
    fig.colorbar(frame=f"x+l{label}", position="+o0c/1.5c+e0.3c+ml")
    # Mw all
    fig.plot(
        x=df_eq_external.longitude,
        y=df_eq_external.latitude,
        style="c0.07c",
        fill=fill_external,
        cmap=True,
    )
    # # Mw >= 3.9
    # fig.plot(
    #     x=df_eq_usgs.longitude,
    #     y=df_eq_usgs.latitude,
    #     style="c0.07c",
    #     fill="cyan",  # fill_usgs,
    #     # cmap=True,
    # )
    # # CMT
    # df_eq_cmt_mod["depth"] = fill_cmt
    # fig.meca(
    #     spec=df_eq_cmt_mod,
    #     scale="0.45c",
    #     outline="0.1p,gray50",
    #     compressionfill="magenta",
    #     # cmap=True,
    # )

    fig.shift_origin(xshift="w+0.5c")

fig.show() # method="external")

# fig_name = f"11_{i_coord_red + 1}_santorini_earthquake_" + str(coord_red)[0:4] + "deg"
fig_name = "11_santorini_earthquake_" + str(coord_red)[0:4] + "deg"
for ext in ["png"]:  # "pdf", "eps"
    fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)
