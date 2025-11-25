#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Updated on Wed Jul 30 2025
Author: ronja ehlers
"""

import os
import subprocess
from paraview.simple import *

# === SETTINGS ===

# Input files
input_vtp = "00_post_vtk/averaged_output.vtp"
input_bed_pvtp = "../REEF3D_SFLOW_VTP_BED/REEF3D-SFLOW-BED-00000000.pvtp"
# Output directory
output_dir = "00_post_vtk/plots"
os.makedirs(output_dir, exist_ok=True) # make the output directory if it does not exist
# Output names
# Get the name of the folder the script is in
script_dir = os.path.dirname(os.path.abspath(__file__))
folder_name = os.path.basename(script_dir)


# Parameter name -> colorbar label
parameters = {
    "velocity_magnitude": "$\|u\|$ $[$m/s$]$",
    "velocity_x": "$u$ $[$m/s$]$",
    "velocity_y": "$v$ $[$m/s$]$",
    "velocity_z": "$w$ $[$m/s$]$",
    "pressure": "$p$ $[$Pa$]$",
    "waterlevel": "$h$ $[$m$]$",
    "eta": "$\\eta$ $[$m$]$",
}

# Optional: Define custom color limits
color_limits = {
    "velocity_magnitude": [0, 1.2],
    "velocity_x": [-0.5, 0.5],
    "velocity_y": [-0.5, 0.5],
    "velocity_z": [-0.3, 0.3],
    "waterlevel": [-0.001, 0.09],
    "eta": [-0.22, 0.0],
}

label_formats = {
    "pressure": "%.1e",
    "velocity_magnitude": "%.2f",
    "velocity_x": "%.2f",
    "velocity_y": "%.2f",
    "velocity_z": "%.2f",
    "waterlevel": "%.3f",
    "eta": "%.2f",
}


# === LOAD AND PREPARE DATA ===

mesh = OpenDataFile(input_vtp)
mesh.UpdatePipeline()

bed_mesh = OpenDataFile(input_bed_pvtp)
bed_mesh.UpdatePipeline()


# === Add velocity magnitude and components ===

if "velocity" in mesh.PointData.keys():
    calc_mag = Calculator(Input=mesh)
    calc_mag.Function = "mag(velocity)"
    calc_mag.ResultArrayName = "velocity_magnitude"
    calc_mag.UpdatePipeline()

    calc_x = Calculator(Input=mesh)
    calc_x.Function = "velocity_X"
    calc_x.ResultArrayName = "velocity_x"
    calc_x.UpdatePipeline()

    calc_y = Calculator(Input=mesh)
    calc_y.Function = "velocity_Y"
    calc_y.ResultArrayName = "velocity_y"
    calc_y.UpdatePipeline()

    calc_z = Calculator(Input=mesh)
    calc_z.Function = "velocity_Z"
    calc_z.ResultArrayName = "velocity_z"
    calc_z.UpdatePipeline()

    final_mesh = AppendAttributes(Input=[mesh, calc_mag, calc_x, calc_y, calc_z])
    final_mesh.UpdatePipeline()
else:
    final_mesh = mesh

# === Compute figure size ===

final_mesh.UpdatePipeline()
bounds = final_mesh.GetDataInformation().GetBounds()
xmin, xmax, ymin, ymax, zmin, zmax = bounds
xrange = xmax - xmin
yrange = ymax - ymin

scale = 1000  # pixels per unit
plot_width = int(xrange * scale)
plot_height = int(yrange * scale)

extra_width = 200  # space for colorbar
render_size = [plot_width + extra_width, plot_height]

print(f"xrange = {xrange}, yrange = {yrange}, plot_width = {plot_width}, plot_height = {plot_height}")
print(f"RenderView size: {render_size}")

print("Bounds:", bounds)
print(f"x: {xmin} to {xmax} meters")
print(f"y: {ymin} to {ymax} meters")

# === Prepare view ===
LoadPalette(paletteName='WhiteBackground')
renderView = GetActiveViewOrCreate('RenderView')
renderView.ViewSize = render_size
renderView.InteractionMode = '2D'
renderView.OrientationAxesVisibility = 0

# === Display bed mesh ===
bed_display = Show(bed_mesh, renderView)
bed_display.Representation = 'Surface' 

# === Loop over parameters ===

for param, label in parameters.items():
    if param not in final_mesh.PointData.keys():
        print(f"Skipping '{param}': Not found.")
        continue

    display = Show(final_mesh, renderView)
    ColorBy(display, ('POINTS', param))
    lut = GetColorTransferFunction(param)

    # Set color range
    if param in color_limits:
        lut.RescaleTransferFunction(*color_limits[param])
    else:
        lut.RescaleTransferFunction(*final_mesh.PointData[param].GetRange())

    lut.ApplyPreset("Cool to Warm (Extended)", True)
    lut.ColorSpace = 'Diverging'


    # Show scalar bar
    display.SetScalarBarVisibility(renderView, True)
    ResetCamera(renderView)
    
    scalarBar = GetScalarBar(lut, renderView)
    scalarBar.WindowLocation = 'Any Location'
    scalarBar.Title = label
    scalarBar.TitleFontSize = 30
    scalarBar.LabelFontSize = 30
    scalarBar.TitleFontFamily = 'Times'
    scalarBar.LabelFontFamily = 'Times'
    scalarBar.AutomaticLabelFormat = 0
    scalarBar.LabelFormat = label_formats.get(param, "%.2f")
    scalarBar.RangeLabelFormat = label_formats.get(param, "%.2f")
    scalarBar.Orientation = 'Vertical'
    scalarBar.Position = [0.92, 0.1]  # Fix position right-bottom
    scalarBar.ScalarBarLength = 0.8  # percentage of the plot height
    scalarBar.ScalarBarThickness = 50

    # Control camera
    renderView.CameraParallelProjection = 1
    renderView.CameraPosition = [(xmin + xmax) / 2, (ymin + ymax) / 2, 1000]  # high z-value
    renderView.CameraFocalPoint = [(xmin + xmax) / 2, (ymin + ymax) / 2, 0]
    renderView.CameraViewUp = [0, 1, 0]

    # Zoom
    renderView.CameraParallelScale = (ymax - ymin)*0.6

    # Axis
    renderView.AxesGrid.Visibility = 1
    renderView.AxesGrid.XTitle = ""
    renderView.AxesGrid.YTitle = ""
    renderView.AxesGrid.ZTitle = ""
    renderView.AxesGrid.XTitleFontSize = 20
    renderView.AxesGrid.YTitleFontSize = 20
    renderView.AxesGrid.ZTitleFontSize = 20
    renderView.AxesGrid.XLabelFontSize = 30
    renderView.AxesGrid.YLabelFontSize = 30
    renderView.AxesGrid.ZLabelFontSize = 30

    renderView.AxesGrid.XTitleFontFamily = 'Times'
    renderView.AxesGrid.YTitleFontFamily = 'Times'
    renderView.AxesGrid.ZTitleFontFamily = 'Times'
    renderView.AxesGrid.XLabelFontFamily = 'Times'
    renderView.AxesGrid.YLabelFontFamily = 'Times'
    renderView.AxesGrid.ZLabelFontFamily = 'Times'

    renderView.AxesGrid.XAxisUseCustomLabels = 1
    renderView.AxesGrid.XAxisLabels = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.25]

    renderView.AxesGrid.YAxisUseCustomLabels = 1
    renderView.AxesGrid.YAxisLabels = [0.05, 0.25, 0.5, 0.75, 0.99]

    Render()

    # EXPORT
    svg_path = os.path.join(output_dir, f"{folder_name}_{param}.svg")
    pdf_direct_path = os.path.join(output_dir, f"{folder_name}_{param}_direct.pdf")

    # ExportView(svg_path, renderView)
    # print(f"Saved SVG: {svg_path}")

    try:
        ExportView(pdf_direct_path, renderView, Rasterize3Dgeometry=0)
        print(f"Saved PDF directly from ParaView: {pdf_direct_path}")
    except Exception as e:
        print(f"Direct PDF export from ParaView failed: {e}")

    # Cleanup display
    display.SetScalarBarVisibility(renderView, False)
    Delete(display)
    Render()

print("All plots done.")
