import os
import numpy as np
import nibabel as nib
import pydicom
from pydicom.dataset import FileDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian
from datetime import datetime

input_dir = ""
output_dir = ""

os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dir):

    if not file.endswith(".nii") and not file.endswith(".nii.gz"):
        continue

    nii_path = os.path.join(input_dir, file)
    case_name = file.replace(".nii.gz", "").replace(".nii", "")
    case_out = os.path.join(output_dir, case_name)

    os.makedirs(case_out, exist_ok=True)

    nii = nib.load(nii_path)
    volume = nii.get_fdata().astype(np.uint16)

    # get number of slices
    num_slices = volume.shape[2]

    study_uid = generate_uid()
    series_uid = generate_uid()

    for i in range(num_slices):

        slice_data = volume[:, :, i]

        filename = os.path.join(case_out, f"IM_{i:04d}.dcm")

        file_meta = pydicom.dataset.FileMetaDataset()
        file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

        ds = FileDataset(filename, {}, file_meta=file_meta,
                         preamble=b"\0" * 128)

        # Required DICOM tags
        ds.Modality = "OT"
        ds.ContentDate = datetime.now().strftime('%Y%m%d')
        ds.ContentTime = datetime.now().strftime('%H%M%S')

        ds.PatientName = "PancreasMask"
        ds.PatientID = "0000"

        ds.StudyInstanceUID = study_uid
        ds.SeriesInstanceUID = series_uid
        ds.SOPInstanceUID = generate_uid()

        ds.InstanceNumber = i + 1

        ds.Rows, ds.Columns = slice_data.shape

        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"

        ds.PixelRepresentation = 0
        ds.HighBit = 15
        ds.BitsStored = 16
        ds.BitsAllocated = 16

        ds.PixelData = slice_data.tobytes()

        ds.save_as(filename)

    print(f"Converted {file} -> {case_out}")
