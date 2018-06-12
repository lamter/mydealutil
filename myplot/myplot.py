# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, date2num, MonthLocator, YearLocator
# from matplotlib import candlestick_ohlc

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class CandleStick:
    """
    蜡烛图(K线图)
    """

    def __init__(self, data, code=None, fig_ax=None):
        """
        只能聚合日线
        :param data: pd.DataFrame(columns=["open", "high", "low", "close"], index='date')
        :param code: 股票代码,或者股票名
        :param fig_ax: 给定 (fix, ag)
        :return:
        """

        self.fig, self.ax = fig_ax or plt.subplots()
        self.code = code or "K线图"

        # 检查是否含有关键的数据
        self.data = data.copy()
        self.columns = ["open", "high", "low", "close"]
        if not set(self.columns).issubset(set(self.data.columns)):
            raise ValueError("确实数据")
        if self.data.shape[0] == 0:
            raise ValueError("没有数据")

    def draw(self, gap=True):
        """
        绘制蜡烛图
        :param gap: 是否保留空缺的数据
        :return:
        """

        fig = self.fig
        ax = self.ax

        # 获取图片实例 fig 和 数据实例 ax
        fig.set_size_inches(20, 10)
        fig.subplots_adjust(bottom=0.2)

        # 数据源要这样的 这样的格式 (time, open, high, low, close, ...)
        quotes = self.data[["open", "high", "low", "close"]]
        quotes.index.name = "date"
        quotes = quotes.reset_index()
        quotes["date"] = quotes.date.apply(date2num)
        quotes = np.asarray(quotes)

        size = len(quotes)
        if size < 20:
            major_locator = WeekdayLocator(MONDAY)  # 主要刻度
            minor_locator = DayLocator()  # 次要刻度
        elif size < 500:
            major_locator = MonthLocator()  # 主要刻度
            minor_locator = DayLocator(15)  # 次要刻度
        else:
            major_locator = YearLocator()  # 主要刻度
            minor_locator = MonthLocator(6)  # 次要刻度

        mondayFormatter = DateFormatter('%Y-%m-%d')  # 如：2-29-2015
        dayFormatter = DateFormatter('%d')  # e.g., 12

        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_minor_locator(minor_locator)
        ax.xaxis.set_major_formatter(mondayFormatter)
        ax.xaxis.set_minor_formatter(dayFormatter)

        if gap:
            candlestick_ohlc(ax, quotes, width=0.6, colorup='r', colordown='g', alpha=1.0)
        else:
            # weekday_quotes = quotes
            weekday_quotes = [tuple([i] + list(quote[1:])) for i, quote in enumerate(quotes)]

            # 调用绘图
            self._candlestick(ax, weekday_quotes, width=0.6, colorup='r', colordown='g', alpha=1.0, ochl=False)
            # 设置横轴的日期
            ax.set_xticks(range(0, len(weekday_quotes), 5))  ####
            ax.set_xticklabels(
                [mdates.num2date(quotes[index][0]).strftime('%Y-%m-%d') for index in ax.get_xticks()])  ####

        ax.xaxis_date()
        ax.autoscale_view()
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

        ax.grid(True)
        plt.title(self.code)

    @staticmethod
    def _candlestick(ax, quotes, width=0.2, colorup='k', colordown='r',
                     alpha=1.0, ochl=True):

        """
        Plot the time, open, high, low, close as a vertical line ranging
        from low to high.  Use a rectangular bar to represent the
        open-close span.  If close >= open, use colorup to color the bar,
        otherwise use colordown

        Parameters
        ----------
        ax : `Axes`
            an Axes instance to plot to
        quotes : sequence of quote sequences
            data to plot.  time must be in float date format - see date2num
            (time, open, high, low, close, ...) vs
            (time, open, close, high, low, ...)
            set by `ochl`
        width : float
            fraction of a day for the rectangle width
        colorup : color
            the color of the rectangle where close >= open
        colordown : color
             the color of the rectangle where close <  open
        alpha : float
            the rectangle alpha level
        ochl: bool
            argument to select between ochl and ohlc ordering of quotes

        Returns
        -------
        ret : tuple
            returns (lines, patches) where lines is a list of lines
            added and patches is a list of the rectangle patches added

        """

        OFFSET = width / 2.0

        lines = []
        patches = []
        for q in quotes:
            if ochl:
                t, open, close, high, low = q[:5]
            else:
                t, open, high, low, close = q[:5]

            if close >= open:
                color = colorup
                lower = open
                height = close - open
            else:
                color = colordown
                lower = close
                height = open - close

            vline = Line2D(
                xdata=(t, t), ydata=(low, high),
                color=color,
                linewidth=0.5,
                antialiased=True,
            )

            rect = Rectangle(
                xy=(t - OFFSET, lower),
                width=width,
                height=height,
                facecolor=color,
                edgecolor=color,
            )
            rect.set_alpha(alpha)

            lines.append(vline)
            patches.append(rect)
            ax.add_line(vline)
            ax.add_patch(rect)
        ax.autoscale_view()

        return lines, patches


