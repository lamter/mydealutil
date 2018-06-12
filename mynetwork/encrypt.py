#coding=utf-8
'''
Created on 2015-10-24

@author: Shawn
'''


from Crypto.Cipher import AES


aess = {}           # AES 加密实例 {AES_KEY: AES()}

def getAesByKey(AES_KEY):
    """
    没有对应 KEY 就新增一个
    :param AES_KEY:
    :return:
    """
    return aess.get(AES_KEY, newAes(AES_KEY))



def newAes(AES_KEY):
    """
    根据 KEY 生成新的解密 实例
    :param AES_KEY:
    :return:
    """
    aes = AES.new(AES_KEY, AES.MODE_CBC)
    aess[AES_KEY] = aes
    return aes




def aes128_encrypt(AES_KEY, data):
    """
    AES 128 位解密
    :param AES_KEY:
    :param data:
    :return:
    """
    size = len(data)
    diff = 16 - size%16

    # 必须要将长度补位为16的整数才能加密
    for i in range(diff):
        data += chr(diff)

    return getAesByKey(AES_KEY).encrypt(data)


def aes128_decrypt(AES_KEY, _data):
    """
    AES 128 位解密
    :param requestData:
    :return:
    """
    # 秘钥实例
    newAes = getAesByKey(AES_KEY)

    # 解密
    data = newAes.decrypt(_data)
    rawDataLength = len(data)

    # 剔除掉数据后面的补齐位
    paddingNum = ord(data[rawDataLength - 1])
    if paddingNum > 0 and paddingNum <= 16:
        data = data[0:(rawDataLength - paddingNum)]
    return data

