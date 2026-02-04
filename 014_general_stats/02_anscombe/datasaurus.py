# #############################################################################
# Datasaurus
# -----------------------------------------------------------------------------
# - Related content
#   - https://www.research.autodesk.com/publications/same-stats-different-graphs/
#   - last access: 2024/01/10
# - literature
#   - https://www.research.autodesk.com/app/uploads/2023/03/same-stats-different-graphs.pdf_rec2hRjLLGgM7Cn2T.pdf
#     file:///C:/Users/Admin/C2/EigeneDokumente/Studium/Promotion/E_GMT/00_upcoming/anscome/anscombe1973.pdf
#   - last access: 2024/01/10
# - data
#   - https://www.dropbox.com/sh/xaxpz3pm5r5awes/AADUbGVagF9i4RmM9JkPtviEa?dl=0&preview=Datasaurus_data.csv
#   - last access: 2024/01/10
# -----------------------------------------------------------------------------
# History
# - Created: 2024/01/10
# - Updated: 2025/07/21
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.16.0 - v0.18.0 -> https://www.pygmt.org
# - GMT 6.5.0 - 6.6.0 -> https://www.generic-mapping-tools.org
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt as gmt
import pandas as pd


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Path
path_in = "01_in_data"
path_out = "02_out_figs"

# Data
df_dino = pd.read_csv(f"{path_in}/datasaurus_data.csv", sep="\t",)


# %%
# -----------------------------------------------------------------------------
# Datasaurus
# -----------------------------------------------------------------------------
fig = gmt.Figure()
fig.basemap(projection="X8c/8c", region=[7, 115, -10, 110], frame="btrl+gtan@20")

# gmt.makecpt(cmap="batlow", series=[min(df_dino["x"]), max(df_dino["x"])])
fig.plot(
    x=df_dino["x"],
    y=df_dino["y"],
    fill="brown",
    # fill=df_dino["x"],
    # cmap=True,
    style="c0.08c",
    pen="0.1p,gray30",
)

fig.show()
fig_name = "datasaurus"
# for ext in ["png"]:  # "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
