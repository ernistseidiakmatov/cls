# import zipfile
# import os

# def unzip_file(zip_file_path, output_folder):
#     with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#         zip_ref.extractall(output_folder)
#     return output_folder



from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor
import os
 
def unzip_file(input_file, output_path):
    # open the zip file
    with ZipFile(input_file, 'r') as handle:
        # start the thread pool
        with ThreadPoolExecutor(100) as exe:
            # unzip each file from the archive
            _ = [exe.submit(handle.extract, m, output_path) for m in handle.namelist()]

    return os.path.join(output_path, input_file.split("/")[-1][:-4])
 
