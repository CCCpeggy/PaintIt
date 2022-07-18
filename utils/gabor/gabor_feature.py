'''
Edit From: https://github.com/duycao2506/Gabor-Filter-Face-Extraction/blob/master/FaceClassManager.py
'''

from cmath import pi, tan
import cv2
from cv2 import sqrt
from cv2 import log
from cv2 import exp
import numpy as np
from numpy.fft import fft2, ifft2, fftshift
import math

class GaborFeature(object):
    "Class for recognizing faces"
    "There will be a training datasets first"
    "Method: Gabor filter"
    def __init__(self, height, width, img=None):
        self.scale = 4
        self.orientation = 6
        self.Ul = 0.2
        self.Uh = 0.8
        self.img = img
        self.height = height
        self.width = width
        
        kernel = self.build_filters()
        self.fft_filters = [np.fft.fft2(i) for i in kernel]
        
        if img is not None:
            self.set_image(img)
        
    def set_image(self, img):
        assert self.height == img.shape[0]
        assert self.width == img.shape[1]
        self.img = img
        img_fft = np.fft.fft2(self.img)
        a = img_fft * self.fft_filters
        s = [np.fft.ifft2(i) for i in a]
        self.k = [p.real for p in s]

    def build_filters(self):
        """ Get set of filters for GABOR
        num_theta: N (total number of orientation)
        """
        filters = []
        for s in range(self.scale):
            for n in range(self.orientation):
                kernel_real, kernel_image = self.get_gabor_kernel(s, n)
                # kernel = 2.0 * kernel / kernel.sum()
                # kernel = cv2.normalize(kernel, kernel, 1.0, 0, cv2.NORM_L2)
                kernel = np.zeros(kernel_real.shape, dtype=complex)
                kernel.real = kernel_real
                kernel.imag = kernel_image
                filters.append(kernel)
        return filters

    def get_gabor_kernel(self, s, n):
        base = self.Uh / self.Ul
        a = pow(base, 1 / (self.scale - 1))
        u0 = self.Uh / pow(a, self.scale - s)

        Uvar = (a - 1) * u0 / ((a + 1) * math.sqrt(2 * math.log(2)))

        z = -2.0 * math.log(2) * (Uvar * Uvar) / u0
        Vvar = math.tan(pi / (2 * self.orientation)) * (u0 + z) / math.sqrt(2 * math.log(2.0) - z * z / (Uvar * Uvar))

        Xvar = 1 / (2 * pi * Uvar)
        Yvar = 1 / (2 * pi * Vvar)

        t1 = math.cos(pi / self.orientation * (n - 1))
        t2 = math.sin(pi / self.orientation * (n - 1))

        side = int((self.height - 1) // 2)

        # gabor_real_kernel_matrix = np.zeros((2 * side + 1, 2 * side + 1))
        # gabor_image_kernel_matrix = np.zeros((2 * side + 1, 2 * side + 1))
        # for x in range(2 * side + 1):
        #     for y in range(2 * side + 1):
    
        # gabor_real_kernel_matrix = np.zeros((self.height, self.width))
        gabor_image_kernel_matrix = np.zeros((self.height, self.width))
        
        def get_pixel_gabor_real_kernel(x, y):
            X =  (x - side) * t1 + (y - side) * t2
            Y = -(x - side) * t2 + (y - side) * t1
            G = 1 / (2 * pi * Xvar * Yvar) * math.pow(a, self.scale - s) * math.exp(-0.5 * ((X * X) / (Xvar * Xvar) + (Y * Y) / (Yvar * Yvar)))
            return G * math.cos(2.0 * pi * u0 * X)
            # gabor_real_kernel_matrix[y, x] = G * math.cos(2.0 * pi * u0 * X)
            # gabor_image_kernel_matrix[y, x] = G * math.sin(2.0 * pi * u0 * X)
        gabor_real_kernel_matrix = np.array([[get_pixel_gabor_real_kernel(x, y) for x in range(self.width)]for y in range(self.height)])
        return gabor_real_kernel_matrix, gabor_image_kernel_matrix

    def get_distance_off_v(self, fv1, fv2):
        "distance of feature vector 1 and feature vector 2"
        normset = []
        for i in range(len(fv1)):
            k = fv1[i]
            p = fv2[i]
            # k = cv2.normalize(fv1[i],k,1.0,0,norm_type=cv2.NORM_L2)
            # p = cv2.normalize(fv2[i],p,1.0,0,norm_type=cv2.NORM_L2)
            normset.append((p-k) ** 2.0)
        sums = 0
        sums = sum([i.sum() for i in normset])
        return math.sqrt(sums) / 100000

    def get_avg_dist(self, imgFVClass, imgFV):
        "classify the imgFV in the classes"
        distes = [self.get_distance_off_v(iFv,imgFV) for iFv in imgFVClass]
        print(len(distes))
        return (sum(distes) / len(distes))

    def classify(self, imgFV, imgFVClasses):
        avg_distes = [self.get_avg_dist(imgFVClass, imgFV) for imgFVClass in imgFVClasses]
        print(avg_distes)
        return avg_distes.index(min(avg_distes))

    def extract_features(self, mask=None):
        "A vector of 2n elements where n is the number of theta angles"
        "and 2 is the number of frequencies under consideration"
        mask = mask > 0 if mask is not None else True
        # feature = [np.mean(f[mask]) for f in self.k] + [np.std(f[mask]) for f in self.k]
        feature = [np.mean(f) for f in self.k] + [np.std(f) for f in self.k]
        blur_img = self.img * 1
        blur_img = blur_img.astype(float)
        blur_img[1:-1, 1:-1] *= 0.25
        blur_img[1:-1, 1:-1] += (self.img[0:-2, 1:-1]+self.img[1:-1, 0:-2]+self.img[2:, 1:-1]+self.img[1:-1, 2:]) * 0.125
        blur_img[1:-1, 1:-1] += (self.img[0:-2, 0:-2]+self.img[0:-2, 2:]+self.img[2:, 0:-2]+self.img[2:, 2:]) * 0.0625
        feature.append(np.mean(blur_img[mask]) / 255 * 10)
        return np.array(feature)

if __name__ == "__main__":
    imgs = [
        cv2.imread(r"D:\shared\datasets\20220214\dot\dot_gap_6_7\0001.png", 0),
        cv2.imread(r"D:\shared\datasets\20220214\dot\dot_gap_6_7\0002.png", 0),   
        cv2.imread(r"D:\shared\datasets\20220214\dot\dot_gap_6_7\0017.png", 0)
    ]
    feats = []
    for i, img in enumerate(imgs):
        gabor_feature_extractor = GaborFeature(img)
        feat = gabor_feature_extractor.extract_features()
        feats.append(np.array(feat))
        # total = np.zeros((img.shape[0], img.shape[1]))
        # for f in feat:
        #     total += f
        # cv2.imshow(str(i), total / 24)
        # cv2.waitKey()
    print(abs(np.sum((feats[0] - feats[1]) ** 2)))
    print(abs(np.sum((feats[0] - feats[2]) ** 2)))
    print(abs(np.sum((feats[1] - feats[2]) ** 2)))