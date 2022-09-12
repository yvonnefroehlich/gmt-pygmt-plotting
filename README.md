# Python Scripts or Jupyter Notebooks using PyGMT

Collection of Python scripts or Jupyter Notebooks (also supported by Jupyter Lab) to reproduce some of the geographic maps shown in the publications I am involved. To prepare these maps I am using [_PyGMT_](https://www.pygmt.org/latest/) the _Python_ wrapper for the [_Generic Mapping Tools_ (_GMT_)](https://www.generic-mapping-tools.org/).

_Please note_: The scripts or notebooks are available upon acceptance of the related publication.


## Citation

If you make use of this material, please acknowledge the relating publications in which framework these scripts or notebooks were written:

- **_Fröhlich, Yvonne, Grund, Michael & Ritter, Joachim R. R. (202X)_**. Laterally and vertically varying seismic anisotropy in the lithosphere-asthenosphere system revealed from SK(K)S splitting at neighboring sites in the Upper Rhine Graben area, Central Europe. in preparation for *Geophysical Journal International*.
- **_Ritter, Joachim R. R., Fröhlich, Yvonne, Sanz Alonso, Yasmin & Grund, Michael (2022)_**. Short-scale laterally varying SK(K)S shear wave splitting at BFO, Germany – implications for the determination of anisotropic structures. accepted by *Journal of Seismology*. DOI: 10.1007/s10950-022-10112-w.


## Content

### **[001_paper_RFSG_JoS_2022](https://github.com/yvonnefroehlich/GMT_PyGMT_plotting/tree/main/001_paper_RFSG_JoS_2022)**

_Related publication_: Ritter, J. R. R., Fröhlich, Y., Sanz Alonso, Y. & Grund, M. (2022)\
_Required versions_: PyGMT v0.3.0, GMT 6.1.1 (Figure_1); PyGMT v0.7.0, GMT 6.4.0 (Figure_S4)

- [Figure_1](https://github.com/michaelgrund/GMT-plotting/tree/main/010_paper_RFSG2022): Piercing points in the upper mantle related to shear wave splitting measurements (SWSMs) at the Black Forest Observatory (BFO), see [GMT-plotting](https://github.com/michaelgrund/GMT-plotting) by [Michael Grund](https://github.com/michaelgrund)
- [Figure_S4](https://github.com/yvonnefroehlich/GMT_PyGMT_plotting/tree/main/001_paper_RFSG_JoS_2022/Figure_S4): Piercing points and SKS-SKKS pairs in the lowermost mantle related to SWSMs at BFO

![github_map_figures4readme_BFO](https://user-images.githubusercontent.com/94163266/188328824-d53c1620-fb27-4d9f-9c3f-9e73921c2832.png)

### **[002_paper_FGR_GJI_2022](https://github.com/yvonnefroehlich/GMT_PyGMT_plotting/tree/main/002_paper_FGR_GJI_2022)**

_Related publication_: Fröhlich, Y., Grund, M. & Ritter, J. R. R. (202X)\
_Required versions_: PyGMT v0.y.z, GMT 6.4.z

- [Figure_1](https://github.com/yvonnefroehlich/GMT_PyGMT_plotting/tree/main/002_paper_FGR_GJI_2022/Figure_1): Seismological recording stations in the Upper Rhine Graben (URG) area and epicenter distribution of the used teleseismic earthquakes
- [Figure_X](https://github.com/yvonnefroehlich/GMT_PyGMT_plotting/tree/main/002_paper_FGR_GJI_2022/Figure_X): Piercing points in the upper mantle related to shear wave splitting measurements (SWSM) at seismological recording stations in the URG area

<!---
### **[003_XXX]()**

_Related to_: XXX\
_Required versions_: PyGMT vx.y.z, GMT 6.y.z

- [Figure_X](): XXX
-->

<!---
FIGURE
-->


## Requirements

_Please note_: The required versions are given in the Content section.

- [PyGMT](https://www.pygmt.org/latest/), [GMT](https://www.generic-mapping-tools.org/)
- [Python](https://www.python.org/), [NumPy](https://numpy.org/) <!---, [Pandas]()-->
- [Jupyter Notebook](https://jupyter.org/) or [Jupyter Lab](https://jupyter.org/)


## Contributing

For bug reports, suggestions or recommendations feel free to open an issue or submit a pull request directly here on GitHub.


## References

[**_Bird, P. (2003)_**](https://doi.org/10.1029/2001GC000252).
An updated digital model of plate boundaries.
*Geochemistry, Geophysics, Geosystems*, volume 4, issue 3, page 1027.
https://doi.org/10.1029/2001GC000252.

[**_Crameri, F. (2021)_**](http://doi.org/10.5281/zenodo.1243862).
Scientific colour maps. *Zenodo*. http://www.fabiocrameri.ch/colourmaps.php. http://doi.org/10.5281/zenodo.1243862.

[**_Grimmer, J., Ritter, J. R. R., Eisbacher, H. & Fielitz, W. (2017)_**](https://doi.org/10.1007/s00531-016-1336-x).
The Late Variscan control on the location and asymmetry of the Upper Rhine Graben.
*International Journal of Earth Sciences*, volume 106, pages 827–853.
https://doi.org/10.1007/s00531-016-1336-x.

[**_Thyng, K. M., Greene, C. A., Hetland, R. D., Zimmerle, H. M. & DiMarco, S. F. (2016)_**](http://dx.doi.org/10.5670/oceanog.2016.66).
True colors of oceanography: Guidelines for effective and accurate colormap selection.
*Oceanography*, volume 29, issue 3, pages 9–13.
http://dx.doi.org/10.5670/oceanog.2016.66.

<!---
[**_Uieda, L., Tian, D., Leong, W. J., Jones, M., Schlitzer, W., Grund, M., Toney, L., Yao, J., Magen, Y., Materna, K., Newton, T., Anant, A., Ziebarth, M., Quinn, J. & Wessel, P. (2022)_**](https://doi.org/10.5281/zenodo.6426493).
PyGMT: A Python interface for the Generic Mapping Tools, version v0.6.1.
*Zenodo*. https://doi.org/10.5281/zenodo.6426493.
-->

[**_Uieda, L., Tian, D., Leong, W. J., Jones, M., Schlitzer, W., Grund, M., Toney, L., Yao, J., Magen, Y., Materna, K., Fröhlich, Y., Belem, A., Newton, T., Anant, A., Ziebarth, M., Quinn, J. & Wessel, P. (2022)_**](https://doi.org/10.5281/zenodo.6702566).
PyGMT: A Python interface for the Generic Mapping Tools, version v0.7.0.
*Zenodo*. https://doi.org/10.5281/zenodo.6702566.

[**_Wessel, P., Smith, W. H. F., Scharroo, R., Luis, J. F. & Wobbe. F. (2013)_**](https://doi.org/10.1002/2013EO450001).
Generic mapping tools: improved version released.
*Eos*, volume 94, issue 45, pages 409-410.
https://doi.org/10.1002/2013EO450001.

[**_Wessel, P., Luis, J. F., Uieda, L., Scharroo, R., Wobbe, F., Smith, W. H. F. & Tian, D. (2019)_**](https://doi.org/10.1029/2019GC008515).
The Generic Mapping Tools version 6.
*Geochemistry, Geophysics, Geosystems*, 20, pages 5556-5564.
https://doi.org/10.1029/2019GC008515.

<!---
[**_Wessel, P., Luis, J. F., Uieda, L., Scharroo, R., Wobbe, F., Smith, W. H. F., Tian, D., Jones, M. & Esteban, F. (2021)_**](https://doi.org/10.5281/zenodo.5708769).
The Generic Mapping Tools, version 6.3.0.
*Zenodo*. https://doi.org/10.5281/zenodo.5708769.
-->

[**_Wessel, P., Luis, J. F., Uieda, L., Scharroo, R., Wobbe, F., Smith, W. H. F., Tian, D., Jones, M. & Esteban, F. (2022)_**](https://doi.org/10.5281/zenodo.6623271).
The Generic Mapping Tools, version 6.4.0.
*Zenodo*. https://doi.org/10.5281/zenodo.6623271.
