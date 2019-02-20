import os

try:
    fifo = open('fifo', 'r')
    counter = 0
    while True:
        read = fifo.read(5)
        if read == '':
            continue
        print 'read ', read, counter
        counter += 1
except KeyboardInterrupt:
    fifo.close()
    print 'Cleaned, Exiting...'

