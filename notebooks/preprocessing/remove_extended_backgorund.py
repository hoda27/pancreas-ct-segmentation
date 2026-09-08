import cv2
import numpy as np
import os

# Root folders (PNG versions)
ct_root = ""
labels_root = ""

# Output folders
ct_output_root = ""
labels_output_root = ""

os.makedirs(ct_output_root, exist_ok=True)
os.makedirs(labels_output_root, exist_ok=True)

threshold = 10  # adjust if black is not pure black

for patient_label_folder in os.listdir(labels_root):
    label_folder_path = os.path.join(labels_root, patient_label_folder)
    if not os.path.isdir(label_folder_path):
        continue

    # Corresponding CT folder
    # patient_ct_folder = patient_label_folder.replace("pancreas", "")
    # ct_folder_path = os.path.join(ct_root, patient_ct_folder)
    # Assuming same folder name for CT and label
    patient_ct_folder = patient_label_folder
    ct_folder_path = os.path.join(ct_root, patient_ct_folder)
    if not os.path.exists(ct_folder_path):
        print(f" CT folder missing for {patient_label_folder}, skipping.")
        continue

    # Create output folders
    ct_output_folder = os.path.join(ct_output_root, patient_ct_folder)
    label_output_folder = os.path.join(
        labels_output_root, patient_label_folder)
    os.makedirs(ct_output_folder, exist_ok=True)
    os.makedirs(label_output_folder, exist_ok=True)

    print(f"Processing patient: {patient_label_folder}")

    for label_file in os.listdir(label_folder_path):
        if not label_file.lower().endswith(".png"):
            continue

        label_file_path = os.path.join(label_folder_path, label_file)

        # # Determine corresponding CT file
        # slice_number = label_file.split("_")[-1].split(".")[0][1:]  # e.g., '0001'
        # ct_file_name = f"1-{slice_number}.png"
        ct_file_path = os.path.join(ct_folder_path, label_file)

        if not os.path.exists(ct_file_path):
            print(f" CT slice not found for {label_file}, skipping.")
            continue

        # Read images
        img = cv2.imread(ct_file_path)
        mask = cv2.imread(label_file_path)

        if img is None or mask is None:
            print(
                f" Could not read {ct_file_path} or {label_file_path}, skipping.")
            continue

        # Convert CT to grayscale for cropping
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find non-black rows
        non_black_rows = np.where(np.any(gray > threshold, axis=1))[0]
        if len(non_black_rows) == 0:
            print(f"All black CT slice {label_file}, skipping.")
            continue

        last_row = non_black_rows[-1] + 1

        # Crop both CT and label
        cropped_img = img[:last_row, :]
        cropped_mask = mask[:last_row, :]

        # Save cropped results
        cv2.imwrite(os.path.join(ct_output_folder, label_file), cropped_img)
        cv2.imwrite(os.path.join(
            label_output_folder, label_file), cropped_mask)

        print(f" Cropped {label_file} and {label_file}")

print("\n All patients cropped")
print(f"CT images saved to: {ct_output_root}")
print(f"Labels saved to:  {labels_output_root}")
