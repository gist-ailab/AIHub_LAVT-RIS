

# import os
# import json
# import csv
# import glob
# import random
# from tqdm import tqdm

# def split_data(input_base_dir_1, input_base_dir_2, existing_csv_file, output_csv_file, num_test_groups=2000):
#     # 기존 CSV 파일에서 그룹 ID와 스플릿 읽기
#     group_splits = {}
#     with open(existing_csv_file, 'r', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             group_id = row['group_id']
#             split = row['set']
#             group_splits[group_id] = split

#     # 기존 그룹 ID 목록
#     existing_group_ids = set(group_splits.keys())

#     # 데이터에서 모든 그룹 ID 수집
#     ann_list = glob.glob(os.path.join(input_base_dir_1, "group_*", "annotation", "*.json")) + \
#                glob.glob(os.path.join(input_base_dir_2, "group_*", "annotation", "*.json"))
#     all_group_ids = set()
#     for annotation_file in tqdm(ann_list):
#         # 데이터 유형 판별 ('real' 또는 'syn')
#         if '/real/' in annotation_file:
#             data_type = 'real'
#         elif '/synthetic/' in annotation_file:
#             data_type = 'syn'
#         else:
#             print(f"데이터 유형을 판별할 수 없습니다: {annotation_file}")
#             continue

#         # 그룹 ID 추출
#         group_dir = os.path.dirname(os.path.dirname(annotation_file))
#         group_num = os.path.basename(group_dir).split('_')[1]  # group_000001에서 숫자 부분 추출
#         group_id = f"{data_type}_{group_num}"  # 예: 'real_000001' 또는 'syn_000001'
#         all_group_ids.add(group_id)

#     # 새로운 그룹 ID 식별 (기존 CSV에 없는 그룹)
#     new_group_ids = all_group_ids - existing_group_ids

#     # 새로운 그룹 ID는 모두 train으로 지정
#     for gid in new_group_ids:
#         group_splits[gid] = 'train'

#     # 기존 validation 그룹 ID 목록
#     existing_validation_group_ids = [gid for gid, split in group_splits.items() if split == 'validation']

#     # 기존 validation 그룹에서 2000개를 무작위로 선택하여 test로 이동
#     if len(existing_validation_group_ids) >= num_test_groups:
#         test_group_ids = random.sample(existing_validation_group_ids, num_test_groups)
#     else:
#         print(f"validation 그룹 수가 {num_test_groups}보다 적습니다. 전체를 test로 지정합니다.")
#         test_group_ids = existing_validation_group_ids.copy()

#     # 선택된 그룹을 test로 지정
#     for gid in test_group_ids:
#         group_splits[gid] = 'test'

#     # 나머지 validation 그룹은 그대로 유지
#     remaining_validation_group_ids = [gid for gid in existing_validation_group_ids if gid not in test_group_ids]

#     # 최종 그룹별 스플릿 계산
#     final_train_group_ids = [gid for gid, split in group_splits.items() if split == 'train']
#     final_validation_group_ids = remaining_validation_group_ids
#     final_test_group_ids = test_group_ids

#     # 결과를 CSV로 저장
#     csv_data = [{'group_id': group_id, 'set': group_splits[group_id]} for group_id in group_splits]
#     with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
#         fieldnames = ['group_id', 'set']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for row in csv_data:
#             writer.writerow(row)

#     # 최종 그룹 수 출력
#     print(f"최종 그룹 수:")
#     print(f"Train 그룹 수: {len(final_train_group_ids)}")
#     print(f"Validation 그룹 수: {len(final_validation_group_ids)}")
#     print(f"Test 그룹 수: {len(final_test_group_ids)}")
#     print(f"CSV 파일이 {output_csv_file}에 저장되었습니다.")

# # if __name__ == "__main__":
#     # # 어노테이션 디렉토리 (실제 경로로 수정하세요)
#     # input_dir_1 = "/SSDb/sangbeom_lee/2.라벨링데이터/real"
#     # input_dir_2 = "/SSDb/sangbeom_lee/2.라벨링데이터/synthetic"
#     # existing_csv_file = "/SSDb/sangbeom_lee/existing_group_splits.csv"  # 기존 CSV 파일 경로
#     # output_csv_file = "/SSDb/sangbeom_lee/output_group_splits.csv"  # 결과를 저장할 CSV 파일 경로

#     # split_data(input_dir_1, input_dir_2, existing_csv_file, output_csv_file, total_test_groups=2000)

# if __name__ == "__main__":
#     # 어노테이션 디렉토리 (실제 경로로 수정하세요)
#     input_dir_1 = "/SSDb/sangbeom_lee/2.라벨링데이터/real"
#     input_dir_2 = "/SSDb/sangbeom_lee/2.라벨링데이터/synthetic"
#     existing_csv_file = "refer/data/aihub_refcoco_format/group_split.csv"  # 기존 validation 그룹이 포함된 CSV 파일 경로
#     output_csv_file = "refer/data/aihub_refcoco_format/output_group_splits.csv"  # 결과를 저장할 CSV 파일 경로
    
#     split_data(input_dir_1, input_dir_2, existing_csv_file, output_csv_file, num_test_groups=2000)

import os
import json
import csv
import glob
import random
from tqdm import tqdm

def split_data(input_base_dir_1, input_base_dir_2, existing_csv_file, output_csv_file, num_test_groups=2000):
    # 기존 CSV 파일에서 그룹 ID와 스플릿 읽기
    group_splits = {}
    with open(existing_csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            group_id = row['group_id']
            split = row['set']
            group_splits[group_id] = split

    # 기존 그룹 ID 목록
    existing_group_ids = set(group_splits.keys())

    # 데이터에서 모든 그룹 ID 수집
    ann_list = glob.glob(os.path.join(input_base_dir_1, "group_*", "annotation", "*.json")) + \
               glob.glob(os.path.join(input_base_dir_2, "group_*", "annotation", "*.json"))
    all_group_ids = set()
    for annotation_file in tqdm(ann_list):
        # 데이터 유형 판별 ('real' 또는 'syn')
        if '/real/' in annotation_file:
            data_type = 'real'
        elif '/synthetic/' in annotation_file:
            data_type = 'syn'
        else:
            print(f"데이터 유형을 판별할 수 없습니다: {annotation_file}")
            continue

        # 그룹 ID 추출
        group_dir = os.path.dirname(os.path.dirname(annotation_file))
        group_num = os.path.basename(group_dir).split('_')[1]  # group_000001에서 숫자 부분 추출
        group_id = f"{data_type}_{group_num}"  # 예: 'real_000001' 또는 'syn_000001'

        # 그룹의 어노테이션 파일이 실제로 존재하는지 확인
        if not os.path.exists(annotation_file):
            continue  # 파일이 존재하지 않으면 스킵

        all_group_ids.add(group_id)

    # 새로운 그룹 ID 식별 (기존 CSV에 없는 그룹)
    new_group_ids = all_group_ids - existing_group_ids

    # 새로운 그룹 ID는 모두 train으로 지정
    for gid in new_group_ids:
        group_splits[gid] = 'train'

    # 기존 validation 그룹 ID 목록 중 실제로 존재하는 그룹만 선택
    existing_validation_group_ids = [gid for gid, split in group_splits.items() if split == 'validation' and gid in all_group_ids]

    # 기존 validation 그룹에서 num_test_groups개의 그룹을 무작위로 선택하여 test로 이동
    if len(existing_validation_group_ids) >= num_test_groups:
        test_group_ids = random.sample(existing_validation_group_ids, num_test_groups)
    else:
        print(f"validation 그룹 수가 {num_test_groups}보다 적습니다. 전체를 test로 지정합니다.")
        test_group_ids = existing_validation_group_ids.copy()

    # 선택된 그룹을 test로 지정
    for gid in test_group_ids:
        group_splits[gid] = 'test'

    # 나머지 validation 그룹은 그대로 유지
    remaining_validation_group_ids = [gid for gid in existing_validation_group_ids if gid not in test_group_ids]

    # 최종 그룹별 스플릿 계산
    final_train_group_ids = [gid for gid, split in group_splits.items() if split == 'train']
    final_validation_group_ids = remaining_validation_group_ids
    final_test_group_ids = test_group_ids

    # 결과를 CSV로 저장
    csv_data = [{'group_id': group_id, 'set': group_splits[group_id]} for group_id in group_splits]
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['group_id', 'set']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)

    # 최종 그룹 수 출력
    print(f"최종 그룹 수:")
    print(f"Train 그룹 수: {len(final_train_group_ids)}")
    print(f"Validation 그룹 수: {len(final_validation_group_ids)}")
    print(f"Test 그룹 수: {len(final_test_group_ids)}")
    print(f"CSV 파일이 {output_csv_file}에 저장되었습니다.")

if __name__ == "__main__":
    # 어노테이션 디렉토리 (실제 경로로 수정하세요)
    input_dir_1 = "/SSDb/sangbeom_lee/2.라벨링데이터/real"
    input_dir_2 = "/SSDb/sangbeom_lee/2.라벨링데이터/synthetic"
    existing_csv_file = "refer/data/aihub_refcoco_format/group_split.csv"  # 기존 validation 그룹이 포함된 CSV 파일 경로
    output_csv_file = "refer/data/aihub_refcoco_format/output_group_splits.csv"  # 결과를 저장할 CSV 파일 경로

    split_data(input_dir_1, input_dir_2, existing_csv_file, output_csv_file, num_test_groups=2000)
