import os
import json
import csv
import glob
import random
from tqdm import tqdm

# Function to update splits, ensuring 16,000 train groups, 2,000 validation groups, and 2,000 test groups
def update_splits_with_validation_and_test(
    input_base_dir_1,
    input_base_dir_2,
    existing_csv_file,
    output_csv_file,
    total_train_groups=16000,
    validation_groups=2000,
    test_groups=2000
):
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

    # Assign splits to new group IDs, adding to train if needed to reach total_train_groups
    current_train_count = len(train_group_ids)
    needed_train_groups = total_train_groups - current_train_count
    print(f"Current train groups: {current_train_count}")
    print(f"Needed train groups to reach {total_train_groups}: {needed_train_groups}")

    # Convert new_group_ids to list and shuffle
    new_group_ids = list(new_group_ids)
    random.shuffle(new_group_ids)

    # Assign splits to new group IDs
    if needed_train_groups > 0:
        # Assign new group IDs to train until we reach total_train_groups
        new_train_group_ids = new_group_ids[:needed_train_groups]
        remaining_new_group_ids = new_group_ids[needed_train_groups:]
    else:
        # No additional train groups needed
        new_train_group_ids = []
        remaining_new_group_ids = new_group_ids

    # Add new train groups to existing splits
    for group_id in new_train_group_ids:
        existing_group_splits[group_id] = 'train'

    # Combine existing validation groups and remaining new groups
    combined_val_groups = val_group_ids + remaining_new_group_ids

    # Total validation and test groups needed
    total_val_test_needed = validation_groups + test_groups
    current_val_test_count = len(combined_val_groups)
    print(f"Total validation and test groups needed: {total_val_test_needed}")
    print(f"Current available validation groups: {current_val_test_count}")

    if current_val_test_count < total_val_test_needed:
        # Need to move groups from train to validation/test
        needed_extra_groups = total_val_test_needed - current_val_test_count
        print(f"Not enough validation/test groups. Moving {needed_extra_groups} groups from train to validation/test.")
        # Randomly select groups to move from train to validation/test
        random.shuffle(train_group_ids)
        groups_to_move = train_group_ids[:needed_extra_groups]
        # Update splits
        for group_id in groups_to_move:
            existing_group_splits[group_id] = 'validation'  # Temporarily assign to validation
        # Update lists
        combined_val_groups.extend(groups_to_move)
        train_group_ids = train_group_ids[needed_extra_groups:]

    # Now assign validation and test splits
    random.shuffle(combined_val_groups)
    final_val_group_ids = combined_val_groups[:validation_groups]
    final_test_group_ids = combined_val_groups[validation_groups:validation_groups + test_groups]

    # Update splits in existing_group_splits
    for group_id in final_val_group_ids:
        existing_group_splits[group_id] = 'validation'
    for group_id in final_test_group_ids:
        existing_group_splits[group_id] = 'test'

    # Any remaining groups (if combined_val_groups is larger) are assigned to validation
    extra_groups = combined_val_groups[validation_groups + test_groups:]
    for group_id in extra_groups:
        existing_group_splits[group_id] = 'validation'

    # Re-count groups
    final_train_group_ids = [gid for gid, split in existing_group_splits.items() if split == 'train']
    final_val_group_ids = [gid for gid, split in existing_group_splits.items() if split == 'validation']
    final_test_group_ids = [gid for gid, split in existing_group_splits.items() if split == 'test']

    print(f"Final train groups: {len(final_train_group_ids)}")
    print(f"Final validation groups: {len(final_val_group_ids)}")
    print(f"Final test groups: {len(final_test_group_ids)}")

    # Save updated splits to CSV
    csv_data = [{'group_id': group_id, 'set': split} for group_id, split in existing_group_splits.items()]

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
    # existing_csv_file = "refer/data/aihub_refcoco_format/manufact_80/group_split.csv"
    # output_csv_file = "refer/data/aihub_refcoco_format/manufact_80/group_split_updated.csv"

    input_dir_1 = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-39.가정환경/실제데이터/annotation"
    input_dir_2 = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-39.가정환경/가상데이터/annotation"
    existing_csv_file = "refer/data/aihub_refcoco_format/indoor_80/group_split.csv"
    output_csv_file = "refer/data/aihub_refcoco_format/indoor_80/group_split_updated.csv"

    update_splits_with_validation_and_test(
        input_dir_1,
        input_dir_2,
        existing_csv_file,
        output_csv_file,
        total_train_groups=16000,
        validation_groups=2000,
        test_groups=2000
    )
