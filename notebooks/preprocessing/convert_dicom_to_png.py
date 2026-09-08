import os
import pydicom
import numpy as np
from PIL import Image

# Paths
dcm_root = ""
png_root = ""

def convert_dcm_to_png(dcm_root, png_root):
    for patient_folder in os.listdir(dcm_root):
        patient_path = os.path.join(dcm_root, patient_folder)
        if not os.path.isdir(patient_path):
            continue

        # Create corresponding folder in PNG directory
        png_patient_path = os.path.join(png_root, patient_folder)
        os.makedirs(png_patient_path, exist_ok=True)

        print(f"Processing {patient_folder}...")

        for dcm_file in os.listdir(patient_path):
            if not dcm_file.lower().endswith(".dcm"):
                continue

            dcm_file_path = os.path.join(patient_path, dcm_file)
            png_file_name = os.path.splitext(dcm_file)[0] + ".png"
            png_file_path = os.path.join(png_patient_path, png_file_name)

            try:
                ds = pydicom.dcmread(dcm_file_path)
                img_array = ds.pixel_array

                # Normalize to 0-255
                img_array = img_array.astype(float)
                img_array -= img_array.min()
                if img_array.max() > 0:
                    img_array = img_array / img_array.max() * 255
                img_array = img_array.astype(np.uint8)

                img = Image.fromarray(img_array)
                img.save(png_file_path, "PNG")

            except Exception as e:
                print(f"❌ Failed: {dcm_file_path} → {e}")

        print(f"✅ Finished {patient_folder}")

convert_dcm_to_png(dcm_root, png_root)