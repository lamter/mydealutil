#coding=utf-8
'''
Created on 2015-05-28

@author: Ron2
'''

import zlib


class ZipData(object):
    """
    压缩数据
    """

    @staticmethod
    def zip_data(requestData, level=6):
        """
        压缩数据
        :param requestData:
        :param level:
        :return:
        """
        return zlib.compress(requestData, level)


    @staticmethod
    def unzip_data(responseData):
        """
        解压缩数据
        :param responseData:
        :return:
        """
        return zlib.decompress(responseData)


if __name__=="__main__":

    # originData = "xxx xx fds dfjadksj fasdkf xx0 0 xx000000"
    originData = "witch which has which witches wrist watch"

    compressData = ZipData.zip_data(originData)
    # print "compressData ==> ", len(compressData), compressData

    decompressData = ZipData.unzip_data(compressData)
    # print "decompressData ==> ", len(decompressData), originData


