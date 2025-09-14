# PyGMT Plotting

Collection of Python scripts or Jupyter notebooks (supported by JupyterLab) to reproduce some of the geographic and
geophysical maps shown in the publications I am involved in. To prepare these maps, [_PyGMT_](https://www.pygmt.org)
the Python wrapper for the [_Generic Mapping Tools_ (_GMT_)](https://www.generic-mapping-tools.org) is used.

<img src="https://github.com/yvonnefroehlich/gmt-pygmt-plotting/raw/main/_images/github_maps_readme_main.png">


## Content

_Please note_: Scripts or notebooks are available up on acceptance of the related publication.

| Folder of repository (click for more content) | Overview |
| --- | --- |
| • **[000_general_stuff](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/000_general_stuff#000_general_stuff)** <br> • **[001_paper_RFSG_2022](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/001_paper_RFSG_2022#001_paper_RFSG_2022)** <br> • **[002_paper_FGR_2024](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/002_paper_FGR_2024#002_paper_FGR_2024)** <br> • **[003_taup](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/003_taup#003_taup)** <br> • **[004_earthquakes_eruptions](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/004_earthquakes_eruptions#004_earthquakes_eruptions)** <br> • **[005_global_seismicity](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/005_global_seismicity#005_global_seismicity)** <br> • **[006_tomographies_databases](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/006_tomographies_databases#006_tomographies_databases)** <br> • **[007_dissrtation_F_2025](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/007_dissertation_F_2025#007_dissertation_F_2025)** <br> • **[008_urg_vs_norsa](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/008_urg_vs_norsa#008_urg_vs_norsa)** <br> • **[009_deepdyn](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/009_deepdyn#009_deepdyn)** <br> • **[010_axisem](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/010_axisem#010_axisem)** <br> • **[011_agu_FTLJG_2024](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/011_agu_FTLJG_2024#011_agu_FTLJG_2024)** <br> • **[012_uefa_euro25](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/012_uefa_euro25#012_uefa_euro25)** <br> • **[013_general_maps](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/013_general_maps#013_general_maps)** <br> • **[014_general_stats](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/tree/main/014_general_stats#014_general_stats)** | ![github_maps_readme_main](https://github.com/user-attachments/assets/fa61c920-0111-44dd-8544-345466f5b8d7) |


## Requirements

_Please note_: The required versions are given above in the single folders as well as notebooks and scripts.

- [PyGMT](https://www.pygmt.org)
- [GMT](https://www.generic-mapping-tools.org)
- [Python](https://www.python.org)
- [Jupyter notebook](https://jupyter.org) or [JupyterLab](https://jupyter.org)
- [NumPy](https://numpy.org)
- [pandas](https://pandas.pydata.org)
- [ObsPy](https://docs.obspy.org)
- [pymagglobal](https://sec23.git-pages.gfz-potsdam.de/korte/pymagglobal)


## Citation

If you make use of this material, please acknowledge the relating publications in which framework these scripts and notebooks were written:

**Peer-reviewed journal articles**
- [**_Fröhlich Y, Grund M, Ritter J R R (2024)_**](https://doi.org/10.1093/gji/ggae245).
  Lateral and vertical variations of seismic anisotropy in the lithosphere-asthenosphere system underneath Central Europe from long-term splitting measurements.
  *Geophysical Journal International*, 239(1):112-135.
  https://doi.org/10.1093/gji/ggae245.
- [**_Ritter J R R, Fröhlich Y, Sanz Alonso Y, Grund M (2022)_**](https://doi.org/10.1007/s10950-022-10112-w).
  Short-scale laterally varying SK(K)S shear wave splitting at BFO, Germany – implications for the determination of anisotropic structures.
  *Journal of Seismology*, 26:1137-1156.
  https://doi.org/10.1007/s10950-022-10112-w, correction https://doi.org/10.1007/s10950-023-10136-w.

**Doctoral studies**
- [**_Fröhlich Y (2025a)_**](https://doi.org/10.5445/IR/1000183786).
  Shear wave splitting analysis of long-term data: Anisotropy studies in the Upper Rhine Graben area, Central Europe.
  Dissertation, *Karlsruhe Institute of Technology, Geophysical Institute*.
  https://doi.org/10.5445/IR/1000183786.
- [**_Fröhlich Y (2025b)_**](https://doi.org/10.5281/zenodo.15982581).
  Shear wave splitting analysis of long-term data: Anisotropy studies in the Upper Rhine Graben area, Central Europe.
  Disputation, *Karlsruhe Institute of Technology, Geophysical Institute*.
  https://doi.org/10.5281/zenodo.15982581.

**Presentations**
- [**_Fröhlich Y, Ritter J R R (2024)_**](https://dx.doi.org/10.5281/zenodo.14510993).
  Vertical and Small-scale Lateral Varying Seismic Anisotropy in the Upper Mantle Underneath the Upper Rhine Graben, Central Europe.
  *Annual Meeting of the American Geophysical Union*, Washington D.C..
  Division Session Exploring Innovations and New Directions in Seismic Anisotropy and Attenuation: Observations, Models, and Experiments I Oral, DI21A-02.
  [Abstract ID 1578275](https://agu.confex.com/agu/agu24/meetingapp.cgi/Paper/1578275).
  https://dx.doi.org/10.5281/zenodo.14510993.
- [**_Fröhlich Y, Tian D, Leong W J, Jones M, Grund M (2024)_**](https://doi.org/10.6084/m9.figshare.28049495).
  PyGMT – Accessing and Integrating GMT with Python and the Scientific Python Ecosystem.
  *Annual Meeting of the American Geophysical Union*, Washington D.C..
  Union Session The impact of GMT in the Earth, Ocean and Space sciences: What's next? I Oral, U12B-05 (invited).
  [Abstract ID 1578856](https://agu.confex.com/agu/agu24/meetingapp.cgi/Paper/1578856).
  https://doi.org/10.6084/m9.figshare.28049495.

**Posters**
- [**_Fröhlich Y, Dorn F, Dillah M I F, Ritter J R R (2024)_**](https://doi.org/10.5281/zenodo.14801004).
  Investigation of seismic anisotropy in the D'' layer using *X*KS pairs.
  *2th DeepDyn annual meeting*, Rügen.
  https://doi.org/10.5281/zenodo.14801004.
- [**_Fröhlich Y, Dillah M I F, Dorn F, Ritter J R R (2024)_**](https://doi.org/10.5281/zenodo.12658821).
  Investigation of seismic anisotropy in the D'' layer and at the CMB regarding intense magnetic flux regions.
  *18th Symposium of Study of the Earth's Deep Interior*, Great Barrington.
  https://doi.org/10.5281/zenodo.12658821.
- [**_Fröhlich Y, Thiyagarajan H, Tölle L S, Ritter J R R, Thomas C (2024)_**](https://doi.org/10.5281/zenodo.10927349).
  Understanding the influence of seismic mantle structures at the core-mantle boundary on intense magnetic flux regions.
  *84th Annual Meeting of the German Geophysical Society*, Jena.
  https://doi.org/10.5281/zenodo.10927349.


## Contributing

For bug reports, suggestions, or recommendations feel free to [open an issue](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/issues)
or [submit a pull request](https://github.com/yvonnefroehlich/gmt-pygmt-plotting/pulls) directly here on
[GitHub](https://github.com/yvonnefroehlich/gmt-pygmt-plotting).


## References

_Please note_: Specific references are given in the single notebooks and scripts.

- [**_Crameri F (2023)_**](https://doi.org/10.5281/zenodo.1243862).
  Scientific colour maps.
  https://www.fabiocrameri.ch/colourmaps.php.
  *Zenodo*. https://doi.org/10.5281/zenodo.1243862.
- [**_Thyng K M, Greene C A, Hetland R D, Zimmerle H M, DiMarco S F (2016)_**](https://dx.doi.org/10.5670/oceanog.2016.66).
  True colors of oceanography: Guidelines for effective and accurate colormap selection.
  *Oceanography*, 29(3):9-13.
  https://dx.doi.org/10.5670/oceanog.2016.66.
- [**_Tian D, Uieda L, Leong W J, Fröhlich Y, Grund M, Schlitzer W, Jones M, Toney L, Yao J, Tong J-H, Mage Y, Materna K, Belem A, Newton T, Anant A, Ziebarth M, Quinn J, Wessel P (2024)_**](https://doi.org/10.5281/zenodo.15071586).
  PyGMT: A Python interface for the Generic Mapping Tools, version v0.16.0.
  *Zenodo*. https://doi.org/10.5281/zenodo.15628725 (v0.16.0), https://doi.org/10.5281/zenodo.3781524 (all versions / latest version).
- [**_Wessel P, Smith W H F, Scharroo R, Luis J F, Wobbe F (2013)_**](https://doi.org/10.1002/2013EO450001).
  Generic mapping tools: improved version released.
  *Eos, Transactions American Geophysical Union*, 94(45):409-410.
  https://doi.org/10.1002/2013EO450001.
- [**_Wessel P, Luis J F, Uieda L, Scharroo R, Wobbe F, Smith W H F, Tian D (2019)_**](https://doi.org/10.1029/2019GC008515).
  The Generic Mapping Tools version 6.
  *Geochemistry, Geophysics, Geosystems*, 20(11):5556-5564.
  https://doi.org/10.1029/2019GC008515.
- [**_Wessel P, Luis J F, Uieda L, Scharroo R, Wobbe F, Smith W H F, Tian D, Jones M, Esteban F, Fröhlich Y (2025)_**](https://doi.org/10.5281/zenodo.16448627).
  The Generic Mapping Tools, version 6.6.0.
  *Zenodo*. https://doi.org/10.5281/zenodo.16448627 (6.6.0), https://doi.org/10.5281/zenodo.3407865 (all versions / latest version).


## Funding

The presented research and YF received support from various sources:

- [Graduate Funding from the German States](https://www.khys.kit.edu/english/graduate_funding.php) (scholarship)
- [NSF grant EAR-1948602](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1948602) (travel support for AGU24)
- [DFG grant RI1133/14-1](https://gepris.dfg.de/gepris/projekt/521545943?language=en) within the
  [DFG Priority Program 2404 DeepDyn](https://www.geo.lmu.de/deepdyn/en/) (research assistant)
