from collections import OrderedDict
import sys
import torch
from torch import nn
from torch.nn import functional as F
from bert.modeling_bert import BertModel
from transformers import AutoTokenizer, AutoModelForMaskedLM



class _LAVTSimpleDecode(nn.Module):
    def __init__(self, backbone, classifier):
        super(_LAVTSimpleDecode, self).__init__()
        self.backbone = backbone
        self.classifier = classifier

    def forward(self, x, l_feats, l_mask):
        input_shape = x.shape[-2:]
        features = self.backbone(x, l_feats, l_mask)
        x_c1, x_c2, x_c3, x_c4 = features
        x = self.classifier(x_c4, x_c3, x_c2, x_c1)
        x = F.interpolate(x, size=input_shape, mode='bilinear', align_corners=True)

        return x


class LAVT(_LAVTSimpleDecode):
    pass


###############################################
# LAVT One: put BERT inside the overall model #
###############################################
class _LAVTOneSimpleDecode(nn.Module):
    def __init__(self, backbone, classifier, args):
        super(_LAVTOneSimpleDecode, self).__init__()
        self.backbone = backbone
        self.classifier = classifier
        self.args = args
        if args.model == 'lavt_one':
            self.text_encoder = BertModel.from_pretrained(args.ck_bert)
        elif args.model == 'lavt_one_xlm':
            self.text_encoder = AutoModelForMaskedLM.from_pretrained('xlm-roberta-base')
        # self.text_encoder = BertModel.from_pretrained(args.ck_bert)
        # self.text_encoder = AutoModelForMaskedLM.from_pretrained('xlm-roberta-base')
        self.text_encoder.pooler = None

    def forward(self, x, text, l_mask):
        input_shape = x.shape[-2:]
        ### language inference ###
        # print("text shape: ", text.shape)
        # print("l_mask shape: ", l_mask.shape)
        if self.args.model == 'lavt_one_xlm':
            l_feats = self.text_encoder(text, attention_mask=l_mask, output_hidden_states=True,)  # (6, 10, 768)
            # print(l_feats.logits.size())
            # print(len(l_feats))
            # print(l_feats.hidden_states[0].size())
            # print(l_feats.hidden_states[1:])
            # print(l_feats.hidden_states[1:][-1].size())
            # print('=========================')
            # l_feats = l_feats.hidden_states[1:][-1]
            l_feats = l_feats.hidden_states[0]

        else:
            l_feats = self.text_encoder(text, attention_mask=l_mask)[0]  # (6, 10, 768)

        # print('l_feats:', l_feats.shape)
        l_feats = l_feats.permute(0, 2, 1)  # (B, 768, N_l) to make Conv1d happy
        l_mask = l_mask.unsqueeze(dim=-1)  # (batch, N_l, 1)
        ##########################
        # print('l_feats:', l_feats.shape)
        # print('l_mask:', l_mask.shape)
        features = self.backbone(x, l_feats, l_mask)
        x_c1, x_c2, x_c3, x_c4 = features
        x = self.classifier(x_c4, x_c3, x_c2, x_c1)
        x = F.interpolate(x, size=input_shape, mode='bilinear', align_corners=True)

        return x


class LAVTOne(_LAVTOneSimpleDecode):
    pass
