# specufex_preprocessing


### 1_makeaveformsDataset.py : 

Script for loading a folder of waveforms into properly formatted [HDF5](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) file. Must add path names, station parameters, and other user-specific settings into functions/setParams.py and functions/generators.py.

*input* Folder of waveforms (most seismic data formats accepted), catalog (csv)

*output* new HDF5 of waveforms 



### 2_convertToSpectrograms.py

Script for converting HDF5 waveforms to HDF5 spectrograms for use in SpecUFEx. Must update the specrtogram parameters in functions/setParams.py


*input*  HDF5 of waveforms 

*output* new HDF5 of spectrograms 



### 3_runSpecUFEx.py

Script for running [SpecUFEx(1)](https://advances.sciencemag.org/content/4/5/eaao2929) on HDF5 of spectrograms, using [Python implementation(2)](https://github.com/ngroebner/specufex). Saves output to H5. 

*input*  HDF5 of spectrograms 

*output* Same HDF5, updated with output from SpecUFEx



#### References


(1) Holtzman et al., 2018; Machine learning reveals cyclic changes in seismic source spectra in Geysers geothermal field. Science Advances. 4. eaao2929. 10.1126/sciadv.aao2929. 


(2) Nate Groebner reference https://github.com/ngroebner/specufex
