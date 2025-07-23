# #############################################################################
# Global seismicity
# - Request earthquake data from USGS
# - Download the data into a pandas DataFrame
# - Write the data to a CSV file
# - Create geographic map with coding for
#   - color (hypocentral depth)
#   - size (moment magitude)
# For making a gif: https://ezgif.com/maker
# -----------------------------------------------------------------------------
# History
# - Created: 2025/01/26
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
# import obspy
import pandas as pd


# %%
# -----------------------------------------------------------------------------
# Set up
# -----------------------------------------------------------------------------
# >>> Set for your needs <<<

# Set projection of map
proj = "epi"  ## "rob" | "epi" | "ortho"
fig_size = 11   # in centimeters

# Recording stations
sta_lat = np.array([48.413, 48.216, 48.771, 48.331, 49.020, 48.989])
sta_lon = np.array([7.354, 7.159, 9.194, 8.330, 8.367, 8.492])
mean_lon = np.mean(sta_lon)
mean_lat = np.mean(sta_lat)
sta_name = ["WLS", "ECH", "STU", "BFO", "TMO07", "TMO44"]

# epicentral distance
lon_center = mean_lon  # degrees East
lat_center = mean_lat  # degrees North
center_coord = {"x": lon_center, "y": lat_center}
epi_dist = 160  # degrees
size2dist = fig_size / epi_dist
dist_min = 90
dist_max = 150
# orthographic
lon0 = 60  # degrees East
lat0 = 10  # degrees North

# Request earthquake data
# >>> Only works with single quotation marks <<<
start_date = '1991-01-01'
end_date = '2019-12-31'
min_mag_w = '6'  # magnitude, later filter regarding moment magnitude
max_mag_w = '10'
order_records = 'time-asc'  # 'magnitude'

# -----------------------------------------------------------------------------
dpi_png = 1200
path_in = "01_in_data/"
path_out = "02_out_figs/"
file_pb = "plate_boundaries_Bird_2003.txt"
file_legend = "legend_gmt_magitude.txt"

# Plotting
color_highlight = "255/90/0"
color_sta = "gold"
color_land = "gray90"
color_water = "white"  # "lightskyblue@50"
color_pb = "216.750/82.875/24.990"
color_sl = "gray60"
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
# -----------------------------------------------------------------------------
# Download earthquake data
# -----------------------------------------------------------------------------
# Set up request
# see https://earthquake.usgs.gov/fdsnws/event/1/
# last access: 2025/01/26
url_usgs = 'https://earthquake.usgs.gov/fdsnws/event/1/query.csv'

url_usgs_request = url_usgs + '?' + \
    '&'.join([
        'starttime=' + start_date + '%2000:00:00',
        'endtime=' + end_date + '%2000:00:00',
        'minmagnitude=' + min_mag_w,
        'maxmagnitude=' + max_mag_w,
        'orderby=' + order_records,
    ])

eq_catalog_name = f"global_seismicity_{start_date}to{end_date}_mw{min_mag_w}to{max_mag_w}"

# Download data into a pandas DataFrame
data_eq_raw = pd.read_csv(url_usgs_request)

# Write data to a CSV file
data_eq_raw.to_csv(path_or_buf=f"{path_in}/data_{eq_catalog_name}.csv", sep="\t", index=False)

# Filter data
# mw, mwc, mwb, mwr, mww
data_eq_used = data_eq_raw[data_eq_raw["magType"].str.contains("mw")]

# Sort descending by magnitude to avoid overplotting
data_eq_used = data_eq_used.sort_values(by=["mag"], ascending=False)

# Scale hypocentral depth for size-coding
# >>> If you change the scaling you also have to update the legend file <<<
data_eq_used["mag_scaled"] = np.exp(data_eq_used["mag"] / 1.7) * 0.0035



# %%
# -----------------------------------------------------------------------------
# Make histogram for hypocentral depth
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
pygmt.config(FONT="11p") #, MAP_FRAME_PEN="0.8p,gray50")

fig.histogram(
    region=[-10.1, 500, 0, 4700], #1650],
    projection="X17c/10c",
    frame=["WStr", "xa50f10+lhypcentral depth / km", "y+lcounts of earthquakes"],
    data=data_eq_used["depth"],
    series=10,
    # fill=f"{color_highlight}@85",
    fill="gray@85",
    pen="0.5p,gray40,solid",
    histtype=0,
    annotate="+o2p+r+f7p",
    cumulative="r",
    extreme="b",
    barwidth="10+o10",
)

args_text = {
    "font": "10p,black",
    "position": "TR",
    "pen": "0.8p,gray50",
    "clearance": clearance_standard,
}

fig.plot(x=[5, 5], y=[0, 4308], pen=f"9p,{color_highlight}@60", no_clip=True)
fig.plot(x=[15, 15], y=[0, 4065], pen=f"9p,{color_highlight}@60", no_clip=True)

fig.plot(x=[25, 25], y=[0, 2554], pen=f"9p,{color_highlight}@80", no_clip=True)
fig.plot(x=[35, 35], y=[0, 1984], pen=f"9p,{color_highlight}@80", no_clip=True)
fig.plot(x=[45, 45], y=[0, 1255], pen=f"9p,{color_highlight}@80", no_clip=True)

fig.plot(x=[50, 50], y=[-100, 4700], pen=f"1.5p,{color_highlight},6_2", no_clip=True)
fig.plot(x=[20, 20], y=[-100, 4700], pen=f"1.5p,{color_highlight},6_2", no_clip=True)

fig.text(text=f"{start_date} to {end_date}", offset="-0.6c/-0.5c", **args_text)
fig.text(text=f"M@-w@- = {min_mag_w} to {max_mag_w}", offset="-0.6c/-1.2c", **args_text)

fig.show()
fig_name = f"histo_hdepth_{eq_catalog_name}"
for ext in ["pdf", "png"]:  # "pdf", "eps"
    fig.savefig(fname=f"{path_out}{fig_name}.{ext}", dpi=dpi_png)

print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Make histogram for moment magnitude
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
pygmt.config(FONT="11p") #, MAP_FRAME_PEN="0.8p,gray50")

fig.histogram(
    region=[6, 9.5, 0, 0],
    projection="X10c",
    frame=["WStr", "xa0.50.1+lmoment magnitude", "y+lcounts of earthquakes"],
    data=data_eq_used["mag"],
    series=0.1,
    fill=f"{color_highlight}@80",
    pen="0.5p,gray40,solid",
    histtype=0,
    annotate="+o2p+r+f7p",
)

args_text = {
    "font": "10p,black",
    "position": "TR",
    "pen": "0.8p,gray50",
    "clearance": clearance_standard,
}
fig.text(text=f"{start_date} to {end_date}", offset="-0.6c/-0.5c", **args_text)
fig.text(text=f"M@-w@- = {min_mag_w} to {max_mag_w}", offset="-0.6c/-1.2c", **args_text)

fig.show()
fig_name = f"histo_mw_{eq_catalog_name}"
for ext in ["pdf", "png"]:  # "pdf", "eps"
    fig.savefig(fname=f"{path_out}{fig_name}.{ext}", dpi=dpi_png)

print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Create geographic map
# -----------------------------------------------------------------------------
fig = pygmt.Figure()

fig.basemap(projection=proj_used, region="g", frame=0)
# fig.coast(shorelines=f"1/0.01p,{color_sl}", land=color_land, water=color_water,
          # dcw=["Japan+gblue", "Indonesia+ggreen"])

# -----------------------------------------------------------------------------
# Plot plate boundaries
fig.plot(data=f"{path_in}{file_pb}", pen=f"0.8p,{color_pb}")

# -----------------------------------------------------------------------------
#"""
if proj == "epi":
    # Color epicentral distance range for XKS phases
    center_coord = {"x": lon_center, "y": lat_center}
    fig.plot(
        style=f"w{dist_min * size2dist}/0/360+i{dist_max* size2dist}",
        fill=f"{color_highlight}@90",
        **center_coord,
    )
#"""

# -----------------------------------------------------------------------------
# Make colormap for hypocentral depth
pygmt.makecpt(cmap="lajolla", series=[0, 500, 1])

# Plot epicenters
epi_columns = ["longitude", "latitude", "depth", "mag_scaled"]
# fig.plot(data=data_eq_used[epi_columns], cmap=True, style="cc", pen="0.3p,gray30")
# fig.plot(data=data_eq_used[epi_columns], style="a0.2c", fill="darkred", pen="0.01p,white")

"""
# Add colorbar for hypocentral depth color-coding
with pygmt.config(FONT="14p"):
    fig.colorbar(
        frame=["xa100+lhypocentral depth", "y+lkm"],
        position="JBC+o-2.5c/0.8c+w5c/0.3c+h+ml+ef0.2c",
        box=box_standard,
    )

# Add legend for magnitude size-coding
fig.legend(spec=f"{path_in}{file_legend}", position="JBC+o3c/0.93c+w4c", box=box_standard)

# Add label for time period
fig.text(
    text=f"{start_date} to {end_date}",
    font="black", #col_highlight,
    position="BR",
    offset="-0.6c/-0.7c",
    pen="0.8p,gray50",
    clearance=clearance_standard,
    no_clip=True,
)
"""

# -----------------------------------------------------------------------------
# Plot map frame on top
with pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray30"):
    fig.basemap(frame=frame_used)


# -----------------------------------------------------------------------------
if proj == "epi":
    #"""
    # Mark epicentral distance range for XKS phases
    for epi_lim in [dist_min, dist_max]:
        fig.plot(style=f"E-{epi_lim*2}+d", pen=f"1p,{color_highlight},-", **center_coord)

    # Cover earthquakes outside of epicentral distance range for XKS phases
    # fig.plot(x=lon_center, y=lat_center, style=f"w{fig_size-0.1}/-55/260+i10.35c", fill="white")
    # in_size = 6.1
    # shift = (fig_size - in_size) / 2
    # fig.shift_origin(xshift=f"{shift}c", yshift=f"{shift}c")
    # with pygmt.config(MAP_FRAME_PEN="cyan@100"):
    #     proj_in = f"E{lon_center}/{lat_center}/{dist_min}/{in_size}c"
    #     fig.basemap(projection=proj_in, region="g", frame=0)
    # fig.coast(shorelines=f"1/0.01p,{color_sl}", land=color_land, water=color_water)

    # Label epicentral distance range for XKS phases
    for epi_lim in [dist_min, dist_max]:
        fig.text(
            text=f"{epi_lim}@.",
            offset=f"0c/-{epi_lim * size2dist / 2}c",
            fill="white@30",
            pen=f"0.3p,{color_highlight}",
            clearance=clearance_standard,
            no_clip=True,
            **center_coord,
        )
    #"""

    # Plot recording stations
    fig.plot(style="i0.4c", fill=color_sta, pen="0.8p,black", **center_coord)
    fig.text(
        text="URG",
        offset="0c/0.4c",
        fill="white@30",
        # pen=f"0.3p,{color_sta}",
        pen=f"0.8p,{color_highlight}",
        clearance=clearance_standard,
        # font="black",
        font=f"8p,1,{color_highlight}",
        **center_coord,
    )


# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = f"map_{proj}_{eq_catalog_name}4talk_dist"
# for ext in ["png"]:  # "pdf", "eps"
#     fig.savefig(fname=f"{path_out}{fig_name}.{ext}", dpi=dpi_png, transparent=True)
print(fig_name)
