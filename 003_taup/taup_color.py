# #############################################################################
# This functions
# - Assigns colors to the seismological phases
# - Outputs a dictionary
# - Is related to the function taup_path_curve.py
# Feel free to adjust and extend the dictionary for your needs (:
# -----------------------------------------------------------------------------
# Related to
# - Fröhlich Y., Grund M. & Ritter J. R. R. (2024).
#   Lateral and vertical variations of seismic anisotropy in the lithosphere-
#   asthenosphere system underneath Central Europe from long-term splitting
#   measurements. Geophysical Journal International, 239(1), 112-135.
#   https://doi.org/10.1093/gji/ggae245.
# - Fröhlich Y. (2025). Shear wave splitting analysis of long-term data:
#   Anisotropy studies in the Upper Rhine Graben area, Central Europe.
#   Dissertation, Karlsruhe Institute of Technology, Geophysical Institute.
#   https://doi.org/10.5445/IR/1000183786.
# -----------------------------------------------------------------------------
# History
# - Created: 2024/05/07
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


def taup_color():

    phase_colors = {
        "P": "0/0/128",  # GMT navyblue
        "PcP": "0/191/255",  # GMT deepskyblue
        "S": "0/0/255",  # GMT blue
        "ScS": "0/255/255",  # GMT cyan
        "PKS": "238/238/0",  # GMT yellow2
        "PKKS": "160/32/240",  # GMT purple
        "SKS": "205/0/0",  # GMT red3
        "SKKS": "238/118/0",  # GMT darkorange2
        "PKKP": "139/125/107",  # GMT bisque4
        "PKPPKP": "188/143/143",  # GMT rosybrown
        "PKIKS": "127/255/0",  # GMT chartreuse1
        "PKJKS": "50/205/50",  # GMT limegreen
        "SKIKS": "34/139/34",  # GMT forestgreen
        "SKJKS": "0/100/0",  # GMT darkgreen
        # Deth phases for SKS and SKKS phases
        "pSKS": "139/0/0",  # GMT darkred
        "sSKS": "255/128/128",  # GMT lightred
        "pSKKS": "255/69/0",  # GMT orangered
        "sSKKS": "255/192/128",  # GMT lightorange
    }

    # Depth phases for PcP and ScS phases
    # phase_colors = {
    #     "P": "0/255/255",  # GMT cyan
    #     "PcP": "0/191/255",  # GMT deepskyblue
    #     "pPcP": "0/0/255",  # GMT blue
    #     "sPcP": "0/0/139",  # GMT darkblue
    #     "S": "255/0/255",  # GMT magenta
    #     "ScS": "255/128/128",  # GMT lightred
    #     "pScS": "255/0/0",  # GMT red
    #     "sScS": "139/0/0",  # GMT darkred
    # }

    return phase_colors
