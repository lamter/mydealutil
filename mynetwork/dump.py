#coding=utf-8
'''
Created on 2015-10-23

@author: lamter
'''

import zlib
from .encrypt import *
from .intn import int32Head


def dumpInt32(_json, AES_KEY=None, zipdata=True):
    """
    压缩加密
    :param _json:
    :param AES_KEY:
    :return:
    """

    data = _json

    # 加压
    if zipdata:
        data = zlib.compress(_json, 6)

    # 加密
    if AES_KEY:
        data = aes128_encrypt(AES_KEY, data)

    # Int32位
    int32Data = int32Head(data ) + data

    return int32Data

def foo():
    pass