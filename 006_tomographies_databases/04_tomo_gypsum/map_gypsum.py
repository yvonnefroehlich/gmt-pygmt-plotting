# #############################################################################
# GyPSuM tomography; Simmons et al. 2010
# -----------------------------------------------------------------------------
# History
# - Created: 2025/01/24
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.14.0 - v0.18.0 -> https://www.pygmt.org
# - GMT 6.5.0 - 6.6.0 -> https://www.generic-mapping-tools.org
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data/"
path_out = "02_out_figs/"

grid_tomo = f"{path_in}tomo_gypsum_1d_grid_dvs_22_2650to2900km.grd"

color_highlight = "255/90/0"
color_sl = "gray10"  # shorelines (used data built-in in PyGMT / GMT)

cmap_in = "roma"
cmap_lim = 2.5  # Absolute limit used to set up to colormap, in percentage
color_bg = "pink"  # Color for values smaller the value range
color_fg = "cyan"  # Color for values larger than the value range

font_label = 6


# %%
# -----------------------------------------------------------------------------
# Make geographic map
# -----------------------------------------------------------------------------
fig = gmt.Figure()
fig.basemap(region="d", projection="N10c", frame=["xa90f45", "ya30f45", "wSnE"])

# -----------------------------------------------------------------------------
# Plot grid with color-coding
# Uncomment if you like to highlight values outside the value range in specific colors
# gmt.config(COLOR_BACKGROUND=color_bg, COLOR_FOREGROUND=color_fg)
gmt.makecpt(series=[-cmap_lim, cmap_lim, 0.01], cmap="roma")  #, overrule_bg=True)
fig.grdimage(grid=grid_tomo, cmap=True)
fig.colorbar(frame=["xa1f0.1", "y+ldvs / %"], position="+e0.3c")

# -----------------------------------------------------------------------------
# Plot shorelines
fig.coast(shorelines=f"1/0.1p,{color_sl}")

# -----------------------------------------------------------------------------
args_label = {"font": f"{font_label}p,{color_highlight}", "no_clip": True}
# Add label for depth
fig.text(position="TL", text=f"@@{2650} - {2900} km", **args_label)
# Add label for tomography name
fig.text(position="BL", text="GyPSuM", **args_label)

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()

fig_name = f"gypsum_1deg_global_dvs_2650to2900km_dvlim{cmap_lim}"
# for ext in ["png"]:
#     fig.savefig(fname=f"{path_out}{fig_name}.{ext}")

print(fig_name)
