import os
import random
import shutil

base_dir = r"C:\Users\nparo\OneDrive\GT - Mahidol\Class\2nd\ITGT523 Computer Vision\ITGT523_Naddanai\Yolo_2"
image_dir = os.path.join(base_dir, "dataset", "images")  
label_dir = os.path.join(base_dir, "dataset", "labels")  

splits = ["train", "val", "test"]
split_ratio = [0.8, 0.1, 0.1]  

for split in splits:
    os.makedirs(os.path.join(base_dir, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, split, "labels"), exist_ok=True)

image_files = [f for f in os.listdir(image_dir) if f.endswith((".jpg", ".png"))]
random.shuffle(image_files)  

train_count = int(len(image_files) * split_ratio[0])
val_count = int(len(image_files) * split_ratio[1])

train_files = image_files[:train_count]
val_files = image_files[train_count:train_count + val_count]
test_files = image_files[train_count + val_count:]

def move_files(files, split):
    for file in files:
        shutil.move(os.path.join(image_dir, file), os.path.join(base_dir, split, "images", file))
        label_file = file.replace(".jpg", ".txt").replace(".png", ".txt")
        if os.path.exists(os.path.join(label_dir, label_file)):
            shutil.move(os.path.join(label_dir, label_file), os.path.join(base_dir, split, "labels", label_file))

move_files(train_files, "train")
move_files(val_files, "val")
move_files(test_files, "test")