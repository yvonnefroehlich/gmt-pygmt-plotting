# #############################################################################
# Comprehensive global data set of uniformly processed shear-wave splitting
# measurements
# Wolf J, Becker T W, Garnero E, Liu K H, West J D (2025). GJI, 241(2):863–875.
# https://doi.org/10.1093/gji/ggaf076.
#
# Data available at
# Last accessed: 2026/06/02
#
# Skript I: Prepare data for plotting
#           - Remove white spaces (around column names, before enteries)
#           - Calculate piercing points (2889, 660, 410, 210 km depth)
#           - Save to new txt files (each for PKS, SKS, SKKS)
# -----------------------------------------------------------------------------
# History
# - Created: 2026/03/13
# - Updated: 2026/06/02
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

import numpy as np
import pandas as pd
from obspy.taup import TauPyModel
earth_model = TauPyModel(model="iasp91")


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
path_in = "01_in_data"
path_out = "02_out_figs"


# %%
# -----------------------------------------------------------------------------
# Prepare data
# -----------------------------------------------------------------------------
# Load txt files
df_sks = pd.read_csv(f"{path_in}/SKS_measurements.txt", sep="\t")
df_skks = pd.read_csv(f"{path_in}/SKKS_measurements.txt", sep="\t")
df_pks = pd.read_csv(f"{path_in}/PKS_measurements.txt", sep="\t")

# -----------------------------------------------------------------------------
# Remove white spaces
cols = df_sks.select_dtypes(['object']).columns
df_sks[cols] = df_sks[cols].apply(lambda x: x.str.strip())
df_skks[cols] = df_skks[cols].apply(lambda x: x.str.strip())
df_pks[cols] = df_pks[cols].apply(lambda x: x.str.strip())

# Use underscores in column names
header = [
    "event_name", "event_lat", "event_lon", "event_dep",
    "station_code", "network_code", "station_lat", "station_lon", "quality",
    "dt", "dt_minus_err", "dt_plus_err",
    "phi", "phi_minus_err", "phi_plus_err",
    "SI", "SI_minus_err", "SI_plus_err",
]
# Save to txt files
args_csv = {"sep": ";", "index": False, "header": header}
file_name = "measurements_NOwhitespaces"
df_sks.to_csv(f"{path_in}/SKS_{file_name}.txt", **args_csv)
df_skks.to_csv(f"{path_in}/SKKS_{file_name}.txt", **args_csv)
df_pks.to_csv(f"{path_in}/PKS_{file_name}.txt", **args_csv)

# -----------------------------------------------------------------------------
# Reload txt files
df_sks = pd.read_csv(f"{path_in}/SKS_{file_name}.txt", sep=";")
df_skks = pd.read_csv(f"{path_in}/SKKS_{file_name}.txt", sep=";")
df_pks = pd.read_csv(f"{path_in}/PKS_{file_name}.txt", sep=";")

# -----------------------------------------------------------------------------
# Add column for event year
for df_xks in [df_sks, df_skks, df_pks]:
    event_year = []
    for i_swsm in range(len(df_xks)):
        event_name_temp = df_xks["event_name"][i_swsm]
        event_year_temp = int(event_name_temp[1:5])
        event_year.append(event_year_temp)
    df_xks["event_year"] = event_year


# %%
# -----------------------------------------------------------------------------
# Calculate piercing points
# -----------------------------------------------------------------------------
# for df_xks, pp_phase in zip([df_sks, df_skks, df_pks], ["SKS", "SKKS", "PKS"]):
# for df_xks, pp_phase in zip([df_sks], ["SKS"]):
# for df_xks, pp_phase in zip([df_skks], ["SKKS"]):
for df_xks, pp_phase in zip([df_pks], ["PKS"]):
    print(pp_phase)

    ray_depths = []
    ray_lons = []
    ray_lats = []
    ray_times = []
    ray_dists = []
    slowness = []
    pp210_lon = []
    pp210_lat = []
    pp410_lon = []
    pp410_lat = []
    pp2889_lon = []
    pp2889_lat = []

    for i_swsm in range(len(df_xks)):
        reminder = i_swsm % 500
        if reminder == 0:
            print(f"{i_swsm}/{len(df_xks)}")

        pp_temp = earth_model.get_pierce_points_geo(
           source_depth_in_km=df_xks["event_dep"][i_swsm],
           source_latitude_in_deg=df_xks["event_lat"][i_swsm],
           source_longitude_in_deg=df_xks["event_lon"][i_swsm],
           receiver_latitude_in_deg=df_xks["station_lat"][i_swsm],
           receiver_longitude_in_deg=df_xks["station_lon"][i_swsm],
           phase_list=[pp_phase],
           resample=False,
        )

        # Complete ray
        if pp_temp == []:
            ray_depths_temp = np.nan
            ray_lons_temp = np.nan
            ray_lats_temp = np.nan
            ray_times_temp = np.nan
            ray_dists_temp = np.nan
            slowness_temp = np.nan
        else:
            ray_depths_temp = pp_temp[0].pierce["depth"].tolist()
            ray_lons_temp = pp_temp[0].pierce["lon"].tolist()
            ray_lats_temp = pp_temp[0].pierce["lat"].tolist()
            ray_times_temp = pp_temp[0].pierce["time"].tolist()
            ray_dists_temp = pp_temp[0].pierce["dist"].tolist()
            slowness_temp = pp_temp[0].pierce["p"][0]
        ray_depths.append(ray_depths_temp)
        ray_lons.append(ray_lons_temp)
        ray_lats.append(ray_lats_temp)
        ray_times.append(ray_times_temp)
        ray_dists.append(ray_dists_temp)
        slowness.append(slowness_temp)

        # Specific depths
        if pp_temp == []:
            pp210_lon.append(np.nan)
            pp210_lat.append(np.nan)
            pp410_lon.append(np.nan)
            pp410_lat.append(np.nan)
            pp2889_lon.append(np.nan)
            pp2889_lat.append(np.nan)
        else:
            for i_depth, depth_temp in enumerate(ray_depths_temp):
                # if depth_temp < ray_depths_temp[i_depth - 1]:  # source-side
                if i_depth < (len(ray_depths_temp) - 1) and \
                   depth_temp > ray_depths_temp[i_depth + 1]:  # source-side
                    if depth_temp == 210:
                        pp210_lon.append(ray_lons_temp[i_depth])
                        pp210_lat.append(ray_lats_temp[i_depth])
                    elif depth_temp == 410:
                        pp410_lon.append(ray_lons_temp[i_depth])
                        pp410_lat.append(ray_lats_temp[i_depth])
                    if depth_temp == 2889:
                        pp2889_lon.append(ray_lons_temp[i_depth])
                        pp2889_lat.append(ray_lats_temp[i_depth])

    df_xks["phase"] = [pp_phase] * len(df_xks)
    df_xks["ray_depths"] = ray_depths
    df_xks["ray_lons"] = ray_lons
    df_xks["ray_lats"] = ray_lats
    df_xks["ray_times"] = ray_times
    df_xks["ray_dists"] = ray_dists
    df_xks["slowness"] = slowness
    df_xks["pierce210km_lon"] = pp210_lon
    df_xks["pierce210km_lat"] = pp210_lat
    df_xks["pierce410km_lon"] = pp410_lon
    df_xks["pierce410km_lat"] = pp410_lat
    df_xks["pierce2889km_lon"] = pp2889_lon
    df_xks["pierce2889km_lat"] = pp2889_lat


#%%
# -----------------------------------------------------------------------------
# Use underscores in column names
header = [
    "event_name", "event_lat", "event_lon", "event_dep",
    "station_code", "network_code", "station_lat", "station_lon", "quality",
    "dt", "dt_minus_err", "dt_plus_err",
    "phi", "phi_minus_err", "phi_plus_err",
    "SI", "SI_minus_err", "SI_plus_err",
    "event_year", "phase",
    "ray_depths", "ray_lons", "ray_lats",
    "ray_times", "ray_dists", "slowness",
    "pierce210km_lon", "pierce210km_lat",
    "pierce410km_lon", "pierce410km_lat",
    "pierce2889km_lon", "pierce2889km_lat",
]
# Save to txt files
args_csv = {"sep": ";", "index": False, "header": header}
file_name = "measurements_NOwhitespaces_pierce"
# df_sks.to_csv(f"{path_in}/SKS_{file_name}.txt", **args_csv)
# df_skks.to_csv(f"{path_in}/SKKS_{file_name}.txt", **args_csv)
df_pks.to_csv(f"{path_in}/PKS_{file_name}.txt", **args_csv)
