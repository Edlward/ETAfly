# Single Color RGB565 Blob Tracking Example
#
# This example shows off single color RGB565 tracking using the OpenMV Cam.

import sensor, image, time, math , pyb ,json
from pyb import LED,UART

threshold_index = 0 # 0 for red, 1 for green, 2 for blue
LEDB = pyb.LED(1) # Red LED = 2, Green LED = 3, Blue LED = 1, IR LEDs = 4.
LEDR = pyb.LED(2)
LEDG = pyb.LED(3)



# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
thresholds = [(21, 84, 22, 90, -18, 58), # 橙红色块
              (30, 100, -64, -8, -32, 32), # generic_green_thresholds
              (0, 30, 0, 64, -128, 0)] # generic_blue_thresholds


sensor.reset()
sensor.set_pixformat(sensor.RGB565) # RGB565即一个彩色图像点由RGB三个分量组成，总共占据2Byte，高5位为R分量，中间6位为G分量，低5位为B分量
sensor.set_framesize(sensor.QVGA) # 320*240
sensor.skip_frames(time = 500) # 跳过，等待摄像头稳定
sensor.set_auto_gain(False) # 自动增益在颜色识别中一般关闭，不然会影响阈值
sensor.set_auto_whitebal(False) # 白平衡在颜色识别中一般关闭，不然会影响阈值
clock = time.clock() # 构造时钟对象

uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1, timeout_char=1000) # 使用给定参数初始化 timeout_char是以毫秒计的等待字符间的超时时长

test_num = [3,9,4,1,3,4]

def find_max(blobs): # 比较返回最大色块（blobs为色块元组，中可能含有多个色块）
    max_size = 0
    for blob in blobs:
        if blob.w() * blob.h() > max_size: #长*宽
            max_blob = blob #
            max_size = blob.w()*blob.h()
    return max_blob




def sum_checkout(data_list): # 把除校验位的数据包全部累加 生成 累加和校验位
    data_sum = 0
    for temp in data_list:
        data_sum += temp
    return hex(data_sum) #返回16进制




while(True):
    clock.tick() # 追踪时钟
    img = sensor.snapshot() #thresholds为阈值元组0
    blobs = img.find_blobs([thresholds[threshold_index]], pixels_threshold=200, area_threshold=200, merge=False)
    # pixels_threshold为像素阈值，只有大于pixels_threshold才会被识别出来，area_threshold 为面积阈值，只有大于area_threshold才能被识别出来
    # merge=True”合并图像中所有重叠的斑点
    if blobs:
        max_blob = find_max(blobs) #找到最大的色块
        img.draw_rectangle(max_blob.rect()) #画矩形
        img.draw_cross(max_blob.cx(), max_blob.cy())#中心画十字

        print(int(max_blob.cx()/2),max_blob.cy(),max_blob.pixels(),max_blob.w()*max_blob.h(),max_blob.count(),int(max_blob.density()*100))

        datalist = [0xAA,0x55,0x01,0x07,threshold_index,max_blob.cx(),max_blob.cy()]
        #---包头------功能位----数据个数位-----------------------数据包--------------------------累加和校验
        #【AA 55】    【01】     【07】         【阈值、色块个数、简单距离、色块中心坐标(x,y)】       【sum】



        data = bytearray([0xAA,0x55,0x07,max_blob.cx(),max_blob.cy(),0,threshold_index,0x00,0x00,0x88])#转成16进制

        LEDR.on()

        print(sum_checkout(test_num))
        #print("fps:%0.2f" %clock.fps())
    else:
        LEDR.off()
        #datalist = [0xAA,0x55,0x01,0x]




'''
for res in data:
    print("%x" %res)
'''
