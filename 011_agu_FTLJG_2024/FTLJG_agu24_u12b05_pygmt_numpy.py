# #############################################################################
# AGU24 | Washington, D.C. | December 9, 2024
#
# The impact of GMT in the Earth, Ocean and Space sciences: What's next? – U12B-05
# PyGMT – Accessing and Integrating GMT with Python and the Scientific Python Ecosystem
#
# Yvonne Fröhlich | Dongdong Tian | Wei Ji Leong | Max Jones | Michael Grund
#
# Python scripts to reproduce the examples shown in the talk
#
# Slides of the talk are freely available at https://doi.org/10.6084/m9.figshare.28049495
# -----------------------------------------------------------------------------
# History
# - Created: 2024/11/30
# - Updated: 2025/12/02 - Correct RGB code for Python's blue
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.13.0 -> https://www.pygmt.org/v0.13.0/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


# %%
# -----------------------------------------------------------------------------
# Example for NumPy
# -----------------------------------------------------------------------------

import pygmt
import numpy as np  # Required dependency
import datetime

# Data retrieved from https://star-history.com/#GenericMappingTools/gmt&Date
# last access 2024-12-01
dates_gmt = np.array(
    [
        "2018-08-13",
        "2019-01-04",
        "2019-03-01",
        "2019-07-27",
        "2019-11-29",
        "2020-03-13",
        "2020-07-08",
        "2020-09-26",
        "2021-03-15",
        "2021-09-13",
        "2022-02-16",
        "2022-08-23",
        "2023-04-13",
        "2023-11-17",
        "2024-05-29",
        "2024-12-01",
    ],
    dtype=np.datetime64,
)
stars_gmt = np.array(
    [0, 60, 120, 180, 240, 300, 360, 390, 450, 510, 570, 630, 690, 750, 810, 864]
)
color_gmt = "238/86/52"  # GMT red

# Data retrieved from https://star-history.com/#GenericMappingTools/pygmt&Date
# last access 2024-12-01
dates_py = np.array(
    [
        "2017-03-30",
        "2017-08-05",
        "2018-05-24",
        "2019-01-11",
        "2019-12-10",
        "2020-05-18",
        "2020-12-29",
        "2021-06-22",
        "2021-12-01",
        "2022-03-06",
        "2022-07-26",
        "2023-02-16",
        "2023-09-11",
        "2023-11-11",
        "2024-05-11",
        "2024-12-01",
    ],
    dtype=np.datetime64,
)
stars_py = np.array(
    [0, 30, 90, 150, 210, 240, 300, 360, 420, 450, 510, 570, 630, 660, 720, 769]
)
color_py = "48/105/152"  # Python blue

# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(
    projection="X12c/6c",
    region=[datetime.date(2017, 1, 1), datetime.date(2025, 6, 30), 0, 900],
    frame=["x+lyear", "y+lGitHub stars"],
)

args_dots = {"style": "c0.23c", "no_clip": True}

fig.plot(x=dates_gmt, y=stars_gmt, pen=color_gmt, no_clip=True)
fig.plot(x=dates_gmt, y=stars_gmt, fill="238/86/52", label="GMT", **args_dots)

fig.plot(x=dates_py, y=stars_py, pen=color_py, no_clip=True)
fig.plot(x=dates_py, y=stars_py, fill="63/124/173", label="PyGMT", **args_dots)

fig.legend(position="jBR")
fig.show()


fig_path = "02_out_figs"
fig_name_basic = "FTLJG_agu24_u12b05_pygmt_"
dpi_png = 720
# fig.savefig(fname=f"{fig_path}/{fig_name_basic}numpy.png", dpi=dpi_png)
