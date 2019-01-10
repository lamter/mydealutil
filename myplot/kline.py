# coding=utf-8
from __future__ import unicode_literals
import logging
import pymongo
import datetime
import pandas as pd
from pyecharts import Overlap, Line, Kline, Grid
import pytz
from bson.codec_options import CodecOptions

LOCAL_TIMEZONE = pytz.timezone('Asia/Shanghai')

DIRECTION_LONG = '多'
DIRECTION_SHORT = '空'


def kline_tooltip_formatter(params):
    text = (
        params[0].axisValue
        + "<br/>"
        + "- open:"
        + params[0].data[1]
        + "<br/>"
        + "- high:"
        + params[0].data[4]
        + "<br/>"
        + "- low:"
        + params[0].data[3]
        + "<br/>"
        + "- close:"
        + params[0].data[2]
        + "<br/>"
        + "- volume:"
        + params[0].data[5]
    )
    return text

def qryBarsMongoDB(
        underlyingSymbol,
        host,
        port,
        dbn,
        collection,
        username,
        password,
        startTradingDay=None,
        endTradingDay=None,
        contract='contract',
):
    """
    查询对应品种的 bar_1min
    :param symbol:
    :param host:
    :param port:
    :param dbn:
    :param collection:
    :param username:
    :param password:
    :param startTradingDay:
    :param endTradingDay:
    :return:
    """
    client = pymongo.MongoClient(
        host=host,
        port=port,
    )
    db = client[dbn]
    db.authenticate(
        username,
        password
    )
    bars = []
    contract = db[contract].with_options(
        codec_options=CodecOptions(tz_aware=True, tzinfo=LOCAL_TIMEZONE))
    for c in contract.find({'underlyingSymbol': underlyingSymbol, 'activeStartDate': {'$ne': None}}).sort([('startDate', pymongo.ASCENDING),('endDate', pymongo.ASCENDING)]):
        symbol = c['symbol']
        _flt = {
            'symbol': symbol,
            'tradingDay': {},
        }

        if startTradingDay:
            startDate = max(c['activeStartDate'], startTradingDay)
        else:
            startDate = c['activeStartDate']

        if endTradingDay:
            endDate = min(c['activeEndDate'], endTradingDay)
        else:
            endDate = c['activeEndDate']

        if startDate > endDate:
            # 没有合适的 bar 跳过
            continue

        _flt['tradingDay'] = {'$gte': startDate, '$lte': endDate}

        col = db[collection].with_options(
            codec_options=CodecOptions(tz_aware=True, tzinfo=LOCAL_TIMEZONE))
        cursor = col.find(_flt, {'high': 1, 'low': 1, 'open': 1, 'close': 1, 'volume': 1, 'datetime': 1, '_id': 0})
        for d in cursor:
            bars.append(d)

    return  bars


def qryBtresultMongoDB(
        underlyingSymbol,
        optsv,
        host,
        port,
        dbn,
        collection,
        username,
        password,
):
    """
    查询回测结果
    :param symbol:
    :param optsv:
    :param host:
    :param port:
    :param dbn:
    :param collection:
    :param username:
    :param password:
    :return:
    """
    client = pymongo.MongoClient(
        host=host,
        port=port,
    )
    db = client[dbn]
    db.authenticate(
        username,
        password,
    )
    col = db[collection].with_options(
        codec_options=CodecOptions(tz_aware=True, tzinfo=LOCAL_TIMEZONE))

    sql = {
        'underlyingSymbol': underlyingSymbol,
        'optsv': optsv,
    }
    items = {'成交单': 1, '_id': 0}
    cursor = col.find(sql, items)
    return [_ for _ in cursor]


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
            if r['entryDt'].second == 0:
                entryDt = r['entryDt'].strftime('%Y-%m-%d %H:%M')
            else:
                entryDt = r['entryDt'] + datetime.timedelta(seconds=60)
                entryDt = entryDt .strftime('%Y-%m-%d %H:%M')

            if r['exitDt'].second == 0:
                exitDt = r['exitDt'].strftime('%Y-%m-%d %H:%M')
            else:
                exitDt = r['exitDt'] + datetime.timedelta(seconds=60)
                exitDt = exitDt .strftime('%Y-%m-%d %H:%M')
            tr = {
                'dt': [entryDt, exitDt],
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
        # mark_point=["max"],
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


class TrCheck(Exception):
    # 撮合异常
    pass


class DealOrder(object):
    # 成交单对象
    def __init__(self, tr, _open=True):
        self.open = _open  # 开平仓
        self.direction = tr['direction']  # 方向
        self.price = tr['price']  # 成交价格
        self.datetime = tr['datetime']

        self.volume = tr['volume']  # 成交数量，多单为正，空单为负

    @property
    def close(self):
        return not self.open

    def __str__(self, *args, **kwargs):
        return super.__str__(self, *args, **kwargs) + ' [' + ' '.join(
            ['{}:{}'.format(k, v) for k, v in self.__dict__.items()]) + ']'

    @property
    def turnover(self):
        return self.price * self.volume

    def sum(self, tr):
        volume = self.volume + tr['volume']
        turnover = tr['price'] * tr['volume']
        self.price = (self.turnover + turnover) / volume
        self.volume = volume


class DealMatcher(object):
    def __init__(self, df):
        self.df = df
        self.tradeResultList = []

        self.openOrder = None
        self.closeOrder = None

        self.count = 0

    def merge(self, tr):
        """
        合并成交单
        :param tr:
        :return:
        """
        # 开仓单部分 >>>>>>>>>>
        if self.openOrder is None:
            self.openOrder = DealOrder(tr)
            return

        if self.closeOrder is None:
            if tr['direction'] == self.openOrder.direction:
                # 同方向，合并开仓单
                self.openOrder.sum(tr)
                return
                # 开仓单部分 <<<<<<<<<<
                # 平仓单部分 >>>>>>>>>>
            else:
                # 方向不同，平仓单
                self.closeOrder = DealOrder(tr, _open=False)
                return

        if tr['direction'] == self.closeOrder.direction:
            self.closeOrder.sum(tr)
            # 平仓单部分 <<<<<<<<<<
        else:
            # 平仓仓位不足就已经转变方向
            # 仓位异常
            # 抛弃开仓单，平仓单转为开仓单
            self.openOrder, self.closeOrder = self.closeOrder, None
            # 重新进入合并
            self.merge(tr)

    def match(self):
        """
        匹配
        :param tr:
        :return:
        """
        import arrow
        if self.openOrder and self.closeOrder:
            if self.openOrder.volume == self.closeOrder.volume:
                # 开平仓数量一致
                self.tradeResultList.append({
                    'entryDt': arrow.get(self.openOrder.datetime).datetime,
                    'exitDt': arrow.get(self.closeOrder.datetime).datetime,
                    'entryPrice': self.openOrder.price,
                    'exitPrice': self.closeOrder.price,
                    'volume': self.openOrder.volume if self.openOrder.direction == DIRECTION_LONG else -self.openOrder.volume,
                })
                self.openOrder, self.closeOrder = None, None
                return
            if self.openOrder.volume < self.closeOrder.volume:
                # 平仓单数量超过开仓单
                # 将平仓单转换为开仓单
                # 抛弃开仓单
                self.openOrder, self.closeOrder = self.closeOrder, None

    def do(self):
        for _, tr in self.df.iterrows():
            self.merge(tr)
            self.match()

        # 模仿从MongoDB 读取的数据结构
        self.originTrl = [{'成交单': self.tradeResultList}]


def qryTradeListMongodb(host, port, dbn, username, password, collection, sql):
    """
    从数据库中读取实盘/模拟盘成交单
    :return:
    """
    client = pymongo.MongoClient(
        host=host,
        port=port,
    )
    db = client[dbn]
    db.authenticate(
        username,
        password
    )

    # 读取实盘成交单
    col = db[collection].with_options(
        codec_options=CodecOptions(tz_aware=True, tzinfo=LOCAL_TIMEZONE))

    # 成交单查询条件
    items = {'_id': 0, }
    cursor = col.find(sql, items)
    logging.info('查询获得 {} 条成交记录'.format(cursor.count()))

    documents = [i for i in cursor]
    df = pd.DataFrame(documents)
    # 查询结果根据时间排序
    df = df.reset_index(drop=False)
    df = df.drop_duplicates(['datetime', 'tradeID'])
    df = df.sort_values(['datetime', 'index'])

    # 校验并撮合成交单
    matcher = DealMatcher(df)
    matcher.do()
    return matcher

