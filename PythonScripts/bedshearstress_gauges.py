#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 13:24:45 2021
@author: ronja ehlers

"""

import numpy as np
import matplotlib.pyplot as plt
import os
import re
from scipy.signal import find_peaks

#%%
# CFD oder NHFLOW?
mode = "CFD"
# mode = "NHFLOW"

t_start = 0.0 # omit time (only for numerical data)
t_end = None # omit time after a certain time or None (only for numerical data)

# ---------- Plot limits (None = autoscale) ----------
xlim = None     # (xmin, xmax) or None for auto
ylim = None     # (ymin, ymax) or None for auto

# ===============================================================
# read experimental data if exists
# ===============================================================
expData = None  # if no experimental data available
# OR load experimental data here, e.g.:
# expData = np.loadtxt(r"../exp/Boers_mild_exp_bedshear/Gauge0_Boers_mild_exp_bedshear.dat",skiprows=1)

# ===============================================================
# create folder for saving plots in the case directory
# ===============================================================
savedir='./00_post_sed/'
if os.path.exists(savedir) == False: 
    os.mkdir(savedir)

# ===============================================================
# read numerical data: wave gauges
# ===============================================================
# ------- get location of gauges, here for 2D case only x-loc important --------
# first line: number of gauges, pick just the number from that and then skip the nr of rows
with open('./REEF3D_'+mode+'_Sediment/REEF3D-'+mode+'-Sediment-Bedshear.dat','r') as f:
    firstline = f.readline().rstrip()
    n_gauges = re.findall(r'\d+',firstline)
    N_gauges = int(n_gauges[0])
N_headers=N_gauges+7 # 7 header lines + N_gauges lines of location
loc = np.loadtxt(r"./REEF3D_"+mode+"_Sediment/REEF3D-"+mode+"-Sediment-Bedshear.dat",skiprows=3, max_rows=N_gauges, delimiter=' ') #3+N_gauges

print(f'Nr gauges: {N_gauges}')
print("Gauge locations (Nr, x, y):")
for row in loc:
    print(f"  {row[0]:6.0f}   {row[1]:8.3f}   {row[2]:8.3f}")

locx = loc[:,1]  # array with x-coordinates of gauges

# -------- read data of gauges -------
numData1 = np.loadtxt(r"./REEF3D_"+mode+"_Sediment/REEF3D-"+mode+"-Sediment-Bedshear.dat",skiprows=N_headers) # read data, skipping rows above data

# -------- mask for time frame --------
mask = (numData1[:,0]>=0) # get a certain time frame
numData1_mask=numData1[mask]

# -------- calculate min and max values --------
minval = np.min(numData1_mask,axis=0) # min value for each gauge
maxval = np.max(numData1_mask,axis=0) # max value for each gauge

minvalue = min(minval[1:N_gauges+1]) # overall min value
maxvalue = max(maxval[1:N_gauges+1]) # overall max value

mintime = minval[0] # min time
maxtime = maxval[0] # max time


# ==============================================================
#  Plots
# ============================================================== 

# ==============================================================
# single plot of every gauge
# ==============================================================
cm = 1/2.54  # centimeters in inches
marker = '.'
markersize = 1.0

for i in range(1,N_gauges+1):
    title = f'G{i} at x =  {locx[i-1]:.2f}'
    fig, (ax1) = plt.subplots(1, figsize=(15*cm, 5*cm))

    if expData is not None:
        ax1.plot(expData[:,0], expData[:,i], label = 'exp', linewidth = 1.0, color='k', linestyle = 'dashed') # experimental data
    ax1.plot(numData1_mask[:,0], numData1_mask[:,i], label ='num', linewidth = 1.0, color = 'r')  # simumlation data
    
    ax1.hlines(0.0,minval[0],maxval[0],'k', linewidth = 0.5, linestyle = '--') # 
    
    ax1.set_title(title)
    plt.xlabel('t [s]')
    plt.ylabel(r'$\tau_b$ $[N/m^2]$')
    ax1.legend();  # Add a legend
    
    # grid
    ax1.grid(True, color='w', linestyle='-', linewidth=1)
    ax1.set_facecolor('0.95')

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    
    # Apply limits if provided
    if xlim is not None:
        xmin, xmax = xlim
        if xmax is None:
            xmax = maxtime
        ax1.set_xlim(xmin, xmax)

    if ylim is not None:
        ymin, ymax = ylim
        ax1.set_ylim(ymin, ymax)

    p = i
    fig.savefig(savedir + 'gauge_bedshear_' + "%.0f" %p  + '.pdf', format='pdf', bbox_inches='tight')
    # fig.savefig(savedir+'gauge_bedshear_' + "%.0f" %p +'.eps',bbox_inches = 'tight')
    # fig.savefig(savedir + 'gauge_bedshear_' + "%.0f" %p  + '.jpg', format='jpg',dpi = 1000, bbox_inches='tight')
    # print message
    print(f'Gauge {p} plot saved in folder: {savedir}')

# ==============================================================
# all gauges in one plot
# ==============================================================
cm = 1/2.54  # centimeters in inches
# fig, axs = plt.subplots(N_gauges,figsize=(15*cm, 55*cm), sharex = True)
fig, axs = plt.subplots(nrows=N_gauges, ncols=1, figsize=(15*cm, 5*cm*N_gauges), sharex=True, constrained_layout=False)
plt.subplots_adjust(hspace=0.35) # adjust the height between subplots

for i in range(1,N_gauges+1):
    # print (f'Loop{i} = G{i-1}')
    title= f'G{i-1} at x =  {locx[i-1]:.2f}'

    if expData is not None:
        axs[i-1].plot(expData[:,0], expData[:,i], label = 'exp', linewidth = 1.0, color='k', linestyle = 'dashed') # experimental data
    axs[i-1].plot(numData1_mask[:,0], numData1_mask[:,i], label ='num', linewidth = 1.0, color = 'r')

    axs[i-1].hlines(0.0,minval[0],maxval[0],'k', linewidth = 0.5, linestyle = '--') #
    
    axs[i-1].set_title(title)
    plt.xlabel('t [s]') #, fontweight='bold'
    plt.ylabel(r'$\tau_b$ $[N/m^2]$') #,fontweight='bold'
    axs[1].legend();  # Add a legend.
    
    # grid
    axs[i-1].grid(True, color='w', linestyle='-', linewidth=1)
    axs[i-1].set_facecolor('0.95')

    axs[i-1].spines['top'].set_visible(False)
    axs[i-1].spines['right'].set_visible(False)
    axs[i-1].spines['bottom'].set_visible(False)
    axs[i-1].spines['left'].set_visible(False)

    # Apply limits if provided
    if xlim is not None:
        xmin, xmax = xlim
        if xmax is None:
            xmax = maxtime
        axs[i-1].set_xlim(xmin, xmax)

    if ylim is not None:
        ymin, ymax = ylim
        axs[i-1].set_ylim(ymin, ymax)
    
fig.savefig(savedir + 'all_gauge_bedshear.pdf', format='pdf', bbox_inches='tight')
# fig.savefig(savedir+'all_gauge_bedshear.eps',bbox_inches = 'tight')
# fig.savefig(savedir + 'all_gauge_bedshear.jpg', format='jpg',dpi = 1000, bbox_inches='tight')
# print message
print(f'All Gauges plot saved in folder: {savedir}')