import os
import json
import pickle
from datetime import datetime
import glob
import shutil
import random
import logging
from tqdm import tqdm
import csv



# Function to split annotations from multiple files and save as JSON and Pickle files
def split_annotations_for_dataset(input_base_dir_1, input_base_dir_2, output_csv_file, total_train_groups=16000):
    # Prepare the COCO-style structure for vision annotations
    
    # Iterate through all groups
    ann_list = glob.glob(os.path.join(input_base_dir_1, "*")) + glob.glob(os.path.join(input_base_dir_2, "*"))
    
    group_ids = set()
    group_to_files = {}

    for annotation_file in tqdm(ann_list):
        
        with open(annotation_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract image file name from the annotation and compare with the actual image file
        image_file = annotation_file.replace("annotation", "rgb")
        image_file = image_file.replace("json", "png")
        
        
        if image_file.split('/')[-3] == '실제데이터':
            file_name = f"real_{image_file.split('/')[-1]}"
        elif image_file.split('/')[-3] == '가상데이터':
            file_name = f"syn_{image_file.split('/')[-1]}"
        
        group_id = '_'.join(file_name.split('_')[0:2])
        group_ids.add(group_id)
        
    # Convert the set of group IDs to a list for indexing
    group_ids = list(group_ids)
    print(len(group_ids))
    # Shuffle the group IDs to randomize
    random.shuffle(group_ids)
    
    # Split into train and validation sets
    train_group_ids = group_ids[:total_train_groups]
    val_group_ids = group_ids[total_train_groups:]
    
    # Prepare data for CSV
    csv_data = []
    for group_id in train_group_ids:
        csv_data.append({'group_id': group_id, 'set': 'train'})
    for group_id in val_group_ids:
        csv_data.append({'group_id': group_id, 'set': 'validation'})
    
    # Save to CSV file
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['group_id', 'set']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)
    
    print(f"Total groups: {len(group_ids)}")
    print(f"Train groups: {len(train_group_ids)}")
    print(f"Validation groups: {len(val_group_ids)}")
    print(f"CSV file saved to {output_csv_file}")


if __name__ == "__main__":

    # 80 percent AIHub indoor 
    input_dir_1 = "/SSDa/sangbeom_lee/22-39.가정환경/실제데이터/annotation"
    input_dir_2 = "/SSDa/sangbeom_lee/22-39.가정환경/가상데이터/annotation"
    # output_vision_file = "/SSDa/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/indoor_80/instances.json"
    # output_referring_file = "/SSDa/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/indoor_80/refs.p"
    output_csv_file = "/SSDa/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/indoor_80/group_split.csv"


    # 80 percent AIHub manufact 
    # input_dir_1 = "/SSDe/sangbeom_lee/22-38.제조환경/실제데이터/annotation"
    # input_dir_2 = "/SSDe/sangbeom_lee/22-38.제조환경/가상데이터/annotation"
    # output_vision_file = "/SSDe/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/manufact_80/instances.json"
    # output_referring_file = "/SSDe/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/manufact_80/refs.p"
    # output_csv_file = "/SSDe/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/manufact_80/group_split.csv"

    # convert_to_refcoco_format(input_dir, output_file)
    split_annotations_for_dataset(input_dir_1, input_dir_2, output_csv_file, total_train_groups=16000)
    