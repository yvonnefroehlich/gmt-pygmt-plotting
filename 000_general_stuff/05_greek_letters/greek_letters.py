# #############################################################################
# Write Greek letters in GMT
# -----------------------------------------------------------------------------
# History
# - Created: 2025/06/06
# -----------------------------------------------------------------------------
# Versions
# - PyGMT v0.14.2 -> https://www.pygmt.org/v0.14.2/ | https://www.pygmt.org/
# - GMT 6.5.0 -> https://www.generic-mapping-tools.org/
# -----------------------------------------------------------------------------
# Contact
# - Author: Yvonne Fröhlich
# - ORCID: https://orcid.org/0000-0002-8566-0619
# - GitHub: https://github.com/yvonnefroehlich/gmt-pygmt-plotting
# #############################################################################


import pygmt
import string

lower_letters = string.ascii_lowercase
upper_letters = string.ascii_uppercase

fig = pygmt.Figure()
fig.basemap(region=[0, 26, -5, 5], projection= "X15c/4c", frame=0)

x = 0.5
for i_letter in range(len(lower_letters)):

    lower_letter = lower_letters[i_letter]
    fig.text(x=x, y=4, text=f"@~{lower_letter}@~")
    fig.text(x=x, y=2, text=lower_letter)

    upper_letter = upper_letters[i_letter]
    fig.text(x=x, y=-2, text=f"@~{upper_letter}@~")
    fig.text(x=x, y=-4, text=upper_letter)

    x = x + 1

fig.hlines(y=0, pen="0.8p,2_2")

fig_name = "greek_letters"
for ext in ["png"]:
    fig.savefig(fname=f"{fig_name}.{ext}")
fig.show()
print(fig_name)

