# #############################################################################
# Global seismicity
# - Request earthquake data from USGS
# - Download the data into a pandas DataFrame
# - Write the data to a CSV file
# -----------------------------------------------------------------------------
# History
# - Created: 2025/07/23
# - Updated: 2025/09/07 - improve code style and comments
# -----------------------------------------------------------------------------
# Versions
#   PyGMT v0.16.0 -> https://www.pygmt.org/v0.16.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pandas as pd

# %%
# -----------------------------------------------------------------------------
# Request earthquake data
# -----------------------------------------------------------------------------
# >>> Set for your needs <<<

# >>> Only works with single quotation marks <<<
start_date = "1991-01-01"
end_date = "2019-12-31"
min_mag_w = "6"  # magnitude, later filter regarding moment magnitude
max_mag_w = "10"
order_records = "time-asc"  # 'magnitude'

path_in = "01_in_data"


# %%
# -----------------------------------------------------------------------------
# Download earthquake data
# -----------------------------------------------------------------------------
# Set up request
# see https://earthquake.usgs.gov/fdsnws/event/1/
# last access: 2025/01/26
url_usgs = "https://earthquake.usgs.gov/fdsnws/event/1/query.csv"

url_usgs_request = (
    url_usgs
    + "?"
    + "&".join(
        [
            "starttime=" + start_date + "%2000:00:00",
            "endtime=" + end_date + "%2000:00:00",
            "minmagnitude=" + min_mag_w,
            "maxmagnitude=" + max_mag_w,
            "orderby=" + order_records,
        ]
    )
)

eq_catalog_name = (
    f"global_seismicity_{start_date}to{end_date}_mw{min_mag_w}to{max_mag_w}"
)

# Download data into a pandas DataFrame
data_eq_raw = pd.read_csv(url_usgs_request)

# Write data to a CSV file
data_eq_raw.to_csv(
    path_or_buf=f"{path_in}/data_{eq_catalog_name}.csv", sep="\t", index=False
)

print(eq_catalog_name)
