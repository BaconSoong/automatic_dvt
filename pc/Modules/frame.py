import struct
import crcmod.predefined
import socket
import threading
import queue
import time

F_HEADER = (0xC3, 0xF5, 0xD4, 0xA6)
F_HEADER_SIZE = 4
F_TAILER = (0xA7, 0xC8)
F_TAILER_SIZE = 2
F_MES_TAG_SIZE = 3


class FrameDVT(object):

    def __init__(self, **kwargs):
        self.f_header = F_HEADER
        self.f_type = kwargs.get('type')
        self.f_dev_tag = kwargs.get('dev_tag')
        self.f_mod_tag = kwargs.get('mod_tag')
        self.f_islast_tag = 0x01  # kwargs.get('islast_tag')
        self.f_status = 0x00  # kwargs.get('status')
        self.f_mes_tag = 0x000001  # kwargs.get('mes_tag')
        self.f_stream_tag = 0x00000001  # kwargs.get('stream_tag')
        self.f_content_len = None  # len(kwargs.get('content'))
        self.f_content = kwargs.get('content')
        self.f_crc = None
        self.f_tailer = F_TAILER

    def get_variables(self):
        return {
            'f_header': tuple(hex(x) for x in self.f_header),
            'f_type': hex(self.f_type),
            'f_dev_tag': hex(self.f_dev_tag),
            'f_mod_tag': hex(self.f_mod_tag),
            'f_islast_tag': hex(self.f_islast_tag),
            'f_status': hex(self.f_status),
            'f_mes_tag': hex(self.f_mes_tag),
            'f_stream_tag': hex(self.f_stream_tag),
            'f_content_len': hex(self.f_content_len),
            'f_content': [hex(x) for x in self.f_content],
            'f_crc': hex(self.f_crc),
            'f_tailer': tuple(hex(x) for x in self.f_tailer)
        }

    @staticmethod
    def crc(frame):
        # 定义 CRC16/MODBUS 参数
        width = 16
        poly = 0x8005
        initial_value = 0xFFFF
        final_xor = 0x0000

        # 创建 CRC16/MODBUS 校验对象
        crc16 = crcmod.predefined.Crc('modbus')

        crc16.update(frame)
        return crc16.crcValue

    def pack_frame(self):
        content_len = len(self.f_content)
        if content_len != self.f_content_len:
            self.f_content_len = content_len
        frame_data = struct.pack(
            "!{}BBBBBIII{}B".format(F_HEADER_SIZE, content_len),
            *self.f_header,
            self.f_type,
            self.f_dev_tag,
            self.f_mod_tag,
            self.f_islast_tag,
            (self.f_status << 24 | self.f_mes_tag),
            self.f_stream_tag,
            self.f_content_len,
            *self.f_content
        )
        self.f_crc = FrameDVT.crc(frame_data)
        frame = frame_data + struct.pack("!H", self.f_crc) + struct.pack("!BB", *self.f_tailer)

        return frame

    def parse_frame(self, frame):
        header_size = F_HEADER_SIZE
        tailer_size = F_TAILER_SIZE

        # 解析帧头部
        header = frame[:header_size]
        self.f_header = tuple(header)

        # 解析帧类型
        self.f_type = frame[header_size]

        # 解析设备标识、模块标识、是否最后一帧标识、状态和消息标识
        self.f_dev_tag, self.f_mod_tag, self.f_islast_tag, f_status_mes_tag = struct.unpack(
            "!BBBI",
            frame[header_size + 1:header_size + 8]
        )
        self.f_status = f_status_mes_tag >> 24
        self.f_mes_tag = f_status_mes_tag & 0x00FFFFFF

        # 解析流标识、内容长度和内容
        self.f_stream_tag, self.f_content_len = struct.unpack("!II", frame[header_size + 8:header_size + 16])
        self.f_content = list(frame[header_size + 16:header_size + 16 + self.f_content_len])

        # 解析校验和和帧尾部
        crc_index = len(frame) - tailer_size - 2
        self.f_crc = struct.unpack("!H", frame[crc_index:crc_index + 2])[0]
        self.f_tailer = tuple(frame[-tailer_size:])
        crc_value = FrameDVT.crc(frame[:-4])
        if self.f_crc != crc_value:
            print('ERR: wrong crc, calculate cre: %x  original crc: %x.' % (crc_value, self.f_crc))
            return -1
        return 0
