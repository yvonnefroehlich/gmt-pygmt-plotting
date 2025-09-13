# #############################################################################
# Harvard CMT catalog
# - Cartesian plots for strike dip rake (Aki and Richards convention)
# - Data are from the earthquake catalog provided along with the MATLAB package
#   SplitLab (Wüstefeld et al. 2008) exported as CSV file
#   See https://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/COMBO/combo.ndk
#   last accessed 2025/09/08
# -----------------------------------------------------------------------------
# History
# - Created: 2025/09/10
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


import pandas as pd
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# Adjust for your needs
# -----------------------------------------------------------------------------
# minimum of moment magnitude
min_mag = 5

# Resolution of output PNG
dpi_png = 360  # dpi

# Path
path_in = "01_in_data"
path_out = "02_out_figs"


# %%
# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
df_eq_raw = pd.read_csv(f"{path_in}/harvardcmt.csv", sep=",")

# Keep only relevant columns
columns = [
    "year", "month", "day", "hour", "minute", "second", "jday", "dstr",
    "latitude", "longitude", "azi", "bazi", "dis", "depth",
    "magnitude", "M0", "strike", "dip", "rake", "region",
]
df_eq_mod = df_eq_raw[columns]

df_eq_mag = df_eq_mod[df_eq_mod["magnitude"] >= min_mag]


# %%
# -----------------------------------------------------------------------------
# Make Cartesian plot
# -----------------------------------------------------------------------------
for i_plot in range(3):

    fig = gmt.Figure()

    if i_plot == 0:
        columns = ["strike", "dip", "rake"]
        region = [0, 360, 0, 90]
        frame_map = ["WsNe", "xa30f10+lstrike+u°", "ya10f5+ldip+u°"]
        frame_cb = ["xa30f10+u°", "y+lrake"]
        gmt.makecpt(cmap="romaO", series=[-180, 180], cyclic=True)
    elif i_plot == 1:
        columns = ["strike", "rake", "dip"]
        region = [0, 360, -180, 180]
        frame_map = ["WsNe", "xa30f10+lstrike+u°", "ya30f10+lrake+u°"]
        frame_cb = ["xa10f5+u°", "y+ldip"]
        gmt.makecpt(cmap="navia", series=[0, 90])
    elif i_plot == 2:
        columns = ["rake", "dip", "strike"]
        region = [-180, 180, 0, 90]
        frame_map = ["WsNe", "xa30f10+lrake+u°", "ya10f5+ldip+u°"]
        frame_cb = ["xa30f10+u°", "y+lstrike"]
        gmt.makecpt(cmap="romaO", series=[0, 360], cyclic=True)

    fig.basemap(region=region, projection="X12c/12c", frame=frame_map)
    if len(df_eq_mag) > 0:
        fig.plot(data=df_eq_mag[columns], cmap=True, style="c0.1c")
    with gmt.config(FONT="10p"):
        fig.colorbar(frame=frame_cb)

    fig.show()
    fig_name = "plot_harvardcmt_" + "_".join(columns) + \
                "_mw" + "p".join(str(min_mag).split("."))
    # for ext in ["png"]:  # "pdf", "eps"
    #     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
    print(fig_name)
