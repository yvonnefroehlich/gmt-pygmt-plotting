# -*- coding: utf-8 -*-
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
import pandas as pd


# %%
# -----------------------------------------------------------------------------
# Set up
# -----------------------------------------------------------------------------
# >>> Set for your needs <<<

# Set projection of map
proj = "rob"  ## "rob", "ortho"
fig_size = 12
lon_center = 6  # degrees East
lat_center = 48  # degrees North
epi_dist = 150  # degrees

# Request earthquake data
# >>> Only works with single quotation marks <<<
start_year = 2000
end_year = 2023
start_date = str(start_year) + '-01-01'
end_date = str(end_year) + '-12-31'
min_magnitude = '6'
max_magnitude = '10'
order_records = 'time-asc'  # 'magnitude'

# -----------------------------------------------------------------------------
dpi_png = 360
path_in = "01_in_data/"
path_out = "02_out_figs/"
file_pb = "plate_boundaries_Bird_2003.txt"
file_legend = "legend_gmt_magitude.txt"

# Plotting
color_highlight = "255/90/0"
col_land = "gray90"
col_water = "steelblue@85"
col_pb = "216.750/82.875/24.990"
col_sl = "gray60"
box_standard = "+gwhite@30+p0.8p,black+r2p"
clearance_standard = "0.1c/0.1c+tO"

match proj:
    case "rob":
        proj_used = f"N{fig_size}c"
    case "ortho":
        proj_used =f"E{lon_center}/{lat_center}/{epi_dist}/{fig_size}c"


# %%
# -----------------------------------------------------------------------------
# Download earthquake data
# -----------------------------------------------------------------------------
# Set up request
# see https://earthquake.usgs.gov/fdsnws/event/1/
# last access: 2023/11/20
url_usgs = 'https://earthquake.usgs.gov/fdsnws/event/1/query.csv'

url_usgs_request = url_usgs + '?' + \
    '&'.join([
        'starttime=' + start_date + '%2000:00:00',
        'endtime=' + end_date + '%2000:00:00',
        'minmagnitude=' + min_magnitude,
        'maxmagnitude=' + max_magnitude,
        'orderby=' + order_records,
    ])

eq_catalog_name = f"global_seismicity_{start_date}to{end_date}_mw" + \
                   f"{min_magnitude}to{max_magnitude}"

# Download data into a pandas DataFrame
data_eq_raw = pd.read_csv(url_usgs_request)

# Write data to a CSV file
data_eq_raw.to_csv(
    index=False, path_or_buf=f"{path_in}/data_{eq_catalog_name}.csv", sep="\t",
)

# Filter data
# mw, mwc, mwb, mwr, mww
data_eq_used = data_eq_raw[data_eq_raw["magType"].str.contains("mw")]

# Sort descending by magnitude to avoid overplotting
data_eq_used = data_eq_used.sort_values(by=["mag"], ascending=False)

# Scale hypocentral depth for size-coding
data_eq_used["mag_scaled"] = np.exp(data_eq_used["mag"] / 1.7) * 0.0035


# %%
# -----------------------------------------------------------------------------
# Create geographic map
# -----------------------------------------------------------------------------
fig = pygmt.Figure()

fig.basemap(projection=proj_used, region="g", frame=0)
fig.coast(shorelines=f"1/0.01p,{col_sl}", land=col_land, water=col_water)

# -----------------------------------------------------------------------------
# Plote plate boundaries
fig.plot(data=f"{path_in}{file_pb}", pen=f"0.8p,{col_pb}")

# -----------------------------------------------------------------------------
# Make colormap for hypocentral depth
pygmt.makecpt(cmap="lajolla", series=[0, 500, 1])

# Plot epicenters
epi_columns = ["longitude", "latitude", "depth", "mag_scaled"]
fig.plot(data=data_eq_used[epi_columns], cmap=True, style="cc", pen="0.01p,gray30")

# Add colorbar for hypocentral depth color-coding
with pygmt.config(FONT="14p"):
    fig.colorbar(
        frame=["xa100+lhypocentral depth", "y+lkm"],
        position="JBC+o-2.6c/1.4c+w5c/0.3c+h+ml+ef0.2c",
        box=box_standard,
    )

# Add legend for magnitude size-coding
fig.legend(spec=f"{path_in}{file_legend}", position="JBC+o3c/1.53c+w4c", box=box_standard)

# Plot map frame on top
fig.basemap(frame="af")

# -----------------------------------------------------------------------------
# Add label for time period
fig.text(
    text=f"{start_date} to {end_date}",
    font=color_highlight,
    position="BR",
    offset="-1.2c/-1.2c",
    pen="0.8p,black",
    clearance=clearance_standard,
    no_clip=True,
)

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = f"map_{proj}_{eq_catalog_name}"
# for ext in ["png"]:  # "pdf", "eps"
#     fig.savefig(fname=f"{path_out}{fig_name}.{ext}", dpi=dpi_png)

print(fig_name)
