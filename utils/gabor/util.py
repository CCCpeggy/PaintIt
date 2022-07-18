import cv2
import numpy as np
from skimage import measure

def get_connected_compenent(mask):
    ## find connect component
    _, mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    labels = measure.label(mask, connectivity=1)
    np.set_printoptions(threshold=np.inf)
    labels = np.array(labels ,dtype=np.uint8)
    
    connected_component = []
    properties = measure.regionprops(labels)
    for prop in properties:
        n = prop.label
        if prop.area > 0:
            img = labels * 1
            img[img != n] = 0
            img[img == n] = 255
            connected_component.append(img)
    return connected_component

def get_image_with_mask(img, mask, color=(255, 0, 0)):
    if len(img.shape) == 2:
        img = np.stack([img] * 3, axis=-1)
    elif img.shape[2] == 1:
        img = np.stack([img[:, :, 0]] * 3, axis=-1)
    img[:,:,0][mask > 0] = img[:,:,0][mask > 0] * 0.5 + color[0] * 0.5
    img[:,:,1][mask > 0] = img[:,:,1][mask > 0] * 0.5 + color[1] * 0.5
    img[:,:,2][mask > 0] = img[:,:,2][mask > 0] * 0.5 + color[2] * 0.5
    return img