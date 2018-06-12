# coding:utf-8
"""
需要使用 with 语法，以保证在批量绘图时能关闭掉图片，以免内存爆掉
"""
from contextlib import contextmanager
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


@contextmanager
def draw_nav(series, title=None, figsize=(20, 10), subPlotNum=1, grid=True, logy=False):
    """
    用于绘制指定大小的净值曲线图

    :param title: 标题
    :param series: Series(index=DatetimeIndex())
    :return:
    """
    fig = plt.figure(0, figsize=figsize)

    subplot = plt.subplot(subPlotNum, 1, 1)
    if title:
        if logy:
            title += '_logy'
        subplot.set_title(title)
    else:
        if logy:
            subplot.set_title('logy')

    series.plot(ax=subplot, grid=grid, logy=logy)

    yield subplot
    plt.close(0)


@contextmanager
def draw_3D_potentiometric(df, title=None, figsize=(20, 10), onlyShadow=False, view=None, fontsize=None, isShow=True):
    """
    将绘制成 3D 等势图
    :return:
    """

    # 数据数目
    # 定义x, y
    x = np.array(df.columns)
    y = df.index

    # # 生成网格数据
    X, Y = np.meshgrid(x, y)

    # 计算Z轴的高度
    Z = np.array(df)

    # 定义figure
    fig = plt.figure(0, figsize=figsize)

    # 将figure变为3d
    ax = fig.gca(projection='3d')

    if title:
        ax.set_title(title)

    # 设置刻度字体大小
    if fontsize:
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)

    # 绘制3D曲面
    if view:
        ax.view_init(*view)
    if not onlyShadow:
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))

    # 绘制从3D曲面到底部的投影
    ax.contour(X, Y, Z, zdim='z', offset=-2, cmap='rainbow')

    # 设置z轴的维度
    # _max = int(df.max().max()) + 1
    # _min = 0
    # if _max < _min:
    #     _min, _max = _max, _min
    # ax.set_zlim(_min, _max)

    # left = 0.05, right = 0.95, top = 0.95, bottom = 0.05
    ax.set_adjustable('datalim')

    if isShow:
        plt.show()

    yield fig
    plt.close(0)
