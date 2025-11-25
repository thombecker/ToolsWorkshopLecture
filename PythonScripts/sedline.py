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
import os, fnmatch


# ===============================================================
# input parameters
# ===============================================================
swl = 0.75 # still water level [m] for plotting

# CHOOSE THE FOLDER from where you want to import sedline files:
# 1) simply choose all files from the default output folder "REEF3D_CFD_SedimentLine"
# sedline_folder = './REEF3D_CFD_Sediment/Line/'
# or
# 2) put the sedline files you want to plot into the folder "00_post_sedline" and choose this folder here:
sedline_folder = './00_post_sed/'

# if EXPERIMENTAL DATA is available for sedline comparison:
# 1) check the import at section "Import experimental data if available"
# 2) check/uncomment the plotting section below "Plot sedline at different times":
#       ==== plot exp data if available ====


# ===============================================================
# Function to find files with certain pattern
# ===============================================================
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

# ===============================================================
# Create folder for saving plots: sedtime
# ===============================================================
savedir_01="./00_post_mainlog/"
if os.path.exists(savedir_01) == False: 
    os.mkdir(savedir_01)

# ===============================================================
# Create folder for saving plots: sedline
# ===============================================================
savedir_02="./00_post_sed/"
if os.path.exists(savedir_02) == False: 
    os.mkdir(savedir_02)
    
# ===============================================================
# Import sim sediment data: sedimentlog.dat
# ===============================================================

file = './REEF3D_Log/REEF3D_sedimentlog.dat' # path to sedimentlog file
header_list = ['it', 't_sim','dt_sed','t_sed','sediter','slidecells','bedmin','bedmax'] # column names
sedlog = pd.read_csv(file, sep=r"\s+",skiprows=3, names=header_list)
t_sim_end=sedlog['t_sim'].iloc[-1]
t_sed_end=sedlog['t_sed'].iloc[-1]

# === find first iteration where sediment was calculated ===
pos = np.argmax(sedlog['t_sed']>0)
it_min= sedlog['it'].iloc[pos] # first iteration where sediment was calculated
it_max= sedlog['it'].iloc[-1] # last iteration
# ===============================================================

# ===============================================================
# Plot sedtime and simtime (= hydro time) from sedimentlog.dat
# ===============================================================
size=(12,4)
fig, ax = plt.subplots(figsize=size)

ax.plot(sedlog.it, sedlog.t_sim, label='$t_{sim}$ with max = ' + f'{t_sim_end:.2f}' + ' s')
ax.plot(sedlog.it, sedlog.t_sed, label='$t_{sed}$ with max = ' + f'{t_sed_end:.2f}' + ' s')

ax.set_xlabel('iteration with max = ' +str(it_max))
ax.set_ylabel('t [s]')
#ax.set_title("Title")
ax.legend()
ax.grid(True)
# ax.set_aspect('equal')

# === save plot ===
fig.savefig(savedir_01 + 'SedSimtime.pdf',bbox_inches='tight')
# fig.savefig(savedir_01 + 'SedSimtime.eps', format='eps',bbox_inches='tight')
# fig.savefig(savedir_01 + 'SedSimtime.jpg', format='jpg',dpi = 1000, bbox_inches='tight')

# ===============================================================
# Import experimental data if available
# ===============================================================

# file = '.exp/expdata.csv' # path to experimental data
# header_list = ['x', 'z_sed']
# sedline_exp = pd.read_csv(file, sep=",",skiprows=1, names=header_list) # import experimental data

# ===============================================================
# Plot sedline at different times
# ===============================================================
# e.g. if the data needs to be shifted
loc_sed_start = 0.0
intersect_sed_swl= 0.0 # location of intersection of sed line and swl in exp data
offset_x = 0.0 # e.g. shift of exp data in x direction

offset_y = 0.0 # e.g. SWL

lw = 1.0 # linewidth
ms = 3 # markersize
c='k' # color for exp data

# ============ find sedline files in specified folder ==========================
# filelist_all = find('*' + '.dat','./REEF3D_CFD_SedimentLine') # all files for checking purposes
# filelist_all.sort()

filelist = find('*.dat',sedline_folder) # put the files you want to plot in there ->  e.g. check it_min and it_max
filelist.sort()
# print('Found sedline files to plot:')
# print(filelist)

# ========== plot sedline at different times ==================
size=(12,4)
fig, ax1 = plt.subplots(figsize=size)

# ================= loop over sedline files ==============
# for file in filelist_all: # loop over all sedline files
for file in filelist: # loop over sedline files in the folder 00_apost_sedline
    f=open(file)
    content = f.readlines()
    t_sed = content[0]
    t_sim = content[1]
    sedline = pd.read_csv(file, sep=r"\s+", skiprows=9, names=['x','zsed']) # import sedline data
    print('Plotting sedline from file: ' + str(file))
    # sedline = sedline.mask(sedline['x']>37.448) #mask if needed
# ===== plot sedline ====
    ax1.plot(sedline.x-offset_x, sedline.zsed-offset_y, label=t_sed +''+ t_sim)

# ==== plot exp data if available ====
# ax1.scatter(sedline_exp.x, sedline_exp.z_sed, label='Exp', marker='o', s=15,facecolors='none', edgecolors=c, linewidths = 0.5) # for exp data

# ==== plot swl line ====
ax1.axhline(swl, c='b', ls = '--',linewidth=lw, label = 'swl')

# ==== finalize plot ====
ax1.set_xlabel('x [m] \n $t_{sed}(end)$ = '+f'{t_sed_end:.2f}'+' s  $t_{sim}(end)$ = '+f'{t_sim_end:.2f}'+' s')
ax1.set_ylabel('$z_{sed}$ [m]')
# ax1.set_title("sedline at different times")
# major_ticks = np.arange(0, 100, 2)
# ax1.set_xticks(major_ticks)
ax1.grid(True, linestyle='--')
# ax1.set_xlim(63,86)
# ax1.set_ylim(-1.2, 0.7)
ax1.legend()
# ax1.set_aspect('equal')

# === save plot ===
fig.savefig(savedir_02 + 'sedline.pdf',bbox_inches='tight')
# fig.savefig(savedir_02 + 'sedline.eps', format='eps',bbox_inches='tight')
# fig.savefig(savedir_02 + 'sedline.jpg', format='jpg',dpi = 1000, bbox_inches='tight')
# print message
print(f'Sedlines plot saved in folder: {savedir_02}')