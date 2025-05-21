import os
import slicer
import numpy as np
import vtk

# === 📁 Paramètres ===
input_root = r"D:\PIR_SEP\Datasets\Updated_Brain_MRI_Dataset60"
output_root = r"D:\PIR_SEP\Datasets\datagood2"
step_mm = 1.0

views = {
    "Red": "red",       # axial (Z)
    "Green": "green",   # coronal (Y)
    "Yellow": "yellow"  # sagittal (X)
}

# === ⚙️ Fonction de conversion IJK → RAS
def ijk_to_ras(ijk, matrix):
    ras = [0, 0, 0, 1]
    vtk.vtkMatrix4x4.MultiplyPoint(matrix, ijk + [1], ras)
    return ras[:3]

# === ⚙️ Export d'une slice synchronisée
def export_slice(volumeNode, offset_mm, view_name, output_path):
    layoutManager = slicer.app.layoutManager()
    sliceWidget = layoutManager.sliceWidget(view_name)
    sliceLogic = sliceWidget.sliceLogic()
    sliceView = sliceWidget.sliceView()

    sliceLogic.FitSliceToAll()
    sliceLogic.SetSliceOffset(offset_mm)
    slicer.app.processEvents()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sliceView.grab().save(output_path)

# === 🔁 Parcours des volumes ===
for root, _, files in os.walk(input_root):
    for filename in files:
        if filename.lower().endswith(('.nii', '.nrrd', '.mha', '.mhd')):
            input_path = os.path.join(root, filename)
            relative_path = os.path.relpath(input_path, input_root)
            base_name = os.path.splitext(relative_path.replace(os.sep, "_"))[0]

            print(f"🔄 Chargement : {input_path}")
            volumeNode = slicer.util.loadVolume(input_path)
            if not volumeNode:
                print(f"❌ Échec : {filename}")
                continue

            # Dimensions, matrices, etc.
            imageData = volumeNode.GetImageData()
            dims = imageData.GetDimensions()
            spacing = volumeNode.GetSpacing()
            ijk_to_ras_matrix = vtk.vtkMatrix4x4()
            volumeNode.GetIJKToRASMatrix(ijk_to_ras_matrix)

            # Détermine le nombre max de slices dans chaque axe
            slice_counts = []
            slice_centers = []

            for axis_index, view_name in enumerate(views.keys()):
                extent_mm = dims[axis_index] * spacing[axis_index]
                num_slices = int(extent_mm // step_mm)
                slice_counts.append(num_slices)
                center_voxel = dims[axis_index] // 2
                center_offset_mm = center_voxel * spacing[axis_index]
                slice_centers.append(center_offset_mm)

            # Nombre de slices à synchroniser (le plus petit)
            min_count = min(slice_counts)
            print(f"📐 Slices alignées (min across axes): {min_count}")

            for i in range(min_count):
                relative_offset = (i - min_count // 2) * step_mm

                for axis_index, (view_name, folder_name) in enumerate(views.items()):
                    center_offset_mm = slice_centers[axis_index]
                    absolute_offset = center_offset_mm + relative_offset

                    output_dir = os.path.join(output_root, folder_name)
                    output_name = f"{base_name}_{folder_name}_{i:03d}.png"
                    output_path = os.path.join(output_dir, output_name)

                    export_slice(volumeNode, absolute_offset, view_name, output_path)

            slicer.mrmlScene.RemoveNode(volumeNode)

print("✅ Toutes les captures synchronisées sont terminées.")
