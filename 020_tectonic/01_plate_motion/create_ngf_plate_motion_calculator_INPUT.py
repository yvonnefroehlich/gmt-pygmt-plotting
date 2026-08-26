# #############################################################################
# Create input files for usage with NGF Plate Motion Calculator
# -> used in script map_plate_motion.py
# -----------------------------------------------------------------------------
# Data calculated with
# - https://www.unavco.org/software/geodetic-utilities/plate-motion-calculator/plate-motion-calculator.html
# - last access: 2024/06/08
# - model GSRM v2.1 (2014) -> Kreemer, Blewitt, Klein (2014)
#
# - DeMets C, Gordon R G, Argus D F (2010). Geologically current plate motions.
#   Geophysical Journal International, 181(1), 1-80.
#   https://doi.org/10.1111/j.1365-246X.2009.04491.x
#   See also Erratum (2011). Geophysical Journal International, 187(1), 538-538.
#   https://doi.org/10.1111/j.1365-246X.2011.05186.x.
# - Kreemer C, Blewitt G, Klein E C (2014). A geodetic plate motion and Global
#   Strain Rate Model. Geochemistry, Geophysics, Geosystems, 15, 3849-3889.
#   https://doi.org/10.1002/2014GC005407
# -----------------------------------------------------------------------------
# History
# - Created: 2024/06/08
# - Updated: 2026/08/25 - Adjusted for GitHub
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


import os

min_lon = -180
max_lon = 180
min_lat = -90
max_lat = 90

step_lon = 2
step_lat = 2
elevation = 0

data_out = f"01_in_data/ngf_plate_motion_calculator_INPUT_Dlon{step_lon}deg_Dlat{step_lat}deg_ele{elevation}m.txt"
try:
    os.remove(data_out)
except:
    pass

with open(data_out, "a") as f_new:

    for lon in range(min_lon, max_lon + step_lon, step_lon):
        for lat in range(min_lat, max_lat + step_lat, step_lat):

            line_temp = [str(lon), str(lat), str(elevation)]
            line_temp_join = " ".join(line_temp)

            if lon == max_lon and lat == max_lat:
                f_new.write(line_temp_join)
            else:
                f_new.write(line_temp_join + ",\n")
