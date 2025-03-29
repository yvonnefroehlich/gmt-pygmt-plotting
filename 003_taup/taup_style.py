# #############################################################################
# This functions
# - Assigns line styles to the seismological phases
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
# - Created: 2025/03/29
# #############################################################################


def taup_style():

    phase_styles = {
        "P": "solid",
        "PcP": "dashed",
        "S": "solid",
        "ScS": "dashed",
        "PKS": "solid",
        "PKKS": "solid",
        "SKS": "solid",
        "SKKS": "solid",
        "PKKP": "solid",
        "PKPPKP": "solid",
        "PKIKS": "-.",
        "PKJKS": "-.",
        "SKIKS": "-.",
        "SKJKS": "-.",
        # Deth phases for SKS and SKKS phases
        "pSKS": "4_2",
        "sSKS": "4_2",
        "pSKKS": "4_2",
        "sSKKS": "4_2",
    }

    # Depth phases for PcP and ScS phases
    # phase_styles = {
    #     "P": "solid",
    #     "PcP": "solid",
    #     "pPcP": "solid",
    #     "sPcP": "solid",
    #     "S": "solid",
    #     "ScS": "solid",
    #     "pScS": "solid",
    #     "sScS": "solid",
    # }

    return phase_styles
