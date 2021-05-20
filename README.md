# specufex_preprocessing

### 1_makeaveformsDataset.py : 

Script for loading a folder of waveforms into properly formatted [HDF5](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) file Must add path names, station parameters and others into functions/setParams.py and functions/generatorspy.

### 2_convertToSpectrograms.py

Script for converting HDF5 waveforms to HDF5 spectrograms for use in SpecUFEx

### 3_runSpecUFExpy

Script for running SpecUFEx$^{1}$ on HDF5 of spectrograms, using Python implementation$^{2}$ 

(1) Holtzman et al., 2018; Machine learning reveals cyclic changes in seismic source spectra in Geysers geothermal field. Science Advances. 4. eaao2929. 10.1126/sciadv.aao2929. 
(2) Nate Groebner reference https://github.com/ngroebner/specufex
