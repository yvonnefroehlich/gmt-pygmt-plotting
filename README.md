# Python Scripts and Jupyter Notebooks using PyGMT

Collection of Python scripts or Jupyter notebooks (supported by JupyterLab) to reproduce some of the geographic maps shown in the publications I am involved. To prepare these maps I am using [_PyGMT_](https://www.pygmt.org/latest/) the Python wrapper for the [_Generic Mapping Tools_ (_GMT_)](https://www.generic-mapping-tools.org/).

_Please note_: Scripts or notebooks are available up on acceptance of the related publication.


## Citation

If you make use of this material, please acknowledge the relating publications in which framework these scripts and notebooks were written:

- [**_Fröhlich Y., Grund M., Ritter J. R. R. (2024)_**](https://doi.org/10.1093/gji/ggae245).
  Lateral and vertical variations of seismic anisotropy in the lithosphere-asthenosphere system underneath Central Europe from long-term splitting measurements.
  *Geophysical Journal International*.
  https://doi.org/10.1093/gji/ggae245.
- [**_Fröhlich Y., Dillah M. I. F., Dorn F., Ritter J. R. R. (2024)_**](https://doi.org/10.5281/zenodo.12658821).
  Investigation of seismic anisotropy in the D'' layer and at the CMB regarding intense magnetic flux regions.
  *18th Symposium of Study of the Earth's Deep Interior*, [proceedings, session 2-04](https://sedi-conference-2024-2675c.ingress-baronn.ewp.live/abstracts/).
  https://doi.org/10.5281/zenodo.12658821.
- [**_Fröhlich Y., Thiyagarajan H., Tölle L. S., Ritter J. R. R., Thomas C. (2024)_**](https://doi.org/10.5281/zenodo.10927349).
  Understanding the influence of seismic mantle structures at the core-mantle boundary on intense magnetic flux regions.
  *84th Annual Meeting of the German Geophysical Society*, [proceedings, session SO-P-07, 181-182](https://dgg2024.dgg-tagung.de/english-home-1/).
  https://doi.org/10.5281/zenodo.10927349.
- [**_Ritter J. R. R., Fröhlich Y., Sanz Alonso Y. & Grund M. (2022)_**](https://doi.org/10.1007/s10950-022-10112-w).
  Short-scale laterally varying SK(K)S shear wave splitting at BFO, Germany – implications for the determination of anisotropic structures.
  *Journal of Seismology*, 26, 1137-1156.
  https://doi.org/10.1007/s10950-022-10112-w. https://doi.org/10.1007/s10950-023-10136-w.


## Content

- **[000_general_stuff](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/000_general_stuff)**: Custom symbols
- **[001_paper_RFSG_2022](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/001_paper_RFSG_2022)**: Maps of [**_Ritter J. R. R., Fröhlich Y., Sanz Alonso Y. & Grund M. (2022)_**](https://doi.org/10.1007/s10950-022-10112-w)
- **[002_paper_FGR_2024](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/002_paper_FGR_2024)**: Maps of [**_Fröhlich Y., Grund M. & Ritter J. R. R. (2024)_**](https://doi.org/10.1093/gji/ggae245)
- **[003_taup](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/003_taup)**: Travel paths of seismological phases through the Earth interior
- **[004_earthquakes_eruptions](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/004_earthquakes_eruptions)**: Maps of selected earthquakes and eruptions between 2021 and present
- **[006_tomographies_databases](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/006_tomographies_databases)**: `shear wave splitting`, `deep anisotropy`, `votemap analysis`, `cluster analysis`
- **[007_magnetic_field](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/007_magnetic_field)**: `gufm1`

![](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/raw/main/_images/github_maps_readme_main.png)


## Requirements

_Please note_: The required versions are given above in the single folders as well as notebooks and scripts

- [PyGMT](https://www.pygmt.org/latest/)
- [GMT](https://www.generic-mapping-tools.org/)
- [Python](https://www.python.org/)
- [Jupyter notebook](https://jupyter.org/) or [JupyterLab](https://jupyter.org/)
- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [ObsPy](https://docs.obspy.org/)
- [pymagglobal](https://sec23.git-pages.gfz-potsdam.de/korte/pymagglobal/)


## Contributing

For bug reports, suggestions, or recommendations feel free to [open an issue](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/issues) or [submit a pull request](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/pulls) directly here on [GitHub](https://github.com/yvonnefroehlich/gmt-pygmt-plotting).


## References

_Please note_: Specific references are given in the single notebooks and scripts

[**_Bird, P. (2003)_**](https://doi.org/10.1029/2001GC000252).
An updated digital model of plate boundaries.
*Geochemistry, Geophysics, Geosystems*, volume 4, issue 3, page 1027.
https://doi.org/10.1029/2001GC000252.

[**_Crameri, F. (2021)_**](http://doi.org/10.5281/zenodo.1243862).
Scientific colour maps. *Zenodo*. http://www.fabiocrameri.ch/colourmaps.php. http://doi.org/10.5281/zenodo.1243862.

[**_Thyng, K. M., Greene, C. A., Hetland, R. D., Zimmerle, H. M. & DiMarco, S. F. (2016)_**](http://dx.doi.org/10.5670/oceanog.2016.66).
True colors of oceanography: Guidelines for effective and accurate colormap selection.
*Oceanography*, volume 29, issue 3, pages 9-13.
http://dx.doi.org/10.5670/oceanog.2016.66.

[**_Tian, D., Uieda, L., Leong, W. J., Fröhlich, Y., Schlitzer, W., Grund, M., Jones, M., Toney, L., Yao, J., Magen, Y., Tong, J-H., Materna, K., Belem, A., Newton, T., Anant, A., Ziebarth, M., Quinn, J. & Wessel, P. (2024)_**](https://doi.org/10.5281/zenodo.10578540).
PyGMT: A Python interface for the Generic Mapping Tools, version v0.12.0.
*Zenodo*. https://doi.org/10.5281/zenodo.11062720 (v0.12.0). https://doi.org/10.5281/zenodo.3781524 (all versions / latest version).

[**_Wessel, P., Smith, W. H. F., Scharroo, R., Luis, J. F. & Wobbe. F. (2013)_**](https://doi.org/10.1002/2013EO450001).
Generic mapping tools: improved version released.
*Eos, Transactions American Geophysical Union*, volume 94, issue 45, pages 409-410.
https://doi.org/10.1002/2013EO450001.

[**_Wessel, P., Luis, J. F., Uieda, L., Scharroo, R., Wobbe, F., Smith, W. H. F. & Tian, D. (2019)_**](https://doi.org/10.1029/2019GC008515).
The Generic Mapping Tools version 6.
*Geochemistry, Geophysics, Geosystems*, volume 20, issue 11, pages 5556-5564.
https://doi.org/10.1029/2019GC008515.

[**_Wessel, P., Luis, J. F., Uieda, L., Scharroo, R., Wobbe, F., Smith, W. H. F., Tian, D., Jones, M. & Esteban, F. (2022)_**](https://doi.org/10.5281/zenodo.6623271).
The Generic Mapping Tools, version 6.4.0.
*Zenodo*. https://doi.org/10.5281/zenodo.6623271.


## Funding

The presented research and YF received support from various sources:

- Scholarship of the [Graduate Funding from the German States](https://www.khys.kit.edu/english/graduate_funding.php)
- [DFG grant RI1133/14-1](https://gepris.dfg.de/gepris/projekt/521545943?language=en) within the [DFG Priority Program 2404 DeepDyn](https://www.geo.lmu.de/deepdyn/en/)
