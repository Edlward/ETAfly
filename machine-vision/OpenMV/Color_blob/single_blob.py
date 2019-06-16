# Single Color RGB565 Blob Tracking Example
#
# This example shows off single color RGB565 tracking using the OpenMV Cam.

import sensor, image, time, math , pyb ,json
from pyb import LED,UART,Timer

threshold_index = 0 # 0 for red, 1 for green, 2 for blue
LEDB = pyb.LED(1) # Red LED = 2, Green LED = 3, Blue LED = 1, IR LEDs = 4.
LEDR = pyb.LED(2)
LEDG = pyb.LED(3)

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
thresholds = [(21, 84, 22, 90, -18, 58), # 橙红色块
              (30, 100, -64, -8, -32, 32), # generic_green_thresholds
              (0, 30, 0, 64, -128, 0)] # generic_blue_thresholds


sensor.reset() # 传感器复位
sensor.set_pixformat(sensor.RGB565) # RGB565即一个彩色图像点由RGB三个分量组成，总共占据2Byte，高5位为R分量，中间6位为G分量，低5位为B分量
sensor.set_framesize(sensor.QVGA) # 320*240
sensor.skip_frames(time = 500) # 跳过，等待摄像头稳定
sensor.set_auto_gain(False) # 自动增益在颜色识别中一般关闭，不然会影响阈值
sensor.set_auto_whitebal(False) # 白平衡在颜色识别中一般关闭，不然会影响阈值
clock = time.clock() # 构造时钟对象


uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1, timeout_char=1000) # 使用给定参数初始化 timeout_char是以毫秒计的等待字符间的超时时长
def InitSuccess_LED():
    for i in range(2):
        LEDG.on()
        time.sleep(100)
        LEDG.off()
        time.sleep(100)
InitSuccess_LED()

class ctrl_info(object):
    WorkMode = 0x01 # 色块检测模式  0x01为固定单颜色识别  0x02为自主学习颜色识别
    Threshold_index = 0x00 # 阈值编号
Ctrl = ctrl_info() # 定义控制信息类
'''-----------------------------------------------初始化分割线------------------------------------------------'''


 # 比较返回最大色块（blobs为色块元组，中可能含有多个色块）
def find_max(blobs):
    max_size = 0
    for blob in blobs:
        if blob.w() * blob.h() > max_size: #长*宽
            max_blob = blob #
            max_size = blob.w()*blob.h()
    return max_blob



# 把除校验位的数据包全部累加 生成 累加和校验位
def sum_checkout(data_list):
    data_sum = 0
    for temp in data_list:
        data_sum += temp
    return (data_sum) #返回16进制

# 获取与色块的距离（利用识别度进行补偿）
def get_length(blob):
    blob_R = (blob.w()+blob.h())/2 # 长+高取平均较为准确
    length = 1800/blob_R
    length = length /((blob.density()/2)+0.5) # 进行准确度补偿（准确度补偿50%）
    print("length:%0.2f" %length)
    return int(length)

# 色块检测数据打包
def pack_blob_data(blob):

    #---包头------功能位----数据个数位----------------------------------数据包------------------------------------------累加和校验
    #【AA 55】    【01】     【09】      【阈值、色块个数、识别度、简单距离、色块中心坐标(高8位x，低8位x,高8位y，低8位y)、res】     【sum】

    datalist = [0xAA,0x55,Ctrl.WorkMode,0x09,
    Ctrl.Threshold_index,
    blob.count(),
    int(blob.density()*100),
    get_length(blob),
    blob.cx()>>8,blob.cx(),
    blob.cy()>>8,blob.cy(),
    0x00,0x00,0x00,0x00,0x00,0x00] # 定义返回数据列表

    print(datalist)
    datalist.append(sum_checkout(datalist))# 在list尾插入累加和校验
    data = bytearray(datalist)
    for res in data:
        print("%x" %res)
    #print(data)
    return data

# 检测色块时灯的状态
def check_blob_LEDStatus(blobs):
    if blobs:
        if Ctrl.Threshold_index == 0:
            LEDR.on()
        elif Ctrl.Threshold_index == 1:
            LEDG.on()
        elif Ctrl.Threshold_index == 2:
            LEDB.on()
    else:
        LEDR.off()
        LEDG.off()
        LEDB.off()

def check_blob(img):
    blobs = img.find_blobs([thresholds[threshold_index]], pixels_threshold=5, area_threshold=5, merge=True)
    # pixels_threshold为像素阈值，只有大于pixels_threshold才会被识别出来，area_threshold 为面积阈值，只有大于area_threshold才能被识别出来
    # merge=True 合并图像中所有重叠的斑点
    if blobs:
        max_blob = find_max(blobs) #找到最大的色块
        img.draw_rectangle(max_blob.rect()) #画矩形
        img.draw_cross(max_blob.cx(), max_blob.cy())#中心画十字
        #---包头------功能位----数据个数位----------------------------------数据包------------------------------------------累加和校验
        #【AA 55】    【01】     【09】      【阈值、色块个数、识别度、简单距离、色块中心坐标(高8位x，低8位x,高8位y，低8位y)、res】   【sum】
        uart.write(pack_blob_data(max_blob))

    check_blob_LEDStatus(blobs)









while(True):

    clock.tick() # 追踪时钟
    img = sensor.snapshot() #thresholds为阈值元组0
    if Ctrl.WorkMode == 0x01:
        check_blob(img)
    elif Ctrl.WorkMode == 0x02:
        a = 0 # 暂时为空











