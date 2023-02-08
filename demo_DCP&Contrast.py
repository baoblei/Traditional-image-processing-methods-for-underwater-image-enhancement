# coding=utf-8
import cv2
import numpy as np
# import time 

# 新建一个VideoCapture对象，打开视频
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('./video/uw4.mp4')

# 获取原始视频帧大小及fps信息，注意宽高需要强制类型转换成int，否则VideoWriter会报错
width = int(cap.get(3)/2)
height = int(cap.get(4))
fps = 24
# 根据视频文件属性设置waitTime和fps
waitTime = 1
if cap.get(5) != 0:
    waitTime = int(1000.0 / cap.get(5))
    fps = cap.get(5)

# fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
# out = cv2.VideoWriter("DCP_enhance.mp4", fourcc, fps, (width,height))

out_frame = np.zeros((height, width, 3), np.uint8)
frame2gray = np.zeros((height, width, 3), np.uint8)
# times = []
while 1:
    ret, frame = cap.read()
    frame = frame[:,:640]
    if frame is None:
        break
    else:
        cv2.imshow("video",frame)
        
        # s = time.time()
        # TODO 在获取每一帧并进行处理后，进行输出
        # frame2gray[:, :, 0] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame2gray[:, :, 1] = frame2gray[:, :, 0]
        # frame2gray[:, :, 2] = frame2gray[:, :, 0]

        # cv2.imshow("gray", frame2gray)
        # times.append(time.time()-s)

        # 全局直方图均衡
        # (b_g,g_g,r_g) = cv2.split(frame2gray)
        # bH_g = cv2.equalizeHist(b_g)
        # gH_g = cv2.equalizeHist(g_g)
        # rH_g = cv2.equalizeHist(r_g)
        # enhance_gray = cv2.merge((bH_g,gH_g,rH_g))
        # cv2.imshow("enhance_gray", enhance_gray)

        (b,g,r) = cv2.split(frame)
        bH = cv2.equalizeHist(b)
        gH = cv2.equalizeHist(g)
        rH = cv2.equalizeHist(r)
        enhance = cv2.merge((bH,gH,rH))
        cv2.imshow("enhance", enhance)

        # 局部直方图均衡
        clahe = cv2.createCLAHE(clipLimit = 2.0, tileGridSize=(8,8))
        # local_eqH_bg = clahe.apply(bH_g)
        # local_eqH_gg = clahe.apply(gH_g)
        # local_eqH_rg = clahe.apply(rH_g)
        # local_enhance_gray = cv2.merge((local_eqH_bg,local_eqH_gg,local_eqH_rg))
        # cv2.imshow("local_eqH_gray", local_enhance_gray)
        
        local_eqH_b = clahe.apply(bH)
        local_eqH_g = clahe.apply(gH)
        local_eqH_r = clahe.apply(rH)
        local_enhance = cv2.merge((local_eqH_b,local_eqH_g,local_eqH_r))
        cv2.imshow("local_eqH", local_enhance)

        # 全局对比度增强
        from PIL import Image
        from PIL import ImageEnhance
        img = np.uint8(frame)
        inp_img = Image.fromarray(img)
        enh_con = ImageEnhance.Contrast(inp_img)
        contrast = 1.5
        img_con = enh_con.enhance(contrast)
        cv2.imshow("contrast_enhance", np.uint8(img_con))

        # 暗通道先验 DCP
        from DCP import *
        enh_DCP = deHaze(frame/255.0)
        cv2.imshow("DCP_enhance", enh_DCP)
        # out.write(enh_DCP)

        k = cv2.waitKey(waitTime) & 0xFF
        if k == 27:
            break

cap.release()
# Ttime, Mtime = np.sum(times[1:]), np.mean(times[1:]) 
# print ("Time taken: %d sec at %0.3f fps" %(Ttime, 1./Mtime))