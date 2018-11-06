# coding=utf-8
from __future__ import unicode_literals
import arrow
import pandas as pd
from pyecharts import Overlap, Line, Kline, Grid

def kline_tooltip_formatter(params):
    text = (
        params[0].axisValue
        + "<br/>"
        + "- open:"
        + params[0].data[1]
        + "<br/>"
        + "- close:"
        + params[0].data[2]
        + "<br/>"
        + "- low:"
        + params[0].data[3]
        + "<br/>"
        + "- high:"
        + params[0].data[4]
        + "<br/>"
        + "- volume:"
        + params[0].data[5]
    )
    return text


def _lineTradeList(tradeResultList):
    line = Line('')
    # line.use_theme('dark')
    for t in tradeResultList:
        line_color = 'red' if t['pro'] > 0 else 'green'
        #         print(line_color, t['pro'])
        line.add(
            '', t['dt'], t['price'],
            yaxis_max='dataMax',
            yaxis_min='dataMin',
            line_color=line_color,
            is_legend_show=False,
            line_width=2,
            is_datazoom_show=True,
        )
    return line


def _aggregate(bars, period='1T'):
    """
    聚合数据
    :param period: K线周期，默认 1T = 1min
    :param bars: 从 mongodb 中读取的原始 K 线数据
    :return:
    """

    df = pd.DataFrame(bars)
    df.set_index('datetime', inplace=True)
    df = df.sort_index()
    r = df.resample(period, closed='left', label='left')
    close = r.close.last()
    high = r.high.max()
    low = r.low.min()
    _open = r.open.first()
    volume = r.volume.sum()

    ndf = pd.DataFrame({
        'close': close,
        'high': high,
        'low': low,
        # 'lowerLimit': lowerLimit,
        'open': _open,
        'volume': volume,
        # 'upperLimit': upperLimit,
    }, columns=['open', 'close', 'low', 'high', 'volume']).dropna(how='any')

    return ndf

def _getTradeResultList(tradeResultList, ndf):
    """
    转化成 [
        {
          'dt':[openDatetime, closeDatetime] ,
          'price':[openPrice, closePrice]
        }
    ]
    :return:
    """
    _tradeResultList = []
    for tr in tradeResultList:
        _tradeResultList.extend(tr['成交单'])

    trl = []

    # K线图的起止时间
    b = ndf.index.min()
    e = ndf.index.max()

    for r in _tradeResultList:
        if b <= r['entryDt'] and r['exitDt'] <= e:
            # 有时间限制，成交单不能超出K线的范围
            tr = {
                'dt': [r['entryDt'].strftime('%Y-%m-%d %H:%M'), r['exitDt'].strftime('%Y-%m-%d %H:%M')],
                'price': [r['entryPrice'], r['exitPrice']],
                'vol': r.get('volume', r.get('voluem')),
            }
            p = tr['price']
            # 盈亏
            tr['pro'] = (p[1] - p[0]) * tr['vol']
            trl.append(tr)

    return trl

def _getKline(ndf, period):

    # 生成K线图
    dates = []
    kdata = []
    for bar in ndf.iterrows():
        dates.append(bar[0].strftime('%Y-%m-%d %H:%M'))
        kdata.append(list(bar[1]))

    kline = Kline("{}".format(period))
    # kline.use_theme('dark')
    kline.add(
        "{} K线".format(period),
        dates, kdata,
        mark_point=["max"],
        yaxis_interval=1,
        is_datazoom_show=True,
        tooltip_formatter=kline_tooltip_formatter,
        xaxis_label_textcolor='green',
        yaxis_label_textcolor='green',
    )

    return kline

def _getTradeLine(tradeResultList):
    line = Line('')
    line.use_theme('dark')
    for i, t in enumerate(tradeResultList):
        line_color = 'red' if t['pro'] > 0 else 'green'
        #         print(line_color, t['pro'])
        line.add(
            '', t['dt'], t['price'],
            line_color=line_color,
            is_legend_show=False,
            line_width=2,
            is_datazoom_show=True,
        )

    return line


def tradeOnKLine(period, bars, tradeResultList, width=2000, height=1000):
    """

    :param symbol:
    :param period:
    :param bars:
    :return:
    """
    # 聚合成指定周期的K线
    ndf = _aggregate(bars, period)

    # 生成K线图
    kline = _getKline(ndf, period)

    # 叠加图层
    overlap = Overlap(width=width, height=height)
    overlap.use_theme('light')
    overlap.add(kline)

    # 生成成交单
    tradeResultList = _getTradeResultList(tradeResultList, ndf)

    # 叠加成交图层
    if tradeResultList:
        line = _getTradeLine(tradeResultList)
        overlap.add(line)

    return overlap
