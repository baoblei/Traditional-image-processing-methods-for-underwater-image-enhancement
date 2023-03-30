# 导入所需模块
import cv2
import numpy as np
import time


def distortion(img, k1=0.3, k2=0.1, p1=0.0, p2=0.0):
    # 获取图像尺寸
    h, w = img.shape[:2]

    # 计算畸变中心
    cx = w / 2
    cy = h / 2

    # 计算像素坐标的畸变校正
    map_x = np.zeros((h, w), dtype=np.float32)
    map_y = np.zeros((h, w), dtype=np.float32)
    for y in range(h):
        for x in range(w):
            # 将像素坐标转换为归一化坐标
            nx = (x - cx) / cx
            ny = (y - cy) / cy
            
            # 计算畸变校正后的归一化坐标
            r2 = nx**2 + ny**2
            xn = nx * (1 + k1 * r2 ) 
            yn = ny * (1 + k1 * r2 ) 
            
            # xn = nx * (1 + k1 * r2 + k2 * r2**2) + 2 * p1 * nx * ny + p2 * (r2 + 2 * nx**2)
            # yn = ny * (1 + k1 * r2 + k2 * r2**2) + 2 * p2 * nx * ny + p1 * (r2 + 2 * ny**2)

            # xn = k1*r2 + k2*r2**2
            # yn = k1*r2 + k2*r2**2
            
            # 将归一化坐标转换为像素坐标
            map_x[y, x] = cx + cx * xn
            map_y[y, x] = cy + cy * yn

    # 应用畸变校正
    dst = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)
    return dst

if __name__ == "__main__":
    # 加载图像
    img = cv2.imread('VR_distortion.jpg')

    s = time.time()
    dst = distortion(img)

    # 显示结果
    cv2.imshow('Input', img)
    cv2.imshow('Output', dst)
    print(time.time()-s)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
