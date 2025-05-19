import os
import pandas as pd
import nibabel as nib
import numpy as np

# Chemins
excel_path = r"D:\PIR_SEP\Datasets\spacing.xlsx"
nifti_root_dir = r"D:\PIR_SEP\Datasets\Brain MRI Dataset of Multiple Sclerosis with Consensus Manual Lesion Segmentation and Patient Meta Information_Thomas"
output_root_dir = r"D:\PIR_SEP\Datasets\Updated_Nifti"

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(output_root_dir, exist_ok=True)

# Lire l'Excel
df = pd.read_excel(excel_path)
df['ID'] = df['ID'].astype(str)
df['Spacing Between Slices'] = df['Spacing Between Slices'].astype(str).str.replace(',', '.').astype(float)

# Parcourir tous les fichiers dans tous les sous-dossiers
for root, dirs, files in os.walk(nifti_root_dir):
    for file in files:
        if file.endswith(".nii") or file.endswith(".nii.gz"):
            file_id = file.split("-")[0]  # l'ID est au début du nom de fichier
            if file_id in df['ID'].values:
                z_spacing = df.loc[df['ID'] == file_id, 'Spacing Between Slices'].values[0]

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, nifti_root_dir)
                output_dir = os.path.join(output_root_dir, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                # Charger l'image
                img = nib.load(file_path)
                header = img.header.copy()
                affine = img.affine.copy()

                # Ancien spacing
                old_spacing = header.get_zooms()
                new_spacing = (old_spacing[0], old_spacing[1], z_spacing)

                # Créer une nouvelle image avec nouveau spacing
                new_affine = np.diag([*new_spacing, 1])
                new_img = nib.Nifti1Image(img.get_fdata(), affine=new_affine, header=header)
                new_img.header.set_zooms(new_spacing)

                output_path = os.path.join(output_dir, file)
                nib.save(new_img, output_path)
                print(f"✔ {file} (ID {file_id}) -> spacing z mis à jour à {z_spacing} mm")
