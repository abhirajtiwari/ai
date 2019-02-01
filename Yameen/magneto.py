import BNO080 as B
mag = B.BNO080(B.BNO080BNO080_ADDRESS_B)
mag = B.begin()

#B.enable_rotation_vector(50)
while True:

    x,y,z = mag.get_mag()
    print('x:',x,'y:',y,'z:',z)
