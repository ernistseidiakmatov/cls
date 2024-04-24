import ultralytics
from ultralytics import YOLO
import os
import shutil

# ultralytics.checks()

model = YOLO('lastTrain/best3.pt')  # give right path

input_dir = "lastTrain/testSample3"

classes = ["balaclava", "banknote", "baseball_bat", "blood",
        "cigarette", "drug", "fire", "knife", "pistol", "rifle", "other",]

er = []
output_dir = "lastTrain/output6"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

preds = []
p_d = {}

for f in os.listdir(input_dir):
  img = os.path.join(input_dir, f)

  # try:
  results = model(img)

  probs = results[0].probs
  
  top1 = results[0].probs.numpy().top1conf
  preds.append(top1)
  # pred_class = 8
  pred_class = probs.top1
  if  top1 <= 0.85:
      pred_class = -1
      p_d[img] = top1
  


  dst = os.path.join(output_dir, classes[pred_class])

  if not os.path.exists(dst):
    os.makedirs(dst)
  
  shutil.copyfile(img, os.path.join(dst, os.path.basename(img)))
  print(img, "done")
  # except Exception as e:
  #    er.append(f + f" {e}")
  #    continue

print(er)
print(sum(preds)/len(preds))

print(p_d)