# Structure des dossiers et fichiers pour nnU-Net v2

## Arborescence des répertoires

```
nnUNet_preprocessed/

nnUNet_raw/
└── Dataset300_Sep/
    ├── imagesTr/          # Images d'entraînement (entrées)
    ├── labelsTr/          # Masques d'entraînement (annotations binaires)
    ├── imagesTs/          # Images de test (facultatif)
    └── dataset.json       # Fichier de configuration du dataset

nnUNet_results/            # Résultats des entraînements
```

---

## Nom des fichiers attendus

- **imagesTr/** :
  ```
  Patient-1_1_0000.png
  Patient-2_2_0000.png
  ...
  ```

- **labelsTr/** :
  ```
  Patient-1_1.png
  Patient-2_2.png
  ...
  ```

🔹 Le suffixe `_0000` désigne le **canal 0** (obligatoire même s’il n’y a qu’une modalité).  
🔹 Les masques doivent porter le **même préfixe** que les images, sans le suffixe de canal.

---

## Contraintes techniques

Ces contraintes sont réglées par le setup_data_nnunet.ipynb.

- Les images et labels doivent être au format `.png`
- Les images doivent être en **niveau de gris (`uint8`)**
- Les labels doivent contenir **uniquement les valeurs 0 (fond) et 1 (lésion)**
- Le fichier `dataset.json` doit inclure :



