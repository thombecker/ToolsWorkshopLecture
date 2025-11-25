#!/bin/bash

# @autor: ronja ehlers

# ausführen:

# sh download_results.sh MODELNAME
# z.B.
# sh download_results.sh NHFLOW

# ---------------------------------------
#          CONFIGURATION
# ---------------------------------------

remote="2025-0424-1638"                    # Remote result folder name
remotebase="username@betzy.sigma2.no:/cluster/work/users/username/03_cases"

# --- Input Argument ---
model=$1  # Model name (e.g. CFD, NHFLOW, SFLOW)
if [ -z "$model" ]; then
    echo "❗ Bitte gib ein Modell als Argument an (z.B. sh download_results.sh NHFLOW)"
    exit 1
fi

# --- Local folder name ---
local=${PWD##*/}

# ---------------------------------------
#         START DOWNLOAD PROCESS
# ---------------------------------------

# --- Start ---
echo "Downloading results for model: $model"
echo "Remote folder: $remote"
echo "Local folder:  $local"

# --- Basic files ---
rsync -avz "$remotebase/$remote/c"* .
rsync -avz "$remotebase/$remote/log.*" .
rsync -avz "$remotebase/$remote/DIVEMesh_Paraview" .
rsync -avz "$remotebase/$remote/REEF3D_"*Log* .

# ---------------------------------------
#              WATER DATA
# ---------------------------------------

# rsync -avz "$remotebase/$remote/REEF3D_${model}_WSF" .                        # Free surface elevation
# rsync -avz "$remotebase/$remote/REEF3D_${model}_WSFLINE" .                    # Water level along a line (e.g. P52)
# rsync -avz "$remotebase/$remote/REEF3D_${model}_WSFLINE_Y" .                  # Cross-sectional water level (e.g. P56)
# rsync -avz "$remotebase/$remote/REEF3D_${model}_ProbeLine" .                  # Line probes (e.g. P62)
# rsync -avz "$remotebase/$remote/REEF3D_${model}_ProbePoint" .                 # Point probes (e.g. P61 for CFD, P63 for SFLOW)

# ---------------------------------------
#            SEDIMENT DATA
# ---------------------------------------

# rsync -avz "$remotebase/$remote/REEF3D_${model}_SedimentPoint" .             # Bed shear stress, bed level (e.g. P121, P125, P126)
# rsync -avz "$remotebase/$remote/REEF3D_${model}_SedimentMax" .               # Maximum bed change (e.g. P122)

# mkdir -p "REEF3D_${model}_SedimentLine"                                   # Sediment profile lines (e.g. P123, P124)

# # Example: selective sediment profile lines
# rsync -avz "$remotebase/$remote/REEF3D_${model}_SedimentLine/REEF3D-${model}-bedprobe_line_x-023795*" "./REEF3D_${model}_SedimentLine/"
# rsync -avz "$remotebase/$remote/REEF3D_${model}_SedimentLine/REEF3D-${model}-bedprobe_line_x-532230*" "./REEF3D_${model}_SedimentLine/"
# rsync -avz "$remotebase/$remote/REEF3D_${model}_SedimentLine/REEF3D-${model}-bedprobe_line_x-101660*" "./REEF3D_${model}_SedimentLine/"
# rsync -avz "$remotebase/$remote/REEF3D_${model}_SedimentLine/REEF3D-${model}-bedprobe_line_x-212930*" "./REEF3D_${model}_SedimentLine/"
# rsync -avz "$remotebase/$remote/REEF3D_${model}_SedimentLine/REEF3D-${model}-bedprobe_line_x-330800*" "./REEF3D_${model}_SedimentLine/"
# rsync -avz "$remotebase/$remote/REEF3D_${model}_SedimentLine/REEF3D-${model}-bedprobe_line_x-444785*" "./REEF3D_${model}_SedimentLine/"

# # Download all sediment lines:
# rsync -avz "$remotebase/$remote/REEF3D_${model}_SedimentLine" .              # All sediment profiles

# ---------------------------------------
#               VTU DATA
# ---------------------------------------

vtu_folder="REEF3D_${model}_VTU"

# --- Option 1: download selected  files ---
mkdir -p "$vtu_folder"
# rsync -avz "$remotebase/$remote/$vtu_folder/REEF3D-${model}-00000000*" "./$vtu_folder/" # REEF3D-${model}-00000000* this is one group of one iteration
rsync -avz "$remotebase/$remote/$vtu_folder/REEF3D-${model}-000000*" "./$vtu_folder/"

# --- Option 2: download the entire folder (uncomment to use) ---
# rsync -avz "$remotebase/$remote/$vtu_folder" .  # This creates the folder and downloads everything into it
 


# ---------------------------------------
#               VTP DATA BED
# ---------------------------------------

# vtp_folder="REEF3D_${model}_VTP_BED"

# --- Option 1: download selected files ---
# mkdir -p "$vtp_folder"
# rsync -avz "$remotebase/$remote/$vtp_folder/REEF3D-${model}-000000*" "./$vtp_folder/"

# --- Option 2: download the entire folder (uncomment to use) ---
# rsync -avz "$remotebase/$remote/$vtp_folder" .  # This creates the folder and downloads everything into it


# ---------------------------------------
#               VTP DATA FSF
# ---------------------------------------

# vtp_folder="REEF3D_${model}_VTP_FSF"

# --- Option 1: download selected files ---
# mkdir -p "$vtp_folder"
# rsync -avz "$remotebase/$remote/$vtp_folder/REEF3D-${model}-000000*" "./$vtp_folder/"

# --- Option 2: download the entire folder (uncomment to use) ---
# rsync -avz "$remotebase/$remote/$vtp_folder" .  # This creates the folder and downloads everything into it