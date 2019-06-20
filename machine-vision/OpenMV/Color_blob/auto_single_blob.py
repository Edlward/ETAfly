'''
自动识别单个颜色(自动学习阈值)
'''

import sensor, image, time,math , pyb,single_blob

print("Letting auto algorithms run. Don't put anything in front of the camera!")

LEDB = pyb.LED(1) # Red LED = 2, Green LED = 3, Blue LED = 1, IR LEDs = 4.
LEDR = pyb.LED(2)
LEDG = pyb.LED(3)

# 检测色块时灯的状态
def auto_single_blob_LEDStatus(status):
    if status == 0:
        for i in range(2):
            LEDG.on()
            time.sleep(100)
            LEDG.off()
            time.sleep(100)
    elif status == 1:
        for i in range(2):
            LEDR.on()
            LEDG.on()
            time.sleep(100)
            LEDR.off()
            LEDG.on()
            time.sleep(100)
    else:
        LEDR.off()
        LEDG.off()
        LEDB.off()

# Capture the color thresholds for whatever was in the center of the image.
r = [(sensor.width()//2)-(50//2), (sensor.height()//2)-(50//2), 50, 50] # 屏幕中心范围50x50  //表示整除
threshold = [50, 50, 0, 0, 0, 0] # Middle L, A, B values.


def get_auto_single_blob_threshold():

    print("Auto algorithms done. Hold the object you want to track in front of the camera in the box.")
    print("MAKE SURE THE COLOR OF THE OBJECT YOU WANT TO TRACK IS FULLY ENCLOSED BY THE BOX!")
    for i in range(60):
        img = sensor.snapshot()
        img.draw_rectangle(r)

    auto_single_blob_LEDStatus(0)

    print("Learning thresholds...")

    for i in range(60):
        img = sensor.snapshot()
        hist = img.get_histogram(roi=r)
        lo = hist.get_percentile(0.01) # Get the CDF of the histogram at the 1% range (ADJUST AS NECESSARY)!
        hi = hist.get_percentile(0.99) # Get the CDF of the histogram at the 99% range (ADJUST AS NECESSARY)!
        # Average in percentile values.
        threshold[0] = (threshold[0] + lo.l_value()) // 2
        threshold[1] = (threshold[1] + hi.l_value()) // 2
        threshold[2] = (threshold[2] + lo.a_value()) // 2
        threshold[3] = (threshold[3] + hi.a_value()) // 2
        threshold[4] = (threshold[4] + lo.b_value()) // 2
        threshold[5] = (threshold[5] + hi.b_value()) // 2
        for blob in img.find_blobs([threshold], pixels_threshold=5, area_threshold=5, merge=True, margin=10):
            img.draw_rectangle(blob.rect())
            img.draw_cross(blob.cx(), blob.cy())
            img.draw_rectangle(r)

    auto_single_blob_LEDStatus(1)
    print("Thresholds learned...")
    print("Tracking colors...")



def auto_single_blob(img,ctrl,uart):

    blobs = img.find_blobs([threshold], pixels_threshold=5, area_threshold=5, merge=True, margin=10)
    # pixels_threshold为像素阈值，只有大于pixels_threshold才会被识别出来，area_threshold 为面积阈值，只有大于area_threshold才能被识别出来
    # merge=True 合并图像中所有重叠的斑点
    if blobs:
        flag = 0x01
        max_blob = single_blob.find_max(blobs) #找到最大的色块
        img.draw_rectangle(max_blob.rect()) #画矩形
        img.draw_cross(max_blob.cx(), max_blob.cy())#中心画十字
        #---包头------功能位----数据个数位----------------------------------数据包------------------------------------------累加和校验
        #【AA 55】    【01】     【09】      【阈值、色块个数、识别度、简单距离、色块中心坐标(高8位x，低8位x,高8位y，低8位y)、res】   【sum】
        uart.write(single_blob.pack_blob_data(max_blob,ctrl,flag))
        LEDG.on()
    else:
        flag = 0x00
        uart.write(single_blob.pack_no_blob_data(ctrl,flag))
        LEDG.off()



