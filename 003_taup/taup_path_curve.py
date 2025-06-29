# #############################################################################
# Seismological phases through the Earth
# - Calculate via ObsPy based on the Java TauP Toolkit by [Crotwell 1999]
#   - travel times and travel paths
# - Plot via PyGMT
#   - travel path(s) in separate Figures
#   - travel path share with epicentral distance cumulative in one Figure
#   - travel time(s) in separate Figures
#   - travel time curve with epicentral distance cumulative in one Figure
# -----------------------------------------------------------------------------
# Related to
#   Fröhlich Y., Grund M. & Ritter J. R. R. (2024).
#   Lateral and vertical variations of seismic anisotropy in the lithosphere-
#   asthenosphere system underneath Central Europe from long-term splitting
#   measurements. Geophysical Journal International, 239(1), 112-135.
#   https://doi.org/10.1093/gji/ggae245.
# -----------------------------------------------------------------------------
# History
# - Created: 2024/04/07
# - Updated: 2024/04/23 - Maintenance: Coding style
# - Updated: 2024/05/04 - Maintenance: Arguments and comments for colors
# - Updated: 2024/05/04 - Enhancement: PyGMT Figure instance
# - Updated: 2024/05/07 - Refractor: Introduce function taup_color
# - Updated: 2024/05/10 - Enhancement: Plot specific distance and depth ranges
# - Updated: 2024/09/06 - Enhancement: Travel time (curve) with distance (cumulative)
# - Updated: 2025/03/27 - Maintenance: Adjust building file name
# - Updated: 2025/03/29 - Enhancement: Introduce function taup_style
# - Updated: 2025/03/30 - Enhancement: Allow setting step of epicentral distance annotations
# - Updated: 2025/03/31 - Enhancement: Introduce function taup_symbol
# - Updated: 2025/03/31 - Enhancement: Add crust
# - Updated: 2025/05/01 - Maintenance: Adjust creating legend for travel time curves
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.14.0 -> https://www.pygmt.org/v0.14.0/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
import pygmt
from obspy.taup import TauPyModel

from taup_color import taup_color
from taup_style import taup_style
from taup_symbol import taup_symbol

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
    step_dist=10,
    font_size="4p",
    earth_color="tan",
    path_overlay=False,
    fig_path_width="6c",
    fig_path_instance=None,
    thick_line_path="1.2p",
    legend_path=True,
    time_curve=False,
    fig_curve_width="10c",
    curve_dist_range=[0, 180],
    curve_time_range=[0, 3000],
    fig_curve_instance=None,
    legend_curve=True,
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
    # - earth_model: Earth model | Default "iasp91"
    # - r_earth: Earth's radius | km | Default 6371
    # - min_depth: Minimum for plotting | km | Default 0
    # - max_depth: Maximum for plotting | km | Default Earth's radius
    # - min_dist: Minimum for plotting | degrees | Default 0
    # - max_dist: Maximum for plotting | degrees | Default epicentral distance + 10
    # - step_dist: Step of epicentral distance annotations | degrees | Default 10
    # - font_size: Font size for text | Default "4p"
    # - path_overlay: Plot travel path on top of each other | False
    # - earth_color: Colors for Earth concentric shells or circles | Default "tan"
    #   Select from "non", "white", "tan", "gray", "bilbao_gray", "bilbao_brown"
    #   or pass any GMT built-in colormap
    # - fig_path_width: Width of figure for travel path plot | Default "6c"
    # - fig_path_instance: Provide a PyGMT Figure instance for the travel path plot |
    #   Default a new one is set up
    # - thick_line_path: Thickness of line for travel path | Default "1.2p" (points)
    # - legend_path: Add legend for travel paths | Default True
    # - time_curve: Create travel time curve plot | Default False
    # - fig_curve_width: Width of figure for travel time plot | Default "6c"
    # - curve_dist_range: Epicentral distance range of travel time plot | degrees |
    #   Default [0, 180]
    # - curve_time_range: Travel time range of travel time plot | seconds |
    #   Default [0, 3000]
    # - fig_curve_instance: Provide a PyGMT Figure instance for the travel time plot |
    #   Default a new one is set up
    # - legend_curve: Add legend for travel time curves | Default True
    # - fig_save: Save figure to file | Default False
    # - save_path: Path of folder to save figure | Default current working directory
    # -------------------------------------------------------------------------
    # Returns
    # -------------------------------------------------------------------------
    # - fig_path: PyGMT figure instance for travel path plot
    # Optional
    # - fig_curve: PyGMT figure instance for travel time curve plot


    # %%
    # -------------------------------------------------------------------------
    # General stuff
    # -------------------------------------------------------------------------
    if max_depth == None:
        max_depth = r_earth

    if max_dist == None:
        max_dist = int(np.round(receiver_dist)) + 10

    rad2deg = 360 / (2 * np.pi)

    # -------------------------------------------------------------------------
    # Region
    max_radius = r_earth - min_depth
    min_radius = r_earth - max_depth

    # -------------------------------------------------------------------------
    # Plotting
    color_highlight = "255/90/0"
    box_standard = "+gwhite+p0.1p,gray30+r2p"

    # Seismological phases
    # Colors: adjust and extend the dictionary for your needs in taup_color.py
    phase_colors = taup_color()
    # Line styles: adjust and extend the dictionary for your needs in taup_style.py
    phase_styles = taup_style()
	# Symbols: adjust and extend the dictionary for your needs in taup_symbol.py
    phase_symbol = taup_symbol()

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
    # Create plots for travel paths and travel times via PyGMT
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Set up polar plot
    add_dist = 0
    if min_dist > 0: add_dist = min_dist
    elif min_dist < 0 and max_dist < 0: add_dist = max_dist

    center_point = (np.abs(max_dist) - np.abs(min_dist)) / 2 + add_dist
    if min_dist == 0 and max_dist == 360: center_point = 0

    # -------------------------------------------------------------------------
    # Create or continue PyGMT Figure instance for travel curve plot
    if fig_path_instance != None:
        fig_path = fig_path_instance
    else:
        fig_path = pygmt.Figure()

    if path_overlay == False:
        pygmt.config(FONT=font_size)
        fig_path.basemap(
            region=[min_dist, max_dist, min_radius, max_radius],
            projection=f"P{fig_path_width}+a+t{center_point}+z",
            frame=0,  # Annotations are set later
        )

    # -------------------------------------------------------------------------
    # Set up colors for Earth concentric shells or circles
    bounds = [30, 120, 440, 660, 2700, 2900, 5120, 6371]  # depth in kilometers
    earth_colors = ["none", "white", "tan", "gray", "bilbao_gray", "bilbao_brown"]

    # Adjust for your needs
    if earth_color not in earth_colors:
        pygmt.makecpt(
            cmap=earth_color, series=[0, len(bounds), 1], transparency=50,
        )

    match earth_color:
        case "none":
            colors = ["white@100"] * len(bounds)
        case "white":
            colors = ["white"] * len(bounds)
        case "tan":
            colors = [
                "white", "244/236/236", "235/222/204", "229/211/188",
                "224/203/176", "220/197/167", "217/193/160", "white",
            ]
        case "gray":
            colors = [
                "white", "246.03", "228.09", "210.16",
                "193.22", "gray69", "159.34", "white",
            ]
        case "bilbao_gray":
            colors = [
                "white", "245.03/245.03/244.06", "225.09/224.09/223.09", "208.16/206.16/199.31",
                "197.22/193.22/177.22", "190.28/183.28/156.28", "184.34/172.34/135.34", "white",
            ]
        case "bilbao_brown":
            colors = [
                "white", "197.22/193.22/177.22", "190.28/183.28/156.28", "184.34/172.34/135.34",
                "177.41/157.41/116.41", "172/142.47/105", "168/127.53/98.531", "white",
            ]

    color_fig_curve = "white"
    if earth_color in ["tan", "bilao_gray", "bilbao_brown"]:
        color_fig_curve = "tan"
    elif earth_color == "gray":
        color_fig_curve = "gray"

    # -------------------------------------------------------------------------
    # Plot dicontinuities
    circle_step = 1
    circle_x = np.arange(min_dist, max_dist + circle_step, circle_step)
    circle_y = np.ones(len(circle_x))

    if path_overlay == False:
        for i_bound, bound in enumerate(bounds):
            # Plot Earth concentric circles
            fill_used = "+z"
            zvalue_used = i_bound
            camp_used = True
            if earth_color in earth_colors:
                fill_used = colors[i_bound]
                zvalue_used = None
                camp_used = None
            fig_path.plot(
                x=circle_x,
                y=circle_y * (r_earth - bound),
                close="+y",
                pen="0.4p,gray10",
                fill=fill_used,
                zvalue=zvalue_used,
                cmap=camp_used,
            )
            # Add depth labels
            if max_dist != 360:
                angle_sign = -1
                if min_dist < 0 and max_dist < 0: angle_sign = 1
                angle_depth = (np.abs(min_dist) + np.abs(max_dist)) / 2 + angle_sign * add_dist
                angle_flip = 0
                justify_depth = "RM"
                if max_dist - min_dist > 200:  # degrees
                    angle_flip = 180
                    justify_depth = "LM"
                if bound > min_depth and bound < max_depth:
                    fig_path.text(
                        x=min_dist,
                        y=r_earth - bound,
                        text=bound,
                        font=font_size,
                        angle=angle_depth + angle_flip,
                        justify=justify_depth,
                        offset="-0.05c/-0.05c",
                        fill="white@30",
                        no_clip=True,
                    )
            else:
                match bound:
                    case 6371: y_offset = 0
                    case 5120: y_offset = 200
                    case 2900: y_offset = -200
                    case 2700: y_offset = 200
                    case 660: y_offset = -200
                    case 440: y_offset = -50
                    case 120: y_offset = -70
                    case 30: y_offset = -1000  # outside of plot
                fig_path.plot(
                    x=np.linspace(min_dist, max_dist, max_dist),
                    y=np.ones(max_dist) * (r_earth - bound + y_offset),
                    style=f"qn1:+l{bound} km+f{font_size}+v+i+gwhite@30+o+c0.03c/0.03c",
                )
                if bound == 6371:
                    fig_path.text(
                        x=180,
                        y=r_earth - bound,
                        text=f"{bound} km",
                        font=font_size,
                        justify="MC",
                        fill="white@30",
                        clearance="0.03c/0.03c+tO",
                        offset=f"0c/{y_offset}c",
                    )

    # -------------------------------------------------------------------------
    # Create or continue PyGMT Figure instance for travel time plot
    if time_curve == True:
        if fig_curve_instance == None:
            # print("fig_curve does not exist and is created!")
            fig_curve = pygmt.Figure()
            pygmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray50")
            fig_curve.basemap(
                region=[
                    curve_dist_range[0], curve_dist_range[1],
                    curve_time_range[0], curve_time_range[1],
                ],
                projection=f"X{fig_curve_width}",
                frame=[
                    f"WSne+g{color_fig_curve}@50",
                    "xa30f10g10+lepicentral distance @~D@~ / @.",
                    "yafg100+ltravel time / s",
                ],
            )
        else:
            # print("fig_curve exist and is continued!")
            fig_curve = fig_curve_instance

    # -------------------------------------------------------------------------
    # Iterate over phases
    fig_name_phase = []
    for i_phase in range(len(pp_temp)):

    # -------------------------------------------------------------------------
        # Plot travel paths

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

        fig_path.plot(
            x=pp_dist_used,
            y=pp_depth,
            pen=f"{thick_line_path},{phase_colors[phase_label_split[0]]},{phase_styles[phase_label_split[0]]}",
            label=f"{phase_label_split[0]} | {phase_time_split[0]} s+S0.5c/1c{leg_col_str}",
        )

    # -------------------------------------------------------------------------
        # Plot travel times
        if time_curve == True:

            fig_curve.plot(
                x=receiver_dist,
                y=phase_time_split[0],
                style=f"{phase_symbol[phase_label_split[0]]}0.13c",
                fill=phase_colors[phase_label_split[0]],
                pen="0.001p,gray10",
                no_clip=True,
            )

    # -------------------------------------------------------------------------
        # Use only the existing phases in the file name
        fig_name_phase.append(phase_label_split[0])
        # Remove doublictes
        fig_name_phase = list(dict.fromkeys(fig_name_phase))
    # Use submitted phase list in case the list of the existing phases is empty
    if fig_name_phase == []:
        fig_name_phase = phases

    # -------------------------------------------------------------------------
    # Add legend for phases in travel time plot
    if time_curve == True and legend_curve == True:
        for phase in phases:
            col_str = ""
            info_str = ""
            fig_curve.plot(
                x=-1,
                y=-1,
                style="c0.05c",
                fill=phase_colors[phase],
                pen="0.05p,gray10",
                label=f"{phase}{info_str}{col_str}+S0.15c",
            )
        fig_curve.legend(position="JRT+jTL+o0.2/0c+w2c", box=box_standard)
    # -------------------------------------------------------------------------
    # Add legend for phase names and travel times in travel path plot
    # Adjust width and height for your needs (+w)
    if legend_path == True:
        fig_path.legend(position="jBC+jTC+o0c/0.5c+w8c/1c", box=box_standard)

    # -------------------------------------------------------------------------
    # Plot source
    if source_depth <= max_depth and source_depth >= min_depth \
       and min_dist <= 0 and max_dist > 0:
        fig_path.plot(
            x=0,
            y=r_earth - source_depth,
            style="a0.35c",
            fill=color_highlight,
            pen="0.4p,black",
            no_clip=True,
        )

    # Add frame with annotations for distance
    if path_overlay == False:
        # Affects the last addressed Figure instance
        with pygmt.config(FORMAT_GEO_MAP="+D"):  # 0°-360°
            fig_path.basemap(frame=[f"xa{step_dist}f5", "wbNe"])

    # Plot receiver always at surface, i.e., 0 km
    if min_depth == 0 and receiver_dist <= max_dist:
        # Rotate to be always perpendicular to tangent to the surface point
        x_receiver = receiver_dist
        # Have the lower edge of the inverse triangle at the top of the surface
        y_receiver = r_earth + 200  # Seems to work in many cases quite well
        angle_reciever = 180 - receiver_dist + center_point
        perspective_receiver = f"{angle_reciever}+w{x_receiver}/{y_receiver}"
        fig_path.plot(
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

    if abs(max_dist - min_dist) > 330:
        info_offsets = ["0.3c/0c", "-1.5c/0c", "-1.5c/-0.3c"]
        for info_text, info_offset in zip(info_texts, info_offsets):
            info_pos = "BR"
            if info_text == earth_model: info_pos = "BL"
            fig_path.text(
                text=info_text,
                position=info_pos,
                offset=info_offset,
                justify="BL",
                font=f"{font_size},{color_highlight}",
                fill="white",
                no_clip=True,
            )
    elif abs(max_dist - min_dist) > 200 and abs(max_dist - min_dist) < 330:  # degrees
        info_offsets = ["0c/0.8c", "0c/0.4c", "0c/0c"]
        for info_text, info_offset in zip(info_texts, info_offsets):
            fig_path.text(
                text=info_text,
                position="BC",
                offset=info_offset,
                justify="TC",
                font=f"{font_size},{color_highlight}",
                fill="white",
                no_clip=True,
            )
    else:
        fig_path.text(
            text=" | ".join(info_texts),
            position="BC",
            offset="0c/-0.1c",
            justify="TC",
            font=f"{font_size},{color_highlight}",
            fill="white",
            no_clip=True,
        )

    # -------------------------------------------------------------------------
    # Show and save figures
    fig_path.show()
    if time_curve == True: fig_curve.show()

    plot_range_str = f"{min_depth}to{max_depth}km_{min_dist}to{max_dist}deg_"
    fig_name_start = f"{save_path}map_travel"
    fig_name_end = f"_{source_depth}km_{int(np.round(receiver_dist))}deg" + \
                    f"_{plot_range_str}" + "_".join(fig_name_phase) + \
                    f"_{earth_color}"

    if fig_save == True:
        for ext in ["png"]: #, "pdf", "eps"]:
            fig_path.savefig(fname=f"{fig_name_start}PATH{fig_name_end}.{ext}")
            if time_curve == True:
                fig_curve.savefig(
                    fname=f"{fig_name_start}CURVE{fig_name_end}.{ext}"
                )

    print(f"{fig_name_start}{fig_name_end}")

    # -------------------------------------------------------------------------
    # Return PyGMT Figure instances
    if time_curve == True:
        return fig_path, fig_curve
    else:
        return fig_path



# %%
# -----------------------------------------------------------------------------
# Examples
# -----------------------------------------------------------------------------
fig_path, fig_curve = taup_path(
    fig_path_width="8c",
    font_size="6.5p",
    earth_color="gray",
    source_depth=500,
    receiver_dist=142,
    max_dist=360,
    phases=["S", "ScS", "PKS", "PKKS", "SKS", "SKKS", "SKIKS", "SKJKS"],
    time_curve=True,
    # fig_save=True,
    # save_path="02_your_example_figures/",
)

fig_path = taup_path(
    fig_path_width="8c",
    font_size="6.5p",
    earth_color="gray",
    source_depth=500,
    receiver_dist=142,
    min_dist=100,
    max_dist=180,
    min_depth=660,
    max_depth=4000,
    phases=["S", "ScS", "PKS", "PKKS", "SKS", "SKKS", "SKIKS", "SKJKS"],
    # fig_save=True,
    # save_path="02_your_example_figures/",
)

# -----------------------------------------------------------------------------
fig_path = taup_path(
    fig_path_width="8c",
    font_size="6.5p",
    source_depth=500,
    receiver_dist=95,
    min_dist=-5,
    max_dist=100,
    phases=["SKS", "pSKS", "sSKS", "SKKS", "pSKKS", "sSKKS"],
    # fig_save=True,
    # save_path="02_your_example_figures/",
)

fig_path = taup_path(
    fig_path_width="8c",
    font_size="6.5p",
    source_depth=500,
    receiver_dist=95,
    min_dist=-5,
    max_dist=100,
    min_depth=0,
    max_depth=4000,
    phases=["SKS", "pSKS", "sSKS", "SKKS", "pSKKS", "sSKKS"],
    # fig_save=True,
    # save_path="02_your_example_figures/",
)

fig_path = taup_path(
    fig_path_width="8c",
    font_size="6.5p",
    source_depth=500,
    receiver_dist=95,
    min_dist=-3,
    max_dist=7,
    step_dist=5,
    min_depth=0,
    max_depth=800,
    phases=["SKS", "pSKS", "sSKS", "SKKS", "pSKKS", "sSKKS"],
    # fig_save=True,
    # save_path="02_your_example_figures/",
)

# -----------------------------------------------------------------------------
dist_min = 0  # degrees
dist_max = 80
dist_step = 20
for dist in np.arange(dist_min, dist_max + dist_step, dist_step):

    if dist == dist_min:
        fig_path_instance = None
        fig_curve_instance = None
        path_overlay = False
    else:
        fig_path_instance = fig_path
        fig_curve_instance = fig_curve
        path_overlay = True

    fig_save = False
    if dist == dist_max: fig_save = True  # Save only the last figure

    fig_path, fig_curve = taup_path(
        fig_path_width="8c",
        font_size="6.5p",
        earth_color="gray",
        thick_line_path="0.5p",
        receiver_dist=dist,
        phases=["P", "PcP"],
        source_depth=500,
        min_dist=0,
        max_dist=360,
        fig_path_instance=fig_path_instance,
        path_overlay=path_overlay,
        time_curve=True,
        fig_curve_instance=fig_curve_instance,
        curve_dist_range=[dist_min - dist_step, dist_max + dist_step],
        curve_time_range=[0, 2700],
        legend_path=False,
        # fig_save=fig_save,
        # save_path="02_your_example_figures/",
    )
