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


def df2markdown(df, index=True):
    """

    根据 df 生成 markdown表格

    :param df:
    :return:
    """
    d = df.copy()

    assert isinstance(d, pd.DataFrame)

    if index:
        d = d.reset_index()
    cols = [x for x in d.columns]
    for col in cols:
        d[col] = d[col].astype(str)

    cols[0] = ""
    df = d

    table = ""
    # 表头
    table += "|%s|\n" % '|'.join(df.columns)
    # 右对齐对齐
    table += "|-:" * df.shape[0] + "|\n"
    for i in np.array(df):
        table += "|" + "|".join(i) + "|\n"

    return table
