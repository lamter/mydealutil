# coding: utf-8
from itertools import chain
import doctest

def p2f(p):
    """
    百分数字符串转为浮点数

    >>> p2f('0.3%')
    0.003

    :param p:
    :return:
    """
    return float(p.strip("%")) / 100


def f2p(f):
    """
    浮点转转为百分比字符串

    >>> f2p(0.003)
    '0.3%'

    :param f:
    :return:
    """
    return str(round(f * 100, 2)) + "%"


def splitnum(num):
    """
    将一个数字各个位数拆分成数组

    >>> splitnum(12.34)
    [10, 2, 0.3, 0.04]

    :param num:
    :return:
    """
    num = str(float(num))
    i, f = num.split('.')

    i_nums = []
    for n in i:
        i_nums = list(map(lambda x: x * 10, i_nums))
        i_nums.append(int(n))

    f_nums = []
    for index, n in enumerate(f):
        index += 1
        f_nums.append(float(n) / 10 ** index)

    return list(chain(i_nums, f_nums))

if __name__ == "__mian__":
    doctest.testmod()