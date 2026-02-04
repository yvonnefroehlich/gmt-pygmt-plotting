# #############################################################################
# Global seismicity based on the Harvard CMT catalog
# - Cartesian plots for year-day as function of the moment magnitude
# - Data are from the earthquake catalog provided along with the MATLAB package
#   SplitLab (Wüstefeld et al. 2008) exported as CSV file
#   See https://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/COMBO/combo.ndk
#   last accessed 2025/09/08
# >>> Just play around with the data <<<
# -----------------------------------------------------------------------------
# History
# - Created: 2025/09/12
# - Updated: 2025/09/15 - Create legend
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.16.0 - v0.18.0 -> https://www.pygmt.org | https://www.pygmt.org
# - GMT 6.5.0 - 6.6.0 -> https://www.generic-mapping-tools.org
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
# Set minimum hypocentral depth
min_depth = 20  # kilometers

# Resolution of output PNG
dpi_png = 360  # dpi

# Path
path_in = "01_in_data"
path_out = "02_out_figs"

# Plotting
fill = "steelblue@95"
symbol_shape = "rounded"

match symbol_shape:
    case "square":
        style = "s0.32c"
        style_leg = "s0.4c"
    case "circle":
        style = "c0.23c"
        style_leg = "c0.31c"
    case "rounded":
        style = "R0.22c/0.22c/0.05c"
        style_leg = "R0.3c/0.3c/0.06c"


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
start_box = 1976
end_box = 2025
len_box = end_box - start_box
x_box = np.arange(start_box, end_box + 1, 1)
step_box = 2
n_layer = 2
y_box = -5.5

step_mag = 0.5
for min_mag in np.arange(4, 10 + step_mag, step_mag):
    df_eq_mag = df_eq_depth[df_eq_depth["magnitude"] >= min_mag]

# -----------------------------------------------------------------------------
    # Set up basic plot
    fig = gmt.Figure()
    fig.basemap(
        region=[start_box - 0.99, end_box + 0.99, 1 - 0.99, 31 + 0.99],
        projection="X15c/10c",
        frame=["WStr", "xa5f1+lyear", "ya2f1+lmonth day"],
    )
    with gmt.config(FONT="14p", MAP_TITLE_OFFSET="8p"):
        fig.basemap(
            frame= f"+thd >= {min_depth} km   Mw >= {min_mag}   " + \
                f"{len(df_eq_mag)}/{len(df_eq_depth)}/{len(df_eq_mod)} events+gblack"
        )

# -----------------------------------------------------------------------------
    # Plot data points with semi-transparency to indicate density
    if len(df_eq_mag) > 0:
        args_plot = {"x": df_eq_mag["year"], "y": df_eq_mag["day"], "style": style}
        fig.plot(fill="white", **args_plot)
        fig.plot(fill=fill, **args_plot)

# -----------------------------------------------------------------------------
    # Create legend
    for i_box, box in enumerate(np.arange(0, len_box, step_box)):
        x_box_temp = x_box[box:len_box:step_box]

        for i_layer in range(n_layer):
            fig.plot(
                x=x_box_temp,
                y=[y_box] * len(x_box_temp),
                style=style_leg,
                fill=fill,
                pen="1p,black",
                no_clip=True
            )

        fig.text(
            text=(i_box + 1) * n_layer,
            x=x_box[box],
            y=y_box,
            offset="0c/-0.4c",
            no_clip=True,
        )

    args_text = {"x": start_box - 1.5, "justify": "RM", "no_clip": True}
    fig.text(y=y_box, text="event", **args_text)
    fig.text(y=y_box - 1, text="count", **args_text)

# -----------------------------------------------------------------------------
    fig.show()
    fig_name = "plot_harvardcmt_1976to2025_mw" + "p".join(str(min_mag).split(".")) + \
            f"_year_day_depth{min_depth}km_{symbol_shape}"
    # for ext in ["png"]:  # "pdf", "eps"
    #     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
    print(fig_name)
