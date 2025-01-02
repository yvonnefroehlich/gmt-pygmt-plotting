# -*- coding: utf-8 -*-
# #############################################################################
# Adjust the font size of a colorbar in GMT 6.5
# - Revert the auto-scaling relatively to the colorbar width
# - For background on this change see the upstream GMT pull request 6802 at
#   https://github.com/GenericMappingTools/gmt/pull/6802
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/11/26
#   PyGMT v0.13.0 -> https://www.pygmt.org/v0.13.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


import pygmt
import numpy as np


plot_size = 5
font_size = 6

cb1_width = 4
cb2_width = 1.5
cb1_label = "cb1 is long"
cb2_label = "cb2 is short"


# -----------------------------------------------------------------------------
def scale_cb_font(cb_width):
    scale_factor = 1 / 15  # scale factor used in GMT 6.5
    font_scaling = np.sqrt(cb_width * scale_factor)
    return font_scaling
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=[-plot_size, plot_size] * 2, projection=f"X{plot_size}c", frame=0)

fig.colorbar(cmap="navia", position=f"jTC+w{cb1_width}c+h", frame=f"x+l{cb1_label}")
fig.colorbar(cmap="navia", position=f"jBC+w{cb2_width}c+h", frame=f"x+l{cb2_label}")

# -----------------------------------------------------------------------------
fig.shift_origin(xshift="5.5c")
fig.basemap(region=[-plot_size, plot_size] * 2, projection=f"X{plot_size}c", frame=0)

font_scaling = scale_cb_font(cb1_width)
with pygmt.config(FONT=f"{font_size / font_scaling}"):
    fig.colorbar(cmap="navia", position=f"jTC+w{cb1_width}c+h", frame=f"x+l{cb1_label}")

font_scaling = scale_cb_font(cb2_width)
with pygmt.config(FONT=f"{font_size / font_scaling}"):
    fig.colorbar(cmap="navia", position=f"jBC+w{cb2_width}c+h", frame=f"x+l{cb2_label}")

# -----------------------------------------------------------------------------
fig.show()
