import os
import json
import cv2
import numpy as np
from pycocotools import mask as maskUtils
import re
from tqdm import tqdm
import glob

def sanitize_filename(filename):
    # Remove or replace characters that are invalid in filenames
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = filename.strip().replace(" ", "_")
    return filename

def decode_segmentation(segmentation, height, width):
    """
    Decodes the segmentation data into a binary mask.
    """
    if isinstance(segmentation, list):
        # Polygon format
        rles = maskUtils.frPyObjects(segmentation, height, width)
        rle = maskUtils.merge(rles)
    elif isinstance(segmentation, dict):
        # RLE format
        counts = segmentation.get('counts')
        if isinstance(counts, list):
            # Uncompressed RLE
            rle = segmentation
        elif isinstance(counts, str):
            # Compressed RLE
            rle = segmentation.copy()
            rle['counts'] = counts.encode('utf-8')
        else:
            print(f"Unknown counts format in segmentation.")
            return None
    elif isinstance(segmentation, str):
        # Compressed RLE string
        rle = {'size': [height, width], 'counts': segmentation.encode('utf-8')}
    else:
        print(f"Unknown segmentation format.")
        return None

    try:
        mask = maskUtils.decode(rle)
        return mask
    except Exception as e:
        print(f"Error decoding segmentation: {e}")
        return None

def visualize_specific_files(annotation_dir, output_dir, desired_file_names):
    """
    Visualizes annotations for specific files with the desired file names.

    Parameters:
    - annotation_dir: Directory containing the annotation JSON files.
    - output_dir: Directory where visualized images will be saved.
    - desired_file_names: List of desired file names to search for.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Prepare a set of desired file names for quick lookup
    desired_file_names_set = set(desired_file_names)

    # Get a list of all annotation files in the directory
    annotation_files = glob.glob(os.path.join(annotation_dir, '**', '*.json'), recursive=True)

    for annotation_file in tqdm(annotation_files, desc="Processing annotations"):
        # Extract image file name from the annotation
        image_file = annotation_file.replace("annotation", "rgb")
        image_file = image_file.replace("json", "png")

        # Construct the file name
        if image_file.split('/')[-3] == '실제데이터':
            file_name = f"real_{image_file.split('/')[-1]}"
        elif image_file.split('/')[-3] == '가상데이터':
            file_name = f"syn_{image_file.split('/')[-1]}"
        else:
            file_name = image_file.split('/')[-1]

        # Check if the file name is in the desired file names
        if file_name not in desired_file_names_set:
            continue  # Skip files that are not desired

        with open(annotation_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Load the image
        image = cv2.imread(image_file)
        if image is None:
            print(f"Failed to read image {image_file}")
            continue

        height, width, _ = image.shape

        # Process each annotation within the JSON file
        for ann in data.get('annotations', []):
            mask = decode_segmentation(ann['segmentation'], height, width)
            if mask is None:
                print(f"Skipping annotation {ann.get('id', 'unknown')} due to segmentation decoding issues.")
                continue

            if mask.ndim == 3:
                mask = np.any(mask, axis=2).astype(np.uint8)

            mask = mask * 255  # Convert to 0 or 255

            # Create color overlay
            overlay_color = [0, 255, 0]  # Green color
            alpha = 0.5  # Transparency factor

            overlay = image.copy()
            overlay[mask == 255] = overlay_color

            blended = cv2.addWeighted(image, 1 - alpha, overlay, alpha, 0)

            # Get the referring expression
            ref_expr = ann.get('referring_expression', 'no_ref_expr')
            sanitized_ref_expr = sanitize_filename(ref_expr)
            sanitized_ref_expr = sanitized_ref_expr.replace(" ", "_")
            sanitized_ref_expr = sanitized_ref_expr[:50]  # Limit length to avoid filename issues

            output_filename = f"{os.path.splitext(file_name)[0]}_{ann['id']}_{sanitized_ref_expr}.png"
            output_image_path = os.path.join(output_dir, output_filename)

            # Save the blended image
            cv2.imwrite(output_image_path, blended)

            # If you only want to process the first matching file, you can uncomment the following line
            # return

if __name__ == "__main__":
    # Specify the annotation directory and the output directory
    # annotation_dir = "/SSDa/sangbeom_lee/22-39.가정환경/가상데이터/annotation"  # Replace with your annotation directory path
    annotation_dir = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-39.가정환경/가상데이터/annotation"  # Replace with your annotation directory path
    output_dir = "aihub_vis_100_fix"          # Replace with your desired output directory path

    # annotation_dir = "/media/sblee/170d6766-97d9-4917-8fc6-7d6ae84df896/aihub_2024_datasets/사숲 공유본/22-38.제조환경/가상데이터/annotation"  # Replace with your annotation directory path
    # output_dir = "aihub_vis_manu_100"          # Replace with your desired output directory path

    os.makedirs(output_dir, exist_ok=True)  

    # Specify the desired file names
    desired_file_names = [
        # "real_image123.png",
        "syn_003947_000000.png",
        "syn_003948_000000.png",
        "syn_003968_000000.png",
        "syn_003975_000000.png",
        "syn_003976_000000.png",
        "syn_003983_000000.png"
        # Add 1or40file names as needed
    ]

    # # Initialize the list to store desired file names
    # desired_file_names = []

    # # Define the starting and ending numbers
    # start_number = 2340
    # end_number = 2519
    # increment = 1  # You can change this to 1 for every file or any other increment

    # # Generate the file names using a for loop
    # for i in range(start_number, end_number + 1, increment):
    #     # If you want to skip specific numbers, you can add a condition here
    #     # For example, to skip 4000:
    #     # if i == 4000:
    #     #     continue
    #     # Format the number with leading zeros to ensure it's 6 digits
    #     file_number = f"{i:06d}"
    #     file_name = f"syn_{file_number}_000000.png"
    #     desired_file_names.append(file_name)

    # Print or use the list as needed
    print(desired_file_names)

    visualize_specific_files(annotation_dir, output_dir, desired_file_names)

