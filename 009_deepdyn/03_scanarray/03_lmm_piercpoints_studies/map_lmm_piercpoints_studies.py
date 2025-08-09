# #############################################################################
# Map of Grund & Ritter 2019 Geology Data Repository DR14
# - Reproduced in PyGMT
# - Modified highlighting concept
# - SKS and SKKS piercing points in the lowermost mantle
# Note: Partly affected by a SplitLab bug, see https://doi.org/10.4401/ag-8781
# -----------------------------------------------------------------------------
# Usage of data provided along with
# - Grund & Ritter 2019 Geology (-> Data Repository: SKS-SKKS pairs)
#   https://doi.org/10.1130/G45514.1
# - Wolf et al. 2023 G^3 (-> GitHub: LLSVPs)
#   https://doi.org/10.1029/2023GC011070
# -----------------------------------------------------------------------------
# Related to
# - ScanArray / LITHOCAP project by Michael Grund, KIT, 2014/08 - 2019/02
# - DeepDyn project by Yvonne Fröhlich, KIT, 2023/08 - 2025/03
# -----------------------------------------------------------------------------
# History
# - Created: 2025/07/25
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
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"

data_GR2019_same = "SKS_SKKS_GR2019_mod4pygmt_onlysame.dat"
data_GR2019_disc = "SKS_SKKS_GR2019_mod4pygmt_onlydisc.dat"
data_GR2019_stations = pd.read_csv(f"{path_in}/2019049_TableDR1_mod.csv", sep=";")

# -----------------------------------------------------------------------------
# Lambert projection
lon_min = -30
lon_max = 110
lat_min = 40
lat_max = 80

# Determine projection center
lon0 = np.mean([lon_min, lon_max])
lat0 = np.mean([lat_min, lat_max])
# Calculate two standard parallels (only these two distortion-free)
lat1 = lat_min + (lat_max - lat_min) / 3
lat2 = lat_min + (lat_max - lat_min) / 3 * 2

region = [lon_min, lon_max, lat_min, lat_max]
projection = f"L{lon0}/{lat0}/{lat1}/{lat2}/10c"
# projection_used = "L40/60/16/80/10c"  # GR2019

# -----------------------------------------------------------------------------
color_XKS = "lightred"
color_sScS = "goldenrod4"
color_SScS = "peru"
color_PSref = "darkbrown"
color_same = "white"

color_null = "white"
color_split = "gray50"
color_SKS = "red3"
color_SKKS = "darkorange"

color_land = "gray@85"
color_sl = "gray70"
color_llvp = "gray50"
pattern_llvp = "p8+b+f"

box_standard = "+gwhite@30+p0.1p,gray30+r2p"


# %%
# -----------------------------------------------------------------------------
# Generate geographic map
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(FONT="5.5p", MAP_GRID_PEN_PRIMARY="0.01p,gray80")

fig.basemap(region=region, projection=projection, frame=["WSne", "a15f5g5"])
fig.coast(shorelines=f"1/0.01p,{color_sl}", resolution="h", land=color_land)

# -----------------------------------------------------------------------------
# Region of other anisotropy studies in the lowermost mantle
args_text = {"font": "4p", "fill": "white@30", "justify": "MC"}
pen = "0.5p"
trans = 70

# P/S reflections
args_psref = {"fill": f"{color_PSref}@{trans}", "pen": f"{pen},{color_PSref}"}
fig.plot(x=91, y=71, style="e145/1.4c/0.5c", **args_psref)
fig.plot(x=0, y=0, style="c0.1c", label="P/S reflections+S0.1c", **args_psref)
fig.text(x=95, y=71, text="W1993", angle=325, **args_text)

# ScS-S sScS-sS and SKS/SPdKS/SKPdS
args_s = {"fill": f"{color_sScS}@{trans}", "pen": f"{pen},{color_sScS}"}
fig.plot(x=-13.5, y=65, style="c1.4c", label="ScS-S sScS-sS+S0.1c", **args_s)
fig.plot(x=0, y=0, style="c0.1c", fill="white", label="SKS/SPdKS/SKPdS+S0.1c") # dummy for legend
fig.text(x=-19, y=67, text="HELM1998", **args_text)
fig.text(x=-15, y=65.9, text="HE2015", **args_text)
fig.text(x=-15, y=62, text="-dvs", justify="MC", font="4p,red", fill="white@30")

# S-ScS
args_scs = {"fill": f"{color_SScS}@{trans}", "pen": f"{pen},{color_SScS}"}
fig.plot(x=75, y=74, style="c0.65c", label="S-ScS+S0.1c", **args_scs)
fig.text(x=75, y=74, text="WK2008",  **args_text)

fig.plot(x=90, y=62, style="e5/2.8c/0.6c", **args_scs)
fig.text(x=90, y=61.5, text="TK2002", angle=5, **args_text)

# SKS-SKKS
args_xks = {"fill": f"{color_XKS}@{trans}", "pen": f"{pen},{color_XKS}"}
fig.plot(x=92.5, y=55, style="c0.55c", label="SKS-SKKS+S0.1c", **args_xks)
fig.text(x=92.5, y=55, text="LL2015", **args_text)

fig.plot(x=40.5, y=58, style="e5/1.8c/1.1c", **args_xks)
fig.text(x=38, y=60, text="LL2015", **args_text)

fig.plot(x=0, y=54, style="e0/1.1c/0.25c", **args_xks)
fig.text(x=0, y=54, text="LL2015", **args_text)

fig.plot(x=5, y=37.5, style="e45/2c/1c", **args_xks)
fig.text(x=5, y=37.5, text="LL2015", **args_text)

with gmt.config(FONT="4.5p"):
    fig.legend(box=box_standard, position="jTL+o-0.41c/-0.32c+w1.85c")

# -----------------------------------------------------------------------------
# Highlight regions with reduced shear wave velocity
for i_model in range(2, 9, 1):
    fig.plot(
        data=f"{path_in}/llvp/3model_2016_{i_model}.txt",
        pen=f"0.2p,{color_llvp}",
        fill=f"{pattern_llvp}{color_llvp}",
        close=True,
    )

# -----------------------------------------------------------------------------
# Plot piercing point SKS-SKKS at CMB by Grund & Ritter (2019) Geology
# DISC
args_same_null = {
    "data": f"{path_in}/{data_GR2019_disc}",
    "incols": [1, 0],
    "fill": "white",
    "style": "c0.07c",
}
args_same_split = {
    "data": f"{path_in}/{data_GR2019_disc}",
    "incols": [1, 0],
    "style": "c0.08c",
    "pen": "0.2p,gray10",
}
fig.plot(
    pen=f"0.5p,{color_SKS}",
    label="disc pairs - SKS null+HGrund & Ritter (2019)",
    find="discSKSNull",
    **args_same_null,
)
fig.plot(
    fill=color_SKS,
    label="disc pairs - SKS split",
    find="discSKSSplit",
    **args_same_split,
)
fig.plot(
    pen=f"0.5p,{color_SKKS}",
    label="disc pairs - SKKS null",
    find="discSKKSNull",
    **args_same_null,
)
fig.plot(
    fill=color_SKKS,
    label="disc pairs - SKKS split",
    find="discSKKSSplit",
    **args_same_split,
)

# SAME
args_same = {
    "data": f"{path_in}/{data_GR2019_same}",
    "style": "c0.04c",
    "pen": "0.2p,gray10",
    "incols": [1, 0],
}
fig.plot(fill=color_null, label="same pairs - both null", find="sameSKSNull", **args_same)
fig.plot(fill=color_null, find="sameSKKSNull", **args_same)
fig.plot(fill=color_split, label="same pairs - both split", find="sameSKSSplit", **args_same)
fig.plot(fill=color_split, find="sameSKKSSplit", **args_same)

with gmt.config(FONT="4.5p"):
    fig.legend(box=box_standard, position="jTR+o-0.21c/-0.32c+w2c")

# -----------------------------------------------------------------------------
# Show and save figure
fig.show()
fig_name = "map_lmm_piercpoints_studies_GR2019_DR14"
# for ext in ["png"]: #, "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
print(fig_name)
