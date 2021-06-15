#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:01:47 2020

@author: theresasawi


Run after "wf_to_H5.py"
Read waveform data from HDF5 file, create .mat spectrograms for SpecUFEx




INPUT:
    HDF5 with waveform data, metadata, etc

OUTPUT:
    .mat Spectrograms in folder
    Add spectrograms AND parameters to HDF5
    spectrogram images



Updates:

    12/09/2020 : Plot avg spectra reintroducted with vert lines for fmin, fmax

    11/17/2020 : Sgrams in H5 file now, using generator

    11/13/2020 : paths.py integrated

    10/29/2020 : plot and DB in spectra and spectrograms
                 little fixes ~TS



@author: theresasawi
"""
# ===================================================
import h5py


import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
# this will close any existing hdf5 _open_files
# if we use while statements, we won't have to do this
import tables
tables.file._open_files.close_all()
sys.path.append('./functions')
sys.path.append('../')

from setParams import setParams, setSgramParams
from generators import gen_sgram_QC


#%% load project variables: names and paths

key = sys.argv[1]

# key = 'Parkfield_Repeaters'


pathProj, pathCat, pathWF, network, station, channel, channel_ID, filetype, cat_columns = setParams(key)
fmin, fmax, winLen_Sec, fracOverlap, nfft = setSgramParams(key)


pathCatWF = pathCat


dataH5_name = f'data_{key}.hdf5'
dataH5_path = pathProj + '/H5files/' + dataH5_name


SpecUFEx_H5_name = f'SpecUFEx_{key}.hdf5'
SpecUFEx_H5_path = pathProj + '/H5files/' + SpecUFEx_H5_name


pathSgram_cat = pathProj + f'sgram_cat_out_{key}.csv'


#%% get wf catalog

wf_cat = pd.read_csv(pathSgram_cat)
evID_list = list(wf_cat.event_ID)
print(evID_list[0])




    #%% get sgram parameters from H5 file

with h5py.File(SpecUFEx_H5_path,'r+') as fileLoad:

    fSTFT = fileLoad['spec_parameters/'].get('fSTFT')[()]
    tSTFT = fileLoad['spec_parameters/'].get('tSTFT')[()]
    lenData = fileLoad['spec_parameters/'].get('lenData')[()]
    nperseg = fileLoad['spec_parameters/'].get('nperseg')[()]
    noverlap = fileLoad['spec_parameters/'].get('noverlap')[()]
    fs = fileLoad['spec_parameters/'].get('fs')[()]
    mode = fileLoad['spec_parameters/'].get('mode')[()].decode('UTF-8')
    scaling = fileLoad['spec_parameters/'].get('scaling')[()].decode('UTF-8')
    nfft = fileLoad['spec_parameters/'].get('nfft')[()]
    lenData = fileLoad['spec_parameters/'].get('lenData')[()]

#padding must be longer than n per window segment
if nfft < nperseg:
    nfft = nperseg*64
    print("nfft too short; changing to ", nfft)







#%%

args = {'station':station,
        'channel':channel,
        'fs': fs,
        'lenData': lenData,
        'nperseg': nperseg,
        'noverlap': noverlap,
        'nfft': nfft,
        'mode': mode,
        'scaling': scaling,
        'fmin': fmin,
        'fmax': fmax}



#%% put sgrams in h5
        ### ### ### CREATE GENERATOR ### ### ###
gen_sgram = gen_sgram_QC(key,
                        evID_list=evID_list,
                        dataH5_path = dataH5_path,
                        h5File=fileLoad, #h5 data file
                        trim=False, #trim to min and max freq
                        saveMat=False, #set true to save folder of .mat files
                        sgramOutfile='.', #path to save .mat files
                        **args
                        ) #path to save sgram figures


#%%


spectra_for_avg=[]
n=0
while n <= len(evID_list): ## not sure a better way to execute this? But it works

    if n%500==0:
        print(n)
    try:   #catch generator "stop iteration" error

        evID,sgram,fSTFT,tSTFT, normConstant, Nkept,evID_BADones, i = next(gen_sgram) #next() command updates generator
        n = i+1

        spectra_for_avg.append(np.array(sgram))


    except StopIteration: #handle generator error
        break


#%% PLOT SOME EXAMPLE SPECTROGRAMS
n=0

with h5py.File(SpecUFEx_H5_path,'r+') as fileLoad:
    for i, sgram in enumerate(fileLoad['spectrograms'].values()):
        if i%500==0:
            plt.figure()
            plt.pcolormesh(tSTFT,fSTFT,sgram,shading='auto')
            plt.xlabel('time (s)')
            plt.ylabel('frequency (Hz)')



#%%

# =================plot avg spectra==========================

#% Plot average and std of spectra
alpha = 1
fig, axes = plt.subplots()

plot = 1
if plot:
    # for s in spectra_for_avg[0:-1:250]:
    #     axes.plot(fSTFT,s,lw=.5,c='k',alpha=.007)

    axes.plot(fSTFT,np.mean(np.mean(spectra_for_avg,axis=0),axis=1),lw=2,c='k',label='mean')
    axes.plot(fSTFT,np.mean(np.mean(spectra_for_avg,axis=0),axis=1)+np.std(np.mean(spectra_for_avg,axis=0),axis=1),c='orange',alpha=alpha,label='+/- 1 std')
    # axes.plot(fSTFT,np.mean(np.mean(spectra_for_avg,axis=0),axis=1)+2*np.std(np.mean(spectra_for_avg,axis=0),axis=1),c='yellow',alpha=alpha,label='+/- 2 std')

    axes.legend()

    axes.plot(fSTFT,np.mean(np.mean(spectra_for_avg,axis=0),axis=1)-np.std(np.mean(spectra_for_avg,axis=0),axis=1),c='orange',alpha=alpha)
    # axes.plot(fSTFT,np.mean(np.mean(spectra_for_avg,axis=0),axis=1)-2*np.std(np.mean(spectra_for_avg,axis=0),axis=1),c='yellow',alpha=alpha)


    axes.set_xlabel(f'Frequency (Hz)')
    axes.set_ylabel(f'power/median(power) [dB]')

    axes.axvline(x=fmin,color='blue',ls='--',label='f min or max')
    axes.axvline(x=fmax,color='blue',ls='--')
    axes.axvline(x=1/winLen_Sec,color='red',ls='-','1/window length')

    # ytext = 150
    # axes.text(fmin-4,ytext,'f_min',color='blue',rotation=0)
    # # axes.text(fmax,ytext,'f_max',color='blue',rotation=0)
    # axes.text(1/winLen_Sec+.5,ytext,'STFT \n window size',color='green',rotation=0)

    # plt.xlim(fmin,fmax)






    #%%
