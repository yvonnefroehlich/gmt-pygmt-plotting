# #############################################################################
# Plot seismograms simulated with AxiSEM3D with PyGMT
# -----------------------------------------------------------------------------
# History
# - Created: -
# - Updatd: 2025/08/19 - adjust for GitHub
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
import obspy as obs
from obspy.taup import TauPyModel
import pygmt as gmt
import string


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
status_pc = "gpi"  ## "gpi", "private"
sim = "01"  ## "01", "02", "03"
sim_nr = "b"  ## "a", "b", "c"
source = "m23e15"
comps = ["E", "N", "Z"]  ## "E", "N", "Z"

time_start_in = 1250  # in seconds
time_end_in = 1900

# time_start_in = 80  # in seconds
# time_end_in = 800

# time_start_in = 200  # in seconds
# time_end_in = 1000

min_dist_plot = 80  # in degrees
max_dist_plot = 160

# min_dist_plot = 10  # in degrees
# max_dist_plot = 90

min_st_plot = 1  # start at 1
max_st_plot = 36  # end at 36 (37)
# min_st_plot = 10
# max_st_plot = 28
# min_st_plot = 18
# max_st_plot = 19

freq_min = 0.015  # in Hz
freq_max = 0.2
# freq_min = 0.015
# freq_max = 0.15

match source:
    case "virginia": factor_sep = 1e7
    case "m23e20": factor_sep = 1e15
    case "m23e15": factor_sep = 1e15
    case "m23e10": factor_sep = 1e15
    case _: factor_sep = 1
y_lim = 0.06  # r = 0.6
# y_lim = 0.1
y_shift = 0
dpi_png = 360

cmap_lat_in = "batlow"
cmap_lon_in = "romaO"
color_highlight = "255/90/0"  # ->  orange | URG paper

path_in = "01_in_data"
path_out = "02_out_figs"

x_label = f"time after event time / s | bandpass filter [{freq_min},{freq_max}] Hz"
args_label = {
    "fill": "white@30", "pen": "1p,darkgray", "clearance": "0.1c/0.1c+tO"
}

time_max = 2500  # seconds | length of simulation
t0 = 0 #-0.41951
time_start = time_start_in - t0
time_end = time_end_in - t0

coord_step = 10  # for lon and lat | degrees
min_dist_plot_i = int(min_dist_plot / coord_step)
max_dist_plot_i = int(max_dist_plot / coord_step)

# -----------------------------------------------------------------------------
match status_pc:
    case "private":
        path_same = "C:/Users/Admin/C2/EigeneDokumente/Studium/Promotion/" + \
                        "00_axisem3d_simulate"
    case "gpi":
        path_same = "/home/yfroe/axisem3d_simulate"

path_sim = f"{path_same}/06_OWN_source_centered_global/period_6p3s/r_0p6/" + \
            f"source_{source}/runsB_sim{sim}_{sim_nr}/sim_out/output/" + \
            "stations/stations_global"

# -----------------------------------------------------------------------------
# Set up for colormap and colorbar

# for backazimuth (-> lon)
lons_left = np.arange(-180, 0, coord_step)
lats_right = np.arange(0, 180, coord_step)
lons = list(lons_left) + list(lats_right)

bazs_left = np.arange(180, 360, coord_step)
bazs_right = np.arange(0, 180, coord_step)
bazs = list(bazs_left) + list(bazs_right)

bazs_left = np.arange(180, 0, -coord_step)
bazs_right = np.arange(360, 180, -coord_step)
bazs = list(bazs_left) + list(bazs_right)

st_nums = np.arange(1, len(bazs) + 1, 1)

cmap_lon_out = f"{path_in}/{cmap_lon_in}_lon_seismos.cpt"
gmt.makecpt(
    cmap=cmap_lon_in,
    series=[-180, 0, coord_step],
    cyclic=True,
    output=cmap_lon_out,
)

# for epicentral distance (-> lat)
lats = np.arange(90 - coord_step, -90 - coord_step, -coord_step)

dists = np.arange(coord_step, 180, coord_step)

st_chars_temp = list(string.ascii_uppercase)
st_chars = st_chars_temp[0:len(dists)]

cmap_lat_out = f"{path_in}/{cmap_lat_in}_lat_seismos.cpt"
gmt.makecpt(
    cmap=cmap_lat_in,
    series=[0 + coord_step, 180 - coord_step, coord_step],
    reverse=True,
    output=cmap_lat_out,
)

# -----------------------------------------------------------------------------
# Set up for travel time calculation
model = TauPyModel(model="prem")  ## "iasp91", "prem"
source_depth = 100  # km
phases = [
    "P", "pP", "PcP", #"PP", "PPP", "Pdiff",
    "S", "sS", "ScS", #"SS", "Sdiff",
   # "PS", "PcS", "SP", "ScP", "pS",
    "PKS", "SKS", "SKKS",
   # "sSKS", "sSKKS", "pSKS", "pSKKS",
   # "PKP", "PKIKP", "PKiKP",
]

# -----------------------------------------------------------------------------
# Read input data - time
data_time = np.loadtxt(f"{path_sim}/data_time.ascii")



#%%
# -----------------------------------------------------------------------------
# Backazimuth dependent plot -> variation of longitude
# -----------------------------------------------------------------------------
# """
# "A" = 80 deg North
for i_lat in range(min_dist_plot_i - 1, max_dist_plot_i, 1):
    lat = lats[i_lat]
    st_char = st_chars[i_lat]
    dist = dists[i_lat]

    for comp in comps:

        frame_x_basic = ["xf10"]
        frame_xlabel = [f"xa50f10+l{x_label}+e"]
        frame_y_sep = ["ya0.03f0.01"]
        frame_y_one = ["yf1"]
        frame_title = [
            f"+tsource {source} | stations {st_char}* " + \
            f"at {lat}@. N or @~D@~={dist}@. | " + \
            f"Displacement | {comp} component",
        ]

        fig_one = gmt.Figure()
        fig_one.basemap(
            region=[time_start, time_end, min_st_plot - 0.5, max_st_plot + 0.5],
            projection=f"X50c/-{(max_st_plot - min_st_plot) * 2}c",
            frame=frame_xlabel + frame_y_one + frame_title,
        )

        fig = gmt.Figure()

# -----------------------------------------------------------------------------
        # Loop over longitude -> backazimuth
        for st_num in range(min_st_plot, max_st_plot + 1, 1):
            st_num_str = str(st_num).zfill(2)
            baz = bazs[st_num - 1]
            lon = lons[st_num - 1]

# -----------------------------------------------------------------------------
            # Calculation of theoretical travel times with TauP via ObsPy
            arrivals = model.get_travel_times(
                source_depth_in_km=source_depth,
                distance_in_degree=dist,
                phase_list=phases,
            )

# -----------------------------------------------------------------------------
            # Displacement U as East E, North N, and Vertical Z components
            st_raw = obs.read(
                f"{path_sim}/sac_files/XX.{st_char}{st_num_str}.BH{comp}.sac",
                # debug_headers=True,
            )

            # Bandpass filter data
            st_filter = st_raw.copy()
            st_filter.filter("bandpass", freqmin=freq_min, freqmax=freq_max)

            # Get amplitude vector
            data_amp = st_filter[0].data

            # Calculate indizes to time window
            freq = len(data_amp) / time_max
            ind_start = int(np.floor(time_start * freq))
            ind_end = int(np.floor(time_end * freq))

            # Select seismogram part within the desired time window
            amp_used = data_amp[ind_start:ind_end]

            # Clip high amplitudes
            amp_used_clip = np.select([np.abs(amp_used) > y_lim], [0], amp_used)

# -----------------------------------------------------------------------------
            # Set up basic map and adjust frame
            gmt.config(MAP_FRAME_PEN="1p,gray30")
            fill_plot = "white"
            if dist > 89 and dist < 151:
                gmt.config(MAP_FRAME_PEN=f"1p,{color_highlight}")
                fill_plot = f"{color_highlight}@95"
            frame_fill = [f"WnSe+g{fill_plot}"]

            if st_num == max_st_plot: frame_x = frame_xlabel
            else: frame_x = frame_x_basic

            fig.basemap(
                region=[time_start, time_end, -y_lim, y_lim],
                projection="X50c/2c",
                frame=frame_x + frame_y_sep + frame_fill,
            )
            if st_num == min_st_plot: fig.basemap(frame=frame_title)

# -----------------------------------------------------------------------------
            # Plot seismogram
            fig.plot(
                x=data_time[ind_start:ind_end],
                y=-1 * amp_used,  # inverse y axis !!!
                pen="2.5p,+z",
                zvalue=lon,
                cmap=cmap_lon_out,
            )
            fig_one.plot(
                x=data_time[ind_start:ind_end],
                y=-1 * amp_used_clip * 10 + st_num,  # inverse y axis !!!
                pen="3p,+z",
                zvalue=lon,
                cmap=cmap_lon_out,
            )
            # fig_one.plot(
            #     x=data_time[ind_start:ind_end],
            #     y=-1 * amp_used_clip * 10 + st_num,  # inverse y axis !!!
            #     pen="2p,black",
            # )

# -----------------------------------------------------------------------------
            # Mark theoretical travel times
            # if st_num == min_st_plot + ((max_st_plot - min_st_plot) / 2):
            for arrival in arrivals:
                if arrival.time > time_start and arrival.time < time_end:
                    # Plot vertical line
                    fig.plot(
                        x=[arrival.time, arrival.time],
                        y=[-y_lim, y_lim],
                        pen=f"1p,{color_highlight}",
                    )
                    fig_one.plot(
                        x=[arrival.time, arrival.time],
                        y=[st_num - 0.25, st_num + 0.25],
                        pen=f"1.5p,{color_highlight}",
                    )
                    # Add label with phase name
                    if st_num == max_st_plot:
                        arrival_str = str(arrival)
                        arrival_str_split = arrival_str.split()
                        fig.text(
                            x=arrival.time,
                            y=-y_lim,
                            text=arrival_str_split[0],  # Get phase name
                            fill="white@30",
                            pen=f"1p,{color_highlight}",
                            clearance="0.1c/0.1c+tO",
                            no_clip=True,
                        )
                        fig_one.text(
                            x=arrival.time,
                            y=st_num + 0.45,
                            text=arrival_str_split[0],  # Get phase name
                            fill="white@30",
                            pen=f"1p,{color_highlight}",
                            clearance="0.1c/0.1c+tO",
                            no_clip=True,
                        )

# -----------------------------------------------------------------------------
            # Add label for
            # recording station and longitude
            fig.text(
                position="TL",
                justify="TL",
                offset="0.3c/0.3c",
                text=f"{st_char}{st_num_str} at {lon}@. E",
                **args_label,
            )
            fig_one.text(
                x=time_start,
                y=st_num,
                justify="ML",
                offset="0.3c/0.4c",
                text=f"{st_char}{st_num_str} at {lon}@. E",
                **args_label,
            )
            # backazimuth
            fig.text(
                position="BL",
                justify="BL",
                offset="0.3c/-0.3c",
                text=f"BAZ = {baz}@.",
                **args_label,
            )
            fig_one.text(
                x=time_start,
                y=st_num,
                justify="ML",
                offset="0.3c/-0.4c",
                text=f"BAZ = {baz}@.",
                **args_label,
            )

            fig.shift_origin(yshift="-h-0.35c")

# -----------------------------------------------------------------------------
        # fig.show()  # method="external")
        fig_one.show()
        fig_name = f"seisbaz_center_source_global_{source}_stations{st_char}_" + \
                    f"{comp}comp_{freq_min}to{freq_max}Hz_" + \
                    f"{time_start_in}to{time_end_in}s_" + \
                    f"baz{bazs[min_st_plot - 1]}to{bazs[max_st_plot - 1]}deg_" + \
                    f"{cmap_lon_in}"
        for ext in ["png", "pdf"]:
            # fig.savefig(
            #     fname=f"{path_out}/sim_{sim}/baz/{fig_name}_SEP.{ext}", dpi=dpi_png,
            # )
            fig_one.savefig(
                fname=f"{path_out}/sim_{sim}/baz/{fig_name}_ONE.{ext}", dpi=dpi_png,
            )
        print(fig_name)

# """


"""
#%%
# -----------------------------------------------------------------------------
# Epidistance dependent plot -> variation of latitude
# -----------------------------------------------------------------------------
# "01" = -180 deg East
# for st_int in range(len(bazs)):
for st_int in range(min_st_plot, max_st_plot, 1):
    st_int_str = str(st_int + 1).zfill(2)

    for comp in comps:

        frame_x_basic = ["xf10"]
        frame_xlabel = [f"xa50f10+l{x_label}+e"]
        frame_y_sep = ["yf1"] # ["ya0.03f0.01"]
        frame_y_one = ["yf1"]
        frame_title = [
            f"+tsource {source} | stations *{st_int_str} " + \
            f"at {lons[int(st_int)]}@. E or " + \
            f"{bazs[int(st_int)]}@. BAZ | " + \
            f"Displacement | {comp} component",
        ]

        fig_one = gmt.Figure()
        fig_one.basemap(
            region=[
                time_start, time_end,
                min_dist_plot_i - 0.5, max_dist_plot_i + 0.5,
            ],
            projection=f"X50c/{(max_dist_plot_i - min_dist_plot_i + 1 + y_shift) * 2}c",
            frame=frame_xlabel + frame_y_one + frame_title,
        )

        # Mark epicentral distance range corresponding to XKS phases
        fig_one.plot(
            x=[time_start, time_end, time_end, time_start, time_start],
            y=[
               90 / coord_step - 0.5, 90 / coord_step - 0.5,
               150 / coord_step + 0.5, 150 / coord_step + 0.5,
               90 / coord_step - 0.5,
            ],
            fill=f"{color_highlight}@95",
            # no_clip=True,
        )

        fig = gmt.Figure()

# -----------------------------------------------------------------------------
        # Loop over latitute -> epicentral distance
        for i_lat in range(min_dist_plot_i - 1, max_dist_plot_i, 1):
            st_char = st_chars[i_lat]
            dist = dists[i_lat]
            lat = lats[i_lat]

# -----------------------------------------------------------------------------
            # Calculation of theoretical travel times with TauP via ObsPy
            arrivals = model.get_travel_times(
                source_depth_in_km=source_depth,
                distance_in_degree=dist,
                phase_list=phases,
            )

# -----------------------------------------------------------------------------
            # Displacement U as East E, North N, and Vertical Z components
            st_raw = obs.read(
                f"{path_sim}/sac_files/XX.{st_char}{st_int_str}.BH{comp}.sac",
                # debug_headers=True,
            )

            # Bandpass filter data
            st_filter = st_raw.copy()
            st_filter.filter("bandpass", freqmin=freq_min, freqmax=freq_max)

            # Get amplitude vector
            data_amp = st_filter[0].data
            if i_lat == min_dist_plot_i - 1 and st_int == min_st_plot:
                data_amp_min = data_amp.min(); print(data_amp_min)
                data_amp_max = data_amp.max(); print(data_amp_max)

            # Calculate indizes to time window
            freq = len(data_amp) / time_max
            ind_start = int(np.floor(time_start * freq))
            ind_end = int(np.floor(time_end * freq))

            # Select seismogram part within the desired time window
            amp_used = data_amp[ind_start:ind_end]

            # Clip high amplitudes
            amp_used_clip = np.select([np.abs(amp_used) > y_lim], [0], amp_used)

# -----------------------------------------------------------------------------
            # Set up basic map and adjust frame
            gmt.config(MAP_FRAME_PEN="1p,black")
            fill_plot = "white"
            if dist > 89 and dist < 151:
                gmt.config(MAP_FRAME_PEN=f"1p,{color_highlight}")
                fill_plot = f"{color_highlight}@95"
            frame_fill = [f"WnSe+g{fill_plot}"]

            if i_lat == max_dist_plot_i - 1: frame_x = frame_xlabel
            else: frame_x = frame_x_basic

            fig.basemap(
                region=[time_start, time_end, -y_lim, y_lim],
                projection="X50c/2c",
                frame=frame_x + frame_y_sep + frame_fill,
            )
            if i_lat == min_dist_plot_i - 1: fig.basemap(frame=frame_title)

# -----------------------------------------------------------------------------
            # Plot seismogram
            fig.plot(
                x=data_time[ind_start:ind_end],
                y=amp_used * factor_sep,
                pen="1p,+z",
                zvalue=dist,
                cmap=cmap_lat_out,
            )
            fig_one.plot(
                x=data_time[ind_start:ind_end],
                y=amp_used_clip * 1e2 + (i_lat + 1) + y_shift,
                pen="1.5p,+z",
                zvalue=dist,
                cmap=cmap_lat_out,
            )

# -----------------------------------------------------------------------------
            # Mark theoretical travel times
            for arrival in arrivals:

                if arrival.time > time_start and arrival.time < time_end:
                    # Plot vertical line
                    fig.plot(
                        x=[arrival.time, arrival.time],
                        y=[-y_lim, y_lim],
                        pen=f"1p,{color_highlight}",
                    )
                    fig_one.plot(
                        x=[arrival.time, arrival.time],
                        y=[i_lat + 1 - 0.25 + y_shift, i_lat + 1 + 0.25 + y_shift],
                        pen=f"1.5p,{color_highlight}",
                    )
                    # Add label with phase name
                    arrival_str = str(arrival)
                    arrival_str_split = arrival_str.split()
                    fig.text(
                        x=arrival.time,
                        y=-y_lim,
                        text=arrival_str_split[0],  # Get phase name
                        fill="white@30",
                        pen=f"1p,{color_highlight}",
                        clearance="0.1c/0.1c+tO",
                        no_clip=True,
                    )
                    fig_one.text(
                        x=arrival.time,
                        y=i_lat + 1 - 0.45 + y_shift,
                        text=arrival_str_split[0],  # Get phase name
                        fill="white@30",
                        pen=f"1p,{color_highlight}",
                        clearance="0.1c/0.1c+tO",
                        no_clip=True,
                    )

# -----------------------------------------------------------------------------
            # Add label for
            # recording station and latitude
            fig.text(
                position="TL",
                justify="TL",
                offset="0.3c/-0.3c",
                text=f"{st_char}{str(st_int + 1).zfill(2)} at {lat}@. N",
                **args_label,
            )
            fig_one.text(
                x=time_start,
                y=i_lat + 1,
                justify="TL",
                offset="0.3c/-0.3c",
                text=f"{st_char}{str(st_int + 1).zfill(2)} at {lat}@. N",
                **args_label,
            )
            # epicentral distance
            fig.text(
                position="BL",
                justify="BL",
                offset="0.3c/0.3c",
                text=f"@~D@~ = {dist}@.",
                **args_label,
            )
            fig_one.text(
                x=time_start,
                y=i_lat + 1,
                justify="BL",
                offset="0.3c/0.3c",
                text=f"@~D@~ = {dist}@.",
                **args_label,
            )

            fig.shift_origin(yshift="-h-0.35c")

# -----------------------------------------------------------------------------
        fig.show()  # method="external")
        # fig_one.show()
        fig_name = f"seisdist_center_source_global_{source}_stations{st_int_str}_" + \
                    f"{comp}comp_{freq_min}to{freq_max}Hz_" + \
                    f"{time_start_in}to{time_end_in}s_" + \
                    f"{min_dist_plot}to{max_dist_plot}deg_" + \
                    f"_{cmap_lat_in}"
        for ext in ["png", "pdf"]:
            fig.savefig(
                fname=f"{path_out}/sim_{sim}/dist/{fig_name}_SEP.{ext}", dpi=dpi_png,
            )
            # fig_one.savefig(
            #     fname=f"{path_out}/sim_{sim}/dist/{fig_name}_ONE.{ext}", dpi=dpi_png,
            # )
        print(fig_name)
#"""
