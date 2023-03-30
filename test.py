# coding=utf-8
from VR_distortion import distortion
import cv2
import numpy as np
# import time 

# 新建一个VideoCapture对象，打开视频
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('./video/video_dst.mp4')

# 获取原始视频帧大小及fps信息，注意宽高需要强制类型转换成int，否则VideoWriter会报错
width = int(cap.get(3))
height = int(cap.get(4))
fps = 24
# 根据视频文件属性设置waitTime和fps
waitTime = 1
if cap.get(5) != 0:
    waitTime = int(1000.0 / cap.get(5))
    fps = cap.get(5)

# 文件存储
# fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
# # out_gl_HST = cv2.VideoWriter("./enhance/gl_HST.mp4", fourcc, fps, (width,height))
# # out_loc_HST = cv2.VideoWriter("./enhance/loc_HST.mp4", fourcc, fps, (width,height))
# # out_contrast = cv2.VideoWriter("./enhance/contrast.mp4", fourcc, fps, (width,height))
# out_DCP = cv2.VideoWriter("./enhance/DCP.mp4", fourcc, fps, (width,height))
# # out_median_filter = cv2.VideoWriter("./enhance/median_filter.mp4", fourcc, fps, (width,height))
# # out_GaussianBlur = cv2.VideoWriter("./enhance/GaussianBlur.mp4", fourcc, fps, (width,height))

out_frame = np.zeros((height, width, 3), np.uint8)
frame2gray = np.zeros((height, width, 3), np.uint8)
# times = []
while 1:
    ret, frame = cap.read()
    # frame = frame[:,:500]
    scale_percent = 33 # percent of original size
    width = int(frame.shape[1] * scale_percent / 130)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    frame1 = frame
    frame = np.concatenate([frame,frame1],axis=1)
    if frame is None:
        break
    else:
        cv2.imshow("original_video",frame)
        # cv2.moveWindow("original_video", 1, 1)
        # s = time.time()
        # frame2gray[:, :, 0] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame2gray[:, :, 1] = frame2gray[:, :, 0]
        # frame2gray[:, :, 2] = frame2gray[:, :, 0]
        # cv2.imshow("gray", frame2gray)
        # times.append(time.time()-s)

        # 全局直方图均衡

        # (b,g,r) = cv2.split(frame)
        # bH = cv2.equalizeHist(b)
        # gH = cv2.equalizeHist(g)
        # rH = cv2.equalizeHist(r)
        # enhance = cv2.merge((bH,gH,rH))
        # cv2.imshow("gl_HST_enhance", enhance)
        # cv2.moveWindow("gl_HST_enhance", 500, 1)
        # out_gl_HST.write(enhance)

        # 局部直方图均衡
        # clahe = cv2.createCLAHE(clipLimit = 1.0, tileGridSize=(8,8))
        # local_eqH_b = clahe.apply(bH)
        # local_eqH_g = clahe.apply(gH)
        # local_eqH_r = clahe.apply(rH)
        # local_enhance = cv2.merge((local_eqH_b,local_eqH_g,local_eqH_r))
        # cv2.imshow("loc_HST_enhance", local_enhance)
        # cv2.moveWindow("loc_HST_enhance", 1000, 1)
        # out_loc_HST.write(local_enhance)

        # 全局对比度增强
        # from PIL import Image
        # from PIL import ImageEnhance
        # img = np.uint8(frame)
        # inp_img = Image.fromarray(img)
        # enh_con = ImageEnhance.Contrast(inp_img)
        # contrast = 1.5
        # img_con = enh_con.enhance(contrast)
        # cv2.imshow("contrast_enhance", np.uint8(img_con))
        # cv2.moveWindow("contrast_enhance", 1, 500)
        # out_contrast(img_con)

        # 暗通道先验 DCP
        from DCP import *
        enh_DCP = deHaze(frame/255.0)
        # mid = int(width/2)
        mid = int(width)
        img_l = enh_DCP[:,:mid]
        img_r = enh_DCP[:,mid:]
        img_l_dst, img_r_dst = distortion(img_l), distortion(img_r)
        img = np.concatenate([img_l_dst,img_r_dst],axis=1)
        cv2.imshow("DCP_enhance", img)
        # out_DCP.write(enh_DCP)
        



        # cv2.imshow("DCP_enhance", enh_DCP)
        # cv2.moveWindow("DCP_enhance", 500, 500)
        # out_DCP.write(enh_DCP)

        # # # 中值滤波
        # median = cv2.medianBlur(frame, 5)
        # cv2.imshow("median_filter", median)
        # cv2.moveWindow("median_filter", 1000, 500)
        # # out_median_filter(median)

        # # # 高斯滤波
        # dst = cv2.GaussianBlur(local_enhance,(5,5),cv2.BORDER_DEFAULT)
        # cv2.imshow("GaussianBlur", dst)
        # cv2.moveWindow("GaussianBlur", 1500, 500)
        # # out_GaussianBlur(dst)

        k = cv2.waitKey(waitTime) & 0xFF
        if k == 27:
            break

cap.release()
# Ttime, Mtime = np.sum(times[1:]), np.mean(times[1:]) 
# print ("Time taken: %d sec at %0.3f fps" %(Ttime, 1./Mtime))