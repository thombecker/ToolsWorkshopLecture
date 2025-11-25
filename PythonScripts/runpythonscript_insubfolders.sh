#!/bin/bash

# Script to run a specified Python script in all subfolders of the current directory,
# skipping specified folders, and logging the results.

# =========================================================
# INPUT SECTION
# =========================================================

# === Full path to the Python interpreter: Dependend on Computer and which python environment to use ===
PYTHON="/Users/xxx/my_python/venv/bin/python" # MacBook Pro M1
# PYTHON="/Applications/ParaView-5.13.3.app/Contents/bin/pvbatch" #  Paraview MacBook Pro M1

# === Name of the Python script to be executed in each subfolder ===
SCRIPT="mainlog.py"
# SCRIPT="wavegauges_single.py"
# SCRIPT="wsfline.py"
# SCRIPT="sedline.py"
# SCRIPT="bedshearstress_gauges_single.py"

# === Folders to skip (space-separated) ===
SKIP_FOLDERS=("00" "data" "exp" "00_post" "00_post_wave" "00_post_sed")  # add more folder names as needed

# =========================================================
# END OF INPUT
# =========================================================
# Name of the log file where results will be recorded
LOGFILE="execution_log.txt"

# Start the log file with a header and timestamp
echo "Execution Log - $(date)" > "$LOGFILE"
echo "-------------------------" >> "$LOGFILE"

# Loop through all subdirectories in the current folder
for dir in */ ; do
    # Remove trailing slash
    dir_name="${dir%/}"

    # Skip folder if in SKIP_FOLDERS
    skip=false
    for skip_dir in "${SKIP_FOLDERS[@]}"; do
        if [ "$dir_name" = "$skip_dir" ]; then
            skip=true
            break
        fi
    done
    if [ "$skip" = true ]; then
        echo "Skipping folder $dir_name"
        continue
    fi

    echo "------------------------------------------"
    echo "Processing $dir"
    echo "------------------------------------------"
    
    # Copy the Python script into the current subdirectory
    cp "$SCRIPT" "$dir"
    
    # Change into the subdirectory
    cd "$dir"
    
    # Write the current directory and timestamp to the log file
    echo -n "[$(date)] $dir: " >> "../$LOGFILE"
    
    # Run the Python script and check if it succeeds
    if "$PYTHON" "$SCRIPT"; then
        echo "Success" >> "../$LOGFILE"
    else
        echo "Failed" >> "../$LOGFILE"
    fi

    # Optionally remove the script after execution to keep folders clean
    # rm "$SCRIPT"
    
    # Return to the parent directory
    cd ..
done
