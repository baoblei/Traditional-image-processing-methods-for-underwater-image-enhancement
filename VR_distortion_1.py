import cv2
import numpy as np

def get_grid_id(x , y, grid_size=30):
    # 获取网格位置
    x_g = x // grid_size 
    y_g = y // grid_size
    return x_g, y_g


def distort_image(img, k1=0.2, k2=0.01, p1=0.0, p2=0.0):
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
            xn = nx * (1 + k1 * r2 + k2 * r2**2) 
            yn = ny * (1 + k1 * r2 + k2 * r2**2) 
            
            # 将归一化坐标转换为像素坐标
            map_x[y, x] = cx + cx * xn
            map_y[y, x] = cy + cy * yn

    # 应用畸变校正
    dst = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)
    return dst
 
if __name__ == "__main__":
    # 加载图像
    img = cv2.imread('VR_distortion.jpg')


    dst = distort_image(img)

    # 显示结果
    cv2.imshow('Input', img)
    cv2.imshow('Output', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()