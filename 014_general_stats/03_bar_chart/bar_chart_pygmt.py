# #############################################################################
# Python function to create a bar chart in PyGMT
# - vertical, horizontal bars
# - single colors, colormap
# - labels with absolute values, percent
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


import pandas as pd
import numpy as np
import pygmt
from pygmt.params import Position

def bar_chart(
    bars,
    annot=[],
    colors=[],
    fill_type="discret",
    bar_width=0.8,
    orientation="vertical",
    colorbar=True,
    bar_labels="value_percent",
    bar_label_offset=None,
    unit=None,
    cb_label=None,
    axis_label=None,
    round_digits=2,
    outline="1p,black,solid",
    font="5p",

):
    # %%
    # -------------------------------------------------------------------------
    # Input
    # -------------------------------------------------------------------------
    # Required
    # - bars
    # Optional
    # - annot: annotations assigned to the colors and used for the colorbar.
    #   Give always a list of strings. | Default "bar1", ..., "barN"
    # - colors: Fill of the sectors. Give a list with one colormap or with one
    #   or multiple colors. | Default colors based on colormap "batlow"
    # - fill_type: How to setup the coloring. Choose between "discret" or
    #   "continuous". | Default "discret"
    # - bar_width: Set width of the bars. | Default 0.8
    # - orientation: Orientation of the bars. Choose between "horizontal" or
    #   "vertical". | Default "vertical"
    # - colorbar: Add a colorbar | Default True, e.g. colorbar plotted
    # - bar_labels: Write labels in the bars. Choose from "value_percent",
    #   "value", "percent", "annot". | Default "value_percent"
    # - bar_label_offset: Offset of bar label and top of bar. Give offsets in
    #   x- and y-directions as string with the format <xoffset/yoffset>. |
    #   Default f"0c/{max(bars) * 0.0025}c" or f"{max(bars) * 0.0025}c/0c"
    # - unit: Add unit to values of labels, axis, colorbar. | Default no unit
    # - cb_label: Add a label to the colorbar. | Default no label
    # - axis_label: Add label to the x or y axis. | Defualt no label
    # - round_digits: Round values to specific number of digits. | Default 2
    # - outline: Outline of the bars. Give a pen to adjust color, thickness,
    #   and style. | Default "1p,black,solid"
    # - font: Size, style, color of the font used for the bar_labels. |
    #   Default "5p"
    # -------------------------------------------------------------------------
    # Returns
    # -------------------------------------------------------------------------
    # - df_bars: pandas Dataframe with given and calculated data for the bars


    # %%
    # -------------------------------------------------------------------------
    # Check and prepare input
    # -------------------------------------------------------------------------
    # Check annot
    if len(bars) != len(annot) and len(annot) != 0:
        print(
            "The lengths of 'bars' and 'cb_annot' must be identical. " + \
            "Using default colorbar annot 'bar1' ... 'barN'."
        )

    if annot == [] or (len(bars) != len(annot)):
        annot = []
        for i_bar in range(len(bars)):
            annot.append(f"bar {i_bar + 1}")

    # Check colors
    if (len(bars) != len(colors)) and (len(colors) > 1) and fill_type=="discret":
        print(
            "The lengths of 'bars' and 'colors' must be identical " + \
            "for using fill_type=='discret'! Using default colormap 'batlow'."
        )

    if len(colors) == 1:
        cmap = colors
    elif len(colors) > 1:
        cmap = ",".join(colors)
    else:
        cmap = "batlow"
    if (len(bars) != len(colors)) and (len(colors) > 1) and fill_type=="discret":
         cmap = "batlow"

    # Calculate percent for bars
    if isinstance(bars, list):
        bars_array = np.array(bars)
    else:
        bars_array = bars
    bars_sum = sum(bars)
    percents = bars_array / bars_sum * 100

    # Axis and colorbar labels
    if axis_label != None and unit != None:
        axis_label = f"{axis_label} / {unit}"

    if axis_label == None:
        axis_label = " "

    if cb_label == None:
        cb_label = " "

    if unit == None:
        unit = " "
    else:
        unit = f" {unit}"  # Add white space before unit

    # Create pandas Dataframe based on orientation of bars
    xy = np.arange(1, len(bars) + 1, 1)
    xy_offset = max(bars) * 0.0025

    match orientation:
        case "vertical":
            region = [0, len(bars) + 1, 0, np.max(bars) + np.max(bars) * 0.1]
            plot_width = len(bars) + 1
            plot_hight = 6
            frame = ["Wbtr", f"yaf+l{axis_label}"]
            dict_bars = {"x": xy, "y": bars}
            style = "b"
            x_text = xy
            y_text = bars
            justify_text = "BC"
            x_offset = 0
            y_offset = xy_offset
        case "horizontal":
            region = [0, np.max(bars) + np.max(bars) * 0.1, 0, len(bars) + 1]
            plot_width = 6
            plot_hight = - (len(bars) + 1)
            frame = ["lbNr", f"xaf+l{axis_label}"]
            dict_bars = {"x": bars, "y": xy}
            style = "B"
            x_text = bars
            y_text = xy
            justify_text = "ML"
            x_offset = xy_offset
            y_offset = 0

    df_bars = pd.DataFrame(dict_bars, columns=["x", "y"])
    match fill_type:
        case "discret":
            df_bars["z_color"] = xy
        case "min_max":
            df_bars["z_color"] = bars
    df_bars["value"] = bars
    df_bars["percent"] = percents

    # Projection
    projection = f"X{plot_width}c/{plot_hight}c"

    # Create bar labels
    text = []
    if bar_labels != None:

        for i_bar, percent in enumerate(percents):
            match bar_labels:
                case "value_percent":
                    text_temp = f"{bars[i_bar]}{unit} | {round(percent, round_digits)} %"
                case "value":
                    text_temp = f"{bars[i_bar]}{unit}"
                case "percent":
                    text_temp = f"{round(percent, round_digits)} %"
                case "annot":
                    text_temp = annot[i_bar]
            text.append(text_temp)

    # Default of bar label offset
    if bar_label_offset == None:
        bar_label_offset = f"{x_offset}c/{y_offset}c"


    # %%
    # -------------------------------------------------------------------------
    # Create plot
    # -------------------------------------------------------------------------
    fig = pygmt.Figure()
    fig.basemap(region=region, projection=projection, frame=0)

    match fill_type:
        case "discret":
            pygmt.makecpt(
                cmap=cmap,
                series=[1, len(bars), 1],
                color_model="+c" + ",".join(annot),
            )
        case "min_max":
            pygmt.makecpt(cmap=cmap, series=[min(bars), max(bars)])

    # Plot bars
    args_bar = {"data": df_bars, "style": f"{style}{bar_width}c", "cmap": True}
    if outline in [None, False, 0, "0p"]:
        fig.plot(**args_bar)
    else:
        fig.plot(pen=outline, **args_bar)

    # Add colorbar
    if colorbar == True:
        args_cb = {
            "position": Position("BC", anchor="TC", offset=(0, 0.6)),
            "orientation": "horizontal",
            "length": plot_width - plot_width * 0.15,
            "move_text": "label",
        }
        match fill_type:
            case "discret":
                fig.colorbar(equalsize=0.2, S=f"+x{cb_label}", **args_cb)
            case "min_max":
                fig.colorbar(frame=f"xaf+u{unit}+l{cb_label}", **args_cb)

    # Add labels on top of the bars
    fig.text(
        text=text,
        x=x_text,
        y=y_text,
        offset=bar_label_offset,
        fill="white@30",
        pen="0.1p,gray30",
        clearance="+tO",
        justify=justify_text,
        font=font,
        no_clip=True,
    )

    # Add frame on top
    fig.basemap(frame=frame)

    fig.show()

    return df_bars



# %%
# -----------------------------------------------------------------------------
# Examples
# -----------------------------------------------------------------------------
bars = [50, 10, 8, 12, 15, 13, 42, 5]
annot = ["aaa", "bbb", "ccc", "ddd", "eee", "fff", "ggg", "hhh"]
colors = ["hawaii"]

df_bars = bar_chart(bars=bars)
df_bars = bar_chart(bars=bars, annot=annot, colors=colors)
df_bars = bar_chart(
    bars=bars,
    annot=annot,
    colors=colors,
    fill_type="min_max",
    bar_labels="annot",
)

# -----------------------------------------------------------------------------
bars = np.array([33, 48, 26, 13, 13, 42, 5])
colors = ["darkred", "lightred", "tomato", "brown", "darkbrown", "pink", "bisque"]

bar_chart(
    bars=bars,
    annot=annot[0:-1],
    colors=colors,
    unit="kg",
    bar_labels="percent",
    cb_label="Object",
    axis_label="Mass of object",
    round_digits=0,
    outline="1p,gray80",
)

# -----------------------------------------------------------------------------
colors = ["gold", "brown"]
bar_chart(
    bars=bars,
    annot=annot[0:-1],
    colors=colors,
    fill_type="min_max",
    outline=None,
    orientation="horizontal",
    bar_labels="annot",
    cb_label="Mass of object",
    unit="kg",
)
