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
# #############################################################################


import numpy as np
from obspy.taup import TauPyModel
import pygmt


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
    fig=None,
    fig_width="6c",
    fig_save=False,
    save_path="",
):

# %%
# -----------------------------------------------------------------------------
# Input
# -----------------------------------------------------------------------------
    # Required
    # - source_depth: hypocentral depth | km
    # - receiver_dist: epicentral distance | degrees
    # - phases: seismological phases | list of strings

    # Optional
    # - earth_model: Earth model | Default iasp91
    # - r_earth: Earth's radius | km | Default 6371
    # - min_depth: minimum for plotting | km | Default 0
    # - max_depth: maximum for plotting | km | Default Earth's radius
    # - min_dist: minimum for plotting | degrees | Default 0
    # - max_dist: maximum for plotting | degrees | Default epicentral distance + 10
    # - font_size: Font size for text | Default 4p
    # - fig: PyGMT figure instance | Default set up new Figure instance
    # - fig_width: Width of figure | Default 6c
    # - fig_save: Save figure to image file | Default False
    # - save_path: path to folder to save figure

    if fig==None:
        fig = pygmt.Figure()

    if max_depth==None:
        max_depth = r_earth

    if max_dist==None:
        max_dist = int(np.round(receiver_dist)) + 10


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
    rad2deg = 360 / (2 * np.pi)

# -----------------------------------------------------------------------------
    # Region
    max_radius = r_earth - min_depth
    min_radius = r_earth - max_depth

    no_clip_used = False
    if min_depth==0 and max_depth==r_earth:
        no_clip_used = True

# -----------------------------------------------------------------------------
    # Plotting
    color_highlight = "255/90/0"
    box_standard = "+gwhite@30+p0.1p,gray30+r2p"
    label_font = font_size

    phase_colors = {
        "P": "navyblue",
        "S": "blue",
        "PcP": "deepskyblue",
        "ScS": "cyan",
        "SKS": "205/0/0",  # -> red  # "blue"
        "SKKS": "238/118/0",  # -> orange  # "green3",
        "PKS": "yellow2",
        "PKKP": "darkgreen",
        "PKIKP": "darkorange",
        "PKJKP": "purple2",
        "SKJKS": "maroon",
        "PKPPKP": "yellow",
    }


# %%
# -----------------------------------------------------------------------------
# Calculate travel times and travel paths via ObsPy and taup
# -----------------------------------------------------------------------------
# https://docs.obspy.org/packages/autogen/obspy.taup.tau.TauPyModel.html
# last access: 2023/12/11

    model = TauPyModel(model=earth_model)

    pp_temp = model.get_ray_paths(
        source_depth_in_km=source_depth,
        distance_in_degree=receiver_dist,
        phase_list=phases,
    )


# %%
# -----------------------------------------------------------------------------
# Create plot for travel paths via PyGMT
# -----------------------------------------------------------------------------

    # Set up polar plot
    pygmt.config(FONT=label_font, FORMAT_GEO_MAP="+D")
    fig.basemap(
        region=[min_dist, max_dist, min_radius, max_radius],
#        projection="P" + fig_width + "+a+t" + str(receiver_dist/2) + "+z",
        projection=f"P{fig_width}+a+t0+z",
        frame="+gwhite",  # annotations are set later
    )

# -----------------------------------------------------------------------------
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
        if max_dist!=360:
            fig.text(
                x=0,
                y=r_earth - bound,
                text=bound,
                font=label_font,
                angle=50,  # degrees counter-clockwise from horizontal
                justify="RM",
                offset="-0.05c/-0.05c",
                no_clip=no_clip_used,
            )
        else:
            if bound==6371: y_offset = 0
            elif bound==5120: y_offset = 200
            elif bound==2900: y_offset = -200
            elif bound==2700: y_offset = 200
            elif bound==660: y_offset = -200
            elif bound==440: y_offset = -50
            elif bound==120: y_offset = -70
            fig.plot(
                x=np.linspace(min_dist, max_dist, max_dist),
                y=np.ones(max_dist) * (r_earth - bound + y_offset),
                style=f"qn1:+l{bound} km+f{label_font}+v+i+gwhite@30+o+c0.03c/0.03c",
            )
            y_offset = 0.05
            if bound==6371: y_offset = 0
            elif bound==5120: y_offset = -0.1
            elif bound==2900: y_offset = 0.15
            elif bound==2700: y_offset = -0.1
            elif bound==660: y_offset = 0.15
            elif bound==440: y_offset = 0.05
            elif bound==120: y_offset = 0.06
            if bound==6371:
                fig.text(
                    # x=receiver_dist/2 + 180,
                    x=180,
                    y=r_earth - bound,
                    text=f"{bound} km",
                    font=label_font,
                    justify="MC",
                    fill="white@30",
                    clearance="0.03c/0.03c+tO",
                    offset=f"0c/{y_offset}c",
                )

# -----------------------------------------------------------------------------
    # Plot travel paths
    fig_name_phase = []
    for i_phase in range(len(pp_temp)):

        # Spread legend over two columns
        leg_col_str = ""
        if i_phase==0: leg_col_str = "+N3"
        # if i_phase==0: leg_col_str = "+N2"

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
        if (np.round(pp_dist_used.max(), 3) > receiver_dist) or \
           (receiver_dist > 180 and np.round(pp_dist_used.max(), 3) < receiver_dist):
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
    fig.legend(position="jBC+jTC+o0c/0.5c+w8c/1c", box=box_standard)
    # fig.legend(position="jBC+jTC+o0c/0.5c+w5c/0.75c", box=box_standard)

# -----------------------------------------------------------------------------
    # Add frame with annotations for distance
    fig.basemap(frame=["xa10f5", "wbNe"])

    # Plot source
    fig.plot(
        x=0,
        y=r_earth-source_depth,
        # style="a0.35c",
        # fill=color_highlight,
        # pen="0.4p,black",
        style="kearthquake.def/0.7c",
        fill=color_highlight,
        pen=color_highlight,
        no_clip=no_clip_used,
    )

    # Plot receiver
    # Rotate receiver to be always perpendicular to tangent to the surface point
    x_receiver = receiver_dist
    y_receiver = r_earth + 200
    angle_reciever = 180 - receiver_dist
    perspective_receiver = f"{angle_reciever}+w{x_receiver}/{y_receiver}"
    fig.plot(
        x=x_receiver,
        y=y_receiver,
        style="t0.3c",
        fill="gold",
        pen="0.4p,black",
        perspective=perspective_receiver,
        no_clip=no_clip_used,
    )

# -----------------------------------------------------------------------------
    # Add labels for Earth model, epicentral distance, hypocentral depth
    fig.text(
        text=earth_model,
        position="BL",
        offset="0.3c/0c",
        justify="BL",
        no_clip=True,
    )
    fig.text(
        text=f"@~D@~ = {round(receiver_dist,3)}°",
        position="BR",
        offset="-1.5c/0c",
        justify="BL",
        no_clip=True,
    )
    fig.text(
        text=f"hd = {round(source_depth,3)} km",
        position="BR",
        offset="-1.5c/-0.3c",
        justify="BL",
        no_clip=True,
    )

# -----------------------------------------------------------------------------
    # Show and save figure
    if fig_save==True:

        fig_name = f"{save_path}map_travelpath_{int(np.round(receiver_dist))}deg_" + \
                   "_".join(fig_name_phase)

        for ext in ["pdf", "png", "eps"]:
            fig.savefig(fname=f"{fig_name}.{ext}")

        fig.show()

        print(fig_name)
