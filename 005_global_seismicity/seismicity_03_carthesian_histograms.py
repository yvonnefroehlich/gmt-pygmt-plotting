# #############################################################################
# Global seismicity
# - Create histograms for
#   - hypocentral depth
#   - moment magitude
# -----------------------------------------------------------------------------
# History
# - Created: 2025/07/23
# - Updated: 2025/09/07
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


import pygmt
import pandas as pd


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"
dpi_png = 360

# Plotting
color_hl = "255/90/0"  # highlight -> orange
box_standard = "+gwhite@30+p0.8p,gray50+r2p"
clearance_standard = "0.1c+tO"

args_text = {
    "font": "10p,black",
    "position": "TR",
    "pen": "0.8p,gray50",
    "clearance": clearance_standard,
}


# %%
# -----------------------------------------------------------------------------
# Load earthquake data
# -----------------------------------------------------------------------------
start_date = "1991-01-01"
end_date = "2019-12-31"
min_mag_w = 6
max_mag_w = 10

eq_catalog_name = f"global_seismicity_{start_date}to{end_date}_mw{min_mag_w}to{max_mag_w}"
df_eq_raw = pd.read_csv(f"{path_in}/data_{eq_catalog_name}.csv", sep="\t")

# Filter data
# mw, mwc, mwb, mwr, mww
df_eq = df_eq_raw[df_eq_raw["magType"].str.contains("mw")]


# %%
# -----------------------------------------------------------------------------
# Make histogram for hypocentral depth
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
pygmt.config(FONT="11p")

fig.histogram(
    region=[-10.1, 500, 0, 4700],
    projection="X17c/10c",
    frame=["WStr", "xa50f10+lhypcentral depth / km", "y+lcounts of earthquakes"],
    data=df_eq["depth"],
    series=10,
    fill="gray@85",
    pen="0.5p,gray40,solid",
    histtype=0,
    annotate="+o2p+r+f7p",
    cumulative="r",  # reverse
    extreme="b",
    barwidth="10+o10",
)

# Highlight bars for hypocentral depth between 0 km and 25 km
fig.plot(x=[5, 5], y=[0, 4308], pen=f"9p,{color_hl}@60", no_clip=True)
fig.plot(x=[15, 15], y=[0, 4065], pen=f"9p,{color_hl}@60", no_clip=True)

# Highlight bars for hypocentral depth between 25 km and 50 km
fig.plot(x=[25, 25], y=[0, 2554], pen=f"9p,{color_hl}@80", no_clip=True)
fig.plot(x=[35, 35], y=[0, 1984], pen=f"9p,{color_hl}@80", no_clip=True)
fig.plot(x=[45, 45], y=[0, 1255], pen=f"9p,{color_hl}@80", no_clip=True)

# Mark hypocentral depth of 50 km and 20 km
fig.plot(x=[50, 50], y=[-100, 4700], pen=f"1.5p,{color_hl},6_2", no_clip=True)
fig.plot(x=[20, 20], y=[-100, 4700], pen=f"1.5p,{color_hl},6_2", no_clip=True)

# Add info labels
fig.text(text=f"{start_date} to {end_date}", offset="-0.6c/-0.5c", **args_text)
fig.text(text=f"M@-w@- = {min_mag_w} to {max_mag_w}", offset="-0.6c/-1.2c", **args_text)

fig.show()
fig_name = f"histo_hdepth_{eq_catalog_name}"
# for ext in ["png"]:  # "pdf", "eps"
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Make histogram for moment magnitude
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
pygmt.config(FONT="11p")

fig.histogram(
    region=[6, 9.5, 0, 0],
    projection="X10c",
    frame=["WStr", "xa0.50.1+lmoment magnitude", "y+lcounts of earthquakes"],
    data=df_eq["mag"],
    series=0.1,
    fill="gray@85",
    pen="0.5p,gray40,solid",
    histtype=0,
    annotate="+o2p+r+f7p",
)

fig.text(text=f"{start_date} to {end_date}", offset="-0.6c/-0.5c", **args_text)
fig.text(text=f"M@-w@- = {min_mag_w} to {max_mag_w}", offset="-0.6c/-1.2c", **args_text)

fig.show()
fig_name = f"histo_mw_{eq_catalog_name}"
# for ext in ["png"]:  # "pdf", "eps"
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}", dpi=dpi_png)
print(fig_name)
