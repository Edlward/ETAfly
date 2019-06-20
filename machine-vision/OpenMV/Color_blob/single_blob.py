import sensor, image, time, math , pyb
from pyb import LED

LEDB = pyb.LED(1) # Red LED = 2, Green LED = 3, Blue LED = 1, IR LEDs = 4.
LEDR = pyb.LED(2)
LEDG = pyb.LED(3)

def InitSuccess_LED():
    for i in range(2):
        LEDG.on()
        time.sleep(100)
        LEDG.off()
        time.sleep(100)

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
    K_value = 1800 # K值根据识别的色块大小而改变
    blob_R = (blob.w()+blob.h())/2 # 长+高取平均较为准确
    length = K_value/blob_R
    length = length /((blob.density()/2)+0.5) # 进行准确度补偿（准确度补偿50%）
    print("length:%0.2f" %length)
    return int(length)

# 色块检测数据打包
def pack_blob_data(blob,ctrl):

    #---包头------功能位----数据个数位----------------------------------数据包------------------------------------------累加和校验
    #【AA 55】    【01】     【09】      【阈值、色块个数、识别度、简单距离、色块中心坐标(高8位x，低8位x,高8位y，低8位y)、res】     【sum】

    datalist = [0xAA,0x55,ctrl.WorkMode,0x09,
    ctrl.Threshold_index,
    blob.count(),
    int(blob.density()*100),
    get_length(blob),
    blob.cx()>>8,blob.cx(),
    blob.cy()>>8,blob.cy(),
    0x00] # 定义返回数据列表

    print(datalist)
    datalist.append(sum_checkout(datalist))# 在list尾插入累加和校验
    data = bytearray(datalist)
    for res in data:
        print("%x" %res)
    #print(data)
    return data

# 检测色块时灯的状态
def single_blob_LEDStatus(blobs,ctrl):
    if blobs:
        if ctrl.Threshold_index == 0:
            LEDR.on()
        elif ctrl.Threshold_index == 1:
            LEDG.on()
        elif ctrl.Threshold_index == 2:
            LEDB.on()
    else:
        LEDR.off()
        LEDG.off()
        LEDB.off()



def check_blob(img,ctrl,thresholds,threshold_index,uart):
    blobs = img.find_blobs([thresholds[threshold_index]], pixels_threshold=5, area_threshold=5, merge=True)
    # pixels_threshold为像素阈值，只有大于pixels_threshold才会被识别出来，area_threshold 为面积阈值，只有大于area_threshold才能被识别出来
    # merge=True 合并图像中所有重叠的斑点
    if blobs:
        max_blob = find_max(blobs) #找到最大的色块
        img.draw_rectangle(max_blob.rect()) #画矩形
        img.draw_cross(max_blob.cx(), max_blob.cy())#中心画十字
        #---包头------功能位----数据个数位----------------------------------数据包------------------------------------------累加和校验
        #【AA 55】    【01】     【09】      【阈值、色块个数、识别度、简单距离、色块中心坐标(高8位x，低8位x,高8位y，低8位y)、res】   【sum】
        uart.write(pack_blob_data(max_blob,ctrl))
        LEDR.on()
    else:
        LEDR.off()

    single_blob_LEDStatus(blobs,ctrl)#LED状态
