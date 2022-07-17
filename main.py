# tcp client

from socket import *
import struct
import crc8
import numpy

FC_TASK_OC_ACTION = 0xFD  # Execute the received mission immediately
FC_TASK_OC_CLEAR = 0xFE  # Clear mission queue
START_FLAG = 0xA6
SOURCE_DEV = 0xC8

FC_TSK_SetEXTIO = 9  # Control External IO (Payload Release, arm lights, strobe light)


def checksum(data_array):
    CRC8_Table = [
        0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65,
        157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220,
        35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98,
        190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255,
        70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7,
        219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154,
        101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36,
        248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185,
        140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205,
        17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80,
        175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238,
        50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115,
        202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139,
        87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22,
        233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168,
        116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53]

    crc_sum = 0

    for b in data_array:
        if b != START_FLAG:
            crc_sum = CRC8_Table[crc_sum ^ b]

    return crc_sum


def build_packet(dest, src, p_data, msgID):
    numData = len(p_data)
    data = [START_FLAG, 6 + numData, msgID, src, dest]

    for elem in p_data:
        data.append(elem)

    crc_flag = checksum(data)
    print(hex(crc_flag))
    data.append(crc_flag)

    return data


def light(OnOFF: bool):
    if OnOFF:
        p_array = [FC_TASK_OC_ACTION, 0, FC_TSK_SetEXTIO, 48, 0, 0, 0, 48, 0, 0, 0]
    else:
        p_array = [FC_TASK_OC_ACTION, 0, FC_TSK_SetEXTIO, 48, 0, 0, 0, 0, 0, 0, 0]

    out = build_packet(0x01, SOURCE_DEV, p_array, 0x34)
    print(out)
    out_b = struct.pack('{}B'.format(len(out)), *out)
    print(out_b)

    return out_b


def payload(OnOFF: bool):
    if OnOFF:
        p_array = [FC_TASK_OC_ACTION, 0, FC_TSK_SetEXTIO, 3, 0, 0, 0, 3, 0, 0, 0]
    else:
        p_array = [FC_TASK_OC_ACTION, 0, FC_TSK_SetEXTIO, 3, 0, 0, 0, 0, 0, 0, 0]

    out = build_packet(0x01, SOURCE_DEV, p_array, 0x34)
    print(out)
    out_b = struct.pack('{}B'.format(len(out)), *out)
    print(out_b)

    return out_b


def clear_mission():
    p_array = [FC_TASK_OC_CLEAR, 0x00]
    out = build_packet(0x01, SOURCE_DEV, p_array, 0x34)
    out_b = struct.pack('{}B'.format(len(out)), *out)
    print('CLEAN')

    return out_b

def parce_report(msg):
    ATTPitch, ATTRoll, ATTYaw, FlySpeed, Altitude, Distance , Voltage, GpsHead, \
    HomeHead, FlyTime_Sec = struct.unpack('3hHhH3hH', bytes(msg[5:25]))
    Lon, Lat, hLat, hLon = struct.unpack('4i', bytes(msg[25:41]))
    FrameType, InGas, VSpeed, VDOP, GpsNum = struct.unpack('BBbBB', bytes(msg[41:46]))


# 1 создать сокет
tcp_socket = socket(AF_INET, SOCK_STREAM)

# 2 Порт привязки
ip = "192.168.2.1"
port = 2022

# 3 подключиться к серверу
tcp_socket.connect((ip, port))


# b'\xa6', b'\x11',
byte_out = [b'\x11', b'\x34', b'\xc8', b'\x01', b'\xfd', b'\x00', b'\x09', b'\x30', b'\x00', b'\x00', b'\x00', b'\x00',
            b'\x00', b'\x00', b'\x00']
byte_out1 = [17, 52, 200, 1, 253, 0, 9, 48, 0, 0, 0, 0, 0, 0, 0]

# 4 Отправка и получение данных

#
# tcp_socket.send(light(False))
# a=input()
# tcp_socket.send(light(False))
# tcp_socket.send(clear_mission())
tcp_socket.send(light(True))
# tcp_socket.send(payload(True))
# a=input()
# tcp_socket.send(payload(False))


with open('log.txt', 'w') as file:
    for i in range(100):
        recv_data = tcp_socket.recv(1024)
        in_data = struct.unpack('{}B'.format(len(recv_data)), recv_data)
        print(in_data[0])
        if in_data[0] == 166 :
            file.write(str(in_data))
            file.write(str(len(in_data)))
            file.write('\n')
    file.close()
# 5 закрыть розетку
tcp_socket.close()
