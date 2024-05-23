from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
 
def unzip_file(input_file, output_path):
    # open the zip file
    with ZipFile(input_file, 'r') as handle:
        # start the thread pool
        with ThreadPoolExecutor(100) as exe:
            # unzip each file from the archive
            _ = [exe.submit(handle.extract, m, output_path) for m in handle.namelist()]

    # path = Path(input_file)
    # filename_without_extension = path.stem
    result = str(Path(output_path) / os.listdir(output_path)[0])
    print("UNZIPEED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    os.remove(input_file)
    
    return result
 