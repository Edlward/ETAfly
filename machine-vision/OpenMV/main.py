import sensor, image, time, math , pyb ,json,single_blob
from pyb import LED,UART,Timer

threshold_index = 0 # 0 for red, 1 for green, 2 for blue


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



class ctrl_info(object):
    WorkMode = 0x01 # 色块检测模式  0x01为固定单颜色识别  0x02为自主学习颜色识别
    Threshold_index = 0x00 # 阈值编号

ctrl = ctrl_info() # 定义控制信息类
single_blob.InitSuccess_LED() # 初始化完成 Green LED 快闪2下
'''-----------------------------------------------初始化分割线------------------------------------------------'''


while(True):

    clock.tick() # 追踪时钟
    img = sensor.snapshot() # thresholds为阈值元组0
    if ctrl.WorkMode == 0x01:
        single_blob.check_blob(img,ctrl,thresholds,threshold_index,uart)
    elif ctrl.WorkMode == 0x02:
        a = 0 # 暂时为空











