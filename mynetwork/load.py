#coding=utf-8
'''
Created on 2015-10-23

@author: lamter
'''

import zlib
from .encrypt import *
from .intn import getDataLength

# 块长度
BLOCK_SIZE = 1024

def loadInt32(_socket, AES_KEY=None, unzip=True):
    """
    以 int32 来解包数据
    :param _socket:
    :param AES_KEY:
    :param zipLevel:
    :return:
    """
    # 收包
    data = _loadInt32(_socket)

    if data and AES_KEY:
        # 解密
        data = aes128_decrypt(AES_KEY, data)

    if data and unzip:
        # 解压
        data = zlib.decompress(data)

    return data



def _loadInt32(_socket):
    """
    以 int32 位收包
    :param _socket:
    :return:
    """
    # 获取长度
    d = _socket.recv(4)

    # 获得数据长度
    length = getDataLength(d)

    if length == 0:
        return ''

    # 接受完数据
    data = ''
    while length > 0:
        if length >= BLOCK_SIZE:
            s = BLOCK_SIZE
        else:
            s = length

        buff = _socket.recv(s)
        data += buff
        length -= len(buff)

    return data