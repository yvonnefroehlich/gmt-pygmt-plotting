# #############################################################################
# Adjust the fontsize of a colorbar in GMT 6.5.0 or higher:
# Automatic scaling relatively to the colorbar length
# - For GMT 6.5.0-6.6.0: Use the scaling factor to revert it manually
# - For GMT >=6.7.0: Use -H to turn it off
#   For PyGMT >= 0.20.0: Use alias no_font_scaling instead
#   Please note besides the auto-scaling of the font also updates regarding the
#   the frame thickness and the tick lengths of the colorbar were made. These
#   are also revert via -H or no_font_scaling
# - For background on this change see
#   https://github.com/GenericMappingTools/gmt/pull/6802
#   https://github.com/GenericMappingTools/gmt/issues/9317#issuecomment-7115238925
# -----------------------------------------------------------------------------
# History
# - Created: 2024/11/26
# - Updated: 2025/08/26 - Include annotations
# - Updated: 2025/10/01 - Adjust specific fontsize default parameters
# - Updated: 2026/07/30 - Include -M or no_font_scaling for GMT 6.7.0 or higher
#                         Be more accurate with the terms "length" and "width"
# -----------------------------------------------------------------------------
# Versions
# - PyGMT 0.18.0 -> https://www.pygmt.org
# - GMT 6.6.0 -> https://www.generic-mapping-tools.org
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt
import numpy as np

# -----------------------------------------------------------------------------
def scale_cb_font(cb_length):
    scale_factor = 1 / 15  # scale factor used in GMT >= 6.5.0
    font_scaling = np.sqrt(cb_length * scale_factor)
    return font_scaling
# -----------------------------------------------------------------------------


# %%
# -----------------------------------------------------------------------------
# Example 1
# -----------------------------------------------------------------------------
font_size = 7

plot_size = 5
args_bmap = {
    "region": [-plot_size, plot_size] * 2,
    "projection": f"X{plot_size}c",
    "frame": 1,
}

cb1_length = 4
cb2_length = 2
cb1_label = "cb1 is long"
cb2_label = "cb2 is short"

# -----------------------------------------------------------------------------
# >>> GMT < 6.7.0 <<<
fig = pygmt.Figure()

# Left
pygmt.config(FONT=font_size)
fig.basemap(**args_bmap)

fig.colorbar(cmap="navia", position=f"jTC+w{cb1_length}c+h", frame=f"x+l{cb1_label}")
fig.colorbar(cmap="navia", position=f"jBC+w{cb2_length}c+h", frame=f"x+l{cb2_label}")

# Right
fig.shift_origin(xshift="6c")
with pygmt.config(FONT=font_size):
    fig.basemap(**args_bmap)

font_scaling1 = scale_cb_font(cb1_length)
with pygmt.config(FONT=f"{font_size / font_scaling1}"):
    fig.colorbar(cmap="navia", position=f"jTC+w{cb1_length}c+h", frame=f"x+l{cb1_label}")
font_scaling2 = scale_cb_font(cb2_length)
with pygmt.config(FONT=f"{font_size / font_scaling2}"):
    fig.colorbar(cmap="navia", position=f"jBC+w{cb2_length}c+h", frame=f"x+l{cb2_label}")

fig.show()
# fig.savefig(fname="cb_font_scaling_1a.png")

# -----------------------------------------------------------------------------
# >>> GMT >= 6.7.0 and PyGMT >= 0.20.0 <<<
fig = pygmt.Figure()
pygmt.config(FONT=font_size)

# Left
fig.basemap(**args_bmap)
fig.colorbar(cmap="navia", position=f"jTC+w{cb1_length}c+h", frame=f"x+l{cb1_label}")
fig.colorbar(cmap="navia", position=f"jBC+w{cb2_length}c+h", frame=f"x+l{cb2_label}")

# Right
fig.shift_origin(xshift="6c")
fig.basemap(**args_bmap)
fig.colorbar(cmap="navia", position=f"jTC+w{cb1_length}c+h", frame=f"x+l{cb1_label}", no_font_scaling=True)
fig.colorbar(cmap="navia", position=f"jBC+w{cb2_length}c+h", frame=f"x+l{cb2_label}", no_font_scaling=True)

fig.show()
# fig.savefig(fname="cb_font_scaling_1b.png")


# %%
# -----------------------------------------------------------------------------
# Example 2
# -----------------------------------------------------------------------------
font_size = 18

plot_size = 5
args_bmap = {
    "region": [-1, 1, -plot_size, plot_size],
    "projection": f"X4c/{plot_size}c",
    "frame": 1,
}

cb_length = 4
args_cb = {
    "cmap": "batlow",
    "position": f"jMC+w{cb_length}c",
    "frame": ["x+lquantity", "y+lunit"],
}
font_scaling = scale_cb_font(cb_length)

# -----------------------------------------------------------------------------
fig = pygmt.Figure()

# Left
fig.basemap(**args_bmap)

fig.colorbar(**args_cb)

# Middle
fig.shift_origin(xshift="+w+1c")

with pygmt.config(
    FONT_ANNOT_PRIMARY=f"{font_size}p",  # x-annotations (-> numbers)
    FONT_ANNOT_SECONDARY=f"{font_size}p",  # y-label (-> unit)
    FONT_LABEL=f"{font_size}p",  # x-label (-> quantity)
    # FONT=f"{font_size}p"  # all three
):
    fig.basemap(**args_bmap)

    fig.colorbar(**args_cb)

# Right
fig.shift_origin(xshift="+w+1c")

with pygmt.config(FONT=font_size):
    fig.basemap(**args_bmap)

with pygmt.config(
    FONT_ANNOT_PRIMARY=f"{font_size / font_scaling}p",
    FONT_ANNOT_SECONDARY=f"{font_size / font_scaling}p",
    FONT_LABEL=f"{font_size / font_scaling}p",
):
    fig.colorbar(**args_cb)

fig.show()
fig.savefig(fname="cb_font_scaling_2.png")
