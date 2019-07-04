import sensor, image, time ,math ,struct
from pyb import UART
from struct import pack, unpack
import json
red_threshold =(8, 95, 29, 79, 12, 68)#(9, 90, 52, 79, 12, 68)#(7, 90, 12, 70, -6, 41)#(15, 100, 40, 100, 40, 80)#(100, 27, 28, 111, 94, -59)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=3000)
sensor.set_auto_whitebal(False)
clock = time.clock()
uart = UART(3, 115200)

def find_max(blobs):
    max_size=1
    if blobs:
        max_blob = 0
        for blob in blobs:
            blob_size = blob.w()*blob.h()
            if ( (blob_size > max_size) & (blob_size > 100) & (blob.density()>0.8*math.pi/4) & (blob.density()<1.2*math.pi/4)  ) :
                if ( math.fabs( blob.w() / blob.h() - 1 ) < 0.5 ) :
                    max_blob=blob
                    max_size = blob.w()*blob.h()
        return max_blob

def find_red(blobs):
    max_size = 0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_size

def line_filter_copy(src, dst):
  for i in range(0, len(dst), 1):
      dst[i] = src[i<<1]
def line_filter_bw(src, dst):
  for i in range(0, len(dst), 1):
      if (src[i<<1] > 200 and src[i<<1] < 255):
          dst[i] = 0xFF
      else:
          dst[i] = 0x00

k = 0
max_number = 0
a = 0
b = 0
min_yellow = 0
tmp_data = 0


while(True):

    clock.tick()
    lines = 0
    img = sensor.snapshot(line_filter = line_filter_copy)
    red_blobs = img.find_blobs([red_threshold])
    max_blob=find_max(red_blobs)
    last_x = 1000
    last_y = 1000
    if max_blob:
        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        bx_x=max_blob.cx()-160
        by_y=120-max_blob.cy()
        x=math.fabs(bx_x)
        y=math.fabs(by_y)
        if 0 <= x < 10 :
            bx_value = 1
        elif 10 <= x < 100 :
            bx_value = 2
        else :
            bx_value = 3

        if 0 <= y < 10 :
            by_value = 1
        elif 10 <= y < 100 :
            by_value = 2
        else :
            by_value = 3


        sumB = 0
        data = bytearray([0xAA,0x55])
        uart.write(data)

        data = bytearray([0x02,8])
        for b in data:
            sumB = sumB + b
        uart.write(data)

        float_value = bx_x
        float_bytes = pack('f', float_value)
        for b in float_bytes:
            sumB = sumB + b
        uart.write(float_bytes)

        float_value = by_y
        float_bytes = pack('f', float_value)
        for b in float_bytes:
            sumB = sumB + b
        uart.write(float_bytes)

        data = bytearray([sumA, sumB])
        uart.write(data)

        print("found: x=",bx_x,"  y=",by_y)
        #b_output_str="x%d%d,y%d%d" % (bx_value,bx_x,by_value,by_y)
        #print('you send black:',b_output_str)
        #uart.write(b_output_str+'\r\n')
    else:
        sumA = 0
        sumB = 0

        data = bytearray([0xAA,0x55])
        uart.write(data)

        data = bytearray([0x01,0])
        for b in data:
            sumB = sumB + b
        uart.write(data)

        data = bytearray([sumA, sumB])
        uart.write(data)
        print(sumA," ",sumB)
        #print('not found!')
        #b_output_str = "x10,y10"
        #print('you send black:',b_output_str)
        #b_output_str = "x3750,y3750"
        #uart.write(b_output_str+'\r\n')
        #pass





