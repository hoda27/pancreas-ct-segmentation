import os
from PIL import Image

input_dir = ""
output_dir = ""

os.makedirs(output_dir, exist_ok=True)

for case in os.listdir(input_dir):

    case_path = os.path.join(input_dir, case)

    if not os.path.isdir(case_path):
        continue

    output_case = os.path.join(output_dir, case)
    os.makedirs(output_case, exist_ok=True)

    for file in os.listdir(case_path):

        if file.lower().endswith(".png"):

            img_path = os.path.join(case_path, file)
            img = Image.open(img_path)

            # rotate 90° clockwise
            rotated = img.rotate(-90, expand=True)

            save_path = os.path.join(output_case, file)
            rotated.save(save_path)

    print(f"Processed {case}")

print("Done.")