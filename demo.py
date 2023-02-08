# coding=utf-8
import cv2
import numpy as np
# import time 

# 新建一个VideoCapture对象，打开视频
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('./demo_uw.mp4')

# 获取原始视频帧大小及fps信息，注意宽高需要强制类型转换成int，否则VideoWriter会报错
width = int(cap.get(3)/2)
height = int(cap.get(4))
fps = 24

# 根据视频文件属性设置waitTime和fps
waitTime = 1
if cap.get(5) != 0:
    waitTime = int(1000.0 / cap.get(5))
    fps = cap.get(5)



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
        frame2gray[:, :, 0] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame2gray[:, :, 1] = frame2gray[:, :, 0]
        frame2gray[:, :, 2] = frame2gray[:, :, 0]

        cv2.imshow("gray", frame2gray)
        # times.append(time.time()-s)

        k = cv2.waitKey(waitTime) & 0xFF
        if k == 27:
            break

cap.release()
# Ttime, Mtime = np.sum(times[1:]), np.mean(times[1:]) 
# print ("Time taken: %d sec at %0.3f fps" %(Ttime, 1./Mtime))