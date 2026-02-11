# #############################################################################
# Winter Olympics 2026 - medals germany
# -----------------------------------------------------------------------------
# History
# - Created: 2026/02/11
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.18.0 -> https://www.pygmt.org
# - GMT 6.6.0 -> https://www.generic-mapping-tools.org
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################

import pygmt
import pandas as pd

path_in = "01_in_data"
path_out = "02_out_figs"


# %%
df_medals = pd.read_csv(f"{path_in}/medals_germany.txt", sep=";")


# %%
fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray60")
fig.basemap(
    region=[5.8, 22.2, 0.8, 3.2],
    projection="X15c/3c",
    frame=["xa1g1+lday in Febuary", "ya1g1+lcount of medals"],
)

fig.plot(x=df_medals["day"] + 0.25, y=df_medals["bronze"], style="c0.3c", fill="tan")
fig.plot(x=df_medals["day"] + 0.50, y=df_medals["silver"], style="c0.3c", fill="gray")
fig.plot(x=df_medals["day"] + 0.75, y=df_medals["gold"], style="c0.3c", fill="gold")

fig.show()
fig.savefig(fname=f"{path_out}/05_medals_germany.png")
