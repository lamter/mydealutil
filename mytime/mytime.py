# coding: utf-8
import doctest
import datetime


def d2s(date):
    """
    日期转为字符串

    >>> d2s(datetime.date(2016, 8, 16))
    '2016-08-16'

    :param date:
    :return:
    """
    return date.strftime("%Y-%m-%d")


if __name__ == "__mian__":
    doctest.testmod()
