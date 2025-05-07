import os
import slicer
from slicer.util import loadVolume

# === 📁 Paramètres à modifier ===
input_folder = r"D:\PIR SEP\Datasets\Brain_MRI_Dataset_of_Multiple_Sclerosis_with_Consensus_Manual_Lesion_Segmentation_and_Patient_Meta_Information"
output_folder = r"D:\PIR_SEP\Datasets\BRAIN_MRI_SLICES"
target_z_mm = 11.0  # Z en mm où capturer la tranche axiale
view_name = "Red"   # Vue axiale

# === ⚙️ Fonction pour exporter UNE tranche à une coordonnée Z donnée en mm ===
def export_slice_at_position(volumeNode, output_file_path, slice_z_mm, view_name="Red"):
    layoutManager = slicer.app.layoutManager()
    sliceWidget = layoutManager.sliceWidget(view_name)
    sliceView = sliceWidget.sliceView()
    sliceLogic = sliceWidget.sliceLogic()

    # Centrer et ajuster la vue
    sliceLogic.FitSliceToAll()

    # Placer la vue à la coordonnée Z souhaitée
    sliceLogic.SetSliceOffset(slice_z_mm)
    slicer.app.processEvents()

    # Sauvegarder l'image
    sliceView.grab().save(output_file_path)

# === 🚀 Boucle sur les fichiers du dossier ===
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.nii', '.nrrd', '.mha', '.mhd')):
        filepath = os.path.join(input_folder, filename)
        print(f"🔄 Chargement de : {filename}")
        success, volumeNode = loadVolume(filepath, returnNode=True)
        if not success:
            print(f"❌ Échec du chargement : {filename}")
            continue

        # Générer le nom de sortie PNG
        base_name = os.path.splitext(filename)[0]
        output_file_path = os.path.join(output_folder, base_name + ".png")

        # Exporter la tranche à 11 mm
        print(f"📸 Capture de la tranche à {target_z_mm} mm pour {base_name}")
        export_slice_at_position(volumeNode, output_file_path, target_z_mm, view_name)

        # Nettoyage
        slicer.mrmlScene.RemoveNode(volumeNode)

print("✅ Capture terminée.")
