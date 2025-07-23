# #############################################################################
# Anscombe's quartet
# -----------------------------------------------------------------------------
# Related content
# - website
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
# - PyGMT v0.16.0 -> https://www.pygmt.org/v0.16.0/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
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
df_ansc = pd.read_csv(f"{path_in}/anscombes_quartet.txt", sep="\t")

# Useful definitions
args_text01 = {"position": "BL", "justify": "LM", "font": "10p"}
args_text02 = {"position": "BC", "justify": "LM", "font": "10p"}


# %%
# -----------------------------------------------------------------------------
# Anscombe's quartet
# -----------------------------------------------------------------------------
fig = gmt.Figure()
gmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray80")

for i_plot in range(4):

    frame_y_afg = "f1g1"
    if i_plot==0:
        df_used = df_ansc[["x1", "y1"]]
        title = "Anscombe's"
        frame_y_afg = "a2f1g1"
    elif i_plot==1:
        df_used = df_ansc[["x2", "y2"]]
        title = "quartet:"
    elif i_plot==2:
        df_used = df_ansc[["x3", "y3"]]
        title= "Visualization"
    elif i_plot==3:
        df_used = df_ansc[["x4", "y4"]]
        title = "matters"

    x = df_used[df_used.columns[0]]
    y = df_used[df_used.columns[1]]

# -----------------------------------------------------------------------------
    # Data points
    fig.plot(
        projection="X10c",
        region=[0, 20, 0, 13.5],
        frame=[f"WSne+t{title}", "xafg", f"y{frame_y_afg}"],
        data=df_used,
        style="c0.3c",
        fill="orange",
        pen="1p,darkorange",
    )

# -----------------------------------------------------------------------------
    # Linear regression
    A_ansc = np.vstack([x, np.ones(len(df_used))]).T
    m, c = np.linalg.lstsq(A_ansc, y, rcond=None)[0]

    fig.plot(x=x, y=m * x + c, pen="1p,darkred")

# -----------------------------------------------------------------------------
    # Pearson correlation coefficients
    R2 = np.corrcoef(x, y)

# -----------------------------------------------------------------------------
    # Add text for stats
    fig.text(text=f"mean of x: {np.mean(x)}", offset="0.5c/2c", **args_text01)
    fig.text(text=f"mean of y: {str(np.mean(y))[0:7]}", offset="0.5c/1.5c", **args_text01)
    fig.text(text=f"median of x: {np.median(x)}", offset="0.5c/1c", **args_text01)
    fig.text(text=f"median of y: {np.median(y)}", offset="0.5c", **args_text01)

    fig.text(text=f"std of x: {str(np.std(x))[0:7]}", offset="0.5c/2c", **args_text02)
    fig.text(text=f"std of y: {str(np.std(y))[0:7]}", offset="0.5c/1.5c", **args_text02)
    fig.text(text=f"y = {str(m)[0:7]} x + {str(c)[0:7]}", offset="0.5c/1c", **args_text02)
    fig.text(text=f"R@+2@+ = {str(R2[0,1])[0:7]}", offset="0.5c", **args_text02)

# -----------------------------------------------------------------------------
    fig.shift_origin(xshift="w+0.5c")

fig.show()
fig_name= "anscombes_quartet"
# for ext in ["png"]:  # "pdf", "eps"]:
#     fig.savefig(fname=f"{path_out}/{fig_name}.{ext}")
