#coding=utf-8
'''
Created on 2015-10-23

@author: lamter
'''


from struct import pack, unpack
STRUCT_FORMAT = "!I"

def getDataLength(d):
    if d:
        length, = unpack(STRUCT_FORMAT, d)
        return length
    else:
        return 0



def int32Head(encryptData):

    return pack(STRUCT_FORMAT, len(encryptData))