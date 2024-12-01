# -*- coding: utf-8 -*-
# #############################################################################
# AGU24 | Washington, D.C. | December 9, 2024
#
# The impact of GMT in the Earth, Ocean and Space sciences: What's next? – U12B-05
# PyGMT – Accessing and Integrating GMT with Python and the Scientific Python Ecosystem
#
# Yvonne Fröhlich | Dongdong Tian | Wei Ji Leong | Max Jones | Michael Grund
#
# Python scripts to reproduce the examples shown in the presentation
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/12/01
#   PyGMT v0.13.0 -> https://www.pygmt.org/v0.13.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


# %%
# -----------------------------------------------------------------------------
# Example for NumPy
# -----------------------------------------------------------------------------

import pygmt
import datetime
import numpy as np

# Data retrieved from https://star-history.com/#GenericMappingTools/pygmt&Date 2024/12/01
x = np.array(
    ["2017-03-30", "2017-08-05", "2018-05-24", "2019-01-11", "2019-12-10", "2020-05-18",
     "2020-12-29", "2021-06-22", "2021-12-01", "2022-03-06", "2022-07-26", "2023-02-16",
     "2023-09-11", "2023-11-11", "2024-05-11", "2024-12-01"], dtype=np.datetime64
)
y = np.array([0, 30, 90, 150, 210, 240, 300, 360, 420, 450, 510, 570, 630, 660, 720, 769])

fig = pygmt.Figure()
fig.basemap(
    projection="X12c/6c",
    region=[datetime.date(2017, 1, 1), datetime.date(2024, 12, 31), 0, 800],
    frame=["x+lyear", "y+lGitHub stars"],
)

fig.plot(x=x, y=y, pen="1p,255/222/87", no_clip=True)
fig.plot(x=x, y=y, style="c0.25c", fill="238/86/52", pen="1.5p,63/124/173", no_clip=True)

fig.show()


fig_name_basic = "FTLJG_agu24_u12b05_pygmt_"
dpi_png = 720
fig.savefig(fname=f"{fig_name_basic}numpy.png", dpi=dpi_png)
