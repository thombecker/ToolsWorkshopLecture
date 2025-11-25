#!/usr/bin/env pvpython
from paraview.simple import *
import os
import shutil

# ================================================================
# Script to load a ParaView statefile, overwrite data sources,
# and export animations and/or static images.
# ================================================================

# ================================================================
# User parameters
# ================================================================
statefile    = "../paraview_state_wrunup.pvsm"  # original statefile
basename     = "vel-x"                           # base name for output files

num_vtu_files   = 800
save_movie   = True      # True = export AVI/MP4 animation
save_images  = False     # True = export static plots

# Animation options
frame_window = [0, 800]     
fps          = 20           
resolution   = [2084, 1008] 

# Static image options
image_format = "pdf"        
image_times  = [0, 200, 400, 800]  

# ================================================================
# Paths: The script resolves paths relative to its location
# ================================================================
# Python script folder
script_dir = os.path.dirname(os.path.abspath(__file__)) # get absolute path of the folder where this script resides
# paraview_dir relative to script
paraview_dir = os.path.join(script_dir, "00_paraview")

# case_dir is parent of paraview_dir
case_dir = os.path.abspath(os.path.join(paraview_dir, ".."))

# data folders
topo_folder = os.path.join(case_dir, "DIVEMesh_Paraview")
vtu_folder  = os.path.join(case_dir, "REEF3D_NHFLOW_VTU")

# ================================================================
# Prepare main output directory
# ================================================================
os.makedirs(paraview_dir, exist_ok=True)

# ================================================================
# Copy statefile into paraview_dir
# ================================================================
statefile_copy = os.path.join(paraview_dir, os.path.basename(statefile))
print(f"Copying statefile to {statefile_copy}")
shutil.copy2(statefile, statefile_copy)

# ================================================================
# Load statefile
# ================================================================
print(f"Loading state file: {statefile_copy}")
LoadState(statefile_copy)

# ================================================================
# Check all registered sources
# ================================================================
sources = GetSources()
print("Registered sources after loading statefile:")
for key in sources:
    print(key)

# ================================================================
# Get Layout
# ================================================================

layout = GetLayout()
view   = GetActiveViewOrCreate("RenderView")

# ================================================================
# Overwrite sources dynamically
# ================================================================
# Find exact registered names
topo_source_name = "REEF3D_Topo.vtp"
vtu_source_name  = "REEF3D-NHFLOW-00000000.pvtu*"

# 1) Topo PolyData
topo_source = FindSource(topo_source_name)  # exact name from Pipeline Browser
topo_source.FileName = os.path.join(topo_folder, topo_source_name)
print(f"Set topo source: {topo_source.FileName}")

# 2) VTU sequence (hardcoded 800 files)
num_vtu_files = 800
vtu_source = FindSource(vtu_source_name)  # exact name from Pipeline Browser
vtu_source.FileName = [os.path.join(vtu_folder, f"REEF3D-NHFLOW-{i:08d}.pvtu") 
                       for i in range(num_vtu_files)]
print(f"Set {num_vtu_files} VTU files for source {vtu_source.SMProxy.GetXMLLabel()}")


# ================================================================
# 1) Save animation(s)
# ================================================================
if save_movie:
    movies_dir = os.path.join(paraview_dir, "movies")
    os.makedirs(movies_dir, exist_ok=True)

    moviefile = os.path.join(movies_dir, f"{basename}.avi")
    print(f"Saving animation: {moviefile}")
    SaveAnimation(
        moviefile,
        viewOrLayout=layout,
        SaveAllViews=1,
        ImageResolution=resolution,
        FrameRate=fps,
        FrameWindow=frame_window
    )

# ================================================================
# 2) Save static images
# ================================================================
if save_images:
    images_dir = os.path.join(paraview_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    for t in image_times:
        print(f" -> Saving frame {t}")
        view.ViewTime = t
        imgfile = os.path.join(images_dir, f"{basename}_t{t}.{image_format}")
        SaveScreenshot(
            imgfile,
            viewOrLayout=view,
            ImageResolution=resolution
        )

print("Done.")
