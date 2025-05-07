import os
import slicer
from slicer.util import loadVolume

# === 📁 Paramètres à modifier ===
input_root = r"D:\PIR_SEP\Datasets\Brain_MRI_Dataset_of_Multiple_Sclerosis_with_Consensus_Manual_Lesion_Segmentation_and_Patient_Meta_Information"
output_root = r"D:\PIR_SEP\Datasets\BRAIN_MRI_SLICES_yellow"
target_z_mm = 11.0  # Z en mm où capturer la tranche
view_name = "Green"  # Vue coronal (avant/arrière)

# === ⚙️ Fonction d’export d’une slice ===
def export_slice_at_position(volumeNode, output_file_path, slice_z_mm, view_name="Yellow"):
    layoutManager = slicer.app.layoutManager()
    sliceWidget = layoutManager.sliceWidget(view_name)
    sliceView = sliceWidget.sliceView()
    sliceLogic = sliceWidget.sliceLogic()

    sliceLogic.FitSliceToAll()
    sliceLogic.SetSliceOffset(slice_z_mm)
    slicer.app.processEvents()

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    sliceView.grab().save(output_file_path)

# === 🔁 Parcours récursif des sous-dossiers ===
for root, _, files in os.walk(input_root):
    for filename in files:
        if filename.lower().endswith(('.nii', '.nrrd', '.mha', '.mhd')):
            input_path = os.path.join(root, filename)
            relative_path = os.path.relpath(input_path, input_root)
            base_name = os.path.splitext(relative_path.replace(os.sep, "_"))[0]  # nom plat
            output_path = os.path.join(output_root, base_name + ".png")

            print(f"🔄 Chargement de : {input_path}")
            success, volumeNode = loadVolume(input_path, returnNode=True)
            if not success:
                print(f"❌ Échec du chargement : {filename}")
                continue

            print(f"📸 Capture à {target_z_mm} mm → {base_name}.png")
            export_slice_at_position(volumeNode, output_path, target_z_mm, view_name)

            slicer.mrmlScene.RemoveNode(volumeNode)

print("✅ Toutes les captures sont terminées.")
