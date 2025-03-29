# #############################################################################
# This functions
# - Assigns lines to the seismological phases
# - Outputs a dictionary
# - Is related to the function taup_path_curve.py
# Feel free to adjust and extend the dictionary for your needs (:
# -----------------------------------------------------------------------------
# Author: Yvonne Fröhlich
# ORCID: https://orcid.org/0000-0002-8566-0619
# GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# -----------------------------------------------------------------------------
# Related to:
#   Fröhlich Y., Grund M. & Ritter J. R. R. (2024).
#   Lateral and vertical variations of seismic anisotropy in the lithosphere-
#   asthenosphere system underneath Central Europe from long-term splitting
#   measurements. Geophysical Journal International, 239(1), 112-135.
#   https://doi.org/10.1093/gji/ggae245.
# -----------------------------------------------------------------------------
# - Created: 2025/03729
# #############################################################################


def taup_lines():

    phase_lines = {
        "P": "solid",  # GMT navyblue
        "PcP": "solid",  # GMT deepskyblue
        "S": "solid",  # GMT blue
        "ScS": "solid",  # GMT cyan
        "PKS": "solid",  # GMT yellow2
        "PKKS": "solid",  # GMT purple
        "SKS": "solid",  # GMT red3
        "SKKS": "solid",  # GMT darkorange2
        "PKKP": "solid",  # GMT bisque4
        "PKPPKP": "solid",  # GMT rosybrown
        "PKIKS": "solid",  # GMT chartreuse1
        "PKJKS": "solid",  # GMT limegreen
        "SKIKS": "solid",  # GMT forestgreen
        "SKJKS": "solid",  # GMT darkgreen
        # Deth phases for SKS and SKKS phases
        "pSKS": "solid",  # GMT darkred
        "sSKS": "solid",  # GMT lightred
        "pSKKS": "solid",  # GMT orangered
        "sSKKS": "solid",  # GMT lightorange
    }

    # Depth phases for PcP and ScS phases
    # phase_lines = {
    #     "P": "solid",  # GMT cyan
    #     "PcP": "solid",  # GMT deepskyblue
    #     "pPcP": "solid",  # GMT blue
    #     "sPcP": "solid",  # GMT darkblue
    #     "S": "solid",  # GMT magenta
    #     "ScS": "solid",  # GMT lightred
    #     "pScS": "solid",  # GMT red
    #     "sScS": "solid",  # GMT darkred
    # }

    return phase_lines
