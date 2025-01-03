import os
import json
import csv
import glob
import random
from tqdm import tqdm

# Function to split dataset into train, validation, and test sets
def update_splits_to_train_val_test(input_base_dir_1, input_base_dir_2, existing_csv_file, output_csv_file, total_train_groups=16000, total_val_groups=2000, total_test_groups=2000):
    # Read existing CSV file
    existing_group_splits = {}
    with open(existing_csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            group_id = row['group_id']
            split = row['set']
            existing_group_splits[group_id] = split

    # Collect existing train and validation group IDs
    existing_train_group_ids = [gid for gid, split in existing_group_splits.items() if split == 'train']
    existing_validation_group_ids = [gid for gid, split in existing_group_splits.items() if split == 'validation']

    # Get all group IDs from the data
    ann_list = glob.glob(os.path.join(input_base_dir_1, "*")) + glob.glob(os.path.join(input_base_dir_2, "*"))
    all_group_ids = set()

    for annotation_file in tqdm(ann_list):
        # Since the annotation files might not be JSON files, we can skip files that can't be opened
        try:
            with open(annotation_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            continue

        # Extract image file name from the annotation and derive group_id
        image_file = annotation_file.replace("annotation", "rgb").replace("json", "png")
        
        if image_file.split('/')[-3] == '실제데이터':
            file_name = f"real_{image_file.split('/')[-1]}"
        elif image_file.split('/')[-3] == '가상데이터':
            file_name = f"syn_{image_file.split('/')[-1]}"
        
        group_id = '_'.join(file_name.split('_')[0:2])
        all_group_ids.add(group_id)

    # Identify new group IDs not present in existing CSV
    all_group_ids = list(all_group_ids)
    new_group_ids = list(set(all_group_ids) - set(existing_group_splits.keys()))
    print(f"Total group IDs in data: {len(all_group_ids)}")
    print(f"New group IDs not in existing CSV: {len(new_group_ids)}")

    total_needed_groups = total_train_groups + total_val_groups + total_test_groups

    if total_needed_groups > len(all_group_ids):
        print(f"Not enough group IDs to meet the desired splits.")
        print(f"Total group IDs available: {len(all_group_ids)}")
        print(f"Total group IDs needed: {total_needed_groups}")
        # You can adjust the total_*_groups variables here if needed
        return

    # Initialize splits
    train_group_ids = existing_train_group_ids.copy()
    test_group_ids = []
    validation_group_ids = []

    # Shuffle existing validation group IDs
    random.shuffle(existing_validation_group_ids)

    # Assign existing validation groups to test set preferentially
    if len(existing_validation_group_ids) >= total_test_groups:
        test_group_ids = existing_validation_group_ids[:total_test_groups]
        remaining_validation_ids = existing_validation_group_ids[total_test_groups:]
    else:
        test_group_ids = existing_validation_group_ids
        remaining_validation_ids = []

    # Add any excess existing validation groups to validation set
    validation_group_ids.extend(remaining_validation_ids)

    # Shuffle new group IDs
    random.shuffle(new_group_ids)

    # Assign new group IDs to validation set to reach total_val_groups
    needed_validation_groups = total_val_groups - len(validation_group_ids)
    if needed_validation_groups > 0:
        groups_to_add = new_group_ids[:needed_validation_groups]
        validation_group_ids.extend(groups_to_add)
        new_group_ids = new_group_ids[needed_validation_groups:]

    # Assign remaining new group IDs to train set to reach total_train_groups
    needed_train_groups = total_train_groups - len(train_group_ids)
    if needed_train_groups > 0:
        groups_to_add = new_group_ids[:needed_train_groups]
        train_group_ids.extend(groups_to_add)
        new_group_ids = new_group_ids[needed_train_groups:]

    # Check if there are still unassigned group IDs (unlikely)
    if new_group_ids:
        print(f"Warning: There are {len(new_group_ids)} unassigned group IDs.")

    # Update existing_group_splits with the new assignments
    for group_id in train_group_ids:
        existing_group_splits[group_id] = 'train'

    for group_id in validation_group_ids:
        existing_group_splits[group_id] = 'validation'

    for group_id in test_group_ids:
        existing_group_splits[group_id] = 'test'

    print(f"Final counts:")
    print(f"Train groups: {len(train_group_ids)}")
    print(f"Validation groups: {len(validation_group_ids)}")
    print(f"Test groups: {len(test_group_ids)}")

    # Save updated splits to CSV
    csv_data = [{'group_id': group_id, 'set': existing_group_splits[group_id]} for group_id in existing_group_splits]

    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['group_id', 'set']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)

    print(f"Updated CSV file saved to {output_csv_file}")
    print(f"Total groups: {len(existing_group_splits)}")

if __name__ == "__main__":
    # Directories containing the annotations
    input_dir_1 = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-38.제조환경/실제데이터/annotation"
    input_dir_2 = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-38.제조환경/가상데이터/annotation"
    existing_csv_file = "./refer/data/aihub_refcoco_format/manufact_80/group_split.csv"
    output_csv_file = "./refer/data/aihub_refcoco_format/manufact_80/group_split_updated.csv"

    # # Directories containing the annotations
    # input_dir_1 = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-39.가정환경/실제데이터/annotation"
    # input_dir_2 = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-39.가정환경/가상데이터/annotation"
    # existing_csv_file = "refer/data/aihub_refcoco_format/indoor_80/group_split.csv"
    # output_csv_file = "refer/data/aihub_refcoco_format/indoor_80/group_split_updated.csv"

    update_splits_to_train_val_test(
        input_dir_1,
        input_dir_2,
        existing_csv_file,
        output_csv_file,
        total_train_groups=16000,
        total_val_groups=2000,
        total_test_groups=2000
    )
