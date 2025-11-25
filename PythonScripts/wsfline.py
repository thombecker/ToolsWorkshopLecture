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
# Input parameters
# ===============================================================
# plot settings
offset_x = 0
swl = 0.75 # still water level, optional
offset_y = swl

# CHOOSE THE FOLDER from where you want to import sedline files:
# 1) simply choose all files from the default output folder "REEF3D_CFD_WSFLINE"
# wsfline_folder = './REEF3D_CFD_WSFLINE/'
# or
# 2) put the files you want to plot into the folder "00_post_wsfline" and choose this folder here:
wsfline_folder = './00_post_wave/'

#%% # ===============================================================
# find files in folder and subfolders
# ===============================================================
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

# =============================================================
# %% creates a folder in the case directory 
# =============================================================
savedir='./00_post_wave/'
if os.path.exists(savedir) == False: 
    os.mkdir(savedir)

# =============================================================== 
# find wsfline files
# ===============================================================
filelist_wsf = find('*wsfline*.dat',wsfline_folder) # put the files you want to plot in there
filelist_wsf.sort()

# ==============================================================
#%% plot wsfline
# ==============================================================
    
# Plot Settings
lw = 0.5 # linewidth
ms = 2 # markersize
size=(12,4) # figure size

# create figure
fig, ax1 = plt.subplots(figsize=size)

# plot sim data: wsfline
for file in filelist_wsf: # read wsfline files
    f=open(file)
    content = f.readlines()
    t_sim = float(content[0].split(":")[1].strip()) # read sim time from first line
    wsfline = pd.read_csv(file, sep=r"\s+", skiprows=9, names=['x','zwsf','theory']) # plot wsfline data from 10th line on

    ax1.plot(wsfline.x-offset_x, wsfline.zwsf-offset_y, label=f'$t_{{sim}}$: {t_sim:.2f}s',linewidth = lw)

# horizontal lines for orientation:
ax1.axhline(swl-offset_y,c='k',lw = 0.5, ls = '--') # still water level

# vertical lines, e.g. for gauges:
# g1 = 4.63
# g2 = 5.85
# ax1.vlines([g1,g2],ymin = -0.1, ymax = 0.1,colors='k', lw = 0.5,ls= '--')

# grid and background color
ax1.grid(True, color='w', linestyle='-', linewidth=1)
ax1.set_facecolor('0.95')

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)

# axis limits and aspect ratio
# ax1.set_xlim(0,7)
# ax1.set_ylim(-0.10, 0.10)
# ax1.set_aspect('equal')

# axis labels
ax1.set_xlabel('x [m]')
ax1.set_ylabel('$\\eta$ [m]')
# legend
ax1.legend(loc='lower center',bbox_to_anchor=(0.5, -0.3), frameon=False,ncol=5, shadow=False)

# save plot
fig.savefig(savedir + 'wsfline.pdf', format='pdf',bbox_inches='tight')
# fig.savefig(savedir + 'wsfline.eps', format='eps',bbox_inches='tight')
# fig.savefig(savedir + 'wsfline.jpg', format='jpg',dpi = 1000, bbox_inches='tight')

# print message
print(f"wsfline plot saved in folder: {savedir}")
