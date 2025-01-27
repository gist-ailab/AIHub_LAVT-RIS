# AIHub LAVT: Language-Aware Vision Transformer for Referring Image Segmentation
Welcome to the official repository for the method presented in
"LAVT: Language-Aware Vision Transformer for Referring Image Segmentation."


## How to run Docker Image
```
docker run --gpus all -it aihub-indoor-lavt
```


## Preprocessing Data
1. Locate test data into "refer/data" (e.g. refer/data/source_data, refer/data/labeling_data)
2. Run python preprocessing code
```
python convert_aihub_to_refcoco_indoor.py
```

## Train with AIHub Data
Indoor Data Train
```
conda activate lavt

CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python -m torch.distributed.launch --nproc_per_node 8 --master_port 12345 train.py --model lavt_one_xlm --dataset aihub_indoor_80 --model_id refcoco_indoor_80_uniq --batch-size 4 --lr 0.00005 --wd 1e-2 --swin_type base --pretrained_swin_weights ./pretrained_weights/swin_base_patch4_window12_384_22k.pth --epochs 40 --img_size 480 2>&1 | tee ./models/refcoco_indoor_80_uniq/output
```

## Test with AIHub Data
Indoor Data Test
```
conda activate lavt

python test.py --model lavt_one_xlm --swin_type base --dataset aihub_indoor_80 --split test --resume ./checkpoints/model_best_refcoco_indoor_80_uniq.pth --workers 4 --ddp_trained_weights --window12 --img_size 480 2>&1 | tee aihub_indoor_lavt_eval_log.txt 
Indoor Data Train
```


## Citing LAVT
```
@inproceedings{yang2022lavt,
  title={LAVT: Language-Aware Vision Transformer for Referring Image Segmentation},
  author={Yang, Zhao and Wang, Jiaqi and Tang, Yansong and Chen, Kai and Zhao, Hengshuang and Torr, Philip HS},
  booktitle={CVPR},
  year={2022}
}
```


## Contributing
We appreciate all contributions.
It helps the project if you could
- report issues you are facing,
- give a :+1: on issues reported by others that are relevant to you,
- answer issues reported by others for which you have found solutions,
- and implement helpful new features or improve the code otherwise with pull requests.

## Acknowledgements
Code in this repository is built upon several public repositories.
Specifically,
* data pre-processing leverages the [refer](https://github.com/lichengunc/refer) repository,
* the backbone model is implemented based on code from [Swin Transformer for Semantic Segmentation](https://github.com/SwinTransformer/Swin-Transformer-Semantic-Segmentation),
* the training and testing pipelines are adapted from [RefVOS](https://github.com/miriambellver/refvos),
* and implementation of the BERT model (files in the bert directory) is from [Hugging Face Transformers v3.0.2](https://github.com/huggingface/transformers/tree/v3.0.2)
(we migrated over the relevant code to fix a bug and simplify the installation process).

Some of these repositories in turn adapt code from [OpenMMLab](https://github.com/open-mmlab) and [TorchVision](https://github.com/pytorch/vision).
We'd like to thank the authors/organizations of these repositories for open sourcing their projects.


## License
GNU GPLv3
