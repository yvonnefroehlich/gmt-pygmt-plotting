# #############################################################################
# Sketches of Earth section
# >>> Not to scale <<<
# -> Adjust the ellipses for your needs
# -----------------------------------------------------------------------------
# History
# - Created: 2025/01/12
# - Updated: 2025/09/17 - Allow to select from different color combinations
# - Updated: 2025/09/19 - Improve coding style
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


import pygmt

# -----------------------------------------------------------------------------
def earth_section(
    # Select section type: Choose from
    # "open_vertical" | "half_vertical" | "half_horizontal" | northeast_quadrant"
    section_type,
    color_concept="green",  # "green" | "brown" | "kit" | "own"
    # Set colors used for color_concept="own"
    color_land="yellowgreen",
    color_water="steelblue",
    color_sl="white",  # shorelines
    pen_grid="0.1p,gray60",
    pen_frame="0.8p,gray30",
    pen_sec="0.01p,gray90",
    pen_qua="0.5p,gray30,dashed",
    color_cover="white",
    # Uncomment line 124 to save the images
    # Set path to folder where images should be stored
    path_out="",
):

    match color_concept:
        case "green":
            color_land = "yellowgreen"
            color_water = "steelblue"
            color_sl = "white"
        case "kit":
            color_land = "76/181/167"
            color_water = "217/239/236"
            color_sl = "0/150/130"
        case "brown":
            color_land = "lightbrown"
            color_water = "lightblue"
            color_sl = "brown"
        case "own":
            color_land = color_land
            color_water = color_water
            color_sl = color_sl

    match section_type:
        case "open_vertical" | "half_vertical":
            projection = "G0/0/10c"
            lon_min = -20
            lon_max = 100
            lat_lim = 89
            x_sec = [lon_min, lon_max, lon_max, lon_min]
            y_sec = [lat_lim, lat_lim, -lat_lim, -lat_lim]
        case "half_horizontal":
            projection = "G0/20/10c"
        case "northeast_quadrant":
            projection = "G0/5/10c"
            x_qua = [-10, -10, 100, 40]
            y_qua = [90, 0, 0, 90]

# -----------------------------------------------------------------------------
    fig = pygmt.Figure()
    pygmt.config(MAP_GRID_PEN_PRIMARY=pen_grid, MAP_FRAME_PEN=pen_frame)

    fig.basemap(projection=projection, region="g", frame=0)
    fig.coast(land=color_land, water=color_water, shorelines=f"1/0.01p,{color_sl}")
    fig.basemap(frame="g10")

# -----------------------------------------------------------------------------
    match section_type:
        case "open_vertical":
            fig.plot(x=x_sec, y=y_sec, fill="gray55", pen=pen_frame)

            args_sec = {"y": 0, "pen": pen_sec}

            fig.plot(x=0.8, style="e90/8.0/2.7", fill="gray65", **args_sec)
            fig.plot(x=0.5, style="e90/5.0/1.9", fill="gray75", **args_sec)
            fig.plot(x=0.6, style="e90/2.5/1.2", fill="gray85", **args_sec)

            fig.plot(x=0, style="w10.0c/-90/90", fill="gray60", **args_sec)
            fig.plot(x=0, style="w8.0c/-90/90", fill="gray70", **args_sec)
            fig.plot(x=0, style="w5.0c/-90/90", fill="gray80", **args_sec)
            fig.plot(x=0, style="w2.5c/-90/90", fill="gray90", **args_sec)

            fig.basemap(frame=0)

        case "half_vertical":
            fig.plot(x=x_sec, y=y_sec, fill=color_cover)

            args_sec = {"x": 0, "y": 0}

            fig.plot(style="w10c/-90/90", pen="1.5p,white", no_clip=True, **args_sec)

            fig.plot(style="e90/10/3.6", pen=pen_frame, fill="gray55", no_clip=True, **args_sec)
            fig.plot(style="e90/8.0/2.7", pen=pen_sec, fill="gray65", **args_sec)
            fig.plot(style="e90/5.0/1.9", pen=pen_sec, fill="gray75", **args_sec)
            fig.plot(style="e90/2.5/1.2", pen=pen_sec, fill="gray85", **args_sec)

        case "half_horizontal":
            args_sec = {"x": 0, "y": 20}

            fig.plot(style="w10c/0/180", pen="1.5p,white", fill=color_cover, no_clip=True, **args_sec)

            fig.plot(style="e0/10.0/3.6", pen=pen_frame, fill="gray55", no_clip=True, **args_sec)
            fig.plot(style="e0/8.0/2.7", pen=pen_sec, fill="gray65", **args_sec)
            fig.plot(style="e0/5.0/1.9", pen=pen_sec, fill="gray75", **args_sec)
            fig.plot(style="e0/2.5/1.2", pen=pen_sec, fill="gray85", **args_sec)

        case "northeast_quadrant":
            fig.plot(x=x_qua, y=y_qua, fill="gray95", pen=pen_frame)

            fig.plot(x=[0, 0], y=[90, 10], pen=pen_qua)
            fig.plot(x=[-10, 0], y=[0, 10], pen=pen_qua)
            fig.plot(x=[0, 90], y=[10, 0], pen=pen_qua)

            fig.coast(
                land=f"{color_land}@90",
                water=f"{color_water}@90",
                shorelines=f"1/0.01p,{color_sl}@50",
            )

            fig.basemap(frame="g10")

# -----------------------------------------------------------------------------
    fig.show()
    fig_name = f"earth_section_{section_type}_{color_concept}"
    for ext in ["png"]:
        alpha_png = False
        if ext == "png":
            alpha_png = True
        # fig.savefig(fname=f"{path_out}{fig_name}.{ext}", transparent=alpha_png)
    print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Examples
# -----------------------------------------------------------------------------
earth_section(section_type="open_vertical")

earth_section(section_type="half_vertical", color_concept="brown")

earth_section(section_type="half_horizontal", color_concept="brown")

earth_section(section_type="northeast_quadrant", color_concept="kit")
