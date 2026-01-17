# #############################################################################
# Python function to create a pie chart in PyGMT
# - sectors, ring sectors
# - single colors, colormap
# - labels with absolute values, percentage
#
# >>> Note <<<
# >>> Numbers and trends are difficult to read visually from pie charts.
# >>> If possible, test and consider using another plot type, e.g., a bar chart.
# -----------------------------------------------------------------------------
# History
# - Created: 2025/10/16
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

# -----------------------------------------------------------------------------
# Function to create a pie chart
# -----------------------------------------------------------------------------

def pie_chart(
    sectors,
    labels=[],
    colors=[],
    radius=10,
    ring=False,
    colorbar=True,  # True | False
    sector_labels="value_percent",  # "value_percent" | "value" | "percent" | None
    unit="",
    cb_label="",
    round_digits=2,
    color_outline="gray20",
):

    # Check labels
    if len(sectors) != len(labels) and len(labels) != 0:
        print("The length of 'sectors' and 'cb_annot' must be identical! " + \
              "Using default colorbar annotations 'sector1' ... 'sectorN'.")

    if labels == [] or (len(sectors) != len(labels)):
        labels = []
        for i_sector in range(len(sectors)):
            labels.append(f"sector {i_sector + 1}")

    # Check colors
    if (len(sectors) != len(colors)) and (len(colors) > 1):
        print("The length of sectors and colors must be identical! " + \
              "Using default colormap 'batlow'.")

    if len(colors) == 1:
        cmap = colors
    elif len(sectors) == len(colors):
        cmap = ",".join(colors)
    else:
        cmap = "batlow"

    # Set inner radius of sectors
    if ring == False:
        radius_inner = 0
    elif ring == True:
        radius_inner = radius - radius * 0.5
    else:
        radius_inner = ring

    # Caclulate percent for sectors
    if isinstance(sectors, list):
        sectors_array = np.array(sectors)
    else:
        sectors_array = sectors
    sectors_sum = sum(sectors)
    percents = sectors_array / sectors_sum * 100

# -----------------------------------------------------------------------------
    fig = pygmt.Figure()
    pygmt.config(FORMAT_GEO_MAP="+D")
    fig.basemap(region=[0, 360, 0, 1], projection=f"P{radius}c", frame=0)

    pygmt.makecpt(
        cmap=cmap,
        series=[0, len(sectors) - 1, 1],
        color_model="+c" + ",".join(labels),
    )

    # Plot sectors
    angel_start = 0
    for i_sector, percent in enumerate(percents):
        angel_end = angel_start + percent * 3.6  # Convert percent to degrees

        fig.plot(
            x=0,
            y=0,
            style=f"w{radius}c/{angel_start}/{angel_end}+i{radius_inner}c",
            pen=f"1p,{color_outline}",
            fill="+z",
            zvalue=i_sector,
            cmap=True,
        )

        angel_start = angel_end

    if colorbar == True:
        fig.colorbar(equalsize=0.2, S=f"+x{cb_label}", position="+e0c+ml")

    # Add labels on top of sectors
    if sector_labels != None:

        angel_start = 0
        for i_sector, percent in enumerate(percents):
            angel_end = angel_start + percent * 3.6

            match sector_labels:
                case "value_percent":
                    text = f"{sectors[i_sector]} {unit} | {round(percent, round_digits)} %"
                case "value":
                    text = f"{sectors[i_sector]} {unit}"
                case "percent":
                    text = f"{round(percent, round_digits)} %"
            if colorbar == False:
                text = labels[i_sector]

            fig.text(
                text=text,
                x=angel_start + percent * 3.6 / 2,
                y=0.8,
                fill="white@30",
                pen="0.1p,gray30",
                clearance="+tO",
                no_clip=True,
            )

            angel_start = angel_end

    fig.show()


# %%
# -----------------------------------------------------------------------------
# Examples
# -----------------------------------------------------------------------------

sectors = [50, 10, 8, 12, 15, 13, 42, 5]

pie_chart(sectors=sectors)

labels = ["aaa", "bbb", "ccc", "ddd", "eee", "fff", "ggg", "hhh"]

pie_chart(sectors=sectors, labels=labels)

colors = ["hawaii"]

pie_chart(sectors=sectors, labels=labels, colors=colors)
pie_chart(sectors=sectors, labels=labels, colors=colors, ring=True, unit="kg")

sectors = np.array([33, 48, 26, 13, 13, 42, 5])
colors = ["darkred", "lightred", "tomato", "brown", "darkbrown", "pink", "bisque"]

pie_chart(
    sectors=sectors,
    labels=labels,
    colors=colors,
    ring=8,
    unit="kg",
    sector_labels="value",
)
pie_chart(
    sectors=sectors,
    labels=labels,
    colors=colors,
    ring=8,
    unit="kg",
    sector_labels="percent",
    cb_label="Letters",
    round_digits=0,
)
pie_chart(sectors=sectors, labels=labels, colors=colors, ring=True, colorbar=False)
