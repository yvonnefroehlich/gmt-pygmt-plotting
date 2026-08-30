# #############################################################################
# Maps of paleo coastlines
# - CM: continental margins
# - CS: coastlines
# -----------------------------------------------------------------------------
# Data
# - PaleoMAP PaleoCoastlines data: https://doi.org/10.5281/zenodo.3903163
# - Version v7.3 https://doi.org/10.5281/zenodo.7994000
# - Last access 2026/08/08
# -----------------------------------------------------------------------------
# History
# - Created: 2026/08/07
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.19.0 -> https://www.pygmt.org
# - GMT 6.7.0 -> https://www.generic-mapping-tools.org
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################

import pygmt
import geopandas as gpd


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"

folder = "paleocoastlines_v7_shapefiles"
file_pb = "plate_boundaries_Bird_2003.txt"

color_hl= "255/90/0"  # highlight -> orange

map_size = 12
# BFO
center_lon = 8.33
center_lat = 48.33
epi_plot = 150

year_start = 300
year_end = 0
year_step = -20


# %%
# -----------------------------------------------------------------------------
# Create maps of paleo coastlines over time
# -----------------------------------------------------------------------------
for proj in ["epi", "robd", "robg"]:

    match proj:
        case "epi":
            projection = f"E{center_lon}/{center_lat}/{epi_plot}/{map_size}c"
            region = "d"
        case "robd":
            projection = f"N{map_size}c"
            region = "d"
        case "robg":
            projection = f"N{map_size}c"
            region = "g"

    for i_year, year in enumerate(range(year_start, year_end + year_step, year_step)):

        # Data provided for 300 Ma, 180 Ma, 80 Ma, 60 Ma
        # For the other ages, download the data from zenodo (see header)
        try:
            gdf_paleo_cm = gpd.read_file(f"{path_in}/{folder}/CM/{year}Ma_CM_v7.shp")
            gdf_paleo_cs = gpd.read_file(f"{path_in}/{folder}/CS/{year}Ma_CS_v7.shp")
        except:
            print(f"No data for {year}Ma")
            continue

        fig = pygmt.Figure()
        fig.basemap(region=region, projection=projection, frame=0)

        fig.plot(data=gdf_paleo_cm, pen="0.2p,darkorange", fill="bisque@50")
        fig.plot(data=gdf_paleo_cs, pen="0.2p,darkred", fill="gray95")

        fig.coast(shorelines="1/0.1p,gray70")

        fig.basemap(frame=True)

        fig.text(position="TR", offset=-0.2, text=f"{year} Ma", font=f"10p,1,{color_hl}")

        fig.show()
        figname_base = f"map_paleo_{proj}"
        # figname_base = f"{i_year}_map_paleo_{proj}"
        figname_add = f"_{year}Ma"
        if proj == "epi":
            figname_add = f"{epi_plot}_{year}Ma"
        # for ext in ["png"]:  #, "pdf", "eps"]:
        #     fig.savefig(fname=f"{path_out}/{proj}/{figname_base}{figname_add}.{ext}")
        print(f"{figname_base}{figname_add}")
