import os
import shutil

def copy_folder(src, dst, excluded_extensions=None):
    if excluded_extensions is None:
        excluded_extensions = {'.pth', '.h5', '.nii.gz'}
    else:
        excluded_extensions = set(excluded_extensions)

    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        dest_path = os.path.join(dst, rel_path)
        os.makedirs(dest_path, exist_ok=True)
        for file in files:
            src_file_path = os.path.join(root, file)
            dst_file_path = os.path.join(dest_path, file)
            file_extension = os.path.splitext(file)[1]
            if file_extension not in excluded_extensions:
                shutil.copy2(src_file_path, dst_file_path)

# Example usage:
source_folder = r'G:/MRI_Code/'
destination_folder = r'C:/Users/VLADKONATA/Desktop/TAO_MRI'

copy_folder(source_folder, destination_folder, excluded_extensions={'.pth', '.h5', '.nii.gz'})
