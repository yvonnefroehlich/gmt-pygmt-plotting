# #############################################################################
# Earth's magnetic field model gufm1 1980 by Jackson et al. (2000)
# - Create grid with pymagglobal
#   https://sec23.git-pages.gfz-potsdam.de/korte/pymagglobal
#   last access: 2024/02/20
#   https://www.gfz-potsdam.de/magservice/faq
# - Convert to and save as GMT-ready grid
# -----------------------------------------------------------------------------
# History
# - Created: 2025/09/17
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


import pygmt as gmt
from pymagglobal import Model
from pymagglobal import field
from pymagglobal.utils import get_grid

# %%
# -----------------------------------------------------------------------------
# Set up for making the grids
# -----------------------------------------------------------------------------
model = "gufm1"
year = 1980
depth = 2900  # in kilometers
N_points = 10000
grid_spacing = "0.5d"
earth_radius = 6371  # in kilometers

# TODO: Account for values form literature: fb = 0.8 and fnz = 0.2
gufm1 = Model(model)

# Path
path_in = "01_in_data"


# %%
# -----------------------------------------------------------------------------
# Make grids
# -----------------------------------------------------------------------------
# Set up a grid for requested depth
grid_pymag = get_grid(N_points, R=earth_radius - depth, t=year)

# grid[0] contains co-latitudes in degrees
# grid[1] contains longitudes in degrees
# grid[2] contains radii in kilometers
# grid[3] contains dates in years
lats = 90 - grid_pymag[0]  # Convert co-latitude to latitude
lons = grid_pymag[1]

# https://sec23.git-pages.gfz-potsdam.de/korte/pymagglobal/package_documentation.html#pymagglobal.utils.nez2dif
N, E, Z = field(grid_pymag, gufm1, field_type="nez")  # north, east, down components
D, I, F = field(grid_pymag, gufm1, field_type="dif")  # declination, inclination, intensity

quantities = {"Z": Z, "N": N, "E": E, "D": D, "I": I, "F": F}


# -----------------------------------------------------------------------------
# Make GMT-ready grid
for quantity in ["Z", "I", "D"]:

    grid_name = f"{model}_{year}_{depth}km_{quantity}"

    gmt.surface(
        x=lons,
        y=lats,
        z=quantities[quantity],
        spacing=grid_spacing,
        tension=0.35,
        region="d",
        outgrid=f"{path_in}/{grid_name}.grd",
    )

    print(f"Saved grid '{grid_name}.grd' to '{path_in}'!")