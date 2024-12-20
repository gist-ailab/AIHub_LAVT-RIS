import os
import json
import pickle
import random
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import pycocotools.mask as mask_util
import re


def generate_mask_from_segmentation(segmentation, image_size):
    """Generate a binary mask image from RLE segmentation data."""
    if isinstance(segmentation, dict):
        # RLE format
        mask = mask_util.decode(segmentation)
        return mask
    elif isinstance(segmentation, list):
        # If segmentation is a list of RLEs
        mask = np.zeros((image_size[1], image_size[0]), dtype=np.uint8)
        for seg in segmentation:
            mask += mask_util.decode(seg)
        return mask
    else:
        print("Segmentation format not supported.")
        return None

def sanitize_filename(text):
    """Sanitize text to create a valid filename."""
    # Remove any invalid characters
    text = re.sub(r'[\\/*?:"<>|]', '', text)
    # Limit the length of the filename
    return text[:50]

# Paths to data files (replace with your actual paths)
instances_json_file = 'refer/data/aihub_refcoco_format/manufact_80/instances_2.json'  # Replace with the path to your instances.json
refs_pickle_file = 'refer/data/aihub_refcoco_format/manufact_80/refs_2.p'            # Replace with the path to your refs.p
images_dir = 'refer/data/aihub_refcoco_format/manufact_80/images'                  # Replace with the path to your images directory
output_dir = 'refer/data/aihub_refcoco_format/manufact_80/visualizations'           # Replace with the path to your output directory

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the COCO annotations
with open(instances_json_file, 'r', encoding='utf-8') as f:
    coco_data = json.load(f)

# Load the referring annotations
with open(refs_pickle_file, 'rb') as f:
    referring_data = pickle.load(f)

# Map image_id to image info
images = {}
for img in coco_data['images']:
    images[img['id']] = img

# Map ann_id to annotation
annotations = {}
for ann in coco_data['annotations']:
    annotations[ann['id']] = ann

<<<<<<< HEAD
N = 100  # Number of samples to check
=======
N = 10000  # Number of samples to check
>>>>>>> 8a681019233734173b6f2ff99160f5b61c7c7c06
sample_refs = random.sample(referring_data, N)

# Sample ann_id is 139465
# sample_refs = [ref for ref in referring_data if ref['ref_id'] == 139465]

for idx, ref in enumerate(sample_refs):
# for idx, ref in enumerate(referring_data):
    ref_id = ref['ref_id']
    image_id = ref['image_id']
    ann_id = ref['ann_id']
    file_name = ref['file_name']
    sentences = ref['sentences']
    print(f"Processing Ref ID: {ref_id}")

    # Get image info
    img_info = images.get(image_id)
    if img_info is None:
        print(f"Image ID {image_id} not found.")
        continue
    img_file_name = img_info['file_name']
    img_path = os.path.join(images_dir, img_file_name)

    # Load image
    if not os.path.exists(img_path):
        print(f"Image file {img_path} not found.")
        continue
    img = Image.open(img_path).convert('RGB')

    # Get annotation
    ann = annotations.get(ann_id)
    if ann is None:
        print(f"Annotation ID {ann_id} not found.")
        continue

    # Get segmentation
    segmentation = ann['segmentation']

    # Generate mask
    mask = generate_mask_from_segmentation(segmentation, (img_info['width'], img_info['height']))
    if mask is None:
        print(f"Could not generate mask for Annotation ID {ann_id}.")
        continue

    # Resize mask if necessary
    if mask.shape[0] != img_info['height'] or mask.shape[1] != img_info['width']:
        mask = np.resize(mask, (img_info['height'], img_info['width']))

    # Create a figure without displaying it
    plt.figure(figsize=(12, 6))

    # Display the original image
    plt.subplot(1, 3, 1)
    plt.imshow(img)
    plt.axis('off')
    plt.title('Image')

    # Display the mask
    plt.subplot(1, 3, 2)
    plt.imshow(mask, cmap='gray')
    plt.axis('off')
    plt.title('Mask')

    # Display the overlay of the mask on the image
    plt.subplot(1, 3, 3)
    plt.imshow(img)
    plt.imshow(mask, alpha=0.5, cmap='jet')
    plt.axis('off')
    plt.title('Overlay')

     # Combine sentences into a single string
    referring_text = '_'.join([s['sent'] for s in sentences])

    # Sanitize the referring text for filename
    sanitized_text = sanitize_filename(referring_text)

    # Construct the output filename
    output_filename = f'ref_{ref_id}_file_{file_name}_ann_{ann_id}_{sanitized_text}.png'
    output_path = os.path.join(output_dir, output_filename)

    # Save the figure to the output directory
    plt.savefig(output_path)
    plt.close()  # Close the figure to free up memory

    print(f"Saved visualization to {output_path}")