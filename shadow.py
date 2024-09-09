import math 
h=float(input('输入观察目标之长度'))
while True:
    angle=math.radians(float(input('输入太阳方位角'))-90)
    angle2=math.radians(float(input('输入太阳高度角')))
    l=h/math.tan(angle2)
   
    result_x=l*math.cos(angle)
    result_y=l*math.sin(angle)

    print('(',-result_x,',',result_y,')')