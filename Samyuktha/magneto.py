import BNO080 as m


mag = m.BNO080(B.BNO080BNO080_ADDRESS_B)
mag = m.begin()
while True:
    if mag.dataAvailable() == True:
        x, y, z = mag.get_mag()
        a = mag.getMagAccuracy()
        print('x componen=', x)
        print('y component=', y)
        print('z component=', z)
        print('accuracy=', a)








