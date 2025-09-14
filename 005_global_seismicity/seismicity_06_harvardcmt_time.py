# #############################################################################
# Global seismicity based on the Harvard CMT catalog
# - Cartesian plots year-day as function of the moment magnitude
# - Data are from the earthquake catalog provided along with the MATLAB package
#   SplitLab (Wüstefeld et al. 2008) exported as CSV file
#   See https://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/COMBO/combo.ndk
#   last accessed 2025/09/08
# >>> Just play around with the data <<<
# -----------------------------------------------------------------------------
# History
# - Created: 2025/09/12
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


import numpy as np
import pandas as pd
import pygmt as gmt

# %%
# -----------------------------------------------------------------------------
# Adjust for your needs
# -----------------------------------------------------------------------------
# minimum hypocentral depth
min_depth = 20 # kilometers

# Resolution of output PNG
dpi_png = 360  # dpi

# Path
path_in = "01_in_data"
path_out = "02_out_figs"


# %%
# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
df_eq_raw = pd.read_csv(f"{path_in}/catalog_harvardcmt_1976to2025_mw4to10.csv", sep=",")

# Keep only relevant columns
columns = [
    "year", "month", "day", "hour", "minute", "second", "jday", "dstr",
    "latitude", "longitude", "azi", "bazi", "dis", "depth",
    "magnitude", "M0", "strike", "dip", "rake", "region",
]
df_eq_mod = df_eq_raw[columns]

df_eq_depth = df_eq_mod[df_eq_mod["depth"] >= min_depth]


# %%
# -----------------------------------------------------------------------------
# Make Cartesian plot
# -----------------------------------------------------------------------------
step_mag = 0.5
for min_mag in np.arange(4, 10 + step_mag, step_mag):

    df_eq_mag = df_eq_depth[df_eq_depth["magnitude"] >= min_mag]

    fig = gmt.Figure()

    fig.basemap(
        region=[1975.01, 2025.99, 0.01, 31.99],
        projection="X15c/10c",
        frame=["WStr", "xa5f1+lyear", "ya2f1+lmonth day"],
    )
    with gmt.config(FONT="14p"):
        fig.basemap(
            frame= f"+thd >= {min_depth} km   Mw >= {min_mag}   " + \
                f"{len(df_eq_mag)}/{len(df_eq_depth)}/{len(df_eq_mod)} events+gblack"
        )

    if len(df_eq_mag) > 0:
        args_plot = {"x": df_eq_mag["year"], "y": df_eq_mag["day"], "style": "s0.35c"}
        fig.plot(fill="white", **args_plot)
        fig.plot(fill="steelblue@95", **args_plot)

    fig.show()
    fig_name = "plot_harvardcmt_1976to2025_mw" + "p".join(str(min_mag).split(".")) + \
                f"_year_day_depth{min_depth}km"
    # for ext in ["png"]:  # "pdf", "eps"
    #     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
    print(fig_name)
