# #############################################################################
# Chropleth map of the population in Chicago using data stored in geopandas
# polygon geometry and adding railroads (line geometry) as well as cities,
# ports, and airports (point geometry)
#
# Data (last accessed 2025/12/02)
# - Population in Chicago: geodatasets
# - Railroads, cities, ports, airports: Natural Earth, 10 m datasets
# -----------------------------------------------------------------------------
# History
# - Created: 2025/12/02
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.17.0 -> https://www.pygmt.org/v0.17.0/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################

import geodatasets
import geopandas as gpd
import pygmt
from pygmt.params import Box


# %%
# -----------------------------------------------------------------------------
# Load and prepare data
# -----------------------------------------------------------------------------
chicago = gpd.read_file(geodatasets.get_path("geoda airbnb"))

provider = "https://naciscdn.org/naturalearth"
files = {
    "railroads": "ne_10m_railroads.zip",
    "airports": "ne_10m_airports.zip",
    "cities": "ne_10m_populated_places_simple.zip",
    "ports": "ne_10m_ports.zip",
}
bbox = (-87.94, -87.52, 41.64, 42.02)  # Define bounding box
data = {}
for key, fname in files.items():
    gdf = gpd.read_file(f"{provider}/10m/cultural/{fname}")
    data[key] = gdf.cx[bbox[0]:bbox[1], bbox[2]:bbox[3]]
railroads = data["railroads"]
airports = data["airports"]
cities = data["cities"]
ports = data["ports"]


# %%
# -----------------------------------------------------------------------------
# Create map
# -----------------------------------------------------------------------------
fig = pygmt.Figure()
fig.basemap(region=chicago.total_bounds[[0, 2, 1, 3]], projection="M10c", frame=0)
fig.coast(shorelines=True, lakes="lightblue", land="gray95")

# Polygon geometry: lot population
pygmt.makecpt(cmap="bilbao", series=[0, chicago["population"].max()])
fig.plot(data=chicago, pen="0.5p,gray30", fill="+z", cmap=True, aspatial="Z=population")

# Line geometry: Plot railroads
fig.plot(data=railroads["geometry"], pen="2p,black")
fig.plot(data=railroads["geometry"], pen="1p,white,2_2")

# Point geometry: Plot cities
fig.plot(data=cities["geometry"], style="s0.32c", fill="red", pen="1p", label="city")
# Point geometry: Plot ports
fig.plot(data=ports["geometry"], style="i0.35c", fill="steelblue", pen="1p", label="harbor")
# Point geometry: Plot airports
fig.plot(data=airports["geometry"], style="t0.35c", fill="darkorange", pen="1p", label="airport")
# Label airports
fig.text(
    x=airports.geometry.x,
    y=airports.geometry.y,
    text=airports["name"],
    offset="-0.25c",
    justify="TL",
    font="8p,Helvetica-Bold",
    fill="white@30",
    pen="0.8p,darkorange",
    clearance="0.08c+tO",
)

# Add colorbar for population
fig.colorbar(
    frame="xaf+lPopulation in Chicago",
    position="jML+o0.95c/-1.5c+w7c+ml",
    box=Box(fill="gray95", clearance="0.5c"),
)
# Add legend for cities, ports, and airports
fig.legend(position="jTR+o0.2c+l1.7", box=Box(fill="white@30", pen="0.5p,gray50"))

fig.show()
fig.savefig(fname="gp_choropleth_chicago.png")
