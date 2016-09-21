# coding: utf-8

import re
import numpy as np
import pandas as pd


def vnpy_opt_DAY_IN(opt):
    """
    vnpy 优化结果清洗,用于 DAY_IN 和 DAY_OUT
    :param opt:
    :return:
    """
    data = re.compile(r'DAY_IN\':\s(\d+),\s\'DAY_OUT\':\s(\d+)\}"\]:\s([\d\.]+)').findall(opt)
    data = np.array(data).T
    dic = {
        "DAY_IN": pd.Series(data[0], dtype=np.int),
        "DAY_OUT": pd.Series(data[1], dtype=np.int),
        "capital": pd.Series(data[2], dtype=np.float)
    }
    return pd.DataFrame(dic)


def vnpy_opt_DAY_IN_2(opt):
    """
    vnpy 优化结果清洗, 针对 DAY_IN_2
    :param opt:
    :return:
    """
    data = re.compile(r'DAY_IN_2\':\s(\d+)\}"\]:\s([\d\.]+)').findall(opt)
    data = np.array(data).T
    dic = {
        "DAY_IN_2": pd.Series(data[0], dtype=np.int),
        "capital": pd.Series(data[1], dtype=np.float)
    }
    return pd.DataFrame(dic)


def testest():
    pd.DataFrame().dropna()