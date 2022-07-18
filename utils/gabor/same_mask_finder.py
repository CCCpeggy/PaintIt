import os
import cv2
import numpy as np
from typing import *

from .util import *
from .gabor_feature import GaborFeature

class FindNeighborMask:
    def __init__(self, img, stroke_img):
        self.ori_img = img
        self.stroke_img = stroke_img
        self.feature_extractor = GaborFeature(self.ori_img.shape[0], self.ori_img.shape[1])
        # self.feats = []
        
    def get_feat(self, mask):
        mask[self.stroke_img == 0] = 0
        img = self.ori_img * 1
        if self.pattern_img is not None:
            img[mask == 0] = self.pattern_img[mask == 0]
        self.feature_extractor.set_image(img)
        return self.feature_extractor.extract_features(mask)
            
    def get_feat_diff(self, feat1, feat2):
        return abs(np.sum((feat1 - feat2) ** 2))
    
    def set_pattern_image(self, pattern_img):
        self.pattern_img = pattern_img
        self.keep_feat = [None] * len(self.mask_relationship) # 保留已算的特徵

    def get_all_neighbor_same_type_masks(self, mask, threshold=1) -> List[np.numarray]:
        self.ori_feat = self.get_feat(mask)
        overlapped_mask_idxs = list(np.unique(self.empty_mask_label[mask > 0].reshape((-1))))
        # print(overlapped_mask_idxs)
        print("Begin masks：", overlapped_mask_idxs)
        self.is_mask_tried = [i in overlapped_mask_idxs for i in range(len(self.mask_relationship))] # 避免重複確認
        now_idx = 0
        while now_idx < len(overlapped_mask_idxs):
            new_mask_idxs = self.get_neighbor_same_type_mask_idxs(overlapped_mask_idxs[now_idx], threshold)
            overlapped_mask_idxs += new_mask_idxs
            now_idx += 1
        print("Found masks：", overlapped_mask_idxs)
        return [self.empty_masks[idx] for idx in overlapped_mask_idxs]
    
    def get_neighbor_same_type_mask_idxs(self, idx, threshold=1) -> List[int]:
        same_type_mask_idxs = [] # 同樣類型的 mask id
        possible_mask = [i for i in self.mask_relationship[idx] if not self.is_mask_tried[i]] # 未算過的鄰居
        for mask_idx in possible_mask:
            if self.keep_feat[mask_idx] is None:
                self.keep_feat[mask_idx] = self.get_feat(self.empty_masks[mask_idx])
            neighbor_feat = self.keep_feat[mask_idx]
            diff = self.get_feat_diff(self.ori_feat, neighbor_feat)
            if diff < threshold:
                # print(mask_idx, diff)
                same_type_mask_idxs.append(mask_idx)
            self.is_mask_tried[mask_idx] = True
        return same_type_mask_idxs
    
    def get_empty_neighbor_masks(self, idx) -> List[np.numarray]:
        neighbor_mask = [self.empty_masks[i] for i in self.mask_relationship[idx]]
        return neighbor_mask

    def init_neighbor_relationship(self):
        kernel = np.ones((3, 3), np.uint8)

        # 建立空白區域的 mask，與其 label 對應
        empty_mask = self.stroke_img * 1
        self.empty_masks = get_connected_compenent(empty_mask)
        empty_mask_label = np.ones_like(self.ori_img) * 255
        for i, m in enumerate(self.empty_masks):
            empty_mask_label[m > 0] = i
        self.empty_mask_label = empty_mask_label
        
        self.mask_relationship = [[] for _ in range(len(self.empty_masks))]
        count = 0

        for i, empty_mask in enumerate(self.empty_masks):
            # 為了尋找鄰居
            empty_mask = cv2.dilate(empty_mask, kernel, iterations = 10)
            connected_mask = list(np.unique(empty_mask_label[empty_mask > 0].reshape((-1))))
            connected_mask.remove(255)
            for n in connected_mask:
                if n != i:
                    self.mask_relationship[n].append(i)
                
            # 存結果
            output_img = empty_mask * 1
            output_img = get_image_with_mask(output_img, self.empty_masks[i], (0, 255, 0))
            for n in connected_mask:
                if n != i:
                    output_img = get_image_with_mask(output_img, self.empty_masks[n])
            # cv2.imwrite(f"debug/neighbor/{count}.png", output_img)
            count += 1

if __name__ == "__main__":
    dir = "data/doraemon"
    img = cv2.imread(os.path.join(dir, "img.png"), 0)
    stroke = cv2.imread(os.path.join(dir, "stroke.png"), 0)
    pattern = cv2.imread(os.path.join(dir, "pattern.png"), 0)
    finder = FindNeighborMask(img, stroke)
    
    mask = cv2.imread(os.path.join(dir, "mask.png"), 0)
    masks: list = get_connected_compenent(mask)

    finder.init_neighbor_relationship()
    print(finder.mask_relationship)

    finder.set_pattern_image(pattern)
    same_type_masks = finder.get_all_neighbor_same_type_masks(masks[5], 0.05)

    result_img = finder.ori_img * 1
    for m in same_type_masks:
        result_img = get_image_with_mask(result_img, m, (0, 255, 0))
    result_img = get_image_with_mask(result_img, masks[5])
    cv2.imwrite("debug/result.png", result_img)