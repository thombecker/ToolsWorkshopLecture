#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ronja ehlers

Put this script into your case folder
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import re

# ===============================================================
#  Input parameters
# ===============================================================
# CHOOSE THE MODE: CFD oder NHFLOW?
mode = "CFD"
# mode = "NHFLOW"

swl = 0.75 # still water level
if mode == "NHFLOW":
    offset_z = 0.0
elif mode == "CFD":
    offset_z = swl

t_start = 0.0 # omit time (only for numerical data)
t_end = None # omit time after a certain time or None (only for numerical data)

# ---------- Plot limits (None = autoscale) ----------
xlim = (5.0, 50.0)      # (xmin, xmax) or None for auto
ylim = (-0.15, 0.15)     # (ymin, ymax) or None for auto

# ===============================================================
# read experimental data if exists
# ===============================================================
# expData = None  # if no experimental data available
# OR load experimental data here, e.g.:
expData = np.loadtxt(r"../exp/Boers_mild_exp.dat",skiprows=1)

# ===============================================================
# create folder for saving plots in the case directory
# ===============================================================
savedir='./00_post_wave/'
if os.path.exists(savedir) == False: 
    os.mkdir(savedir)

# ===============================================================
# read numerical data: wave gauges
# ===============================================================

# ------- get location of gauges, here for 2D case only x-loc important --------
# first line: number of gauges, pick just the number from that and then skip the nr of rows
with open('./REEF3D_'+mode+'_WSF/REEF3D-'+mode+'-WSF-HG.dat','r') as f:
    firstline = f.readline().rstrip()
    n_gauges = re.findall(r'\d+',firstline)
    N_gauges = int(n_gauges[0])
N_headers=N_gauges+7 # 7 header lines + N_gauges lines of location
loc = np.loadtxt(r"./REEF3D_"+mode+"_WSF/REEF3D-"+mode+"-WSF-HG.dat",skiprows=3, max_rows=N_gauges, delimiter=' ') #3+N_gauges
print(f'Nr gauges: {N_gauges}')
print("Gauge locations (Nr, x, y):")
for row in loc:
    print(f"  {row[0]:6.0f}   {row[1]:8.3f}   {row[2]:8.3f}")

locx = loc[:,1] # array with x-coordinates of gauges

# -------- read data of gauges -------
numData1 = np.loadtxt(r"./REEF3D_"+mode+"_WSF/REEF3D-"+mode+"-WSF-HG.dat",skiprows=N_headers) # read data skipping header

# -------- caluclate mask for time frame -------
# mask for time frame
if t_end is None:
    t_end = numData1[:,0].max() # if t_end is None: it will pick the maximum time from the data
mask = (numData1[:,0] >= t_start) & (numData1[:,0] <= t_end) # get a certain time frame
numData1_mask=numData1[mask]

# -------- calculate max and min values -------
minval=np.min(numData1_mask,axis=0) # min value for every gauge
maxval=np.max(numData1_mask,axis=0) # max value for every gauge

minvalue = min(minval[1:N_gauges+1]) # overall min value
maxvalue = max(maxval[1:N_gauges+1]) # overall max value

mintime = minval[0] # min time
maxtime = maxval[0] # max time

# ------- read data of theory if exists -------
theory_file = f"./REEF3D_{mode}_WSF/REEF3D-{mode}-WSF-HG-THEORY.dat"
theory_exists = os.path.isfile(theory_file)
if theory_exists:
    theory = np.loadtxt(theory_file, skiprows=N_headers)
    mask = (theory[:,0] >= t_start) & (theory[:,0] <= t_end)
    theory_mask = theory[mask]
else:
    theory_mask = None
    print("No theory file found, skipping theory plots.")

# ==============================================================
#  Plots
# ==============================================================        

# ==============================================================
# single plot of every gauge
# ==============================================================
cm = 1/2.54  # centimeters in inches
for i in range(1,N_gauges+1):
    title= f'G{i} at x =  {locx[i-1]:.2f}'
    fig, (ax1) = plt.subplots(1, figsize=(15*cm, 5*cm))
    
    if expData is not None:
        ax1.plot(expData[:,0], expData[:,i], label='exp', linewidth=1.0, color='k', linestyle='dashed')
    ax1.plot(numData1_mask[:,0], numData1_mask[:,i]-offset_z, label ='num', linewidth = 1.0, color = 'r') #label ='num' +  f'Gauge {i}'
    if theory_mask is not None:
        ax1.plot(theory_mask[:,0], theory_mask[:,i]-offset_z,label='theory', linewidth=1.0, color='k', linestyle='--') #label ='num' +  f'Gauge {i}'
    
    ax1.hlines(0.0,minval[0],maxval[0],'k', linewidth = 0.5, linestyle = '--')
    
    ax1.set_title(title)
    plt.xlabel('t [s]')
    plt.ylabel('$\\eta$ [m]')
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
    
    # fig.savefig(savedir+'Gauge_' + "%.0f" %i +'.eps',bbox_inches = 'tight')
    # fig.savefig(savedir + 'Gauge_' + "%.0f" %i  + '.jpg', format='jpg',dpi = 1000, bbox_inches='tight')
    fig.savefig(savedir + 'Gauge_' + "%.0f" %i  + '.pdf', format='pdf', bbox_inches='tight')
    
    # print message
    print(f'Gauge {i} plot saved in folder: {savedir}')

# ==============================================================
# all gauges in one plot
# ==============================================================
cm = 1/2.54  # centimeters in inches
# fig, axs = plt.subplots(N_gauges,figsize=(15*cm, N_gauges*5*cm), sharex = True)
fig, axs = plt.subplots(nrows=N_gauges, ncols=1, figsize=(15*cm, 5*cm*N_gauges), sharex=True, constrained_layout=False)
plt.subplots_adjust(hspace=0.35) # adjust the height between subplots
axs = np.atleast_1d(axs)  # wandelt axs in ein 1D-Array um, auch wenn nur ein Plot

for i in range(1,N_gauges+1):
    # print (i)
    title= f'G{i} at x =  {locx[i-1]:.2f}'
    
    if expData is not None:
        axs[i-1].plot(expData[:,0], expData[:,i], label='exp', linewidth=1.0, color='k', linestyle='dashed')
    axs[i-1].plot(numData1_mask[:,0] , numData1_mask[:,i]-offset_z, label ='num', linewidth = 1.0, color = 'r') #label ='num' +  f'Gauge {i}'
    if theory_mask is not None:
        axs[i-1].plot(theory_mask[:,0], theory_mask[:,i]-offset_z, label='theory', linewidth=1.0, color='k', linestyle='--') #label ='num' +  f'Gauge {i}'
    
    axs[i-1].hlines(0.0,minval[0],maxval[0],'k', linewidth = 0.5, linestyle = '--')
    
    axs[i-1].set_title(title)
    plt.xlabel('t [s]') #, fontweight='bold'
    plt.ylabel('$\\eta$ [m]') #,fontweight='bold'
    axs[0].legend();  # Add a legend.
    
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
    
# fig.savefig(savedir+'All_Gauges.eps',bbox_inches = 'tight')
# fig.savefig(savedir + 'All_Gauges.jpg', format='jpg',dpi = 1000, bbox_inches='tight')
fig.savefig(savedir + 'All_Gauges.pdf', format='pdf', bbox_inches='tight')
# print message
print(f'All Gauges plot saved in folder: {savedir}')