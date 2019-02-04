import BNO080 as B
mag = B.BNO080(B.BNO080_ADDRESS_B)
mag.begin()
mag.enable_magnetometer(50)
#B.enable_rotation_vector(50)
while True:
    if mag.data_available is True:
        x,y,z = mag.get_mag()
        print('x:',x,'y:',y,'z:',z)
