import datetime
import os
import time

import torch
import torch.utils.data
from torch import nn

from bert.modeling_bert import BertModel
import torchvision

from lib import segmentation
import transforms as T
import utils

import numpy as np
from PIL import Image
import torch.nn.functional as F

import torchvision.transforms as T_t
import numpy as np
from PIL import Image
from scipy.ndimage.morphology import binary_dilation


def get_dataset(image_set, transform, args):
    from data.dataset_refer_bert import ReferDataset
    ds = ReferDataset(args,
                      split=image_set,
                      image_transforms=transform,
                      target_transforms=None,
                      eval_mode=True
                      )
    num_classes = 2
    return ds, num_classes


def evaluate(model, data_loader, bert_model, device):
    def overlay_davis(image, mask, colors=[[0, 0, 0], [255, 0, 0]], cscale=1, alpha=0.4):
        colors = np.reshape(colors, (-1, 3))
        colors = np.atleast_2d(colors) * cscale

        im_overlay = image.copy()
        object_ids = np.unique(mask)

        for object_id in object_ids[1:]:
            # Overlay color on binary mask
            foreground = image * alpha + np.ones(image.shape) * (1 - alpha) * np.array(colors[object_id])
            binary_mask = mask == object_id

            # Compose image
            im_overlay[binary_mask] = foreground[binary_mask]

            # Contours
            countours = binary_dilation(binary_mask) ^ binary_mask
            im_overlay[countours, :] = 0

        return im_overlay.astype(image.dtype)

    model.eval()
    metric_logger = utils.MetricLogger(delimiter="  ")

    # evaluation variables
    cum_I, cum_U = 0, 0
    eval_seg_iou_list = [.5, .6, .7, .8, .9]
    seg_correct = np.zeros(len(eval_seg_iou_list), dtype=np.int32)
    seg_total = 0
    mean_IoU = []
    header = 'Test:'

    # Counter for naming visualizations
    vis_counter = 0

    with torch.no_grad():
        for data in metric_logger.log_every(data_loader, 100, header):
            image, target, sentences, attentions, info = data
            image, target, sentences, attentions = image.to(device), target.to(device), \
                                                   sentences.to(device), attentions.to(device)
            sentences = sentences.squeeze(1)
            attentions = attentions.squeeze(1)
            target = target.cpu().data.numpy()
            for j in range(sentences.size(-1)):
                if bert_model is not None:
                    last_hidden_states = bert_model(sentences[:, :, j], attention_mask=attentions[:, :, j])[0]
                    embedding = last_hidden_states.permute(0, 2, 1)
                    output = model(image, embedding, l_mask=attentions[:, :, j].unsqueeze(-1))
                else:
                    output = model(image, sentences[:, :, j], l_mask=attentions[:, :, j])

                output = output.cpu()
                output_mask = output.argmax(1).data.numpy()
                I, U = computeIoU(output_mask, target)
                if U == 0:
                    this_iou = 0.0
                else:
                    this_iou = I*1.0/U
                mean_IoU.append(this_iou)
                cum_I += I
                cum_U += U
                for n_eval_iou in range(len(eval_seg_iou_list)):
                    eval_seg_iou = eval_seg_iou_list[n_eval_iou]
                    seg_correct[n_eval_iou] += (this_iou >= eval_seg_iou)
                seg_total += 1

                idx = 0
                # print(output_mask.shape)
                # print(image.shape)
                pred_mask = output_mask[idx]  # Predicted mask
                gt_mask = target[idx]      # Ground truth mask
                # Visualization code
                img_tensor = image[idx]  # Shape: (3, H, W)
                # Unnormalize the image
                unnormalize = T_t.Normalize(
                    mean=[-0.485 / 0.229, -0.456 / 0.224, -0.406 / 0.225],
                    std=[1 / 0.229, 1 / 0.224, 1 / 0.225]
                )
                img_tensor = unnormalize(img_tensor)
                img_numpy = img_tensor.cpu().numpy()  # Shape: (3, H, W)
                img_numpy = np.transpose(img_numpy, (1, 2, 0))  # Shape: (H, W, 3)
                img_numpy = np.clip(img_numpy, 0, 1)
                img_numpy = (img_numpy * 255).astype(np.uint8)

                # Overlay masks
                vis_pred = overlay_davis(img_numpy, pred_mask)
                vis_gt = overlay_davis(img_numpy, gt_mask)

                # Horizontally stack the two visualizations
                # combined_vis = np.hstack((vis_pred, vis_gt))

                # Save visualizations
                # pred_image = Image.fromarray(vis_pred)
                # gt_image = Image.fromarray(vis_gt)
                # pred_image.save(f'aihub_pred_vis/visualization_pred_{vis_counter}.jpg')
                # gt_image.save(f'aihub_pred_vis/visualization_gt_{vis_counter}.jpg')
                file_name = info['file_name'][0].split('.')[0]
<<<<<<< HEAD
                text_raw = info['text'][0][0]
=======
                text_raw = info['text'][0][0].replace('/', '')
>>>>>>> cf722cb10c2efd683d12e214ee5c20a7fd137321
                pred_image = Image.fromarray(vis_pred)
                gt_image = Image.fromarray(vis_gt)
                try:
                    pred_image.save(f'aihub_pred_vis/{file_name}_{text_raw}_pred.jpg')
                    gt_image.save(f'aihub_pred_vis/{file_name}_{text_raw}_gt.jpg')
                except OSError:
                    pred_image.save(f'aihub_pred_vis/{file_name}_{text_raw[:15]}_pred.jpg')
                    gt_image.save(f'aihub_pred_vis/{file_name}_{text_raw[:15]}_gt.jpg')
                vis_counter += 1
                # print(info)
<<<<<<< HEAD

=======
>>>>>>> cf722cb10c2efd683d12e214ee5c20a7fd137321


            del image, target, sentences, attentions, output, output_mask
            if bert_model is not None:
                del last_hidden_states, embedding

    mean_IoU = np.array(mean_IoU)
    mIoU = np.mean(mean_IoU)
    print('Final results:')
    print('Mean IoU is %.2f\n' % (mIoU*100.))
    results_str = ''
    for n_eval_iou in range(len(eval_seg_iou_list)):
        results_str += '    precision@%s = %.2f\n' % \
                       (str(eval_seg_iou_list[n_eval_iou]), seg_correct[n_eval_iou] * 100. / seg_total)
    results_str += '    overall IoU = %.2f\n' % (cum_I * 100. / cum_U)
    print(results_str)


def get_transform(args):
    transforms = [T.Resize(args.img_size, args.img_size),
                  T.ToTensor(),
                  T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                  ]

    return T.Compose(transforms)


def computeIoU(pred_seg, gd_seg):
    I = np.sum(np.logical_and(pred_seg, gd_seg))
    U = np.sum(np.logical_or(pred_seg, gd_seg))

    return I, U


def main(args):
<<<<<<< HEAD
    print('Command: python test.py --model lavt_one_xlm --swin_type base --dataset aihub_manufact_80 --split test --resume ./checkpoints/model_best_refcoco_manufact_80_uniq_id.pth --workers 4 --ddp_trained_weights --window12 --img_size 480 2>&1 | tee aihub_manufact_lavt_eval_log.txt')
=======
    print('Command: python test.py --model lavt_one_xlm --swin_type base --dataset aihub_indoor_80 --split test --resume ./checkpoints/model_best_refcoco_indoor_80_uniq.pth --workers 4 --ddp_trained_weights --window12 --img_size 480 2>&1 | tee aihub_indoor_ris_log.txt')
>>>>>>> cf722cb10c2efd683d12e214ee5c20a7fd137321
    import datetime
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    device = torch.device(args.device)
    dataset_test, _ = get_dataset(args.split, get_transform(args=args), args)
    test_sampler = torch.utils.data.SequentialSampler(dataset_test)
    data_loader_test = torch.utils.data.DataLoader(dataset_test, batch_size=1,
                                                   sampler=test_sampler, num_workers=args.workers)
    print(args.model)
    single_model = segmentation.__dict__[args.model](pretrained='',args=args)
    checkpoint = torch.load(args.resume, map_location='cpu')
    single_model.load_state_dict(checkpoint['model'])
    model = single_model.to(device)

    if args.model != 'lavt_one' and args.model != 'lavt_one_xlm':
        model_class = BertModel
        single_bert_model = model_class.from_pretrained(args.ck_bert)
        # work-around for a transformers bug; need to update to a newer version of transformers to remove these two lines
        if args.ddp_trained_weights:
            single_bert_model.pooler = None
        single_bert_model.load_state_dict(checkpoint['bert_model'])
        bert_model = single_bert_model.to(device)
    else:
        bert_model = None

    evaluate(model, data_loader_test, bert_model, device=device)
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    from args import get_parser
    parser = get_parser()
    args = parser.parse_args()
    print('Image size: {}'.format(str(args.img_size)))
    main(args)
