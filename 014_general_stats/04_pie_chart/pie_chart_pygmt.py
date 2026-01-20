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
import pygmt
from pygmt.params import Position

def pie_chart(
    sectors,
    annot=[],
    colors=[],
    radius_out=10,
    radius_in=0,
    colorbar=True,
    sector_labels="value_percent",
    unit="",
    cb_label="",
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
    # - annot: annotations assigned to the colors and used for the colorbar.
    #   Give always a list of strings. | Default "sector1", ..., "sectorN"
    # - colors: Fill of the sectors. Give a colormap or a list of
    #   colors. | Default colors based on colormap "batlow"
    # - radius_out: Set size of plot. Give outer radius | Default 10
    # - radius_in: Create ring sectors. Give inner radius | Default 0
    # - colorbar: Add a colorbar | Default True
    # - sector_labels: Write labels in the sectors. Choose from "value_percent",
    #   "value", "percent", None. | Default "value_percent"
    # - unit: Add unit to values. | Default no unit
    # - cb_label: Add a label to the colorbar. | Default no label
    # - round_digits: Round values to specific number of digits. | Default 2
    # - outline: Outline of the sectors. Give a disered pen to adjust color,
    #   thickness and style. | Default "1p,black,solid"
    # - font: Size, style, color of the font used for the sector_labels. |
    #   Default "10p"


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
    if (len(sectors) != len(colors)) and (len(colors) > 1):
        print(
            "The lengths of sectors and colors must be identical! " + \
            "Using default colormap 'batlow'."
        )

    if len(colors) == 1:
        cmap = colors
    elif len(sectors) == len(colors):
        cmap = ",".join(colors)
    else:
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

    # Add white space before unit
    if unit != "":
        unit = f" {unit}"


    # %%
    # -------------------------------------------------------------------------
    # Create plot
    # -------------------------------------------------------------------------
    fig = pygmt.Figure()
    pygmt.config(FORMAT_GEO_MAP="+D")
    fig.basemap(region=[0, 360, 0, 1], projection=f"P{radius_out}c", frame="+n")

    pygmt.makecpt(
        cmap=cmap,
        series=[0, len(sectors) - 1, 1],
        color_model="+c" + ",".join(annot),
    )

    # Plot sectors
    angel_start = 0
    for i_sector, percent in enumerate(percents):
        angel_end = angel_start + percent * 3.6  # Convert percent to degrees

        args_sector = {
            "x": 0,
            "y": 0,
            "style": f"w{radius_out}c/{angel_start}/{angel_end}+i{radius_in}c",
            "fill": "+z",
            "zvalue": i_sector,
            "cmap": True,
        }
        if outline in [None, False, 0, "0p"]:
            fig.plot(**args_sector)
        else:
            fig.plot(pen=outline, **args_sector)

        angel_start = angel_end

    if colorbar == True:
        fig.colorbar(
            position=Position("BC", anchor="TC", offset=(0, 0.5)),
            orientation="horizontal",
            length=radius_out - radius_out * 0.15,
            equalsize=0.2,
            S=f"+x{cb_label}",
            move_text="label",
        )

    # Add labels within the sectors
    if sector_labels != None:

        angel_start = 0
        for i_sector, percent in enumerate(percents):
            angel_end = angel_start + percent * 3.6

            match sector_labels:
                case "value_percent":
                    text = f"{sectors[i_sector]}{unit} | {round(percent, round_digits)} %"
                case "value":
                    text = f"{sectors[i_sector]}{unit}"
                case "percent":
                    text = f"{round(percent, round_digits)} %"
            if colorbar == False:
                text = annot[i_sector]

            fig.text(
                text=text,
                x=angel_start + percent * 3.6 / 2,
                y=0.8,
                fill="white@30",
                pen="0.1p,gray30",
                clearance="+tO",
                font=font,
                no_clip=True,
            )

            angel_start = angel_end

    # Add frame on top
    if outline not in [None, False, 0, "0p"]:
        pygmt.config(MAP_FRAME_PEN=outline)
        fig.basemap(frame=0)

    fig.show()



# %%
# -----------------------------------------------------------------------------
# Examples
# -----------------------------------------------------------------------------
sectors = [50, 10, 8, 12, 15, 13, 42, 5]

pie_chart(sectors=sectors)

# -----------------------------------------------------------------------------
annot = ["aaa", "bbb", "ccc", "ddd", "eee", "fff", "ggg", "hhh"]

pie_chart(sectors=sectors, annot=annot)

# -----------------------------------------------------------------------------
colors = ["hawaii"]

pie_chart(sectors=sectors, annot=annot, colors=colors)
pie_chart(sectors=sectors, annot=annot, colors=colors, radius_in=True, unit="kg")

# -----------------------------------------------------------------------------
sectors = np.array([33, 48, 26, 13, 13, 42, 5])
colors = ["darkred", "lightred", "tomato", "brown", "darkbrown", "pink", "bisque"]

pie_chart(
    sectors=sectors,
    annot=annot,
    colors=colors,
    radius_in=8,
    unit="kg",
    sector_labels="value",
)
pie_chart(
    sectors=sectors,
    annot=annot[0:-1],
    colors=colors,
    radius_in=8,
    unit="kg",
    sector_labels="percent",
    cb_label="Letters",
    round_digits=0,
    outline="1p,white",
)
pie_chart(
    sectors=sectors,
    annot=annot[0:-1],
    colors=colors,
    radius_in=True,
    colorbar=False,
    outline=None,
)
