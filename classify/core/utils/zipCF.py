from ultralytics import YOLO
import os
import shutil
from zipfile import ZipFile
from pathlib import Path


utils_path = Path(__file__).parent

class ZipClassifier:
    @classmethod
    def make_zip(cls, input_dir, output_dir):
        with ZipFile(output_dir, 'w') as zip_object:
            # Traverse all files and directories in the input directory
            for root, directories, files in os.walk(input_dir):
                for file in files:
                    # Create the file path
                    file_path = os.path.join(root, file)
                    # Create the relative path within the zip archive
                    arcname = os.path.relpath(file_path, input_dir)
                    # Add the file to the zip archive with the relative path
                    zip_object.write(file_path, arcname)
                    # carry\files\output_files\test_input.zip
        return "\\".join(output_dir.split("\\")[-5:])

    @classmethod
    def classify(cls, input_dir, output_dir):
        model = YOLO(utils_path / 'best3.pt')
        classes = ["balaclava", "banknote", "baseball_bat", "blood",
            "cigarette", "drug", "fire", "knife", "pistol", "rifle", "other",]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        preds = []

        for f in os.listdir(input_dir):
            img = os.path.join(input_dir, f)

            results = model(img)

            probs = results[0].probs

            top1 = results[0].probs.numpy().top1conf
            preds.append(top1)

            pred_class = probs.top1
            if  top1 <= 0.85:
                pred_class = -1

            dst = os.path.join(output_dir, classes[pred_class])

            if not os.path.exists(dst):
                os.makedirs(dst)

            shutil.copyfile(img, os.path.join(dst, os.path.basename(img)))
        zipped = cls.make_zip(output_dir, str(output_dir) + ".zip")
        return zipped
