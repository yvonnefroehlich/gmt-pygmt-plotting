# #############################################################################
# Shear wave splitting database
#
# Splitting parameters of splits as orientated and color-coded (fast
# polarization direction phi) length-scaled (delay time dt) bars
#
# Wüstefeld A., Bokelmann G., Barruol G., Montagner J.-P., (2009). Identifying
# global seismic anisotropy patterns by correlating shear-wave splitting and
# surface-wave data. Physics of the Earth and Planetary Interiors, 176(3–4),
# 198-212, https://doi.org/10.1016/j.pepi.2009.05.006, last access 2024/09/08.
#
# Shear wave splitting data is available at https://ds.iris.edu/ds/products/sws-dbs/
# - SWS-DB: The Géosciences Montpellier SplitLab Shear-Wave Splitting Database
#   https://ds.iris.edu/ds/products/sws-db/, last access 2024/09/08
#   https://doi.org/10.18715/sks_splitting_database
#   https://splitting.gm.univ-montp2.fr/
# - SWS-DB-MST: The Missouri S&T western and central United States shear-wave splitting database
#   https://ds.iris.edu/ds/products/sws-db-mst/, last access 2024/09/08
# -----------------------------------------------------------------------------
# History
# - Created: 2024/04/29
# - Updated: 2025/02/15
# - Updated: 2025/12/27 - Update SWS database
# - Updated: 2025/12/27 - Add orthographic map, studies cumulative map
# - Updated: 2025/12/28 - Add year map, carthesian histogram year
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.17.0 -> https://www.pygmt.org/
# - GMT 6.4.0 - 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pandas as pd
import pygmt as gmt


# %%
# -----------------------------------------------------------------------------
# General stuff
# -----------------------------------------------------------------------------
# Paths
path_in = "01_in_data"
path_out = "02_out_figs"

file_pb = "plate_boundaries_Bird_2003.txt"

# Colors
color_hl = "255/90/0"  # highlight
color_pb = "216.750/82.875/24.990"  # plate boundaries
color_land = "gray95"
color_water = "white"
color_sl = "gray50"  # shorelines
fill_null_max = "white"
pen_null = "0.4p,gray10"



# %%
# -----------------------------------------------------------------------------
# Load and preparare SWSM data
# -----------------------------------------------------------------------------
file_swsm = "sws_db_swsm_barruol_et_al_20251227_COR_GMT_phiGMT4j"
df_swsm_raw = pd.read_csv(f"{path_in}/{file_swsm}.txt", delimiter=",")

file_ref = "sws_db_swsm_barruol_et_al_20251227_ref"
df_swsm_ref = pd.read_csv(f"{path_in}/{file_ref}.txt", delimiter="|")

# %%
# -----------------------------------------------------------------------------
"""
# Add column for publication year of study
# Takes some time ...
years = [1] * len(df_swsm_raw)

for df_swsm_raw_ind in df_swsm_raw.index:

    df_swsm_raw_temp = df_swsm_raw[df_swsm_raw.index == df_swsm_raw_ind]
    ref_id_temp = df_swsm_raw_temp["ref_id"]
    ref_id_temp = ref_id_temp[df_swsm_raw_ind]

    df_swsm_ref_temp = df_swsm_ref[df_swsm_ref["id"] == ref_id_temp]
    df_sws_ref_temp_ind = df_swsm_ref_temp.index[0]
    year = df_swsm_ref_temp["Year"][df_sws_ref_temp_ind]
    years[df_swsm_raw_ind] = int(year)

df_swsm_raw["year"] = years

df_swsm_raw.to_csv(f"{path_in}/{file_swsm}_year.txt", index=False)
"""

#%%
df_swsm_raw = pd.read_csv(f"{path_in}/{file_swsm}_year.txt", delimiter=",")
df_swsm_raw.sort_values(by=["year"])

# -----------------------------------------------------------------------------
# Creat subsets
df_swsm_split = df_swsm_raw[df_swsm_raw.obs == "Split"]
df_swsm_null = df_swsm_raw[df_swsm_raw.obs == "Null"]

df_null_circle = df_swsm_null[["lon", "lat"]]
columns_bar = ["lon", "lat", "phi_sl", "phi_gmt", "dt", "thick", "ref_id"]
df_split_bar = df_swsm_split[columns_bar]
incols_j = "3,4+s0.05,5+s0.006"
ref_ids_unique = list(set(df_split_bar["ref_id"]))



# %%
# -----------------------------------------------------------------------------
# Make geographic map - fast polarization direction
# -----------------------------------------------------------------------------
fig = gmt.Figure()

# Set up basic map
fig.basemap(region="d", projection="N11c", frame=0)

# Plot land masses, shorelines and political borders
fig.coast(land=color_land, shorelines=f"1/0.05p,{color_sl}")

# -----------------------------------------------------------------------------
# Plot plate boundaries
fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.2p,{color_pb}")

# -----------------------------------------------------------------------------
# Plot splitting parameter of splits as orientated and color-coded length-scaled
# bars according to phi and dt; nulls as white-filled black-outlined circles

# Make colormap for phi
gmt.makecpt(cmap="phase", series=[-90, 90], cyclic=True)

# Plot splits
fig.plot(data=df_split_bar, incols=f"0,1,2,{incols_j}", style="j", cmap=True)

# Plot nulls
fig.plot(data=df_null_circle, style="c0.05c", fill=fill_null_max, pen=pen_null)

# Add colorbar for phi colormap
cb_xlabel = "Complete Shear Wave Splitting Database - splits"
cb_ylabel = "@~f@~@-a@- / N@.E"
with gmt.config(FONT_LABEL="10p"):
    fig.colorbar(cmap=True, frame=[f"xa30f10+l{cb_xlabel}", f"y+l{cb_ylabel}"])

# -----------------------------------------------------------------------------
# Add frame on top
with gmt.config(FONT="7p"):
    fig.basemap(frame=["WSnE", "xa90f30", "ya30f15"])

# Show and save figure
fig.show()

fig_name = f"{path_out}/db_sws_splitting_parameters"
for ext in ["png"]:  # , "pdf", "eps"]:
    fig.savefig(fname=f"{fig_name}.{ext}")

print(fig_name)



# %%
# -----------------------------------------------------------------------------
# Make geographic map - year
# -----------------------------------------------------------------------------
fig = gmt.Figure()

fig.basemap(region="d", projection="N11c", frame=0)
fig.coast(land=color_land, water=color_water, shorelines=f"1/0.05p,{color_sl}")
fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.2p,{color_pb}")

gmt.makecpt(
    cmap="batlow",
    series=[df_swsm_raw["year"].min(), df_swsm_raw["year"].max(), 1],
    reverse=True,
)
fig.plot(data=df_swsm_raw[["lon", "lat", "year"]], style="c0.02c", cmap=True)
cb_xlabel = "Complete Shear Wave Splitting Database"
with gmt.config(FONT="10p"):
    fig.colorbar(cmap=True, frame=f"xa5f1+l{cb_xlabel}")

with gmt.config(FONT="7p"):
    fig.basemap(frame=["WSnE", "xa90f30", "ya30f15"])

fig.show()
fig_name = f"{path_out}/db_sws_sp_year"
for ext in ["png"]:  # , "pdf", "eps"]:
    fig.savefig(fname=f"{fig_name}.{ext}")
print(fig_name)



# %%
# -----------------------------------------------------------------------------
# Carthesian Histogram - year
# -----------------------------------------------------------------------------
fig = gmt.Figure()

fig.histogram(
    data=df_swsm_raw["year"],
    region=[
        df_swsm_raw["year"].min(),
        df_swsm_raw["year"].max() + 1,
        0,
        len(df_swsm_raw) + 7000,
    ],
    frame=["xa5f1+lyear", "yaf+lcounts"],
    series=1,
    fill="gray90",
    pen="0.5p,gray70",
    histtype=0,
    cumulative=True,
    annotate="+o3p+r+f8.5p,gray20",
)

fig.show()



# %%
# -----------------------------------------------------------------------------
# Make geographic maps - studies cumulative
# -----------------------------------------------------------------------------
for ref_id in ref_ids_unique:
    if ref_id > -1:

        fig = gmt.Figure()
        fig.basemap(region="d", projection="N11c", frame=0)

        fig.coast(land=color_land, shorelines=f"1/0.05p,{color_sl}")
        fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.2p,{color_pb}")

        if ref_id > 0:
            fig.plot(
                data=df_split_bar[df_split_bar["ref_id"] < ref_id],
                incols=f"0,1,{incols_j}",
                style="j",
                fill="gray50",
            )
        gmt.makecpt(cmap="phase", series=[-90, 90], cyclic=True)
        fig.plot(
            data=df_split_bar[df_split_bar["ref_id"] == ref_id],
            incols=f"0,1,2,{incols_j}",
            # incols=f"0,1,{incols_j}",
            style="j",
            cmap=True,
            # fill=color_hl,
        )

        df_swsm_ref_temp =  df_swsm_ref[df_swsm_ref["id"] == ref_id]
        index = df_swsm_ref_temp.index[0]
        tag = df_swsm_ref_temp['Tag'][index]
        tag_split = tag.split("_")
        tag_ay = tag_split[0]
        if len(tag_split) > 1:  # Without study area
            tag_ay = f"{tag_split[0]}{tag_split[len(tag_split) - 1]}"
        year = df_swsm_ref_temp["Year"][index]
        authors = df_swsm_ref_temp["Authors"][index]
        authors_split = authors.split(",")
        authors_three = ",".join(authors_split[0:6])
        if len(authors_split) > 6:  # Display only the first three authors
            authors_three = f"{authors_three}, et al."
        N_splits = len(df_split_bar[df_split_bar["ref_id"] == ref_id])
        cb_xlabel = f"{authors_three} ({year}) - {N_splits} splits"
        cb_ylabel = "@~f@~@-a@- / N@.E"
        # fig.text(
        #     text=cb_xlabel,
        #     position="TC",
        #     justify="BC",
        #     offset="0c/0.3c",
        #     font=f"8p,{color_hl}",
        #     no_clip=True,
        # )
        with gmt.config(FONT_LABEL="10p"):
            fig.colorbar(
                cmap=True,
                frame=[f"xa30f10+l{cb_xlabel}", f"y+l{cb_ylabel}"],
                position="jBC+o0c/-1.4c+jMC+w8c+h+ml",
            )

        with gmt.config(FONT="7p"):
            fig.basemap(frame=["WSnE", "xa90f30", "ya30f15"])

        fig.show()
        fig_name = f"{path_out}/ref_id/db_sws_sp_refid{ref_id}_{tag_ay}"
        for ext in ["png"]:  # , "pdf", "eps"]:
            fig.savefig(fname=f"{fig_name}.{ext}")
        print(fig_name)



# %%
# -----------------------------------------------------------------------------
# Create maps with orthographic projection for GIFs
# -----------------------------------------------------------------------------
for cmap in ["romaO", "phase"]:

    for lon0 in range(0, 360, 10):

        fig = gmt.Figure()
        gmt.config(MAP_GRID_PEN_PRIMARY="0.01p,gray70")

        fig.basemap(region="d", projection=f"G{lon0}/15/10c", frame=0)
        fig.coast(land=color_land, water=color_water, shorelines=f"1/0.05p,{color_sl}")
        fig.plot(data=f"{path_in}/{file_pb}", pen=f"0.4p,{color_pb}")

        gmt.makecpt(cmap=cmap, series=[-90, 90], cyclic=True)
        fig.plot(data=df_split_bar, incols="0,1,2", style="c0.04c", cmap=True)
        cb_xlabel = "Complete Shear Wave Splitting Database - splits"
        cb_ylabel = "@~f@~@-a@- / N@.E"
        fig.colorbar(
            cmap=True,
            position="jBC+o0c/-0.9c+jMC+w8c+h+ml",
            frame=[f"xa30f10+l{cb_xlabel}", f"y+l{cb_ylabel}"],
        )

        fig.basemap(frame="g10")

        fig.show()
        fig_name = f"{path_out}/gif/circle_{cmap}/db_sws_sp_lon{lon0}deg_circle_{cmap}"
        # for ext in ["png"]:  # , "pdf", "eps"]:
        #     fig.savefig(fname=f"{fig_name}.{ext}")
        print(fig_name)
