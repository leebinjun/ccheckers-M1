import struct
import threading
import time

import serial

from pydobot.message import Message

MODE_PTP_JUMP_XYZ = 0x00
MODE_PTP_MOVJ_XYZ = 0x01
MODE_PTP_MOVL_XYZ = 0x02
MODE_PTP_JUMP_ANGLE = 0x03
MODE_PTP_MOVJ_ANGLE = 0x04
MODE_PTP_MOVL_ANGLE = 0x05
MODE_PTP_MOVJ_INC = 0x06
MODE_PTP_MOVL_INC = 0x07
MODE_PTP_MOVJ_XYZ_INC = 0x08
MODE_PTP_JUMP_MOVL_XYZ = 0x09

board_list = [(246, -124.0), (237, -108.5), (255, -108.5), (228, -93.0), (246, -93.0), (264, -93.0), (219, -77.5), (237, -77.5), (255, -77.5), (273, -77.5), (138, -62.0), (156, -62.0), (174, -62.0), (192, -62.0), (210, -62.0), (228, -62.0), (246, -62.0), (264, -62.0), (282, -62.0), (300, -62.0), (318, -62.0), (336, -62.0), (354, -62.0), (147, -46.5), (165, -46.5), (183, -46.5), (201, -46.5), (219, -46.5), (237, -46.5), (255, -46.5), (273, -46.5), (291, -46.5), (309, -46.5), (327, -46.5), (345, -46.5), (156, -31.0), (174, -31.0), (192, -31.0), (210, -31.0), (228, -31.0), (246, -31.0), (264, -31.0), (282, -31.0), (300, -31.0), (318, -31.0), (336, -31.0), (165, -15.5), (183, -15.5), (201, -15.5), (219, -15.5), (237, -15.5), (255, -15.5), (273, -15.5), (291, -15.5), (309, -15.5), (327, -15.5), (174, 0.0), (192, 0.0), (210, 0.0), (228, 0.0), (246, 0.0), (264, 0.0), (282, 0.0), (300, 0.0), (318, 0.0), (165, 15.5), (183, 15.5), (201, 15.5), (219, 15.5), (237, 15.5), (255, 15.5), (273, 15.5), (291, 15.5), (309, 15.5), (327, 15.5), (156, 31.0), (174, 31.0), (192, 31.0), (210, 31.0), (228, 31.0), (246, 31.0), (264, 31.0), (282, 31.0), (300, 31.0), (318, 31.0), (336, 31.0), (147, 46.5), (165, 46.5), (183, 46.5), (201, 46.5), (219, 46.5), (237, 46.5), (255, 46.5), (273, 46.5), (291, 46.5), (309, 46.5), (327, 46.5), (345, 46.5), (138, 62.0), (156, 62.0), (174, 62.0), (192, 62.0), (210, 62.0), (228, 62.0), (246, 62.0), (264, 62.0), (282, 62.0), (300, 62.0), (318, 62.0), (336, 62.0), (354, 62.0), (219, 77.5), (237, 77.5), (255, 77.5), (273, 77.5), (228, 93.0), (246, 93.0), (264, 93.0), (237, 108.5), (255, 108.5), (246, 124.0)]

class Dobot(threading.Thread):
    on = True
    x = 0.0
    y = 0.0
    z = 0.0
    r = 0.0
    j1 = 0.0
    j2 = 0.0
    j3 = 0.0
    j4 = 0.0

    # joint_angles = [4]

    def __init__(self, port, verbose=False):
        threading.Thread.__init__(self)
        self.verbose = verbose
        self.lock = threading.Lock()
        self.ser = serial.Serial(port,
                                 baudrate=115200,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS)
        is_open = self.ser.isOpen()
        if self.verbose:
            print('pydobot: %s open' % self.ser.name if is_open else 'failed to open serial port')
        self._set_ptp_coordinate_params(velocity=200.0, acceleration=200.0)
        self._set_ptp_common_params(velocity=200.0, acceleration=200.0)
        self.start()

    def run(self):
        while self.on:
            self._get_pose()
            time.sleep(0.2)

    def close(self):
        self.on = False
        self.lock.acquire()
        self.ser.close()
        if self.verbose:
            print('pydobot: %s closed' % self.ser.name)
        self.lock.release()

    def _send_command(self, msg):
        self.lock.acquire()
        self._send_message(msg)
        response = self._read_message()
        self.lock.release()
        return response

    def _send_message(self, msg):
        time.sleep(0.1)
        if self.verbose:
            print('pydobot: >>', msg)
        self.ser.write(msg.bytes())

    def _read_message(self):
        time.sleep(0.1)
        b = self.ser.read_all()
        if len(b) > 0:
            msg = Message(b)
            if self.verbose:
                print('pydobot: <<', msg)
            return msg
        return

    def _get_pose(self):
        msg = Message()
        msg.id   = 10
        msg.len  = 0x02
        msg.ctrl = 0x00
        # print(msg.bytes())
        response = self._send_command(msg)
        self.x = struct.unpack_from('f', response.params, 0)[0]
        self.y = struct.unpack_from('f', response.params, 4)[0]
        self.z = struct.unpack_from('f', response.params, 8)[0]
        self.r = struct.unpack_from('f', response.params, 12)[0]
        self.j1 = struct.unpack_from('f', response.params, 16)[0]
        self.j2 = struct.unpack_from('f', response.params, 20)[0]
        self.j3 = struct.unpack_from('f', response.params, 24)[0]
        self.j4 = struct.unpack_from('f', response.params, 28)[0]
        if self.verbose:
            print("pydobot: x:%03.1f y:%03.1f z:%03.1f r:%03.1f j1:%03.1f j2:%03.1f j3:%03.1f j4:%03.1f" %
                  (self.x, self.y, self.z, self.r, self.j1, self.j2, self.j3, self.j4))
        return response

    def _set_cp_cmd(self, x, y, z):
        msg = Message()
        msg.id = 91
        msg.ctrl = 0x03
        msg.params = bytearray(bytes([0x01]))
        msg.params.extend(bytearray(struct.pack('f', x)))
        msg.params.extend(bytearray(struct.pack('f', y)))
        msg.params.extend(bytearray(struct.pack('f', z)))
        msg.params.append(0x00)
        return self._send_command(msg)

    def _set_ptp_coordinate_params(self, velocity, acceleration):
        msg = Message()
        msg.id = 81
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray(struct.pack('f', velocity)))
        msg.params.extend(bytearray(struct.pack('f', velocity)))
        msg.params.extend(bytearray(struct.pack('f', acceleration)))
        msg.params.extend(bytearray(struct.pack('f', acceleration)))
        return self._send_command(msg)

   #TODO:@binjun
    def _set_ptp_jump_params(self, jumpHeight, zLimit):
        msg = Message()
        msg.id = 82
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray(struct.pack('f', jumpHeight)))
        msg.params.extend(bytearray(struct.pack('f', zLimit)))
        return self._send_command(msg)

    def _set_ptp_common_params(self, velocity, acceleration):
        msg = Message()
        msg.id = 83
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray(struct.pack('f', velocity)))
        msg.params.extend(bytearray(struct.pack('f', acceleration)))
        return self._send_command(msg)

    def _set_ptp_cmd(self, x, y, z, r, mode):
        msg = Message()
        msg.id = 84
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray([mode]))
        msg.params.extend(bytearray(struct.pack('f', x)))
        msg.params.extend(bytearray(struct.pack('f', y)))
        msg.params.extend(bytearray(struct.pack('f', z)))
        msg.params.extend(bytearray(struct.pack('f', r)))
        print(msg.bytes())
        return self._send_command(msg)

    def _set_end_effector_suction_cup(self, suck=False):
        msg = Message()
        msg.id = 62
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(bytearray([0x01]))
        if suck is True:
            msg.params.extend(bytearray([0x01]))
        else:
            msg.params.extend(bytearray([0x00]))
        print(msg.bytes())
        return self._send_command(msg)

    def go(self, x, y, z, r=0., mode=MODE_PTP_MOVJ_XYZ):
        self._set_ptp_cmd(x, y, z, r, mode)

    def suck(self, suck):
        self._set_end_effector_suction_cup(suck)

    def speed(self, velocity=100., acceleration=100.):
        self._set_ptp_common_params(velocity, acceleration)
        self._set_ptp_coordinate_params(velocity, acceleration)

    def set_jumpHeight(self, jumpHeight):
        self._set_ptp_jump_params(jumpHeight = 10, zLimit = 150)

    def foo_suck_open(self):
        self.foo_suck_1()
        self.foo_suck_2()

    def foo_suck_close(self):
        self.foo_suck_1()
        self.foo_suck_3()



    def foo_suck_1(self):
        time.sleep(0.1)
        
        # command = bytes([0xAA, 0xAA, 4, 131, 0x03, self.checksum])
        command = Message()
        command.len      = 2+2
        command.id       = 131
        command.params   = bytes([0x11, 0x00])
        command.header   = bytes([0xAA, 0xAA])
        command.ctrl     = 0x03
        print(command.bytes())
        # command.checksum = None
        
        self.ser.write(command.bytes())

    def foo_suck_2(self):
        time.sleep(0.1)
        
        # command = bytes([0xAA, 0xAA, 4, 131, 0x03, self.checksum])
        command = Message()
        command.len      = 2+2
        command.id       = 131
        command.params   = bytes([0x12, 0x01])
        command.header   = bytes([0xAA, 0xAA])
        command.ctrl     = 0x03
        print(command.bytes())
        # command.checksum = None
        
        self.ser.write(command.bytes())

    def foo_suck_3(self):
        time.sleep(0.1)
        
        # command = bytes([0xAA, 0xAA, 4, 131, 0x03, self.checksum])
        command = Message()
        command.len      = 2+2
        command.id       = 131
        command.params   = bytes([0x12, 0x00])
        command.header   = bytes([0xAA, 0xAA])
        command.ctrl     = 0x03
        print(command.bytes())
        # command.checksum = None
        
        self.ser.write(command.bytes())