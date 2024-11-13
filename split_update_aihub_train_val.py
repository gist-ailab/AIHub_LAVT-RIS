import os
import json
import csv
import glob
import random
from tqdm import tqdm

# Function to update splits with new data, ensuring exactly 16,000 train groups
def update_splits_to_16000_train_groups(input_base_dir_1, input_base_dir_2, existing_csv_file, output_csv_file, total_train_groups=16000):
    # Read existing CSV file
    existing_group_splits = {}
    with open(existing_csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            group_id = row['group_id']
            split = row['set']
            existing_group_splits[group_id] = split

    # Count existing train and validation groups
    train_group_ids = [gid for gid, split in existing_group_splits.items() if split == 'train']
    val_group_ids = [gid for gid, split in existing_group_splits.items() if split == 'validation']

    # Get all group IDs from the data
    ann_list = glob.glob(os.path.join(input_base_dir_1, "*")) + glob.glob(os.path.join(input_base_dir_2, "*"))
    all_group_ids = set()

    for annotation_file in tqdm(ann_list):
        with open(annotation_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

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
    new_group_ids = set(all_group_ids) - set(existing_group_splits.keys())
    print(f"Total group IDs in data: {len(all_group_ids)}")
    print(f"New group IDs not in existing CSV: {len(new_group_ids)}")

    # Assign splits to new group IDs (initially assign to validation)
    for group_id in new_group_ids:
        existing_group_splits[group_id] = 'validation'
        val_group_ids.append(group_id)

    # Update counts after adding new groups to validation
    current_train_count = len(train_group_ids)
    current_val_count = len(val_group_ids)

    print(f"Current train groups: {current_train_count}")
    print(f"Current validation groups (including new groups): {current_val_count}")

    # If current train groups are less than total_train_groups, move validation groups to train
    if current_train_count < total_train_groups:
        needed_train_groups = total_train_groups - current_train_count
        print(f"Needed train groups to reach {total_train_groups}: {needed_train_groups}")

        if len(val_group_ids) >= needed_train_groups:
            # Move needed groups from validation to train
            random.shuffle(val_group_ids)
            groups_to_move = val_group_ids[:needed_train_groups]
            for group_id in groups_to_move:
                existing_group_splits[group_id] = 'train'
                train_group_ids.append(group_id)
            # Remove moved groups from validation list
            val_group_ids = val_group_ids[needed_train_groups:]
        else:
            # Move all validation groups to train
            for group_id in val_group_ids:
                existing_group_splits[group_id] = 'train'
                train_group_ids.append(group_id)
            val_group_ids = []
            # Now, if still not enough, assign new groups (if any) to train
            current_train_count = len(train_group_ids)
            needed_additional_train_groups = total_train_groups - current_train_count
            if needed_additional_train_groups > 0:
                print(f"Not enough validation groups to move. Assigning {needed_additional_train_groups} new groups to train.")
                # All groups have been assigned; cannot assign more groups

    # If current train groups exceed total_train_groups, move some train groups to validation
    elif current_train_count > total_train_groups:
        excess_train_groups = current_train_count - total_train_groups
        print(f"Excess train groups: {excess_train_groups}")
        random.shuffle(train_group_ids)
        groups_to_move = train_group_ids[:excess_train_groups]
        for group_id in groups_to_move:
            existing_group_splits[group_id] = 'validation'
            val_group_ids.append(group_id)
        train_group_ids = train_group_ids[excess_train_groups:]

    # Final counts
    final_train_group_ids = train_group_ids
    final_val_group_ids = val_group_ids
    print(f"Final train groups: {len(final_train_group_ids)}")
    print(f"Final validation groups: {len(final_val_group_ids)}")

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
    # input_dir_1 = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-38.제조환경/실제데이터/annotation"
    # input_dir_2 = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-38.제조환경/가상데이터/annotation"
    # existing_csv_file = "./refer/data/aihub_refcoco_format/manufact_80/group_split.csv"
    # output_csv_file = "./refer/data/aihub_refcoco_format/manufact_80/group_split_updated.csv"

    input_dir_1 = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-39.가정환경/실제데이터/annotation"
    input_dir_2 = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-39.가정환경/가상데이터/annotation"
    existing_csv_file = "refer/data/aihub_refcoco_format/indoor_80/group_split.csv"
    output_csv_file = "refer/data/aihub_refcoco_format/indoor_80/group_split_updated.csv"

    update_splits_to_16000_train_groups(input_dir_1, input_dir_2, existing_csv_file, output_csv_file, total_train_groups=16000)
