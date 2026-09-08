import os
from PIL import Image

# Paths to your datasets
labels_root = ""
ct_root     = ""

def remove_black_slices(labels_root, ct_root):
    for patient_label_folder in os.listdir(labels_root):
        label_path = os.path.join(labels_root, patient_label_folder)
        if not os.path.isdir(label_path):
            continue

        # Derive corresponding CT folder name
        # patient_ct_folder = patient_label_folder.replace("LABEL_", "")
        # ct_path = os.path.join(ct_root, patient_ct_folder)
        patient_ct_folder = patient_label_folder  # Assuming same folder name for CT and label
        ct_path = os.path.join(ct_root, patient_ct_folder)
        if not os.path.exists(ct_path):
            print(f" CT folder missing: {ct_path}")
            continue

        for label_file in os.listdir(label_path):
            if not label_file.endswith(".png"):
                continue

            label_file_path = os.path.join(label_path, label_file)

            # Open label and check if all-black
            img = Image.open(label_file_path)
            if img.getbbox() is None:  # getbbox() returns None if all pixels are 0
                print(f"Removing black label: {label_file_path}")
                os.remove(label_file_path)

                # Determine corresponding CT slice
                # label_0001.png → 1-0001.dcm
                # slice_number = label_file.split("_")[-1].split(".")[0][1:]  # '0001'
                # ct_file_name = f"1-{slice_number}.dcm"
                ct_file_path = os.path.join(ct_path, label_file)

                if os.path.exists(ct_file_path):
                    print(f"Removing corresponding CT slice: {ct_file_path}")
                    os.remove(ct_file_path)
                else:
                    print(f" CT slice not found: {ct_file_path}")

if __name__ == "__main__":
    remove_black_slices(labels_root, ct_root)