# #############################################################################
# Seismological phase through the Earth
# - Calculate travel times and travel paths via ObsPy and taup
# - Plot travel paths via PyGMT
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# Related to:
#   Fröhlich Y., Grund M. & Ritter J. R. R. (2024).
#   Lateral and vertical variations of seismic anisotropy in the lithosphere-
#   asthenosphere system underneath Central Europe from long-term splitting
#   measurements. Revision submitted to Geophysical Journal International
# -----------------------------------------------------------------------------
# - Created: 2024/04/07
#   PyGMT v0.11.0 -> https://www.pygmt.org/v0.11.0/ | https://www.pygmt.org/
#   GMT 6.4.0 -> https://www.generic-mapping-tools.org/
# - Updated: 2024/04/23 - Improve coding style
# - Updated: 2024/05/04 - Improve arguments and comments for colors
# - Updated: 2024/05/04 - Improvements regarding PyGMT Figure instance
# - Updated: 2024/05/07 - Refractor: Introduce function taup_color
# - Updated: 2024/xx/05 - Allow plotting specific distance and depth ranges
# #############################################################################


import numpy as np
import pygmt
from obspy.taup import TauPyModel

from taup_color import taup_color


def taup_path(
    source_depth,
    receiver_dist,
    phases,
    earth_model="iasp91",
    r_earth=6371,
    min_depth=0,
    max_depth=None,
    min_dist=0,
    max_dist=None,
    font_size="4p",
    fig_instance=True,
    fig_width="6c",
    fig_save=False,
    save_path="",
):
    # %%
    # -------------------------------------------------------------------------
    # Input
    # -------------------------------------------------------------------------
    # Required
    # - source_depth: Hypocentral depth | km
    # - receiver_dist: Epicentral distance | degrees
    # - phases: Seismological phases | list of strings

    # Optional
    # - earth_model: Earth model | Default iasp91
    # - r_earth: Earth's radius | km | Default 6371
    # - min_depth: Minimum for plotting | km | Default 0
    # - max_depth: Maximum for plotting | km | Default Earth's radius
    # - min_dist: Minimum for plotting | degrees | Default 0
    # - max_dist: Maximum for plotting | degrees | Default epicentral distance + 10
    # - font_size: Font size for text | Default 4p
    # - fig_instance: Provide a PyGMT figure instance | Default a new one is set up
    # - fig_width: Width of figure | Default 6c
    # - fig_save: Save figure to file | Default False
    # - save_path: Path of folder to save figure | Default current working directory

    fig = pygmt.Figure()
    if fig_instance != None:
        fig = fig_instance

    if max_depth == None:
        max_depth = r_earth

    if max_dist == None:
        max_dist = int(np.round(receiver_dist)) + 10

    # %%
    # -------------------------------------------------------------------------
    # General stuff
    # -------------------------------------------------------------------------
    rad2deg = 360 / (2 * np.pi)

    # -------------------------------------------------------------------------
    # Region
    max_radius = r_earth - min_depth
    min_radius = r_earth - max_depth

    # -------------------------------------------------------------------------
    # Plotting
    color_highlight = "255/90/0"
    box_standard = "+gwhite@30+p0.1p,gray30+r2p"
    label_font = font_size

    # Colors for seismological phases
    # Adjust and extend the dictionary for your needs in taup_path.py
    phase_colors = taup_color()

    # %%
    # -------------------------------------------------------------------------
    # Calculate travel times and travel paths via ObsPy and taup
    # -------------------------------------------------------------------------
    # https://docs.obspy.org/packages/autogen/obspy.taup.tau.TauPyModel.html
    # last access: 2023/12/11

    model = TauPyModel(model=earth_model)

    pp_temp = model.get_ray_paths(
        source_depth_in_km=source_depth,
        distance_in_degree=receiver_dist,
        phase_list=phases,
    )

    # %%
    # -------------------------------------------------------------------------
    # Create plot for travel paths via PyGMT
    # -------------------------------------------------------------------------
    # Set up polar plot
    # Center in the middle of the epicentral distance range
    add_mindist = 0
    if min_dist > 0: add_mindist = min_dist

    center_point = (np.abs(max_dist) - np.abs(min_dist)) / 2 + add_mindist
    if min_dist==0 and max_dist==360: center_point = 0

    pygmt.config(FONT=label_font, FORMAT_GEO_MAP="+D")
    fig.basemap(
        region=[min_dist, max_dist, min_radius, max_radius],
        projection=f"P{fig_width}+a+t{center_point}+z",
        frame="+gwhite",  # annotations are set later
    )

    # -------------------------------------------------------------------------
    # Plot dicontinuities
    bounds = [120, 440, 660, 2700, 2900, 5120, 6371]  # km
    pygmt.makecpt(cmap="batlow", series=[0, len(bounds)])
    for bound in bounds:
        fig.plot(
            x=np.linspace(min_dist, max_dist, max_dist),
            y=np.ones(max_dist) * (r_earth - bound),
            pen="0.4p,gray10",
            fill="tan@75",
            close="+y",
        )
        if max_dist != 360:
            angle_depth = (np.abs(min_dist) + np.abs(max_dist)) / 2 - add_mindist
            angle_flip = 0
            justify_depth = "RM"
            if np.abs(min_dist) + np.abs(max_dist) > 200:  # degrees
                angle_flip = 180
                justify_depth = "LM"
            if bound > min_depth and bound < max_depth:
                fig.text(
                    x=min_dist,
                    y=r_earth - bound,
                    text=bound,
                    font=label_font,
                    angle=angle_depth + angle_flip,
                    justify=justify_depth,
                    offset="-0.05c/-0.05c",
                    fill="white@30",
                    no_clip=True,
                )
        else:
            if bound == 6371: y_offset = 0
            elif bound == 5120: y_offset = 200
            elif bound == 2900: y_offset = -200
            elif bound == 2700: y_offset = 200
            elif bound == 660: y_offset = -200
            elif bound == 440: y_offset = -50
            elif bound == 120: y_offset = -70
            fig.plot(
                x=np.linspace(min_dist, max_dist, max_dist),
                y=np.ones(max_dist) * (r_earth - bound + y_offset),
                style=f"qn1:+l{bound} km+f{label_font}+v+i+gwhite@30+o+c0.03c/0.03c",
            )
            # if bound==6371: y_offset = 0
            # elif bound==5120: y_offset = -0.1
            # elif bound==2900: y_offset = 0.15
            # elif bound==2700: y_offset = -0.1
            # elif bound==660: y_offset = 0.15
            # elif bound==440: y_offset = 0.05
            # elif bound==120: y_offset = 0.06
            if bound == 6371:
                fig.text(
                    x=180,
                    y=r_earth - bound,
                    text=f"{bound} km",
                    font=label_font,
                    justify="MC",
                    fill="white@30",
                    clearance="0.03c/0.03c+tO",
                    offset=f"0c/{y_offset}c",
                )

    # -------------------------------------------------------------------------
    # Plot travel paths
    fig_name_phase = []
    for i_phase in range(len(pp_temp)):
        # Spread legend over several columns
        leg_col_str = ""
        # Adjust number of columns for your needs
        if i_phase == 0: leg_col_str = "+N3"

        pp_depth = []
        pp_dist = []

        for i_depth in range(len(pp_temp[i_phase].path)):
            pp_temp_depth = pp_temp[i_phase].path[i_depth][3]
            pp_temp_dist = pp_temp[i_phase].path[i_depth][2]

            pp_depth.append(r_earth - pp_temp_depth)
            pp_dist.append(pp_temp_dist * rad2deg)

        phase_label = str(pp_temp[i_phase])
        phase_label_split = phase_label.split(" ")
        phase_time = phase_label_split[4]
        phase_time_split = phase_time.split(".")

        # Account for "anders herum gelaufene" phase
        pp_dist_used = np.array(pp_dist)
        if (np.round(pp_dist_used.max(), 3) > receiver_dist) or (
            receiver_dist > 180 and np.round(pp_dist_used.max(), 3) < receiver_dist
        ):
            pp_dist_used = pp_dist_used * -1

        fig.plot(
            x=pp_dist_used,
            y=pp_depth,
            pen=f"1.2p,{phase_colors[phase_label_split[0]]}",
            label=f"{phase_label_split[0]} | {phase_time_split[0]} s+S0.5c/1c{leg_col_str}",
        )

        # Use only the existing phases in the file name
        fig_name_phase.append(phase_label_split[0])

    # Add legend for phases with travel times
    # Adjust width and height for your needs (+w)
    fig.legend(position="jBC+jTC+o0c/0.5c+w8c/1c", box=box_standard)

    # -------------------------------------------------------------------------
    # Add frame with annotations for distance
    fig.basemap(frame=["xa10f5", "wbNe"])

    # Plot source
    if source_depth <= max_depth:
        fig.plot(
            x=0,
            y=r_earth - source_depth,
            style="kearthquake.def/0.7c",
            fill=color_highlight,
            pen=color_highlight,
            no_clip=True,
        )

    # Plot receiver
    if receiver_dist <= max_dist:
        # Rotate receiver to be always perpendicular to tangent to the surface point
        x_receiver = receiver_dist
        y_receiver = r_earth + 200
        angle_reciever = 180 - receiver_dist + center_point
        perspective_receiver = f"{angle_reciever}+w{x_receiver}/{y_receiver}"
        fig.plot(
            x=x_receiver,
            y=y_receiver,
            style="t0.3c",
            fill="gold",
            pen="0.4p,black",
            perspective=perspective_receiver,
            no_clip=True,
        )

    # -------------------------------------------------------------------------
    # Add labels for Earth model, epicentral distance, hypocentral depth
    info_texts = [
        earth_model,
        f"@~D@~ = {round(receiver_dist,3)}°",
        f"hd = {round(source_depth,3)} km",
    ]

    if min_dist==0 and max_dist==360:
        info_offsets = ["0.3c/0c", "-1.5c/0c", "-1.5c/-0.3c"]
        for info_text, info_offset in zip(info_texts, info_offsets):
            info_pos = "BR"
            if info_text==earth_model: info_pos = "BL"
            fig.text(
                text=info_text,
                position=info_pos,
                offset=info_offset,
                justify="BL",
                font=f"{font_size},{color_highlight}",
                no_clip=True,
            )
    elif np.abs(min_dist) + np.abs(max_dist) > 200:  # degrees
        info_offsets = ["0c/0.8c", "0c/0.4c", "0c/0c"]
        for info_text, info_offset in zip(info_texts, info_offsets):
            fig.text(
                text=info_text,
                position="BC",
                offset=info_offset,
                justify="TC",
                font=f"{font_size},{color_highlight}",
                no_clip=True,
            )
    else:
        fig.text(
            text=" | ".join(info_texts),
            position="BC",
            offset="0c/-0.1c",
            justify="TC",
            font=f"{font_size},{color_highlight}",
            no_clip=True,
        )

    # -------------------------------------------------------------------------
    # Show and save figure
    if fig_instance == None:
        fig.show()

    if fig_save == True:
        plot_range_str = f"{min_depth}to{max_depth}km_{min_dist}to{max_dist}deg"
        fig_name = (
            f"{save_path}map_travelPATH_{int(np.round(source_depth))}km_" +
            f"{int(np.round(receiver_dist))}deg_{plot_range_str}_"
            + "_".join(fig_name_phase)
        )
        for ext in ["png"]: #, "pdf", "eps"]:
            fig.savefig(fname=f"{fig_name}.{ext}")

        print(fig_name)
