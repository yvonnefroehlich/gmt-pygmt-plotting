# #############################################################################
# Earth section
# >>> Not to scale <<<
# -> Adjust the ellipses for your needs
# -----------------------------------------------------------------------------
# History
# - Created: 2025/01/12
# -----------------------------------------------------------------------------
# Versions
#   PyGMT v0.14.0 -> https://www.pygmt.org/v0.14.0/ | https://www.pygmt.org/
#   GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt


def earth_section(
    # Select section type: Choose from
    # "open_vertical", "half_vertical", "half_horizontal", northeast_quadrant"
    section_type,
    color_land="lightbrown",
    color_water="lightblue",
    color_shorelines="brown",
    color_cover="white",
    pen_grid="0.1p,gray60",
    pen_map="0.8p,gray30",
    pen_sec="0.01p,gray90",
    pen_qua="0.5p,gray30,dashed",
    # Uncomment line 124 to save the images
    # Set path to folder where images should be stored
    path_out="",
):


# -----------------------------------------------------------------------------
    fig = pygmt.Figure()
    pygmt.config(MAP_GRID_PEN_PRIMARY=pen_grid, MAP_FRAME_PEN=pen_map)

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

    fig.coast(
        projection=projection,
        region="g",
        frame="g10",
        land=color_land,
        water=color_water,
        shorelines=f"1/0.01p,{color_shorelines}",
    )

# -----------------------------------------------------------------------------
    match section_type:
        case "open_vertical":
            fig.plot(x=x_sec, y=y_sec, fill="gray55", pen=pen_map)

            fig.plot(x=0.8, y=0, style="e90/8.0/2.7", pen=pen_sec, fill="gray65")
            fig.plot(x=0.5, y=0, style="e90/5.0/1.9", pen=pen_sec, fill="gray75")
            fig.plot(x=0.6, y=0, style="e90/2.5/1.2", pen=pen_sec, fill="gray85")

            fig.plot(x=0, y=0, style="w10.0c/-90/90", pen=pen_sec, fill="gray60")
            fig.plot(x=0, y=0, style="w8.0c/-90/90", pen=pen_sec, fill="gray70")
            fig.plot(x=0, y=0, style="w5.0c/-90/90", pen=pen_sec, fill="gray80")
            fig.plot(x=0, y=0, style="w2.5c/-90/90", pen=pen_sec, fill="gray90")

            fig.basemap(frame=0)

        case "half_vertical":
            fig.plot(x=x_sec, y=y_sec, fill=color_cover)

            fig.plot(x=0, y=0, style="w10c/-90/90", pen="1.5p,white", no_clip=True)

            fig.plot(x=0, y=0, style="e90/10/3.6", pen=pen_map, fill="gray55", no_clip=True)
            fig.plot(x=0, y=0, style="e90/8.0/2.7", pen=pen_sec, fill="gray65")
            fig.plot(x=0, y=0, style="e90/5.0/1.9", pen=pen_sec, fill="gray75")
            fig.plot(x=0, y=0, style="e90/2.5/1.2", pen=pen_sec, fill="gray85")

        case "half_horizontal":
            fig.plot(x=0, y=20, style="w10c/0/180", pen="1.5p,white", fill=color_cover, no_clip=True)

            fig.plot(x=0, y=20, style="e0/10.0/3.6", pen=pen_map, fill="gray55", no_clip=True)
            fig.plot(x=0, y=20, style="e0/8.0/2.7", pen=pen_sec, fill="gray65")
            fig.plot(x=0, y=20, style="e0/5.0/1.9", pen=pen_sec, fill="gray75")
            fig.plot(x=0, y=20, style="e0/2.5/1.2", pen=pen_sec, fill="gray85")

        case "northeast_quadrant":
            fig.plot(x=x_qua, y=y_qua, fill="gray95", pen=pen_map)

            fig.plot(x=[0, 0], y=[90, 10], pen=pen_qua)
            fig.plot(x=[-10, 0], y=[0, 10], pen=pen_qua)
            fig.plot(x=[0, 90], y=[10, 0], pen=pen_qua)

            fig.coast(
                land=f"{color_land}@90",
                water=f"{color_water}@90",
                shorelines=f"1/0.01p,{color_shorelines}@50",
            )
            fig.basemap(frame="g10")

# -----------------------------------------------------------------------------
    fig.show()
    fig_name = f"earth_section_{section_type}"
    for ext in ["png"]:
        alpha_png = False
        if ext == "png":
            alpha_png = True
        # fig.savefig(fname=f"{path_out}{fig_name}.{ext}", dpi=360, transparent=alpha_png)
    print(fig_name)


# %%
# -----------------------------------------------------------------------------
# Example
# -----------------------------------------------------------------------------
for section_type in [
    "open_vertical",
    "half_vertical",
    "half_horizontal",
    "northeast_quadrant",
]:
    earth_section(section_type=section_type)
