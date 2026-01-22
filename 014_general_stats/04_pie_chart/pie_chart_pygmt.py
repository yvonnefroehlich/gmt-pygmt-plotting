# #############################################################################
# Python function to create a pie chart in PyGMT
# - sectors, ring sectors
# - single colors, colormap
# - labels with absolute values, percent
#
# >>> Note <<<
# >>> Numbers and trends are difficult to read visually from pie charts.
# >>> If applicable use another plot type, e.g., a bar chart.
# -----------------------------------------------------------------------------
# History
# - Created: 2026/01/18
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.18.0 -> https://www.pygmt.org/v0.18.0 | https://www.pygmt.org
# - GMT 6.6.0 -> https://www.generic-mapping-tools.org
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import numpy as np
import pandas as pd
import pygmt
from pygmt.params import Position

def pie_chart(
    sectors,
    annot=[],
    colors=[],
    fill_type="discrete",
    radius_out=10,
    radius_in=0,
    colorbar=True,
    sector_labels="value_percent",
    unit=None,
    cb_label=None,
    round_digits=2,
    outline="1p,black,solid",
    font="8p",
):
    # %%
    # -------------------------------------------------------------------------
    # Input
    # -------------------------------------------------------------------------
    # Required
    # - sectors
    # Optional
    # - annot: Annotations assigned to the colors and used for the colorbar.
    #   Give always a list of strings. | Default "sector1", ..., "sectorN"
    # - colors: Fill of the sectors. Give a list with one colormap or with one
    #   or multiple colors. | Default colors based on colormap "batlow"
    # - fill_type: How to setup the coloring. Choose between "discrete" or
    #   "min_max". | Default "discrete"
    # - radius_out: Set size of plot. Give outer radius | Default 10
    # - radius_in: Create ring sectors. Give inner radius | Default 0
    # - colorbar: Add a colorbar | Default True, e.g. colorbar plotted
    # - sector_labels: Write labels in the sectors. Choose from
    #   "value_percent", "value", "percent", "annot". | Default "value_percent"
    # - unit: Add unit to values of labels and colorbar. | Default no unit
    # - cb_label: Add a label to the colorbar. | Default no label
    # - round_digits: Round values to specific number of digits. | Default 2
    # - outline: Outline of the sectors. Give a pen to adjust color, thickness
    #   and style. | Default "1p,black,solid"
    # - font: Size, style, color of the font used for the sector_labels. |
    #   Default "8p"
    # -------------------------------------------------------------------------
    # Returns
    # -------------------------------------------------------------------------
    # - df_sectors: pandas Dataframe with given and calculated data for the sectors



    # %%
    # -------------------------------------------------------------------------
    # Check and prepare input
    # -------------------------------------------------------------------------
    # Check annot
    if len(sectors) != len(annot) and len(annot) != 0:
        print(
            "The lengths of 'sectors' and 'cb_annot' must be identical. " + \
            "Using default colorbar annot 'sector1' ... 'sectorN'."
        )

    if annot == [] or (len(sectors) != len(annot)):
        annot = []
        for i_sector in range(len(sectors)):
            annot.append(f"sector {i_sector + 1}")

    # Check colors
    if (len(sectors) != len(colors)) and (len(colors) > 1) and fill_type=="discrete":
        print(
            "The lengths of 'sectors' and 'colors' must be identical " + \
            "for using fill_type=='discrete'! Using default colormap 'batlow'."
        )

    if len(colors) == 1:
        cmap = colors
    elif len(colors) > 1:
        cmap = ",".join(colors)
    else:
        cmap = "batlow"
    if (len(sectors) != len(colors)) and (len(colors) > 1) and fill_type=="discrete":
         cmap = "batlow"

    # Set inner radius of sectors
    if radius_in == True:
        radius_in = radius_out - radius_out * 0.5

    # Calculate percent for sectors
    if isinstance(sectors, list):
        sectors_array = np.array(sectors)
    else:
        sectors_array = sectors
    sectors_sum = sum(sectors)
    percents = sectors_array / sectors_sum * 100

    # Axis and colorbar labels
    if cb_label == None:
        cb_label = " "

    if unit == None:
        unit = " "
    else:
        unit = f" {unit}"  # Add white space before unit

    # Set up values for sectors
    angle_start = [0] * len(sectors)
    angle_end = [0] * len(sectors)
    angle_temp = 0
    text = []
    for i_sector, percent in enumerate(percents):
        angle_start[i_sector] = angle_temp
        angle_temp = angle_temp + percent * 3.6  # Convert percent to degrees
        angle_end[i_sector] = angle_temp

        # Create sector labels
        if sector_labels != None:
            match sector_labels:
                case "value_percent":
                    text_temp = f"{sectors[i_sector]}{unit} | {round(percent, round_digits)} %"
                case "value":
                    text_temp = f"{sectors[i_sector]}{unit}"
                case "percent":
                    text_temp = f"{round(percent, round_digits)} %"
                case "annot":
                    text_temp = annot[i_sector]
            text.append(text_temp)

    # Create pandas Dataframe
    dict_sectors = {"x": [0] * len(sectors), "y": [0] * len(sectors)}
    df_sectors = pd.DataFrame(dict_sectors, columns=["x", "y"])
    match fill_type:
        case "discrete":
            df_sectors["z_color"] = np.arange(0, len(sectors), 1)
        case "min_max":
            df_sectors["z_color"] = sectors
    df_sectors["radius_out"] = [radius_out] * len(sectors)
    df_sectors["angle_start"] = angle_start
    df_sectors["angle_end"] = angle_end
    df_sectors["value"] = sectors
    df_sectors["percent"] = percents

    middle_sectors = df_sectors["angle_start"] + \
        (df_sectors["angle_end"] - df_sectors["angle_start"]) / 2


    # %%
    # -------------------------------------------------------------------------
    # Create plot
    # -------------------------------------------------------------------------
    fig = pygmt.Figure()
    pygmt.config(FORMAT_GEO_MAP="+D")
    fig.basemap(region=[0, 360, 0, 1], projection=f"P{radius_out}c", frame="+n")

    match fill_type:
        case "discrete":
            pygmt.makecpt(
                cmap=cmap,
                series=[0, len(sectors) - 1, 1],
                color_model="+c" + ",".join(annot),
            )
        case "min_max":
            pygmt.makecpt(cmap=cmap, series=[min(sectors), max(sectors)])

    # Plot sectors
    args_sector = {"data": df_sectors, "style": f"w+i{radius_in}c", "cmap": True}
    if outline in [None, False, 0, "0p"]:
        fig.plot(**args_sector)
    else:
        fig.plot(pen=outline, **args_sector)

    # Add colorbar
    if colorbar == True:
        args_cb = {
            "position": Position("BC", anchor="TC", offset=(0, 0.8)),
            "orientation": "horizontal",
            "length": radius_out - radius_out * 0.15,
            "move_text": "label",
        }
        match fill_type:
            case "discrete":
                fig.colorbar(equalsize=0.2, S=f"+x{cb_label}", **args_cb)
            case "min_max":
                fig.colorbar(frame=f"xaf+u{unit}+l{cb_label}", **args_cb)

    # Add labels within the sectors
    fig.text(
        text=text,
        x=middle_sectors,
        y=[0.8] * len(df_sectors),
        fill="white@30",
        pen="0.1p,gray30",
        clearance="+tO",
        font=font,
        no_clip=True,
    )

    # Add frame on top
    if outline not in [None, False, 0, "0p"]:
        pygmt.config(MAP_FRAME_PEN=outline)
        fig.basemap(frame=0)

    fig.show()

    return df_sectors



# %%
# -----------------------------------------------------------------------------
# Examples
# -----------------------------------------------------------------------------
sectors = [50, 10, 8, 12, 15, 13, 42, 5]
annot = ["aaa", "bbb", "ccc", "ddd", "eee", "fff", "ggg", "hhh"]
colors = ["hawaii"]

df_sectors = pie_chart(sectors=sectors)
df_sectors = pie_chart(sectors=sectors, annot=annot, colors=colors)
pie_chart(
    sectors=sectors,
    annot=annot,
    colors=colors,
    fill_type="min_max",
    sector_labels="annot",
)

# -----------------------------------------------------------------------------
sectors = np.array([33, 48, 26, 13, 13, 42, 5])
colors = ["darkred", "lightred", "tomato", "brown", "darkbrown", "pink", "bisque"]

pie_chart(
    sectors=sectors,
    annot=annot[0:-1],
    colors=colors,
    radius_in=True,
    outline="1p,white",
    unit="kg",
)

# -----------------------------------------------------------------------------
colors = ["gold", "brown"]

pie_chart(
    sectors=sectors,
    annot=annot[0:-1],
    colors=colors,
    fill_type="min_max",
    radius_in=True,
    outline="1p,gray",
    cb_label="Mass of object",
    sector_labels="annot",
    unit="kg",
)
