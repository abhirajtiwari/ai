# Adafruit BNO080 Absolute Orientation Sensor Library
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import binascii
import logging
import struct
import time
import pigpio
import Adafruit_GPIO.I2C as I2C


# I2C addresses
BNO080_ADDRESS_A                     = 0x4A
BNO080_ADDRESS_B                     = 0x4B
BNO080_ID                            = 0xF8


# SHTP = Sensor Hub Transport Protocol

# All the ways we can configure or talk to the BNO080, figure 34, page 36 reference manual
# These are used for low level communication with the sensor, on channel 2

# Channel names
CHANNEL_COMMAND = 0
CHANNEL_EXECUTABLE = 1
CHANNEL_CONTROL = 2
CHANNEL_REPORTS = 3
CHANNEL_WAKE_REPORTS = 4
CHANNEL_GYRO = 5

SHTP_REPORT_COMMAND_RESPONSE = 0xF1
SHTP_REPORT_COMMAND_REQUEST = 0xF2
SHTP_REPORT_FRS_READ_RESPONSE = 0xF3
SHTP_REPORT_FRS_READ_REQUEST = 0xF4
SHTP_REPORT_PRODUCT_ID_RESPONSE = 0xF8
SHTP_REPORT_PRODUCT_ID_REQUEST = 0xF9
SHTP_REPORT_BASE_TIMESTAMP = 0xFB
SHTP_REPORT_SET_FEATURE_COMMAND = 0xFD

# All the different sensors and features we can get reports from
# These are used when enabling a given sensor
SENSOR_REPORTID_ACCELEROMETER = 0x01
SENSOR_REPORTID_GYROSCOPE = 0x02
SENSOR_REPORTID_MAGNETIC_FIELD = 0x03
SENSOR_REPORTID_LINEAR_ACCELERATION = 0x04
SENSOR_REPORTID_ROTATION_VECTOR = 0x05
SENSOR_REPORTID_GRAVITY = 0x06
SENSOR_REPORTID_GAME_ROTATION_VECTOR = 0x08
SENSOR_REPORTID_GEOMAGNETIC_ROTATION_VECTOR = 0x09
SENSOR_REPORTID_MAGNETIC_FIELD_UNCALIBRATED = 0x0F
SENSOR_REPORTID_TAP_DETECTOR = 0x10
SENSOR_REPORTID_STEP_COUNTER = 0x11
SENSOR_REPORTID_STABILITY_CLASSIFIER = 0x13
SENSOR_REPORTID_PERSONAL_ACTIVITY_CLASSIFIER = 0x1E

# Record IDs from figure 29, page 29 reference manual
# These are used to read the metadata for each sensor type
FRS_RECORDID_ACCELEROMETER = 0xE302
FRS_RECORDID_GYROSCOPE_CALIBRATED = 0xE306
FRS_RECORDID_MAGNETIC_FIELD_CALIBRATED = 0xE309
FRS_RECORDID_ROTATION_VECTOR = 0xE30B

# Command IDs from section 6.4, page 42
# These are used to calibrate, initialize, set orientation, tare etc the sensor
COMMAND_ERRORS = 1
COMMAND_COUNTER = 2
COMMAND_TARE = 3
COMMAND_INITIALIZE = 4
COMMAND_DCD = 6
COMMAND_ME_CALIBRATE = 7
COMMAND_DCD_PERIOD_SAVE = 9
COMMAND_OSCILLATOR = 10
COMMAND_CLEAR_DCD = 11

CALIBRATE_ACCEL = 0
CALIBRATE_GYRO = 1
CALIBRATE_MAG = 2
CALIBRATE_PLANAR_ACCEL = 3
CALIBRATE_ACCEL_GYRO_MAG = 4
CALIBRATE_STOP = 5
CALIBRATE_ACCEL_MAG = 6

ROTATION_VECTOR_Q = 14
ROTATION_ACCURACY_Q = 12
ACCELEROMETER_Q = 8
GYRO_Q = 9
MAGNETOMETER_Q = 4


class BNO080(object):
    receivedData = []
    sequenceNumber = [0, 0, 0, 0, 0, 0]

    accelAccuracy = 0
    rawAccelX = 0
    rawAccelY = 0
    rawAccelZ = 0
    accelLinAccuracy = 0
    rawLinAccelX = 0
    rawLinAccelY = 0
    rawLinAccelZ = 0
    gyroAccuracy = 0
    rawGyroX = 0
    rawGyroY = 0
    rawGyroZ = 0
    magAccuracy = 0
    rawMagX = 0
    rawMagY = 0
    rawMagZ = 0
    quatAccuracy = 0
    rawQuatI = 0
    rawQuatJ = 0
    rawQuatK = 0
    rawQuatReal = 0
    rawQuatRadianAccuracy = 0

    sensorDelay = 0
    magSensorDelay = 0
    gyroSensorDelay = 0
    accelSensorDelay = 0
    posSensorDelay = 0
    linearAccelSensorDelay = 0

    calibrationStatus = 0
    accelCalEnabled = 0
    gyroCalEnabled = 0
    magCalEnabled = 0

    def __init__(self, address=BNO080_ADDRESS_B, gpio=None, **kwargs):
        self.pi = pigpio.pi()
        if self.pi.connected is False:
            raise RuntimeError('Error connecting to the PI with pigpio')

        self.h = self.pi.i2c_open(1, address)

    def _send_packet(self, channelNumber, dataLength, data):

        packetLength = dataLength + 4

        data = [packetLength & 0xFF, packetLength >> 8, channelNumber, self.sequenceNumber[channelNumber]] + data

        # print ''
        # print 'Sending packet'
        # print ' '.join('{:02x}'.format(x) for x in data)
        # self._i2c_device.writeList(0, data)
        self.pi.i2c_write_device(self.h, data)

        # Increment the sequence counter
        self.sequenceNumber[channelNumber] = self.sequenceNumber[channelNumber] + 1

    def _send_command(self, command, data):
        data[0] = SHTP_REPORT_COMMAND_REQUEST
        data[1] = self.sequenceNumber[CHANNEL_CONTROL]
        data[2] = command

        self._send_packet(CHANNEL_CONTROL, 12, data)

    def _receive_packet(self):
        (count, data) = self.pi.i2c_read_device(self.h, 4)
        if count <= 0:
            return False
        # data = self._i2c_device.readList(0, 4)

        # Store the header info.
        shtpHeader = [data[0], data[1], data[2], data[3]]

        # Calculate the number of data bytes in this packet
        dataLength = shtpHeader[1] << 8 | shtpHeader[0]
        dataLength &= ~(1 << 15)  # Clear the MSbit.

        if dataLength == 0:
            return False
        else:
            # print ''
            # print 'Received packet:'
            # print ' '.join('{:02x}'.format(x) for x in shtpHeader)
            # print('Length: {0}'.format(dataLength - 4))
            # print('Channel: {0}'.format(shtpHeader[2]))

            # receivedData = self._i2c_device.readList(0, dataLength)
            (count, receivedData) = self.pi.i2c_read_device(self.h, dataLength)
            if len(receivedData) < 4:
                # Not big enough for the header so its bad data
                return False;
            self.receivedHeader = receivedData[0:4]
            self.receivedData = receivedData[4:dataLength]
            # print ' '.join('{:02x}'.format(x) for x in self.receivedHeader)
            # print ' '.join('{:02x}'.format(x) for x in self.receivedData)
            return True

    def _set_feature_command(self, reportID, timeBetweenReports, specificConfig=0):
        data = []
        data.append(SHTP_REPORT_SET_FEATURE_COMMAND)
        data.append(reportID)
        data.append(0)  # Feature flags
        data.append(0)  # Change sensitivity (LSB)
        data.append(0)  # Change sensitivity (MSB)
        data.append((timeBetweenReports >> 0) & 0xFF)   # Report interval (LSB) in microseconds. 0x7A120 = 500ms
        data.append((timeBetweenReports >> 8) & 0xFF)   # Report interval
        data.append((timeBetweenReports >> 16) & 0xFF)  # Report interval
        data.append((timeBetweenReports >> 24) & 0xFF)  # Report interval (MSB)
        data.append(0)  # Batch Interval (LSB)
        data.append(0)  # Batch Interval
        data.append(0)  # Batch Interval
        data.append(0)  # Batch Interval (MSB)
        data.append((specificConfig >> 0) & 0xFF)   # Sensor-specific config (LSB)
        data.append((specificConfig >> 8) & 0xFF)   # Sensor-specific config
        data.append((specificConfig >> 16) & 0xFF)  # Sensor-specific config
        data.append((specificConfig >> 24) & 0xFF)  # Sensor-specific config (MSB)
        self._send_packet(CHANNEL_CONTROL, 17, data)

    def _set_calibrate_command(self, thing_to_calibrate):
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if thing_to_calibrate == CALIBRATE_ACCEL:
            data[3] = 1
        elif thing_to_calibrate == CALIBRATE_GYRO:
            data[4] = 1
        elif thing_to_calibrate == CALIBRATE_MAG:
            data[5] = 1
        elif thing_to_calibrate == CALIBRATE_PLANAR_ACCEL:
            data[7] = 1
        elif thing_to_calibrate == CALIBRATE_ACCEL_GYRO_MAG:
            data[3] = 1
            data[4] = 1
            data[5] = 1
        elif thing_to_calibrate == CALIBRATE_ACCEL_MAG:
            data[3] = 1
            data[5] = 1

        self._send_command(COMMAND_ME_CALIBRATE, data)

    def save_dcd_command(self):
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # Dynamic calibration data
        self._send_command(COMMAND_DCD, data)

    def save_dcd_periodically_command(self):
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._send_command(COMMAND_DCD_PERIOD_SAVE, data)

    def soft_reset(self):
        self._send_packet(CHANNEL_EXECUTABLE, 1, [1])
        time.sleep(0.5)
        new_data = True
        while new_data:
            new_data = self._receive_packet()
            time.sleep(0.1)

    def begin(self):
        # reset
        self.soft_reset()

        # Check communication with device
        data = [SHTP_REPORT_PRODUCT_ID_REQUEST, 0]
        # Transmit packet on channel 2, 2 bytes
        self._send_packet(CHANNEL_CONTROL, 2, data)

        # Now we wait for response
        if self._receive_packet():
            if self.receivedData[0] == SHTP_REPORT_PRODUCT_ID_RESPONSE:
                return True

        return False

    def stop(self):
        print 'Stopping IMU'
        self.pi.stop()

    def enable_rotation_vector(self, update_time):
        # This is the 3d fusion mode
        self._set_feature_command(SENSOR_REPORTID_ROTATION_VECTOR, update_time * 1000)

    def enable_linear_acceleration(self, update_time):
        self._set_feature_command(SENSOR_REPORTID_LINEAR_ACCELERATION, update_time * 1000)

    def enable_accelerometer(self, update_time):
        self._set_feature_command(SENSOR_REPORTID_ACCELEROMETER, update_time * 1000)

    def enable_gyro(self, update_time):
        self._set_feature_command(SENSOR_REPORTID_GYROSCOPE, update_time * 1000)

    def enable_mag_rotation_vector(self, update_time):
        # This is the 3d fusion mode
        self._set_feature_command(SENSOR_REPORTID_GEOMAGNETIC_ROTATION_VECTOR, update_time * 1000)

    def enable_magnetometer(self, update_time):
        self._set_feature_command(SENSOR_REPORTID_MAGNETIC_FIELD, update_time * 1000)

    def calibrate_all(self):
        self._set_calibrate_command(CALIBRATE_ACCEL_GYRO_MAG)

    def calibrate_main(self):
        self._set_calibrate_command(CALIBRATE_ACCEL_MAG)

    def end_calibrate(self):
        self._set_calibrate_command(CALIBRATE_STOP)

    def save_calibration(self):
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._send_command(COMMAND_DCD, data)

    def get_calibration_status(self):
        return [self.calibrationStatus, self.accelCalEnabled, self.gyroCalEnabled, self.magCalEnabled]

    def data_available(self):
        response = self._receive_packet()
        if response is False:
            return False
        else:
            if self.receivedHeader[2] == CHANNEL_REPORTS:
                data_to_parse = True
                while data_to_parse is not None:
                    data_to_parse = self._parse_input_report()
            elif self.receivedHeader[2] == CHANNEL_CONTROL:
                self._parse_command_report()
            return True

    def get_mag_accuracy(self):
        return self.magAccuracy

    def get_quat_accuracy(self):
        # rotation position accurate to about 5 degrees
        return self.quatAccuracy

    def get_linear_accuracy(self):
        return self.accelLinAccuracy

    def get_accelerometer_accuracy(self):
        return self.accelAccuracy

    def get_gyro_accuracy(self):
        return self.gyroAccuracy

    def get_data_array(self):
        return self.receivedData

    def get_data_delay(self):
        return self.sensorDelay

    def get_gyro_data_delay(self):
        return self.gyroSensorDelay

    def get_pos_data_delay(self):
        return self.posSensorDelay

    def get_linear_accel_data_delay(self):
        return self.linearAccelSensorDelay

    def get_accel_data_delay(self):
        return self.accelSensorDelay

    def get_mag_data_delay(self):
        return self.magSensorDelay

    def get_rotation_quaternion(self):
        # Returns a rotation vector as a unit quaternion
        i = self.rawQuatI        # x
        j = self.rawQuatJ        # y
        k = self.rawQuatK        # z
        real = self.rawQuatReal  # w

        i = self._convert_q_number(i, ROTATION_VECTOR_Q)
        j = self._convert_q_number(j, ROTATION_VECTOR_Q)
        k = self._convert_q_number(k, ROTATION_VECTOR_Q)
        real = self._convert_q_number(real, ROTATION_VECTOR_Q)

        return [i, j, k, real]

    def get_rotation_accuracy(self):
        # Heading accuracy in radians
        accuracy = self.rawQuatRadianAccuracy
        return self._convert_q_number(accuracy, ROTATION_ACCURACY_Q)

    def get_linear_acceleration(self):
        x = self.rawLinAccelX
        y = self.rawLinAccelY
        z = self.rawLinAccelZ

        x = self._convert_q_number(x, ACCELEROMETER_Q)
        y = self._convert_q_number(y, ACCELEROMETER_Q)
        z = self._convert_q_number(z, ACCELEROMETER_Q)
        return [x, y, z]

    def get_acceleration(self):
        x = self.rawAccelX
        y = self.rawAccelY
        z = self.rawAccelZ

        x = self._convert_q_number(x, ACCELEROMETER_Q)
        y = self._convert_q_number(y, ACCELEROMETER_Q)
        z = self._convert_q_number(z, ACCELEROMETER_Q)
        return [x, y, z]

    def get_gyro(self):
        x = self.rawGyroX
        y = self.rawGyroY
        z = self.rawGyroZ

        x = self._convert_q_number(x, GYRO_Q)
        y = self._convert_q_number(y, GYRO_Q)
        z = self._convert_q_number(z, GYRO_Q)
        return [x, y, z]

    def get_mag(self):
        x = self.rawMagX
        y = self.rawMagY
        z = self.rawMagZ

        x = self._convert_q_number(x, MAGNETOMETER_Q)
        y = self._convert_q_number(y, MAGNETOMETER_Q)
        z = self._convert_q_number(z, MAGNETOMETER_Q)

        return [x, y, z]

    @staticmethod
    def _convert_q_number(number, q_point):
        return number * pow(2, (q_point * -1))

    def _parse_base_timestamp(self, data):
        return data[4] << 24 | data[3] << 16 | data[2] << 8 | data[1]

    def parse_sensor_report(self, data):
        report_id = data[0]
        sequence_number = data[1]
        status = data[2] & 0x03
        data1 = data[5] << 8 | data[4]
        data2 = data[7] << 8 | data[6]
        data3 = data[9] << 8 | data[8]
        if len(data) > 11:
            data4 = data[11] << 8 | data[10]
        else:
            data4 = 0
        if len(data) > 13:
            data5 = data[13] << 8 | data[12]
        else:
            data5 = 0
        return [status, data1, data2, data3, data4, data5]

    def _parse_input_report(self):
        if len(self.receivedData) == 0:
            # The data has been parsed, nothing else to do
            return None

        if len(self.receivedData) < 10:
            print 'Report to short'
            print ' '.join('{:02x}'.format(x) for x in self.receivedData)
            return None

        status, data1, data2, data3, data4, data5 = self.parse_sensor_report(self.receivedData)

        if (self.receivedData[0]) == SHTP_REPORT_BASE_TIMESTAMP:
            # report size 5 bytes

            self.sensorDelay = self._parse_base_timestamp(self.receivedData[0:5])
            # print 'Delay between sensor sample and sending it: {0} us'.format(delay)

            # Strip the now parsed sensor packed out
            self.receivedData = self.receivedData[5:(len(self.receivedData))]

        elif self.receivedData[0] == SENSOR_REPORTID_ACCELEROMETER:
            # report size 10 bytes
            # print 'SENSOR_REPORTID_ACCELEROMETER'
            self.accelAccuracy = status
            self.rawAccelX = self._convert_signed_number(data1)
            self.rawAccelY = self._convert_signed_number(data2)
            self.rawAccelZ = self._convert_signed_number(data3)

            self.accelSensorDelay = self.sensorDelay

            # Strip the now parsed sensor packed out
            self.receivedData = self.receivedData[10:(len(self.receivedData))]

        elif self.receivedData[0] == SENSOR_REPORTID_LINEAR_ACCELERATION:
            # report size 10 bytes
            # print 'SENSOR_REPORTID_LINEAR_ACCELERATION'
            self.accelLinAccuracy = status
            self.rawLinAccelX = self._convert_signed_number(data1)
            self.rawLinAccelY = self._convert_signed_number(data2)
            self.rawLinAccelZ = self._convert_signed_number(data3)

            self.linearAccelSensorDelay = self.sensorDelay

            # Strip the now parsed sensor packed out
            self.receivedData = self.receivedData[10:(len(self.receivedData))]

        elif self.receivedData[0] == SENSOR_REPORTID_GYROSCOPE:
            # report size 10 bytes
            # print 'SENSOR_REPORTID_GYROSCOPE'
            self.gyroAccuracy = status
            self.rawGyroX = self._convert_signed_number(data1)
            self.rawGyroY = self._convert_signed_number(data2)
            self.rawGyroZ = self._convert_signed_number(data3)

            self.gyroSensorDelay = self.sensorDelay

            # Strip the now parsed sensor packed out
            self.receivedData = self.receivedData[10:(len(self.receivedData))]

        elif self.receivedData[0] == SENSOR_REPORTID_MAGNETIC_FIELD:
            # report size 10 bytes
            self.magAccuracy = status
            self.rawMagX = self._convert_signed_number(data1)
            self.rawMagY = self._convert_signed_number(data2)
            self.rawMagZ = self._convert_signed_number(data3)

            self.magSensorDelay = self.sensorDelay

            # Strip the now parsed sensor packed out
            self.receivedData = self.receivedData[10:(len(self.receivedData))]

        elif self.receivedData[0] == SENSOR_REPORTID_ROTATION_VECTOR or self.receivedData[0] == SENSOR_REPORTID_GAME_ROTATION_VECTOR or self.receivedData[0] == SENSOR_REPORTID_GEOMAGNETIC_ROTATION_VECTOR:
            # report size 14 bytes
            # print 'SENSOR_REPORTID_ROTATION_VECTOR Channel:{:02x}'.format(self.receivedData[0])
            self.quatAccuracy = status
            self.rawQuatI = self._convert_signed_number(data1)
            self.rawQuatJ = self._convert_signed_number(data2)
            self.rawQuatK = self._convert_signed_number(data3)
            self.rawQuatReal = self._convert_signed_number(data4)
            self.rawQuatRadianAccuracy = data5  # Only available on rotation vector, not game rot vector

            self.posSensorDelay = self.sensorDelay

            # Strip the now parsed sensor packed out
            self.receivedData = self.receivedData[14:(len(self.receivedData))]

        elif self.receivedData[0] == SENSOR_REPORTID_STEP_COUNTER:
            # report size 12 bytes
            print 'SENSOR_REPORTID_STEP_COUNTER'
            self.stepCount = data3

            # Strip the now parsed sensor packed out
            self.receivedData = self.receivedData[12:(len(self.receivedData))]

        elif self.receivedData[0] == SENSOR_REPORTID_STABILITY_CLASSIFIER:
            # report size 6 bytes
            print 'SENSOR_REPORTID_STABILITY_CLASSIFIER'
            self.stabilityClassifier = self.receivedData[4]

            # Strip the now parsed sensor packed out
            self.receivedData = self.receivedData[6:(len(self.receivedData))]

        elif self.receivedData[0] == SENSOR_REPORTID_PERSONAL_ACTIVITY_CLASSIFIER:
            print 'SENSOR_REPORTID_PERSONAL_ACTIVITY_CLASSIFIER'
            self.activityClassifier = self.receivedData[5]

        elif self.receivedData[0] == SHTP_REPORT_COMMAND_RESPONSE:
            print 'SHTP_REPORT_COMMAND_RESPONSE'
            # The BNO080 responds with this report to command requests.
            # It's up to use to remember which command we issued.
            command = self.receivedData[2]  # This is the Command byte of the response
            if command == COMMAND_ME_CALIBRATE:
                # Calibration report found
                self.calibrationStatus = self.receivedData[5]  # R0 - Status (0 = success, non-zero = fail)
                self.accelCalEnabled = self.receivedData[6]  # R0 - Status (1 = enabled, 0 = disabled)
                self.gyroCalEnabled = self.receivedData[7]  # R0 - Status (1 = enabled, 0 = disabled)
                self.magCalEnabled = self.receivedData[8]  # R0 - Status (1 = enabled, 0 = disabled)
                if self.calibrationStatus:
                    print 'Calibration error, response: {0}'.format(self.calibrationStatus)
            else:
                print 'Unknown command response received. Command: {0}'.format(command)
                print ' '.join('{:02x}'.format(x) for x in self.receivedData)

        return True

    def _parse_command_report(self):
        if self.receivedData[0] == SHTP_REPORT_COMMAND_RESPONSE:
            command = self.receivedData[2]
            if command == COMMAND_ME_CALIBRATE:
                # Calibration report found
                self.calibrationStatus = self.receivedData[5]  # R0 - Status (0 = success, non-zero = fail)
                self.accelCalEnabled = self.receivedData[6]  # R0 - Status (1 = enabled, 0 = disabled)
                self.gyroCalEnabled = self.receivedData[7]  # R0 - Status (1 = enabled, 0 = disabled)
                self.magCalEnabled = self.receivedData[8]  # R0 - Status (1 = enabled, 0 = disabled)
                print 'Calibration response: {0}'.format(self.calibrationStatus)
            elif command == COMMAND_DCD:
                print 'DCD command response'
                if self.receivedData[5] != 0:
                    print 'Save DCD command failed'
            else:
                print 'Unknown command response received. Command: {0}'.format(command)
                print ' '.join('{:02x}'.format(x) for x in self.receivedData)

    @staticmethod
    def _convert_signed_number(number):
        if number > 0x7FFF:
            return -((number & 0x7FFF) ^ 0x7FFF)
        return number