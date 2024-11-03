import os
import json
import glob
import random
from tqdm import tqdm
import csv

def split_groups_with_fixed_train_size(input_base_dir_1, input_base_dir_2, output_csv_file, total_train_groups=16000):
    # 모든 주석 파일을 수집합니다.
    ann_list = glob.glob(os.path.join(input_base_dir_1, "*.json")) + glob.glob(os.path.join(input_base_dir_2, "*.json"))
    
    group_to_files = {}

    # 각 주석 파일에 대해 그룹 ID를 추출하고 해당하는 파일을 매핑합니다.
    for annotation_file in tqdm(ann_list, desc="Processing annotation files"):
        # 주석 파일에서 이미지 파일 이름을 추출합니다.
        image_file = annotation_file.replace("annotation", "rgb")
        image_file = image_file.replace(".json", ".png")
        
        # 실제 데이터와 가상 데이터를 구분하여 파일 이름을 생성합니다.
        if "실제데이터" in image_file:
            file_name = f"real_{os.path.basename(image_file)}"
        elif "가상데이터" in image_file:
            file_name = f"syn_{os.path.basename(image_file)}"
        else:
            print(f"Unexpected directory in path: {image_file}")
            continue  # 예상치 못한 경로는 건너뜁니다

        # 파일 이름에서 그룹 ID를 추출합니다.
        # 그룹 ID는 파일 이름의 첫 두 부분으로 구성됩니다.
        group_id = '_'.join(file_name.split('_')[0:2])

        # 그룹 ID를 키로 하여 해당 파일 이름을 리스트에 추가합니다.
        if group_id not in group_to_files:
            group_to_files[group_id] = []
        group_to_files[group_id].append(file_name)
    
    # 이미지가 정확히 5개인 그룹들을 수집합니다.
    groups_with_5_images = [group_id for group_id, files in group_to_files.items() if len(files) == 5]
    num_groups_with_5_images = len(groups_with_5_images)
    print(f"Number of groups with exactly 5 images: {num_groups_with_5_images}")

    # 훈련 세트에 무작위로 16,000개의 그룹을 선택합니다.
    if num_groups_with_5_images >= total_train_groups:
        random.shuffle(groups_with_5_images)
        train_group_ids = groups_with_5_images[:total_train_groups]
        remaining_groups = groups_with_5_images[total_train_groups:]
    else:
        print(f"Warning: Only {num_groups_with_5_images} groups with 5 images available. All will be used for training.")
        train_group_ids = groups_with_5_images
        remaining_groups = []

    # 남은 그룹(이미지가 5개인 그룹 중 훈련 세트에 포함되지 않은 그룹)을 검증 세트에 추가합니다.
    val_group_ids = remaining_groups

    # 이미지 수가 5개가 아닌 그룹들을 검증 세트에 추가합니다.
    other_groups = [group_id for group_id, files in group_to_files.items() if len(files) != 5]
    val_group_ids.extend(other_groups)

    print(f"Total train groups: {len(train_group_ids)}")
    print(f"Total validation groups: {len(val_group_ids)}")

    # CSV 파일에 저장할 데이터를 준비합니다.
    csv_data = []
    for group_id in train_group_ids:
        csv_data.append({'group_id': group_id, 'set': 'train'})
    for group_id in val_group_ids:
        csv_data.append({'group_id': group_id, 'set': 'validation'})
    
    # CSV 파일로 저장합니다.
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['group_id', 'set']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)
    
    print(f"CSV file saved to {output_csv_file}")

if __name__ == "__main__":

    # 80 percent AIHub indoor 
    # input_dir_1 = "/SSDa/sangbeom_lee/22-39.가정환경/실제데이터/annotation"
    # input_dir_2 = "/SSDa/sangbeom_lee/22-39.가정환경/가상데이터/annotation"
    # output_csv_file = "/SSDa/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/indoor_80/group_split.csv"

    # 입력 디렉토리를 설정합니다.
    input_dir_1 = "/SSDe/sangbeom_lee/22-38.제조환경/실제데이터/annotation"
    input_dir_2 = "/SSDe/sangbeom_lee/22-38.제조환경/가상데이터/annotation"
    output_csv_file = "/SSDe/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/manufact_80/group_split.csv"

    # 함수를 호출하여 그룹을 train과 validation으로 나눕니다.
    split_groups_with_fixed_train_size(input_dir_1, input_dir_2, output_csv_file, total_train_groups=16000)
