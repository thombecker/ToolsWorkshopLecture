#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 09:19:06 2021

@author: ronja ehlers

Put this script into your case folder
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# ===============================================================
# Create folder in the case directory for the output plots
# ===============================================================
savedir='./00_post_mainlog/'
if os.path.exists(savedir) == False:
    os.mkdir(savedir)

# ===============================================================
# %% Import main log
# ===============================================================

file = './REEF3D_Log/REEF3D_mainlog.dat'
with open(file) as f:
    header = f.readlines()[4].replace("Volume 1", "Volume1") # fix for column name with space
columns = header.split() # read header line and split into column names
mainlog = pd.read_csv(file, sep=r"\s+", skiprows=5, names=columns) # read data into pandas DataFrame


# --- Convert columns to NumPy arrays ---
iteration = mainlog['#iteration'].to_numpy()
timestep  = mainlog['#timestep'].to_numpy()
simtime   = mainlog['#simtime'].to_numpy()
# itertime  = mainlog['#itertime'].to_numpy()
# ptime     = mainlog['#ptime'].to_numpy()
Vol1      = mainlog['#Volume1'].to_numpy()
Vol2      = mainlog['#Volume2'].to_numpy()
Q_in      = mainlog['#Inflow'].to_numpy()
Q_out     = mainlog['#Outflow'].to_numpy()
Ui        = mainlog['#Ui'].to_numpy()

# Extract max values
it_max = iteration[-1]
simtime_max = simtime[-1]


# ===============================================================
# %% Import sediment log if exists
# ===============================================================
file_sed = './REEF3D_Log/REEF3D_sedimentlog.dat'
if os.path.isfile(file_sed) == True:
    file = file_sed
    header_list = ['it', 't_sim','dt_sed','t_sed','sediter','slidecells','bedmin','bedmax']
    sedlog = pd.read_csv(file, sep=r"\s+", skiprows=3, names=header_list)
    t_sim_end=sedlog['t_sim'].iloc[-1]
    t_sim_start=sedlog['t_sim'].iloc[0]
    t_sed_end=sedlog['t_sed'].iloc[-1]
    it_sed_start = sedlog['it'].iloc[0]
    # it_max= sedlog['it'].iloc[-1]
    DF = t_sed_end/(t_sim_end-t_sim_start) # decoupling factor


# ===============================================================
# %% plot mainlog
# ===============================================================
# set plot parameters
plt.rcParams.update({'font.size': 14}) # setting font size
size=(10,20) # figsize
lw = 1.0 # linewidth

# subplots: 1) simtime (and sedtime if available)   2) timestep   3) Volume1/2   4) In/Outflow   5) Ui
fig, axs = plt.subplots(
    nrows=5, ncols=1, figsize=size, sharex=True,
    gridspec_kw={'hspace':0.5}
)

axs[0].plot(iteration, simtime, linewidth=lw, label = '$t_{sim}$, max = ' + f'{simtime_max:.2f} s')
if os.path.isfile(file_sed) == True:
    axs[0].plot(sedlog.it, sedlog.t_sed, label='$t_{sed}$, max = ' + f'{t_sed_end:.2f}' + ' s' + ' | DF = ' + f'{DF:.2f}', c='gold', linewidth=lw)
    axs[0].axvline(it_sed_start, c='gold', ls = '--',linewidth=2.0, label = '$sed_{start}$ = ' + f'{it_sed_start} it = {t_sim_start:.2f} s')

axs[1].plot(iteration, timestep, linewidth=lw, label='dt')

axs[2].plot(iteration, Vol1, linewidth=lw, label='Vol1')
axs[2].plot(iteration, Vol2, linewidth=lw, label='Vol2')

axs[3].plot(iteration, Q_in, linewidth=lw, label='Q_in')
axs[3].plot(iteration, Q_out, linewidth=lw, label='Q_out')

axs[4].plot(iteration, Ui, linewidth=lw, label='Ui')

# add simtime from mainlog on horizontal axis:
axs0_time = axs[0].twiny()
axs0_time.plot(simtime, timestep, linestyle='None')
axs0_time.set_xlabel(r'simtime, max = ' + f'{simtime_max:.2f} s')
axs0_time.tick_params(axis ='x')
axs0_time.grid(True, axis ='x', linestyle = '--')

axs3_time = axs[3].twiny()
axs3_time.plot(simtime, Q_in, linestyle='None')
axs3_time.set_xlabel(r'simtime, max = ' + f'{simtime_max:.2f} s')
axs3_time.tick_params(axis ='x')
axs3_time.grid(True, axis ='x', linestyle = '--')

# --- Grid, titles, labels ---
for ax in fig.get_axes():
    ax.grid(True)

axs[0].set_title('simtime')
axs[1].set_title('timestep')
axs[2].set_title('Volume 1 vs 2')
axs[3].set_title('Q_in & Q_out')
axs[4].set_title('Ui')

axs[0].legend()
axs[2].legend()
axs[3].legend()

axs[0].set_ylabel('[s]')
axs[1].set_ylabel('[s]')
axs[2].set_ylabel('$[m^3]$')
axs[3].set_ylabel('Q $[m^3/s]$')
axs[4].set_ylabel('Ui $[m/s]$')
axs[4].set_xlabel('iteration, max = ' + str(it_max) + f' & simtime max = {simtime_max:.2f} s') #, fontweight='bold'

# save plot    
fig.savefig(savedir + 'Mainlog.pdf',bbox_inches='tight')
# fig.savefig(savedir + 'Mainlog' +'.eps',bbox_inches = 'tight')
# fig.savefig(savedir + 'Mainlog.jpg', format='jpg',dpi = 1000, bbox_inches='tight')