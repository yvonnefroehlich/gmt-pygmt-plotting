# #############################################################################
# Japan earthquake on 2024/01/01 07:10:09 (UTC)
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# - Created: 2024/04/07
#   PyGMT v0.11.0 -> https://www.pygmt.org/v0.11.0/ | https://www.pygmt.org/
#   GMT 6.4.0 -> https://www.generic-mapping-tools.org/
# #############################################################################


import contextily as ctx
import numpy as np
import pandas as pd
import pygmt as gmt
from obspy.geodetics.base import gps2dist_azimuth
from obspy import UTCDateTime as utc
from obspy.clients.fdsn import Client as Client_fdsn
from obspy.taup import TauPyModel

from taup_path_time import taup_path


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Colors
col_sta = "255/215/0"
col_eq = "255/90/0"
col_pd = "216.750/82.875/24.990"
col_land = "gray90"
col_water = "steelblue"
col_shorelines = "darkgray"
col_phase = "magenta"
dict_col_phase = {
    "P": "navyblue",
    "S": "blue",
    "PcP": "deepskyblue",
    "ScS": "cyan",
    "SKS": "205/0/0",  # -> red
    "SKKS": "238/118/0",  # -> orange
    "PKS": "yellow2",
    "PKKP": "darkgreen",
    "PKIKP": "darkorange",
    "PKJKP": "purple2",
    "SKJKS": "maroon",
    "PKPPKP": "yellow",
}

# Standards
font = "9p"
pen_epi = "0.5p,black"
box_standard = "+gwhite@30+p0.5p,gray30+r1.5p"
clearance_standard = "0.1c/0.1c+tO"

# Recording station BFO
lon_bfo = 8.33
lat_bfo = 48.33

# File name for plate boundaries after Bird 2003
data_pb = "plate_boundaries_Bird_2003.txt"


# %%
# -----------------------------------------------------------------------------
# Earthquake in Japan
# -----------------------------------------------------------------------------
# source: https://earthquake.usgs.gov/earthquakes/eventpage/us6000m0xl/moment-tensor
# last access: 2024/01/02

time_origin = utc(2024, 1, 1, 7, 10, 9)

# Epicenter
lon_epi = 136.91
lat_epi = 37.23

# Focal mechanisem
aki_eq_jp = {
    "strike": 213, "dip": 50, "rake": 79, "magnitude": 7.5, "depth": 10,
}
eq_info = "Date " + "2024-01-01 07:10:09 (UTC)" + " | " \
          f"Location {lon_epi}° E, {lat_epi}° N | " \
          "Mw " + str(aki_eq_jp["magnitude"]) + " | " \
          "Hypocentral depth " + str(aki_eq_jp["depth"]) + " km | " \
          "Strike " + str(aki_eq_jp["strike"]) + "°, " + \
          "Dip " + str(aki_eq_jp["dip"]) + "°, " + \
          "Rake " + str(aki_eq_jp["rake"]) + "°"

inc = 8  # SKS phase in degrees


# %%
# -----------------------------------------------------------------------------
# Region and projections
# -----------------------------------------------------------------------------
map_size = "8c"
map_size_epi = "7c"

# Epicentral distance plot
epi_min = 80  # degrees
epi_max = 150
center_lon = lon_bfo
center_lat = lat_bfo
epi_plot = 160

proj_epi = f"E{center_lon}/{center_lat}/{epi_plot}/{map_size_epi}"

# Mercator projection
proj_merca = f"M{map_size}"

# Region around Japan
lon_min = 130.79
lon_max = 151.39
lat_min = 33.52
lat_max = 51.27
region_jp = [lon_min, lon_max, lat_min, lat_max]  #"JP+r1"


# %%
# -----------------------------------------------------------------------------
# Earthquake data from USGS
# -----------------------------------------------------------------------------
# Set up request
# see https://earthquake.usgs.gov/fdsnws/event/1/
# last access: 2024/01/04
url_usgs = 'https://earthquake.usgs.gov/fdsnws/event/1/query.csv'

start_date_request = '2000-01-01'
end_date_request = '2023-12-31'
min_magnitude_request = '6'
max_magnitude_request = '10'
order_records = 'time-asc'  # 'magnitude'

url_usgs_request = url_usgs + '?' + \
    '&'.join([
        'starttime=' + start_date_request + '%2000:00:00',
        'endtime=' + end_date_request + '%2000:00:00',
        'minmagnitude=' + min_magnitude_request,
        'maxmagnitude=' + max_magnitude_request,
        'orderby=' + order_records,
    ])

eq_catalog_name = "global_seismicity_" + start_date_request + "to" + end_date_request + \
           "_mw" + min_magnitude_request + "to" + max_magnitude_request

# Download data into a pandas DataFrame
data_eq_raw = pd.read_csv(url_usgs_request)

# Filter data
# for magnitude types mw, mwc, mwb, mwr, mww
data_eq_used = data_eq_raw[data_eq_raw["magType"].str.contains("mw")]

# Sort descending by magnitude to avoid overplotting
data_eq_used = data_eq_used.sort_values(by=['mag'], ascending=False)

# Scale hypocentral depth for size-coding
mag_dev = 1.2
mag_exp = 0.002
data_eq_used["mag_scaled"] = np.exp(data_eq_used["mag"] / mag_dev) * mag_exp

# Filter data
# for region around Japan
data_eq_used_jp = data_eq_used[data_eq_used.longitude > lon_min]
data_eq_used_jp = data_eq_used_jp[data_eq_used_jp.longitude < lon_max]
data_eq_used_jp = data_eq_used_jp[data_eq_used_jp.latitude > lat_min]
data_eq_used_jp = data_eq_used_jp[data_eq_used_jp.latitude < lat_max]


# %%
# -----------------------------------------------------------------------------
# Seismological data
# -----------------------------------------------------------------------------
# Set time window around phase
sec_before = 20  # seconds
sec_after = 120  # seconds

# Set corner frequencies for band pass filter
freq_low = 0.020  # Hz
freq_upp = 0.150  # Hz

# Choose Earth model for travel time calculation
earth_model = TauPyModel(model="iasp91")

# Initialize a client object for FDSN web service
fdsn_client = Client_fdsn("BGR")

# Set Parameters for data request
station = "BFO"
network = "GR"
channel = "BH*"
location = "*"
location = ",00"  # location code: test for non or 00
starttime_req = utc(2024, 1, 1, 0, 0, 0, 0)
endtime_req = utc(2024, 1, 2, 0, 0, 0, 0)

#-----------------------------------------------------------------------------
# Request data
st = fdsn_client.get_waveforms(
    network, station, location, channel, starttime_req, endtime_req,
)

# Apply bandpass filter
st_filtered = st.copy()
st_filtered = st_filtered.filter(
    "bandpass",
    freqmin=freq_low,
    freqmax=freq_upp,
    corners=4,
    zerophase=True,
)


# %%
# -----------------------------------------------------------------------------
# Calculate travel times and piercing points
# -----------------------------------------------------------------------------
# https://docs.obspy.org/packages/obspy.taup.html
# last access: 2023/12/07

# Define Earth model
taup_model = "iasp91"
earth_model = TauPyModel(model=taup_model)

# Select desired phase, has to be a list
taup_phase = ["P", "S", "ScS", "SKS", "SKKS"]
taup_depth = 2889  # in km | CMB
taup_lon = []
taup_lat = []

receiver_lat = center_lat
receiver_lon = center_lon

# Great circle distance in m, azimuth A->B in degrees, azimuth B->A in degrees
dist_temp, azi_temp, bazi_temp = gps2dist_azimuth(
    lat_epi,
    lon_epi,
    lat_bfo,
    lon_bfo,
)
# Convert meters to degrees
dist_temp_m2deg = dist_temp / 1000 * (360 / 2 / np.pi / 6371)

arrivals = earth_model.get_travel_times(
    source_depth_in_km=aki_eq_jp["depth"],
    distance_in_degree=dist_temp_m2deg,
    phase_list=taup_phase,
)


# %%
# -----------------------------------------------------------------------------
# Create collage
# -----------------------------------------------------------------------------

fig = gmt.Figure()

# -----------------------------------------------------------------------------
# === Upper Left: Elevation with beachball ===
fig.basemap(region=region_jp, projection=proj_merca, frame=["WsNe", "af"])

# Add elevation grid
grid_topo = gmt.datasets.load_earth_relief(
    region=region_jp,
    resolution="01m",
    registration="gridline",
)
fig.grdimage(grid_topo, cmap="oleron")
fig.colorbar(frame=["x+lelevation", "y+lm"])

# Inset map of study region
# Use with statement and context manager
with fig.inset(position="jTL+o0.1c+w3c"):

    # >>> use ? <<<

    # Azimuthal orthographic projection
    # glon0/lat0[/horizon]/scale or Glon0/lat0[/horizon]/width
    #  - lon0/lat0: set projection center
    #  - horizon: maximum distance from projection center (in degrees, <= 90, default 90)
    #  - scale or width: set figure size

    fig.coast(
        region="g",  # global
        projection=f"G{(lon_min + lon_max) / 2}/{(lat_min + lat_max) / 2}/?",
        area_thresh="50000",
        resolution="c",
        shorelines=f"1/0.01p,{col_shorelines}",
        land=col_land,
        water=col_water,
        frame="g",
    )

    # Plot rectangle at study area
    fig.plot(
        data=[[lon_min, lat_min, lon_max, lat_max]],
        style="r+s",
        pen=f"2p,{col_eq}",
    )

# Plot shorelines
fig.coast(shorelines=f"1/0.01p,{col_shorelines}")

# Plot plate boundaries
fig.plot(data=data_pb, pen=f"1p,{col_pd}")

# Plot epicenter
fig.plot(
    x=lon_epi,
    y=lat_epi,
    style="kearthquake.def/1.3c",
    fill=col_eq,
    pen=col_eq,
)

# Plot beachball
fig.meca(
    spec=aki_eq_jp,
    scale="1c",
    longitude=lon_epi,
    latitude=lat_epi,
    plot_longitude=135,
    plot_latitude=41,
    compressionfill=col_eq,
    offset=pen_epi,
    outline=pen_epi,
)

fig.show()


# %%
# -----------------------------------------------------------------------------
# === Upper Center: USGS earthquake data ===
fig.shift_origin(xshift="w+1c")

fig.basemap(region=region_jp, projection=proj_merca, frame=["wsNe", "af"])

fig.coast(land=col_land, shorelines=f"1/0.01p,{col_shorelines}")

gmt.makecpt(
    cmap="acton",
    series=[data_eq_used_jp.depth.min(), data_eq_used_jp.depth.max()],
    reverse=True,
)
fig.plot(
    data=data_eq_used_jp[["longitude", "latitude", "depth", "mag_scaled"]],
    cmap=True,
    style="cc",
    pen="black",
)
fig.colorbar(frame=["xaf+lhypocentral depth (2000-2023, Mw 6-10)", "y+lkm"])

fig.plot(
    x=lon_epi,
    y=lat_epi,
    style="c" + str(np.exp(aki_eq_jp["magnitude"]/mag_dev)*mag_exp) + "c",
    pen=pen_epi,
)
fig.plot(
    x=lon_epi,
    y=lat_epi,
    style="kearthquake.def/2c",
    fill=col_eq,
    pen=col_eq,
    transparency=30,
)

fig.show()


# %%
# -----------------------------------------------------------------------------
# === Upper Right: Region around Epicenter via tile maps
fig.shift_origin(xshift="w+1c")

# fig.basemap(
#     region=[136.9, 136.9428, 37.21, 37.25],
#     projection=proj_merca,
#     frame=["wsNE", "af"],
# )
fig.tilemap(
    region=[136.9, 136.9428, 37.21, 37.25],
    projection=proj_merca,
    zoom=14,
    source=ctx.providers.OpenStreetMap.HOT,
    # source=ctx.providers.CartoDB.Positron,
    # source="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    frame=["wsNE", "af"],
)

# Plot epicenter
fig.plot(
    x=lon_epi,
    y=lat_epi,
    style="kearthquake.def/1.3c",
    fill=col_eq,
    pen=col_eq,
)

fig.show()


# %%
# -----------------------------------------------------------------------------
# === Middle Left: Epidistance plot ===
fig.shift_origin(xshift="-w-9.2c", yshift="-h-1.5c")

fig.basemap(region="g", projection=proj_epi, frame=True)

# Plot shorelines
fig.coast(land=col_land, shorelines=f"1/0.01p,{col_shorelines}")

# Plot plate boundaries
fig.plot(data=data_pb, pen=f"0.3p,{col_pd}")

# Epicentral distance range used in this study
for epi_limit in [epi_min, epi_max]:

    if epi_limit==epi_min: offset_station_label = "0c/-1.7c"
    elif epi_limit==epi_max: offset_station_label = "0c/-3.2c"

    # Circles
    fig.plot(
        x=center_lon,
        y=center_lat,
        style=f"E-{epi_limit*2}+d",
        pen=f"1p,{col_sta},-",
    )
    # Annotations
    fig.text(
        x=center_lon,
        y=center_lat,
        offset=offset_station_label,
        text=f"{epi_limit}@.",
        font=font,
        fill="white@30",
        pen=f"0.5p,{col_sta}",
        clearance=clearance_standard,
    )

# Plot epicenter
fig.plot(
    x=lon_epi,
    y=lat_epi,
    style="kearthquake.def/1.1c",
    fill=col_eq,
    pen=col_eq,
)

# Plot recording station
fig.plot(
    x=center_lon,
    y=center_lat,
    style="i0.5c",
    fill=col_sta,
    pen="0.5p,black",
)
fig.text(
    x=center_lon,
    y=center_lat,
    offset="0c/-0.65c",
    text="BFO",
    font=font,
    fill="white@30",
    pen=f"1p,{col_sta}",
    clearance=clearance_standard,
)

# Add info text
fig.text(
    text=eq_info,
    position="TC",
    justify="MC",
    font="13p",
    offset="9c/1.3c",
    pen=pen_epi,
    fill=f"{col_eq}@70",
    clearance="0.3c/0.4c+tO",
    no_clip=True,
)

fig.show()


# %%
# -----------------------------------------------------------------------------
# === Middle Right: Seismograms at BFO ZNE coordinate system ===
# === Bottom Right: Seismograms at BFO LQT coordinate system ===
fig.shift_origin(xshift="w+3c", yshift="4.8c")

# Cut to shared time window around earthquake
starttime_eq = utc(2024, 1, 1, 7, 0, 0)
endtime_eq = utc(2024, 1, 1, 9, 0, 0)
st_eq = st_filtered.copy()
st_eq = st_eq.trim(starttime_eq, endtime_eq)

tr_len = len(st_eq[0].data)  # amount of samples
tr_delta = st_eq[0].stats.delta
sample_vec = np.arange(0, tr_len, 1)
y_lim = 1  # normalized

# Shift by difference between cut starttime and origin time
Dtime_cut_origin = starttime_eq - time_origin

for time_window in ["eq", "phase"]:

    if time_window=="eq":
        st_used = st_eq
        sample_show_start = 0
        sample_show_end = tr_len
    elif time_window=="phase":
        # Rotate in LQT coordinate system
        st_lqt = st_eq.copy()
        st_lqt = st_lqt.rotate(
            method="ZNE->LQT", back_azimuth=bazi_temp, inclination=inc,
        )
        st_used = st_lqt
        # Show only time window around SKS phase
        sample_show_start = 38000  # 24000  # 34000
        sample_show_end = 44000  # 60000  # 45000

    st_maxs = []
    for i_tr in range(3):
        st_maxs.append(
            abs(st_used[i_tr].data[sample_show_start:sample_show_end]).max()
        )
    st_max = np.array(st_maxs).max()

    for i_tr in range(3):

        tr_temp = st_used[i_tr]
        tr_temp_chan = tr_temp.stats.channel
        tr_temp_abs_max = abs(
            tr_temp.data[sample_show_start:sample_show_end]
        ).max()

        x_f = 6000
        if time_window=="phase": x_f = 1200

        if i_tr==0:
            frame_used=["Wsne", f"xf{x_f}", "ya"]
        if i_tr==1:
            frame_used=["Wsne", f"xf{x_f}", "ya+lnorm. amplitude per component"]
        if i_tr==2 and time_window=="eq":
            frame_used=["WSne", f"xa12000f{x_f}", "ya"]
        if i_tr==2 and time_window=="phase":
            frame_used=[
                "WSne",
                f"xa2400f{x_f}",
                f"x+lsamples after {tr_temp.stats.starttime} (UTC)" + \
                  f" with @~D@~t = {tr_delta} s",
                "ya",
            ]

        # Use colors as in SplitLab
        if tr_temp_chan=="BHE" or tr_temp_chan=="BHQ": col_tr = "blue"
        elif tr_temp_chan=="BHN" or tr_temp_chan=="BHT": col_tr = "red"
        elif tr_temp_chan=="BHZ" or tr_temp_chan=="BHL": col_tr = "darkgreen"

        fig.basemap(
            region=[sample_show_start, sample_show_end, -y_lim, y_lim],
            projection="X16c/2c",
            frame=frame_used,
        )

        # Plot seismograms
        fig.plot(
            x=sample_vec,
            y=tr_temp.data / tr_temp_abs_max,
            pen=f"0.2p,{col_tr}",
            label=tr_temp_chan,
        )

        # Mark arrival times of phases and add labels for phase names
        for i_phase in range(len(arrivals)):
            phase_text = str(arrivals[i_phase]).split(" ")[0]

            arrival_time = arrivals[i_phase].time
            arrival_time_samples = (-1 * Dtime_cut_origin + arrival_time) / tr_delta
            fig.plot(
                x=[arrival_time_samples, arrival_time_samples],
                y=[-y_lim, y_lim],
                pen="1p," + dict_col_phase[phase_text],
            )

        # Add labels for backazimuth, epicentral distance, and used filter
        if time_window=="eq":
            for i_label, label in enumerate([
                f"BAZ = {round(bazi_temp,3)}°",
                f"@~D@~ = {round(dist_temp_m2deg,3)}°",
                f"band pass [{freq_low},{freq_upp}] Hz",
            ]):
                if i_tr==i_label:
                    fig.text(
                        text=label,
                        position="TL",
                        justify="TL",
                        font=font,
                        offset="0.3c/-0.3c",
                        pen="0.5p,gray30",
                        fill="white@30",
                        clearance=clearance_standard,
                    )
        fig.legend(position="jTR+jTR+o0.1c+w1.5c", box=box_standard)

        fig.shift_origin(yshift="-h-0.5c")

    fig.shift_origin(yshift="-h+1.2c")

fig.show()


# %%
# -----------------------------------------------------------------------------
# # === Bottom Left: Travel paths ===
fig.shift_origin(xshift="-10c", yshift="4c")

# Generate plot for travel paths with self-defined function
taup_path(
    fig=fig,
    fig_width="7c",
    max_dist=360,
    font_size="7p",
    source_depth=aki_eq_jp["depth"],
    receiver_dist=dist_temp_m2deg,
    phases=taup_phase,
)

fig.show()


# %%
# -----------------------------------------------------------------------------
# Show and save
fig.show() # method="external")

fig_name = "japan_earthquake_BFO"
# for ext in ["png"]: # , "pdf", "eps"]:
#     fig.savefig(fname=f"{fig_name}.{ext}")

print(fig_name)
