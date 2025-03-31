# #############################################################################
# This functions
# - Assigns symbols to the seismological phases
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
# - Created: 2025/03/31
# #############################################################################


def taup_symbol():

    phase_symbols = {
        "P": "s",
        "PcP": "c",
        "S": "c",
        "ScS": "c",
        "PKS": "c",
        "PKKS": "c",
        "SKS": "c",
        "SKKS": "c",
        "PKKP": "c",
        "PKPPKP": "c",
        "PKIKS": "c",
        "PKJKS": "c",
        "SKIKS": "c",
        "SKJKS": "c",
        # Deth phases for SKS and SKKS phases
        "pSKS": "c",
        "sSKS": "c",
        "pSKKS": "c",
        "sSKKS": "c",
    }

    # Depth phases for PcP and ScS phases
    # phase_symbols = {
    #     "P": "c",
    #     "PcP": "c",
    #     "pPcP": "c",
    #     "sPcP": "c",
    #     "S": "c",
    #     "ScS": "c",
    #     "pScS": "c",
    #     "sScS": "c",
    # }

    return phase_symbols